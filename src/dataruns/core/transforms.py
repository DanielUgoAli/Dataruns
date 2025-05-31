from abc import ABC
import numpy as np

class Transform(ABC):
    """Base class for all transformations"""
    def __init__(self):
        pass

    def __call__(self, data):
        return self.transform(data)

    def transform(self, data):
        raise NotImplementedError("Transform method must be implemented by subclass")


class Normalize(Transform):
    """Normalize data using min-max normalization"""
    def transform(self, data):
        """
        Parameters
        ----------
        data : array-like
            Input data to normalize

        Returns
        -------
        array-like
            Normalized data scaled between minimum and maximum values
        """
        return (data - data.min()) / (data.max() - data.min())


class LogTransform(Transform):
    """Apply logarithmic transformation"""
    def __init__(self, base=np.e):
        self.base = base
        super().__init__()

    def transform(self, data) -> np.ndarray:
        """
        Parameters
        ----------
        data : array-like
            Input data to transform

        Returns
        -------
        array-like
            Log-transformed data
        """
        return np.log(data) / np.log(self.base) if self.base != np.e else np.log(data)


class PowerTransform(Transform):
    """Apply power transformation"""
    def __init__(self, power=1):
        self.power = power
        super().__init__()

    def transform(self, data) -> np.ndarray:
        """
        Parameters
        ----------
        data : array-like
            Input data to transform

        Returns
        -------
        array-like
            Power-transformed data
        """
        return np.power(data, self.power)


class OneHotEncode(Transform):
    """One-hot encode categorical features"""
    def transform(self, data):
        """
        Parameters
        ----------
        data : array-like
            Input data to encode

        Returns
        -------
        array-like
            One-hot encoded data
        """
        unique_cats = np.unique(data)
        num_cats = len(unique_cats)
        encoding = np.zeros((len(data), num_cats), dtype=int)

        for i, cat in enumerate(data):
            idx = np.where(unique_cats == cat)[0][0]
            encoding[i, idx] = 1
        
        # Store categories as an attribute instead of returning them
        self.categories_ = unique_cats
        return encoding  # Return only the encoding


class Difference(Transform):
    """Calculate difference between input data and its lag"""
    def __init__(self, lag=1):
        self.lag = lag
        super().__init__()

    def transform(self, data):
        """
        Parameters
        ----------
        data : array-like
            Input data to calculate difference

        Returns
        -------
        array-like
            Difference between the input data and its lag
        """
        # Check if it's a pandas DataFrame/Series or numpy array
        if hasattr(data, 'shift'):
            return data - data.shift(self.lag)
        else:
            # NumPy implementation for arrays
            result = np.empty_like(data)
            result[:self.lag] = np.nan  # Fill the first 'lag' elements with NaN
            result[self.lag:] = data[self.lag:] - data[:-self.lag]
            return result

