# from netCDF4 import Dataset
import numpy as np
import xarray as xr
import os
import re
import glob


def load_netcdf_data(file_paths, data_dir='data', variable_names=None, fillna_value=0):
    """
    Load NetCDF files and extract specified variables/bands.
    
    Parameters:
    -----------
    file_paths : list of str
        List of NetCDF file names to load
    data_dir : str, optional
        Directory path where the NetCDF files are located (default: 'data')
    variable_names : list of str, optional
        List of variable/band names to extract (default: ['Band1', 'Band2', 'Band3', 'Band4', 'Band5'])
    fillna_value : float, optional
        Value to use for filling NaN values (default: 0)
    
    Returns:
    --------
    tuple
        (data_array, lat_coords, lon_coords) where:
        - data_array is a NumPy array with shape (num_files, height, width, number_of_channels)
        - lat_coords is a 1D NumPy array of latitude coordinates taken from dataset['lat']
        - lon_coords is a 1D NumPy array of longitude coordinates taken from dataset['lon']
    """
    if variable_names is None:
        variable_names = ['Band1', 'Band2', 'Band3', 'Band4', 'Band5']
    
    # Initialize an empty list to store NumPy arrays
    data_list = []
    lat_coords = None
    lon_coords = None
    
    # Loop through each file, load the variable, and append to the list
    for file_path in file_paths:
        full_path = os.path.join(data_dir, file_path)
        temporarial = []
        if os.path.exists(full_path):  # Check if the file exists
            print(f"Loading file: {file_path}")
            
            # Open the file using xarray
            dataset = xr.open_dataset(full_path)
            dataset = dataset.fillna(fillna_value)
            
            # Capture latitude/longitude coordinates from the first dataset
            if lat_coords is None or lon_coords is None:
                try:
                    lat_coords = dataset["lat"].values
                    lon_coords = dataset["lon"].values
                except KeyError as e:
                    raise KeyError(
                        f"Could not find required coordinate variables 'lat' and 'lon' "
                        f"in NetCDF file {full_path}"
                    ) from e
            
            for variable_name in variable_names:
                # Extract the variable as a NumPy array and append to the list
                data_array = dataset[variable_name].values  # Extract data as NumPy array
                temporarial.append(data_array)
                # print(f"Shape of data from {file_path}: {data_array.shape}")
        data_list.append(temporarial)
    
    if not data_list:
        raise ValueError("No data was loaded from the provided NetCDF file paths.")
    
    if lat_coords is None or lon_coords is None:
        raise ValueError("Latitude/longitude coordinates could not be read from the NetCDF files.")
    
    # Reorder axes to (samples, height, width, number_of_channels)
    array_reordered = np.transpose(np.array(data_list), (0, 2, 3, 1))
    
    return array_reordered, lat_coords, lon_coords


def extract_last_two_numbers(path):
    """Extract the last two numbers from a file path."""
    numbers = re.findall(r'\d+', str(path))  # Find all numbers in the path
    if len(numbers) >= 2:
        return int(numbers[-2]), int(numbers[-1])  # Return the last two numbers
    elif len(numbers) == 1:
        return 0, int(numbers[-1])  # If only one number, assume 0 for the second-to-last
    else:
        return (0, 0)  # Default case if no numbers are found


def sort_paths_by_last_two_numbers(file_paths):
    """Sort file paths based on the last two numbers in the path."""
    return sorted(file_paths, key=extract_last_two_numbers)


