"""
Dataruns Core Module
===================

This module contains the core functionality for pipeline creation and data transformations.

Components:
- pipeline: Pipeline and Make_Pipeline classes for chaining operations
- transforms: Comprehensive set of data transformation classes
- types: Core data types and function wrappers

Example Usage:
    >>> from dataruns.core import Pipeline, StandardScaler, TransformComposer
    >>> from dataruns.core import create_preprocessing_pipeline
    
    >>> # Create individual transforms
    >>> scaler = StandardScaler()
    >>> pipeline = Pipeline(scaler)
    
    >>> # Create composed transforms
    >>> composer = TransformComposer(FillNA(), StandardScaler())
    >>> result = composer.fit_transform(data)
"""
# Pipeline imports
from .pipeline import Pipeline, Make_Pipeline
# Transform imports
from .transforms import (
    # Base class
    Transform,
    
    # Scaling transforms
    StandardScaler,
    MinMaxScaler,
    
    # Missing value handling
    DropNA,
    FillNA,
    
    # Column operations
    SelectColumns,
    RenameColumns,
    
    # Row operations
    FilterRows,
    
    # Encoding
    OneHotEncoder,
    
    # Composition[The PIPELINE of transforms]
    TransformComposer,
    
    # Convenience functions
    create_preprocessing_pipeline
)
# Type imports
from .types import Function

# Define what gets exported with "from dataruns.core import *"
__all__ = [
    # Pipeline classes
    'Pipeline',
    'Make_Pipeline',
    
    # Transform base class
    'Transform',
    
    # Scaling transforms
    'StandardScaler',
    'MinMaxScaler',
    
    # Missing value handling
    'DropNA', 
    'FillNA',
    
    # Column operations
    'SelectColumns',
    'RenameColumns',
    
    # Row operations
    'FilterRows',
    
    # Encoding
    'OneHotEncoder',
    
    # Composition
    'TransformComposer',
    
    # Convenience functions
    'create_preprocessing_pipeline',
    
    # Core types
    'Function'
]

# Module level convenience functions
def list_transforms():
    """
    List all available transform classes.
    
    Returns:
        list: Names of all available transform classes
    """
    transforms = [
        'StandardScaler', 'MinMaxScaler', 'DropNA', 'FillNA',
        'SelectColumns', 'RenameColumns', 'FilterRows', 'ApplyFunction',
        'OneHotEncoder'
    ]
    return transforms

def create_simple_pipeline(*steps):
    """
    Create a simple pipeline from transform steps.
    
    Args:
        *steps: Transform objects or functions
        
    Returns:
        Pipeline: Created pipeline
        
    Example:
        >>> pipeline = create_simple_pipeline(
        ...     FillNA(method='mean'),
        ...     StandardScaler()
        ... )
    """
    return Pipeline(*steps)

# Add convenience functions to exports
__all__.extend(['list_transforms', 'create_simple_pipeline'])
