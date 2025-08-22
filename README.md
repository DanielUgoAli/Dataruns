**Note: Still a lot of bugs**
# Dataruns

Dataruns is a Python-based library designed for seamless data extraction, transformation, and pipeline creation. It supports multiple data sources like CSV, SQLite, and Excel, and provides tools for building and applying data processing pipelines with a comprehensive set of data transformations.

## Features

- **Data Extraction**: Extract data from CSV, SQLite, and Excel files
- **Pipeline Creation**: Build and execute custom data processing pipelines
- **Data Transformations**: Comprehensive set of data transforms including:
  - Scaling (StandardScaler, MinMaxScaler)
  - Missing value handling (DropNA, FillNA)  
  - Column operations (SelectColumns, RenameColumns)
  - One-hot encoding for categorical variables
- **Pipeline Composition**: Chain multiple transforms and operations
- **Flexible Integration**: Works with pandas DataFrames and numpy arrays
- **Experimental Features**: Performance optimization features 😗

## Installation

Clone the repository and install the required dependencies using `uv`:

```bash
pip install datatruns

or 

uv pip install dataruns
```

Or, if you prefer to work with the latest development version, you can clone the repository and set up a virtual environment:

```bash
git clone -b dev https://github.com/DanielUgoAli/Dataruns.git
cd Dataruns

# Create a virtual environment with uv
uv venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
# source .venv/bin/activate

# Install dependencies
uv sync
```

Alternatively, you can install in development mode:

```bash
# Install in editable mode with all dependencies
uv pip install -e .
```

## Quick Start

### Basic Data Extraction

```python
from dataruns.source import CSVSource

# Extract data from CSV
source = CSVSource(file_path='data.csv')
dataframe = source.extract_data()
print(dataframe.head())
```

### Simple Pipeline

```python
from dataruns.core.pipeline import Pipeline

# Create a simple transformation function
def transform_function(data):
    return data * 2

# Build and use pipeline
pipeline = Pipeline(transform_function)
result = pipeline([1, 2, 3, 4, 5])
print(result)  # [2, 4, 6, 8, 10]
```

### Data Transformations

```python
from dataruns.core.transforms import StandardScaler, FillNA, TransformComposer
import pandas as pd

# Create sample data
data = pd.DataFrame({
    'feature1': [1, 2, None, 4, 5],
    'feature2': [10, 20, 30, 40, 50]
})

# Create a preprocessing pipeline
preprocessor = TransformComposer(
    FillNA(method='mean'),
    StandardScaler()
)

# Apply transformations
processed_data = preprocessor.fit_transform(data)
print(processed_data)
```

### Advanced Pipeline Integration

```python
from dataruns.core.pipeline import Pipeline
from dataruns.core.transforms import create_preprocessing_pipeline

# Create preprocessing pipeline
preprocessing = create_preprocessing_pipeline(
    scale_method='minmax',
    handle_missing='fill'
)

# Function to apply preprocessing
def preprocess_data(data):
    numerical_data = data.select_dtypes(include=['number'])
    return preprocessing.fit_transform(numerical_data)

# Integrate with dataruns pipeline
pipeline = Pipeline(preprocess_data)
result = pipeline(your_dataframe)
```

## Examples

Comprehensive examples are available as Jupyter notebooks in the `examples/` folder:

- **`basic_usage_examples.ipynb`**: Basic pipeline and data extraction examples
- **`transform_examples.ipynb`**: Data transformation examples with various scalers and preprocessors
- **`comprehensive_transform_examples.ipynb`**: Advanced examples showing complex pipelines and custom transforms

To run the examples, you can use Jupyter or open them directly in VS Code:

```bash
# Install Jupyter if not already installed
uv add jupyter

# Launch Jupyter Lab
jupyter lab examples/

# Or run a specific notebook
jupyter notebook examples/basic_usage_examples.ipynb
```

Alternatively, you can open the `.ipynb` files directly in VS Code with the Jupyter extension for an integrated experience.

## Tests

Run the test suite to verify functionality:

```bash
# Test core pipeline functionality
python tests/test_core_functionality.py

# Test transform functionality
python tests/test_transforms.py
```

## Project Structure

```plaintext
dataruns/
├── src/dataruns/           # Source code
│   ├── core/              # Core pipeline and transform functionality
│   └── source/            # Data source extractors
├── examples/              # Usage examples and demos
├── tests/                 # Test suite
└── README.md             # This file
```

## API Reference

### Core Pipeline Classes

- **`Pipeline`**: Main pipeline class for chaining functions
- **`Make_Pipeline`**: Builder class for constructing pipelines
- **`Function`**: Wrapper class for consistent function handling

### Transform Classes

- **`Transform`**: Abstract base class for all transforms
- **`StandardScaler`**: Standardize features (mean=0, std=1)
- **`MinMaxScaler`**: Scale features to a specified range
- **`DropNA`**: Remove rows/columns with missing values
- **`FillNA`**: Fill missing values with specified strategy
- **`SelectColumns`**: Select specific columns from DataFrame
- **`TransformComposer`**: Chain multiple transforms together

### Data Sources

- **`CSVSource`**: Extract data from CSV files
- **`DataSource`**: Base class for data extractors

## Contributing

*Any editing should be done on the dev branch.*
Help is much appreciated! Please open a pull request to contribute. 😗

## License

This project is licensed under the MIT License - see the LICENSE file for details.
