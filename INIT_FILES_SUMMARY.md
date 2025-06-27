# Dataruns Init Files Documentation

## Overview
All `__init__.py` files have been completely rewritten to provide comprehensive package organization and improved usability.

## 📁 Updated Files

### 1. **Main Package** (`src/dataruns/__init__.py`)
- **Version Information**: Added `__version__`, `__author__`, `__email__`
- **Comprehensive Imports**: All core classes and transforms available at package level
- **Convenience Functions**: 
  - `quick_pipeline(*transforms)` - Quick pipeline creation
  - `load_csv(file_path)` - Direct CSV loading
- **External Dependencies**: Exposed `pd` (pandas) and `np` (numpy) at package level
- **Proper `__all__`**: 25+ exported items for clean `from dataruns import *`

### 2. **Core Module** (`src/dataruns/core/__init__.py`)
- **Pipeline Classes**: `Pipeline`, `Make_Pipeline`, `SpeedUp` (if available)
- **All Transform Classes**: Complete set of data transformations
  - Scaling: `StandardScaler`, `MinMaxScaler`
  - Missing values: `DropNA`, `FillNA`
  - Column ops: `SelectColumns`, `RenameColumns`
  - Custom: `ApplyFunction`, `FilterRows`, `OneHotEncoder`
  - Composition: `TransformComposer`
- **Core Types**: `Function`, `Data` classes
- **Convenience Functions**:
  - `list_transforms()` - List available transforms
  - `create_simple_pipeline()` - Quick pipeline creation
- **Documentation**: Comprehensive docstrings and usage examples

### 3. **Source Module** (`src/dataruns/source/__init__.py`)
- **Data Sources**: `CSVSource`, `XLSsource`, `SQLiteSource`
- **Smart Logging**: Robust logging with fallbacks for different environments
- **Auto-detection**: `load_data()` function auto-detects file types
- **Utility Functions**:
  - `list_supported_formats()` - Show supported file types
  - `get_source_info()` - Information about each source class
- **Error Handling**: Graceful handling of missing dependencies

### 4. **DL Module** (`src/dataruns/dl/__init__.py`) ⭐ **NEW**
- **Engine Integration**: Imports deep learning engine if available
- **Dependency Checking**: `check_dependencies()` for PyTorch, TensorFlow, scikit-learn
- **Module Info**: `get_dl_info()` provides status and capabilities
- **Graceful Degradation**: Works even if DL dependencies are missing

## 🎯 Key Features

### Easy Imports
```python
# Everything available from main package
from dataruns import Pipeline, StandardScaler, CSVSource

# Or use specific modules
from dataruns.core import TransformComposer
from dataruns.source import load_data
```

### Convenience Functions
```python
# Quick pipeline creation
pipeline = dataruns.quick_pipeline(FillNA(), StandardScaler())

# Auto-detect and load data
data = dataruns.load_csv('data.csv')
data = dataruns.source.load_data('data.xlsx')  # Auto-detects Excel
```

### Information Functions
```python
# List available transforms
print(dataruns.core.list_transforms())

# Check supported file formats
print(dataruns.source.list_supported_formats())

# Check DL dependencies
print(dataruns.dl.check_dependencies())
```

### Robust Error Handling
- Logging falls back to console if file logging fails
- Missing dependencies are handled gracefully
- Clear error messages for common issues

## 🧪 Testing

All init files have been tested with:
- ✅ Individual module imports
- ✅ Cross-module integration  
- ✅ Convenience functions
- ✅ Error handling scenarios
- ✅ Complete package functionality

## 📊 Package Statistics

| Module | Classes | Functions | Total Exports |
|--------|---------|-----------|---------------|
| Main   | 15+     | 2         | 25+           |
| Core   | 12+     | 2         | 18+           |
| Source | 3       | 3         | 7             |
| DL     | 0       | 2         | 3             |

## 🎉 Benefits

1. **Cleaner Imports**: Everything needed available at package level
2. **Better Documentation**: Comprehensive docstrings and examples
3. **Easier Discovery**: List functions help users find available features
4. **Robust Error Handling**: Graceful degradation when dependencies missing
5. **Convenience**: Auto-detection and helper functions reduce boilerplate
6. **Maintainable**: Clear structure and comprehensive `__all__` definitions

## 🚀 Usage Examples

### Basic Usage
```python
import dataruns

# Load data
data = dataruns.load_csv('data.csv')

# Create preprocessing pipeline  
pipeline = dataruns.quick_pipeline(
    dataruns.FillNA(method='mean'),
    dataruns.StandardScaler()
)

# Process data
result = pipeline(data)
```

### Advanced Usage
```python
from dataruns.core import TransformComposer, create_preprocessing_pipeline
from dataruns.source import load_data

# Auto-detect file type and load
data = load_data('unknown_file.xlsx')

# Create advanced pipeline
preprocessor = create_preprocessing_pipeline(
    scale_method='minmax',
    handle_missing='fill'
)

# Apply transformations
processed = preprocessor.fit_transform(data)
```

The init files now provide a professional, well-documented, and user-friendly interface to the entire dataruns library! 🎊
