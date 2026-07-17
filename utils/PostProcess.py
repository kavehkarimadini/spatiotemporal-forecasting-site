import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from scipy import ndimage


def denormalize_dataset(normalized_images, min_max_values):
    """
    Denormalizes a dataset of images from the range [0, 1] channel-wise to the original scale.

    Args:
        normalized_images (numpy.ndarray): Normalized dataset with shape (N, H, W, C).
        min_max_values (list): List of (min, max) tuples for each channel.

    Returns:
        numpy.ndarray: Denormalized dataset with the original scale restored.
    """
    if normalized_images.ndim != 4:
        raise ValueError("Input dataset must be a 4D array with shape (N, H, W, C).")
    
    if len(min_max_values) != normalized_images.shape[-1]:
        raise ValueError("Length of min_max_values must match the number of channels in the dataset.")
    
    denormalized_images = normalized_images.copy()
    
    for c in range(normalized_images.shape[-1]):
        channel_values = normalized_images[:, :, :, c]
        arr_min, arr_max = min_max_values[c]
        
        if arr_max > arr_min:
            denormalized_images[:, :, :, c] = channel_values * (arr_max - arr_min) + arr_min
    
    return denormalized_images


def plot_and_save_predictions(predictions, height, width, num_bands=5, 
                               output_plot_file='predictions_2024.png',
                               output_netcdf_file='output_GraphSage_LSTM_2024.nc',
                               lat_coords=None,
                               lon_coords=None):
    """
    Plot and save predictions as images and NetCDF file.
    
    Args:
        predictions (numpy.ndarray): Denormalized predictions with shape (H, W, C).
        height (int): Height of the spatial grid.
        width (int): Width of the spatial grid.
        num_bands (int): Number of bands to plot and save (default: 5).
        output_plot_file (str): Output file path for the plot (default: 'predictions_2024.png').
        output_netcdf_file (str): Output file path for NetCDF (default: 'output_GraphSage_LSTM_2024.nc').
        lat_coords (numpy.ndarray, optional): 1D latitude coordinates (taken from dataset['lat']).
        lon_coords (numpy.ndarray, optional): 1D longitude coordinates (taken from dataset['lon']).
    
    Returns:
        xarray.Dataset: The created xarray Dataset.
    """
    # Create xarray Dataset for the first num_bands bands
    band_names = [f"Band{i+1}" for i in range(num_bands)]
    
    # Create or validate coordinate arrays
    if lat_coords is None or lon_coords is None:
        # Fallback: use simple index-based coordinates if none are provided
        lat_coords = np.arange(height)
        lon_coords = np.arange(width)
    else:
        # Basic sanity check to ensure consistency with the data grid
        if len(lat_coords) != height or len(lon_coords) != width:
            raise ValueError(
                f"Length of lat_coords ({len(lat_coords)}) / lon_coords ({len(lon_coords)}) "
                f"does not match height ({height}) / width ({width})."
            )
    
    # Create dataset with first num_bands bands
    data_vars = {
        band_names[i]: (["lat", "lon"], predictions[:, :, i]) for i in range(num_bands)
    }
    
    ds = xr.Dataset(
        data_vars,
        coords={
            "lat": lat_coords,
            "lon": lon_coords,
        }
    )
    
    # Plot the bands
    bands = band_names
    fig, axes = plt.subplots(3, 3, figsize=(15, 15))
    axes = axes.flatten()
    
    for i, band in enumerate(bands):
        if i < len(axes):
            data_band = ds[band]
            x = ds['lon']
            y = ds['lat']
            
            im = axes[i].pcolormesh(x, y, data_band, shading='auto', cmap='viridis')
            axes[i].set_title(band)
            axes[i].set_xlabel("X Coordinate")
            axes[i].set_ylabel("Y Coordinate")
            plt.colorbar(im, ax=axes[i])
    
    # Hide unused subplots
    for i in range(len(bands), len(axes)):
        axes[i].axis('off')
    
    plt.suptitle('GraphSAGE-LSTM Predictions for 2024 (Denormalized)', fontsize=16)
    plt.tight_layout()
    
    # Save plot
    plt.savefig(output_plot_file, dpi=300, bbox_inches='tight')
    print(f"Prediction plots saved to {output_plot_file}")
    plt.close()
    
    # Save to NetCDF file
    ds.to_netcdf(output_netcdf_file)
    print(f"Predictions saved to {output_netcdf_file}")
    
    return ds


def upsample_spatial(data, target_height, target_width, method='bilinear'):
    """
    Upsample spatial dimensions (height and width) of the data to target size.
    
    Args:
        data (numpy.ndarray): Input data with shape (..., height, width, channels) or (height, width, channels).
        target_height (int): Target height dimension.
        target_width (int): Target width dimension.
        method (str): Upsampling method: 'bilinear' or 'nearest' (default: 'bilinear').
    
    Returns:
        numpy.ndarray: Upsampled data with shape (..., target_height, target_width, channels).
    """
    original_shape = data.shape
    
    # Handle different input dimensions
    if data.ndim == 2:
        # 2D: (height, width) -> add dummy dimensions
        data = data[np.newaxis, :, :, np.newaxis]
        squeeze_dims = [0, 3]
    elif data.ndim == 3:
        # 3D: (height, width, channels)
        data = data[np.newaxis, :, :, :]
        squeeze_dims = [0]
    elif data.ndim == 4:
        # 4D: (samples, height, width, channels)
        squeeze_dims = []
    elif data.ndim == 5:
        # 5D: (samples, frames, height, width, channels)
        squeeze_dims = []
    else:
        raise ValueError(f"Unsupported number of dimensions: {data.ndim}")
    
    # Get current dimensions
    if data.ndim == 5:
        samples, frames, height, width, channels = data.shape
        data_reshaped = data.reshape(samples * frames, height, width, channels)
        reshape_back = True
    else:
        samples, height, width, channels = data.shape
        data_reshaped = data
        reshape_back = False
    
    # Calculate zoom factors
    zoom_h = target_height / height
    zoom_w = target_width / width
    
    # Upsample each sample
    upsampled_list = []
    for i in range(data_reshaped.shape[0]):
        img = data_reshaped[i]  # (height, width, channels)
        upsampled_channels = []
        
        for c in range(channels):
            channel_data = img[:, :, c]
            
            if method == 'bilinear':
                # Bilinear interpolation using scipy
                upsampled_channel = ndimage.zoom(
                    channel_data, 
                    (zoom_h, zoom_w), 
                    order=1, 
                    mode='constant',
                    cval=0.0
                )
            else:  # nearest
                # Nearest neighbor interpolation
                upsampled_channel = ndimage.zoom(
                    channel_data, 
                    (zoom_h, zoom_w), 
                    order=0, 
                    mode='constant',
                    cval=0.0
                )
            
            upsampled_channels.append(upsampled_channel)
        
        upsampled_img = np.stack(upsampled_channels, axis=-1)  # (target_h, target_w, channels)
        upsampled_list.append(upsampled_img)
    
    upsampled_data = np.array(upsampled_list)
    
    # Reshape back if needed
    if reshape_back:
        upsampled_data = upsampled_data.reshape(samples, frames, target_height, target_width, channels)
    else:
        upsampled_data = upsampled_data.reshape(samples, target_height, target_width, channels)
    
    # Remove dummy dimensions that were added
    for dim in sorted(squeeze_dims, reverse=True):
        upsampled_data = np.squeeze(upsampled_data, axis=dim)
    
    print(f"Upsampled from {original_shape} to {upsampled_data.shape} (target: {target_height}x{target_width})")
    
    return upsampled_data

