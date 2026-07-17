import numpy as np
import torch
from torch_geometric.data import Data
from torch_geometric.utils import to_undirected
def normalize_with_padding_dataset(images):
    """
    Normalizes a dataset of images to the range [0, 1] channel-wise across all samples,
    leaving zero-padding unchanged.

    Args:
        images (numpy.ndarray): Dataset of images with shape (N, H, W, C), where
                                N is the number of samples, H and W are spatial dimensions,
                                and C is the number of channels.

    Returns:
        numpy.ndarray: Normalized dataset with padding (zeros) unchanged.
        list: List of (min, max) values for each channel across the entire dataset.
    """
    # Check the shape of the input array
    if images.ndim != 4:
        raise ValueError("Input dataset must be a 4D array with shape (N, H, W, C).")
    
    # Initialize min-max tracker for each channel
    min_max_values = []
    normalized_images = images.copy()
    
    # Normalize channel-wise across all samples
    for c in range(images.shape[-1]):
        # Extract all channel values across all images
        channel_values = images[:, :, :, c]
        non_zero_mask = channel_values != 0
        
        # Compute min and max across all non-zero values for the channel
        arr_min = channel_values[non_zero_mask].min() if non_zero_mask.any() else 0
        arr_max = channel_values[non_zero_mask].max() if non_zero_mask.any() else 1
        
        # Normalize the channel values for all images
        if arr_max > arr_min:  # Avoid division by zero
            normalized_images[:, :, :, c][non_zero_mask] = (
                channel_values[non_zero_mask] - arr_min
            ) / (arr_max - arr_min)
        
        # Save min-max values for the channel
        min_max_values.append((arr_min, arr_max))
    
    return normalized_images, min_max_values
def preprocess_netcdf_data(data, num_frames=2, target_channels=None):
    """
    Prepares data for training a Conv3D model with temporal input sequences.

    Args:
        data (numpy.ndarray): The input data of shape (num_timesteps, height, width, channels).
        num_frames (int): Number of input frames for each sequence.
        target_channels (list or slice, optional): Which channels to include in target y.
                                                   If None, all channels are included.
                                                   Example: slice(0, 5) for first 5 channels,
                                                   or [0, 1, 2, 3, 4] for specific channels.

    Returns:
        X (numpy.ndarray): Input sequences of shape (num_samples, num_frames, height, width, channels).
        y (numpy.ndarray): Target frames of shape (num_samples, height, width, target_channels).
    """
    # Number of time steps in the data
    num_timesteps, height, width, channels = data.shape

    # Create input (X) and target (y) sequences
    X = []
    y = []

    for i in range(num_timesteps - num_frames):
        X.append(data[i:i + num_frames])  # Take 'num_frames' consecutive frames as input
        
        # Target: next frame, optionally with selected channels only
        target_frame = data[i + num_frames]
        if target_channels is not None:
            target_frame = target_frame[:, :, target_channels]
        y.append(target_frame)

    # Convert to NumPy arrays
    X = np.array(X)  # Shape: (num_samples, num_frames, height, width, channels)
    y = np.array(y)  # Shape: (num_samples, height, width, target_channels)

    return X, y


def create_spatial_graph_edges(height, width, connectivity='4'):
    """
    Create edge indices for a spatial grid graph.
    
    Args:
        height (int): Height of the grid
        width (int): Width of the grid
        connectivity (str): '4' for 4-connected (up, down, left, right) or 
                           '8' for 8-connected (includes diagonals)
    
    Returns:
        torch.Tensor: Edge indices of shape (2, num_edges) in COO format
    """
    edges = []
    
    for i in range(height):
        for j in range(width):
            node_idx = i * width + j
            
            # Right neighbor
            if j < width - 1:
                right_idx = i * width + (j + 1)
                edges.append([node_idx, right_idx])
            
            # Bottom neighbor
            if i < height - 1:
                bottom_idx = (i + 1) * width + j
                edges.append([node_idx, bottom_idx])
            
            # Diagonal neighbors (if 8-connected)
            if connectivity == '8':
                # Bottom-right
                if i < height - 1 and j < width - 1:
                    diag_idx = (i + 1) * width + (j + 1)
                    edges.append([node_idx, diag_idx])
                # Bottom-left
                if i < height - 1 and j > 0:
                    diag_idx = (i + 1) * width + (j - 1)
                    edges.append([node_idx, diag_idx])
    
    if len(edges) == 0:
        return torch.empty((2, 0), dtype=torch.long)
    
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    # Make undirected
    edge_index = to_undirected(edge_index)
    
    return edge_index