def load_ndvi_data(data_dir='data', pattern='ndvi20*.nc', fillna_value=0):
    """
    Load NDVI NetCDF files, sort them by the last two numbers in the filename,
    and extract Band1 from each file.
    
    Parameters:
    -----------
    data_dir : str, optional
        Directory path where the NetCDF files are located (default: 'data')
    pattern : str, optional
        File pattern to match (default: 'ndvi20*.nc')
    fillna_value : float, optional
        Value to use for filling NaN values (default: 0)
    
    Returns:
    --------
    numpy.ndarray
        Array with shape (num_files, height, width, 1) containing Band1 data from each file
    """
    # Find all matching files
    search_pattern = os.path.join(data_dir, pattern)
    matching_files = glob.glob(search_pattern)
    
    if not matching_files:
        raise ValueError(f"No files found matching pattern: {search_pattern}")
    
    # Sort files by the last two numbers in the path
    sorted_paths = sort_paths_by_last_two_numbers(matching_files)
    
    # Initialize list to store data arrays
    data_list = []
    
    # Load data from each file
    for file_path in sorted_paths:
        print(f"Loading file: {os.path.basename(file_path)}")
        data = xr.open_dataset(file_path)
        arr = data["Band1"].fillna(fillna_value).values
        # Add channel dimension: (height, width) -> (height, width, 1)
        arr = np.expand_dims(arr, axis=-1)
        data_list.append(arr)
    
    # Stack all arrays: (num_files, height, width, 1)
    data_array = np.array(data_list)
    
    print(f"Loaded {len(sorted_paths)} NDVI files with final shape: {data_array.shape}")
    
    return data_array


