from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, Callable

import numpy as np
import pandas as pd


# This file contains the core transform class and the pipeline builder class
# This class is used to represent a transform in the pipeline.

class Transform(ABC):
    """
    Abstract base class for all transforms in the dataruns library.
    All transforms must implement the transform method.
    """
    
    def __init__(self, name: Optional[str] = None):
        self.name = name or self.__class__.__name__
        self.fitted = False
        self.metadata = {}
    
    @abstractmethod
    def transform(self, data: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """
        Transform the input data.
        
        Args:
            data: Input data to transform
            
        Returns:
            Transformed data
        """
        pass
    
    def fit(self, data: Union[np.ndarray, pd.DataFrame]) -> 'Transform':
        """
        Fit the transform to the data. Override if needed.
        
        Args:
            data: Data to fit the transform on
            
        Returns:
            Self for method chaining
        """
        self.fitted = True
        return self
    
    def fit_transform(self, data: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """
        Fit the transform and then transform the data.
        
        Args:
            data: Data to fit and transform
            
        Returns:
            Transformed data
        """
        return self.fit(data).transform(data)
    
    def __call__(self, data: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Make transform callable."""
        return self.transform(data)
    
    def __repr__(self):
        return f"{self.name}(fitted={self.fitted})"


class StandardScaler(Transform):
    """
    Standardize features by removing the mean and scaling to unit variance.
    """
    
    def __init__(self, with_mean: bool = True, with_std: bool = True):
        super().__init__()
        self.with_mean = with_mean
        self.with_std = with_std
        self.mean_ = None
        self.std_ = None
    
    def fit(self, data: Union[np.ndarray, pd.DataFrame]) -> 'StandardScaler':
        """Compute the mean and std to be used for later scaling."""
        if isinstance(data, pd.DataFrame):
            if self.with_mean:
                self.mean_ = data.mean()
            if self.with_std:
                self.std_ = data.std()
        else:
            if self.with_mean:
                self.mean_ = np.mean(data, axis=0)
            if self.with_std:
                self.std_ = np.std(data, axis=0)
        
        self.fitted = True
        return self
    
    def transform(self, data: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Perform standardization by centering and scaling."""
        if not self.fitted:
            raise ValueError("StandardScaler must be fitted before transform")
        
        result = data.copy() if isinstance(data, pd.DataFrame) else data.copy()
        
        if self.with_mean and self.mean_ is not None:
            result = result - self.mean_
        
        if self.with_std and self.std_ is not None:
            # Avoid division by zero
            std_safe = self.std_.replace(0, 1) if isinstance(self.std_, pd.Series) else np.where(self.std_ == 0, 1, self.std_)
            result = result / std_safe
        
        return result


class MinMaxScaler(Transform):
    """
    Scale features to a given range, typically [0, 1].
    """
    
    def __init__(self, feature_range: tuple = (0, 1)):
        super().__init__()
        self.feature_range = feature_range
        self.min_ = None
        self.max_ = None
        self.scale_ = None
    
    def fit(self, data: Union[np.ndarray, pd.DataFrame]) -> 'MinMaxScaler':
        """Compute the minimum and maximum to be used for later scaling."""
        if isinstance(data, pd.DataFrame):
            self.min_ = data.min()
            self.max_ = data.max()
        else:
            self.min_ = np.min(data, axis=0)
            self.max_ = np.max(data, axis=0)
        
        # Compute scale
        data_range = self.max_ - self.min_
        # Avoid division by zero
        if isinstance(data_range, pd.Series):
            data_range = data_range.replace(0, 1)
        else:
            data_range = np.where(data_range == 0, 1, data_range)
        
        self.scale_ = (self.feature_range[1] - self.feature_range[0]) / data_range
        self.fitted = True
        return self
    
    def transform(self, data: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Scale features to the specified range."""
        if not self.fitted:
            raise ValueError("MinMaxScaler must be fitted before transform")
        
        result = (data - self.min_) * self.scale_ + self.feature_range[0]
        return result


class DropNA(Transform):
    """
    Remove rows or columns with missing values.
    """
    
    def __init__(self, axis: int = 0, how: str = 'any', thresh: Optional[int] = None):
        super().__init__()
        self.axis = axis  # 0 for rows, 1 for columns
        self.how = how  # 'any' or 'all'
        self.thresh = thresh
    
    def transform(self, data: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Remove missing values."""
        if isinstance(data, pd.DataFrame):
            if self.thresh is not None:
                return data.dropna(axis=self.axis, thresh=self.thresh)
            else:
                return data.dropna(axis=self.axis, how=self.how)
        else:
            # For numpy arrays, remove rows/columns with NaN
            if self.axis == 0:  # Remove rows
                if self.thresh is not None:
                    # Keep rows with at least 'thresh' non-NaN values
                    mask = np.sum(~np.isnan(data), axis=1) >= self.thresh
                elif self.how == 'any':
                    mask = ~np.isnan(data).any(axis=1)
                else:  # 'all'
                    mask = ~np.isnan(data).all(axis=1)
                return data[mask]
            else:  # Remove columns
                if self.thresh is not None:
                    # Keep columns with at least 'thresh' non-NaN values
                    mask = np.sum(~np.isnan(data), axis=0) >= self.thresh
                elif self.how == 'any':
                    mask = ~np.isnan(data).any(axis=0)
                else:  # 'all'
                    mask = ~np.isnan(data).all(axis=0)
                return data[:, mask]


class FillNA(Transform):
    """
    Fill missing values with a specified value or strategy.
    """
    
    def __init__(self, value: Optional[Any] = None, method: Optional[str] = None):
        super().__init__()
        self.value = value
        self.method = method  # 'mean', 'median', 'mode'
        self.fill_values_ = None
    
    def fit(self, data: Union[np.ndarray, pd.DataFrame]) -> 'FillNA':
        """Compute fill values based on the method."""
        if self.value is not None:
            self.fill_values_ = self.value
        elif self.method == 'mean':
            if isinstance(data, pd.DataFrame):
                self.fill_values_ = data.mean()
            else:
                self.fill_values_ = np.nanmean(data, axis=0)
        elif self.method == 'median':
            if isinstance(data, pd.DataFrame):
                self.fill_values_ = data.median()
            else:
                self.fill_values_ = np.nanmedian(data, axis=0)
        elif self.method == 'mode':
            if isinstance(data, pd.DataFrame):
                self.fill_values_ = data.mode().iloc[0]
            else:
                
                def mode_1d(arr):
                    """Calculate mode for 1D array, ignoring NaN values."""
                    arr_clean = arr[~np.isnan(arr)]
                    if len(arr_clean) == 0:
                        return 0
                    values, counts = np.unique(arr_clean, return_counts=True)
                    return values[np.argmax(counts)]
                
                if data.ndim == 1:
                    self.fill_values_ = mode_1d(data)# Pure numpy mode calculation without scipy
                else:
                    self.fill_values_ = np.array([mode_1d(data[:, i]) for i in range(data.shape[1])])
        
        self.fitted = True
        return self
    
    def transform(self, data: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Fill missing values."""
        if isinstance(data, pd.DataFrame):
            if self.method in ['forward', 'backward']:
                return data.fillna(method=self.method)
            else:
                return data.fillna(self.fill_values_)
        else:
            # For numpy arrays
            result = data.copy()
            if self.fill_values_ is not None:
                mask = np.isnan(result)
                if np.isscalar(self.fill_values_):
                    result[mask] = self.fill_values_
                else:
                    for i, fill_val in enumerate(self.fill_values_):
                        result[mask[:, i], i] = fill_val
            return result


class SelectColumns(Transform):
    """
    Select specific columns from a DataFrame.
    """
    
    def __init__(self, columns: List[Union[str, int]]):
        super().__init__()
        self.columns = columns
    
    def transform(self, data: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Select specified columns."""
        if isinstance(data, pd.DataFrame):
            return data[self.columns]
        else:
            # For numpy arrays, assume columns are indices
            return data[:, self.columns]


class RenameColumns(Transform):
    """
    Rename columns in a DataFrame.
    """
    
    def __init__(self, mapping: Dict[str, str]):
        super().__init__()
        self.mapping = mapping
    
    def transform(self, data: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Rename columns."""
        if isinstance(data, pd.DataFrame):
            return data.rename(columns=self.mapping)
        else:
            # Cannot rename columns in numpy arrays
            return data


class FilterRows(Transform):
    """
    Filter rows based on a condition.
    """
    
    def __init__(self, condition: Callable[[Union[np.ndarray, pd.DataFrame]], np.ndarray]):
        super().__init__()
        self.condition = condition
    
    def transform(self, data: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Filter rows based on the condition."""
        mask = self.condition(data)
        if isinstance(data, pd.DataFrame):
            return data[mask]
        else:
            return data[mask]


class OneHotEncoder(Transform):
    """
    Encode categorical variables as one-hot vectors.
    """
    
    def __init__(self, columns: Optional[List[str]] = None, drop_first: bool = False):
        super().__init__()
        self.columns = columns
        self.drop_first = drop_first
        self.categories_ = None
    
    def fit(self, data: Union[np.ndarray, pd.DataFrame]) -> 'OneHotEncoder':
        """Learn the categories for one-hot encoding."""
        if isinstance(data, pd.DataFrame):
            cols = self.columns or data.select_dtypes(include=['object', 'category']).columns.tolist()
            self.categories_ = {col: data[col].unique() for col in cols}
        else:
            raise ValueError("OneHotEncoder requires DataFrame input")
        
        self.fitted = True
        return self
    
    def transform(self, data: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Perform one-hot encoding."""
        if not self.fitted:
            raise ValueError("OneHotEncoder must be fitted before transform")
        
        if isinstance(data, pd.DataFrame):
            result = data.copy()
            for col, categories in self.categories_.items():
                # Create dummy variables
                dummies = pd.get_dummies(result[col], prefix=col, drop_first=self.drop_first)
                # Drop original column and add dummies
                result = result.drop(columns=[col])
                result = pd.concat([result, dummies], axis=1)
            return result
        else:
            raise ValueError("OneHotEncoder requires DataFrame input")


class TransformComposer:
    """
    Compose multiple transforms into a single pipeline-like object.
    """
    
    def __init__(self, *transforms: Transform):
        self.transforms = list(transforms)
        self.fitted = False
    
    def add_transform(self, transform: Transform) -> 'TransformComposer':
        """Add a transform to the composer."""
        self.transforms.append(transform)
        return self
    
    def fit(self, data: Union[np.ndarray, pd.DataFrame]) -> 'TransformComposer':
        """Fit all transforms in sequence."""
        current_data = data
        for transform in self.transforms:
            if hasattr(transform, 'fit'):
                transform.fit(current_data)
                current_data = transform.transform(current_data)
        
        self.fitted = True
        return self
    
    def transform(self, data: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Apply all transforms in sequence."""
        result = data
        for transform in self.transforms:
            result = transform.transform(result)
        return result
    
    def fit_transform(self, data: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Fit all transforms and then transform the data."""
        return self.fit(data).transform(data)
    
    def __call__(self, data: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Make composer callable."""
        return self.transform(data)
    
    def __repr__(self):
        return f"TransformComposer({len(self.transforms)} transforms)"


# Convenience functions for creating common transform pipelines
def create_preprocessing_pipeline(
    scale_method: str = 'standard',
    handle_missing: str = 'drop',
    fill_value: Any = None
) -> TransformComposer:
    """
    Create a common preprocessing pipeline.
    
    Args:
        scale_method: 'standard', 'minmax', or None
        handle_missing: 'drop', 'fill', or None
        fill_value: Value to fill missing data with if handle_missing='fill'
    
    Returns:
        TransformComposer with preprocessing steps
    """
    composer = TransformComposer()
    
    # Handle missing values
    if handle_missing == 'drop':
        composer.add_transform(DropNA())
    elif handle_missing == 'fill':
        if fill_value is not None:
            composer.add_transform(FillNA(value=fill_value))
        else:
            composer.add_transform(FillNA(method='mean'))
    
    # Scaling
    if scale_method == 'standard':
        composer.add_transform(StandardScaler())
    elif scale_method == 'minmax':
        composer.add_transform(MinMaxScaler())
    
    return composer




