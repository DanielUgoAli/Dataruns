"""
Dataruns Source Module
=====================

This module provides data extraction capabilities from various sources including:
- CSV files
- Excel files (XLS/XLSX)
- SQLite databases

Example Usage:
    >>> from dataruns.source import CSVSource, XLSsource, SQLiteSource
    
    >>> # Load CSV data
    >>> csv_source = CSVSource(file_path='data.csv')
    >>> data = csv_source.extract_data()
    
    >>> # Load Excel data
    >>> excel_source = XLSsource(file_path='data.xlsx')
    >>> data = excel_source.extract_data()
    
    >>> # Load SQLite data
    >>> db_source = SQLiteSource(db_path='database.db', table_name='my_table')
    >>> data = db_source.extract_data()
"""

import logging
import os

# Configure logging for the source module
def _setup_logging():
    """Setup logging configuration for the source module."""
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except OSError:
            # If we can't create logs directory, use a simpler logging setup
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            logger.info("Dataruns source module initialized (console logging)")
            return logger
    
    log_file = os.path.join(log_dir, 'dataruns_source.log')
    
    try:
        logging.basicConfig(
            level=logging.INFO,
            filename=log_file,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filemode='a'
        )
        logger = logging.getLogger(__name__)
        logger.info("Dataruns source module initialized successfully 📎")
        return logger
    except (OSError, PermissionError):
        # Fallback to console logging if file logging fails
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.info("Dataruns source module initialized (console logging fallback)")
        return logger

# Setup logger
logger = _setup_logging()

# Import source classes
from .datasource import CSVSource, XLSsource, SQLiteSource

# Try to import the base class if it exists
try:
    from .datasource import DataSource
    _base_class_available = True
except ImportError:
    _base_class_available = False
    logger.warning("DataSource base class not found in datasource module")

# Define exports
__all__ = [
    'CSVSource',
    'XLSsource', 
    'SQLiteSource'
]

# Add base class if available
if _base_class_available:
    __all__.append('DataSource')

# Module level convenience functions 🙂
def load_data(file_path, source_type=None, **kwargs):
    """
    Automatically detect and load data from various sources.
    
    Args:
        file_path (str): Path to the data file
        source_type (str, optional): Force specific source type ('csv', 'excel', 'sqlite')
        **kwargs: Additional arguments passed to the source class
        
    Returns:
        pandas.DataFrame: Loaded data
        
    Raises:
        ValueError: If file type cannot be determined or is not supported
        
    Example:
        >>> data = load_data('data.csv')
        >>> data = load_data('data.xlsx')
        >>> data = load_data('database.db', table_name='users')
    """
    if source_type:
        source_type = source_type.lower()
    else:
        # Auto-detect based on file extension
        _, ext = os.path.splitext(file_path.lower())
        if ext in ['.csv']:
            source_type = 'csv'
        elif ext in ['.xls', '.xlsx']:
            source_type = 'excel'
        elif ext in ['.db', '.sqlite', '.sqlite3']:
            source_type = 'sqlite'
        else:
            raise ValueError(f"Cannot determine source type for file: {file_path}")
    
    # Create appropriate source
    if source_type == 'csv':
        source = CSVSource(file_path=file_path, **kwargs)
    elif source_type == 'excel':
        source = XLSsource(file_path=file_path, **kwargs)
    elif source_type == 'sqlite':
        if 'table_name' not in kwargs:
            raise ValueError("table_name is required for SQLite sources")
        source = SQLiteSource(db_path=file_path, **kwargs)
    else:
        raise ValueError(f"Unsupported source type: {source_type}")
    
    logger.info(f"Loading data from {file_path} using {source_type} source")
    return source.extract_data()

def list_supported_formats():
    """
    List all supported file formats.
    
    Returns:
        dict: Dictionary mapping format names to file extensions
        
    Example:
        >>> formats = list_supported_formats()
        >>> print(formats)
        {'csv': ['.csv'], 'excel': ['.xls', '.xlsx'], 'sqlite': ['.db', '.sqlite', '.sqlite3']}
    """
    return {
        'csv': ['.csv'],
        'excel': ['.xls', '.xlsx'], 
        'sqlite': ['.db', '.sqlite', '.sqlite3']
    }

def get_source_info():
    """
    Get information about available data sources.
    
    Returns:
        dict: Information about each source class
    """
    info = {
        'CSVSource': {
            'description': 'Extract data from CSV files',
            'supported_formats': ['.csv'],
            'required_params': ['file_path']
        },
        'XLSsource': {
            'description': 'Extract data from Excel files',
            'supported_formats': ['.xls', '.xlsx'],
            'required_params': ['file_path']
        },
        'SQLiteSource': {
            'description': 'Extract data from SQLite databases',
            'supported_formats': ['.db', '.sqlite', '.sqlite3'],
            'required_params': ['db_path', 'table_name']
        }
    }
    return info

# Add convenience functions to exports
__all__.extend(['load_data', 'list_supported_formats', 'get_source_info', 'logger'])