def load_static_features(data_dir='data', num_samples=25, fillna_value=0):
    """
    Load static feature files (dem.nc, road_dis.nc, slope.nc) and tile them
    to match the time series data shape.
    
    Parameters:
    -----------
    data_dir : str, optional
        Directory path where the NetCDF files are located (default: 'data')
    num_samples : int, optional
        Number of time samples to tile to (default: 25)
    fillna_value : float, optional
        Value to use for filling NaN values (default: 0)
    
    Returns:
    --------
    numpy.ndarray
        Array with shape (num_samples, height, width, 3) containing dem, road_dis, and slope data
    """
    file_names = ['dem.nc', 'road_dis.nc', 'slope.nc',"river_dis.nc"]
    data_list = []
    
    for file_name in file_names:
        file_path = os.path.join(data_dir, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        print(f"Loading file: {file_name}")
        dataset = xr.open_dataset(file_path)
        dataset = dataset.fillna(fillna_value)
        
        # Try to get the first data variable (skip coordinate variables)
        data_vars = list(dataset.data_vars.keys())
        if not data_vars:
            # If no data_vars, try to get first variable that's not a coordinate
            all_vars = list(dataset.variables.keys())
            coord_vars = list(dataset.coords.keys())
            data_vars = [v for v in all_vars if v not in coord_vars]
        
        if not data_vars:
            raise ValueError(f"No data variables found in {file_name}")
        
        # Use the first data variable
        variable_name = data_vars[0]
        arr = dataset[variable_name].values
        
        # Ensure 2D shape (height, width)
        if arr.ndim > 2:
            arr = arr.squeeze()
        
        if arr.ndim != 2:
            raise ValueError(f"Expected 2D array from {file_name}, got shape {arr.shape}")
        
        # Add channel dimension: (height, width) -> (height, width, 1)
        arr = np.expand_dims(arr, axis=-1)
        
        # Tile along the first axis to match num_samples: (height, width, 1) -> (num_samples, height, width, 1)
        arr_tiled = np.tile(arr, (num_samples, 1, 1, 1))
        
        data_list.append(arr_tiled)
    
    # Concatenate along channel axis: (num_samples, height, width, 1) each -> (num_samples, height, width, 3)
    result = np.concatenate(data_list, axis=3)
    
    print(f"Loaded static features with final shape: {result.shape}")
    
    return result


def downsample_spatial(data, stride=2, method='average'):
    """
    Downsample spatial dimensions (height and width) of the data by the specified stride.
    
    Parameters:
    -----------
    data : numpy.ndarray
        Input data with shape (..., height, width, channels) or (..., height, width)
    stride : int, optional
        Downsampling stride (default: 2). Both height and width will be reduced by this factor.
    method : str, optional
        Downsampling method: 'average' for average pooling or 'max' for max pooling (default: 'average')
    
    Returns:
    --------
    numpy.ndarray
        Downsampled data with shape (..., height//stride, width//stride, channels)
        Original dimensions are preserved except for height and width.
    """
    if stride < 1:
        raise ValueError("Stride must be >= 1")
    
    if stride == 1:
        return data
    
    original_shape = data.shape
    
    # Handle different input dimensions
    if data.ndim == 2:
        # 2D: (height, width) -> add dummy dimensions
        data = data[np.newaxis, np.newaxis, :, :]
        squeeze_dims = [0, 1]
    elif data.ndim == 3:
        # 3D: (height, width, channels) -> add dummy dimension
        data = data[np.newaxis, :, :, :]
        squeeze_dims = [0]
    elif data.ndim == 4:
        # 4D: (samples, height, width, channels) or (samples, frames, height, width)
        squeeze_dims = []
    elif data.ndim == 5:
        # 5D: (samples, frames, height, width, channels)
        squeeze_dims = []
    else:
        raise ValueError(f"Unsupported number of dimensions: {data.ndim}")
    
    # Handle different dimensions
    if data.ndim == 5:
        # (samples, frames, height, width, channels)
        samples, frames, h, w, c = data.shape
        # Truncate to make dimensions divisible by stride
        h_truncated = (h // stride) * stride
        w_truncated = (w // stride) * stride
        new_height = h_truncated // stride
        new_width = w_truncated // stride
        data_reshaped = data.reshape(-1, h, w, c)
        downsampled_list = []
        
        for i in range(data_reshaped.shape[0]):
            img = data_reshaped[i]
            # Truncate image to make dimensions divisible
            img_truncated = img[:h_truncated, :w_truncated, :]
            if method == 'average':
                # Average pooling using reshape
                downsampled = img_truncated.reshape(new_height, stride, new_width, stride, c).mean(axis=(1, 3))
            else:  # max
                # Max pooling
                downsampled = img_truncated.reshape(new_height, stride, new_width, stride, c).max(axis=(1, 3))
            downsampled_list.append(downsampled)
        
        downsampled_data = np.array(downsampled_list).reshape(samples, frames, new_height, new_width, c)
    elif data.ndim == 4:
        # 4D: (samples, height, width, channels)
        samples, h, w, c = data.shape
        # Truncate to make dimensions divisible by stride
        h_truncated = (h // stride) * stride
        w_truncated = (w // stride) * stride
        new_height = h_truncated // stride
        new_width = w_truncated // stride
        downsampled_list = []
        
        for i in range(samples):
            img = data[i]
            # Truncate image to make dimensions divisible
            img_truncated = img[:h_truncated, :w_truncated, :]
            if method == 'average':
                # Average pooling using reshape
                downsampled = img_truncated.reshape(new_height, stride, new_width, stride, c).mean(axis=(1, 3))
            else:  # max
                # Max pooling
                downsampled = img_truncated.reshape(new_height, stride, new_width, stride, c).max(axis=(1, 3))
            downsampled_list.append(downsampled)
        
        downsampled_data = np.array(downsampled_list).reshape(samples, new_height, new_width, c)
    else:
        # For other dimensions, reshape to 4D and process
        if data.ndim == 3:
            # (height, width, channels)
            h, w, c = data.shape
            samples = 1
            data = data[np.newaxis, :, :, :]
        else:
            # Should have been handled above
            raise ValueError(f"Unexpected dimensions after preprocessing: {data.ndim}")
        
        # Truncate to make dimensions divisible by stride
        h_truncated = (h // stride) * stride
        w_truncated = (w // stride) * stride
        new_height = h_truncated // stride
        new_width = w_truncated // stride
        img = data[0]
        # Truncate image to make dimensions divisible
        img_truncated = img[:h_truncated, :w_truncated, :]
        if method == 'average':
            downsampled = img_truncated.reshape(new_height, stride, new_width, stride, c).mean(axis=(1, 3))
        else:
            downsampled = img_truncated.reshape(new_height, stride, new_width, stride, c).max(axis=(1, 3))
        
        downsampled_data = downsampled[np.newaxis, :, :, :]
    
    # Remove dummy dimensions that were added
    for dim in sorted(squeeze_dims, reverse=True):
        downsampled_data = np.squeeze(downsampled_data, axis=dim)
    
    print(f"Downsampled from {original_shape} to {downsampled_data.shape} (stride={stride})")
    
    return downsampled_data