def spatial_to_graph_data(X, y, connectivity='4'):
    """
    Convert spatial-temporal data to graph format for GraphSAGE.
    
    Args:
        X (numpy.ndarray): Input sequences of shape (num_samples, num_frames, height, width, channels).
                           For num_frames=1, shape is (num_samples, 1, height, width, channels)
        y (numpy.ndarray): Target frames of shape (num_samples, height, width, channels).
        connectivity (str): '4' or '8' connectivity for spatial graph
    
    Returns:
        list: List of Data objects, one for each sample in X
        list: List of target tensors, one for each sample in y
    """
    if X.ndim != 5:
        raise ValueError(f"Expected X to have 5 dimensions (num_samples, num_frames, height, width, channels), got {X.ndim}")
    if y.ndim != 4:
        raise ValueError(f"Expected y to have 4 dimensions (num_samples, height, width, channels), got {y.ndim}")
    
    num_samples, num_frames, height, width, channels = X.shape
    _, _, _, target_channels = y.shape  # Get target channels separately (may differ from X channels)
    
    # Create edge indices for spatial graph (same for all samples)
    edge_index = create_spatial_graph_edges(height, width, connectivity=connectivity)
    num_nodes = height * width
    
    graph_list = []
    target_list = []
    
    for i in range(num_samples):
        # Get node features from all frames
        # Shape: (num_frames, height, width, channels) -> (num_frames, num_nodes, channels)
        x_frames = []
        for t in range(num_frames):
            frame = X[i, t]  # (height, width, channels)
            # Reshape to (num_nodes, channels)
            frame_nodes = frame.reshape(num_nodes, channels)
            x_frames.append(frame_nodes)
        
        # Stack frames: (num_frames, num_nodes, channels)
        node_features = np.stack(x_frames, axis=0)
        node_features = torch.FloatTensor(node_features)
        
        # Create graph data object
        graph_data = Data(
            x=node_features,  # (num_frames, num_nodes, channels) - will be processed by model
            edge_index=edge_index,
            num_nodes=num_nodes
        )
        graph_list.append(graph_data)
        
        # Target: (height, width, target_channels) -> (num_nodes, target_channels)
        # Use target_channels instead of channels since y may have fewer channels than X
        y_sample = y[i].reshape(num_nodes, target_channels)
        target_list.append(torch.FloatTensor(y_sample))
    
    return graph_list, target_list


def extract_neighborhood_features(images, kernel_size=3):
    """
    Extract flattened k×k neighborhoods for NA-LSTM (cellular automata style encoding).

    Args:
        images: Array of shape (N, H, W, C) or (H, W, C).
        kernel_size: Neighborhood window size (default 3 → 3×3).

    Returns:
        Array of shape (N, H*W, k*k*C) or (H*W, k*k*C).
    """
    squeeze = False
    if images.ndim == 3:
        images = images[None, ...]
        squeeze = True
    if images.ndim != 4:
        raise ValueError("images must have shape (N, H, W, C) or (H, W, C)")

    pad = kernel_size // 2
    padded = np.pad(images, ((0, 0), (pad, pad), (pad, pad), (0, 0)), mode="constant")
    windows = np.lib.stride_tricks.sliding_window_view(
        padded, (kernel_size, kernel_size), axis=(1, 2)
    )
    # windows: (N, H, W, C, k, k)
    n, h, w, c, _, _ = windows.shape
    flat = windows.transpose(0, 1, 2, 4, 5, 3).reshape(n, h * w, kernel_size * kernel_size * c)
    return flat[0] if squeeze else flat


def preprocess_nalstm_data(
    data,
    num_frames=1,
    target_channels=slice(0, 5),
    kernel_size=3,
    spectral_channels=5,
):
    """
    Build NA-LSTM sequences: neighborhood-augmented inputs and pixel targets.

    Matches the paper/notebook encoding:
      - 3×3 neighborhoods are extracted from the first ``spectral_channels`` only
      - any remaining channels (NDVI / static auxiliaries) are appended as
        per-pixel (center) values, not neighborhood-expanded

    Args:
        data: (T, H, W, C) normalized raster stack.
        num_frames: temporal window length.
        target_channels: channels used as prediction target (Landsat bands).
        kernel_size: spatial neighborhood size.
        spectral_channels: number of leading channels used for neighborhood encoding.

    Returns:
        X: (num_samples, num_pixels, num_frames, neigh_features)
        y: (num_samples, num_pixels, target_channels)
        spatial_shape: (H, W)
    """
    X_seq, y_seq = preprocess_netcdf_data(
        data, num_frames=num_frames, target_channels=target_channels
    )
    # X_seq: (S, F, H, W, C), y_seq: (S, H, W, Ct)
    samples = []
    targets = []
    for i in range(X_seq.shape[0]):
        frame_feats = []
        for t in range(X_seq.shape[1]):
            frame = X_seq[i, t]
            spectral = frame[..., :spectral_channels]
            neigh = extract_neighborhood_features(spectral, kernel_size=kernel_size)
            if frame.shape[-1] > spectral_channels:
                aux = frame[..., spectral_channels:].reshape(-1, frame.shape[-1] - spectral_channels)
                neigh = np.concatenate([neigh, aux], axis=-1)
            frame_feats.append(neigh)
        # (F, P, Feat) -> (P, F, Feat)
        x_i = np.stack(frame_feats, axis=0).transpose(1, 0, 2)
        y_i = y_seq[i].reshape(-1, y_seq.shape[-1])
        samples.append(x_i)
        targets.append(y_i)
    X = np.stack(samples, axis=0)
    y = np.stack(targets, axis=0)
    return X, y, (y_seq.shape[1], y_seq.shape[2])