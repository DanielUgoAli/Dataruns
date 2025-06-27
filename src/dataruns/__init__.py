"""
Dataruns
========

Dataruns is a Python package designed for managing and processing data pipelines. 
It provides tools for data transformation, loading, and sourcing, making it easier 
to handle complex data workflows.

Main Components:
- core: Pipeline creation and data transformations
- source: Data extraction from various sources (CSV, Excel, SQLite)

Example Usage:
    >>> from dataruns import Pipeline
    >>> from dataruns.core.transforms import StandardScaler
    >>> from dataruns.source import CSVSource
    
    >>> # Extract data
    >>> source = CSVSource('data.csv')
    >>> data = source.extract_data()
    
    >>> # Create pipeline
    >>> scaler = StandardScaler()
    >>> pipeline = Pipeline(scaler)
    >>> result = pipeline(data)

😁😁
"""

# Version information
__version__ = "1.0.dev"



# Core imports
from .core import (
    Pipeline, 
    Make_Pipeline,
    Transform,
    StandardScaler,
    MinMaxScaler,
    DropNA,
    FillNA,
    SelectColumns,
    RenameColumns,
    FilterRows,
    ApplyFunction,
    OneHotEncoder,
    TransformComposer,
    create_preprocessing_pipeline
)

# Source imports
from .source import (
    CSVSource,
    XLSsource,
    SQLiteSource
)

# Expose commonly used external dependencies
import pandas as pd
import numpy as np

# Make pandas and numpy available at package level for convenience
__all__ = [
    # Version info
    '__version__',
    '__author__',
    '__email__',
    
    # Core pipeline classes
    'Pipeline',
    'Make_Pipeline',
    
    # Transform classes
    'Transform',
    'StandardScaler', 
    'MinMaxScaler',
    'DropNA',
    'FillNA',
    'SelectColumns',
    'RenameColumns',
    'FilterRows',
    'ApplyFunction',
    'OneHotEncoder',
    'TransformComposer',
    'create_preprocessing_pipeline',
    
    # Data sources
    'CSVSource',
    'XLSsource', 
    'SQLiteSource',
    
    # External dependencies
    'pd',
    'np'
]

# Package level convenience functions
def quick_pipeline(*transforms):
    """
    Create a quick pipeline with the given transforms.
    
    Args:
        *transforms: Transform objects or functions to chain
        
    Returns:
        Pipeline: Configured pipeline ready to use
        
    Example:
        >>> scaler = StandardScaler()
        >>> fillna = FillNA(method='mean')
        >>> pipeline = quick_pipeline(fillna, scaler)
    """
    if len(transforms) == 1 and isinstance(transforms[0], (list, tuple)):
        transforms = transforms[0]
    return Pipeline(*transforms)

def load_csv(file_path, **kwargs):
    """
    Convenience function to load CSV data.
    
    Args:
        file_path (str): Path to CSV file
        **kwargs: Additional arguments passed to CSVSource
        
    Returns:
        pandas.DataFrame: Loaded data
        
    Example:
        >>> data = load_csv('data.csv')
    """
    source = CSVSource(file_path=file_path, **kwargs)
    return source.extract_data()


# Add convenience functions to __all__
__all__.extend(['quick_pipeline', 'load_csv'])


