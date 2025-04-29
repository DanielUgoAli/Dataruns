# Dataruns

Dataruns is a Python-based library designed for seamless data extraction, transformation, and pipeline creation. It supports multiple data sources like CSV, SQLite, and Excel, and provides tools for building and applying data processing pipelines.

## Features

- Extract data from CSV, SQLite, and Excel files.
- Build and execute custom data processing pipelines.
- Includes experimental features for performance optimization. 😗

## Installation

Clone the repository and install the required dependencies:

Soon to be on pypi just more work needed.

```bash
git clone https://github.com/DanielUgoAli/Dataruns.git
cd Dataruns
uv sync
uv pip install -e .
```

## Usage

### Extracting Data

```python
from dataruns.source import CSVSource

source = CSVSource(file_path='data.csv')
dataframe = source.extract_data()
print(dataframe.head())
```

### Building a Pipeline

```python
from dataruns.core import Pipeline

def transform_function(data):
    return data * 2

pipeline = Pipeline(transform_function)
result = pipeline([1, 2, 3])
print(result)
```

### Advanced Pipeline Example

```python
from dataruns.core import Pipeline
import pandas as pd

def clean_data(df):
    return df.dropna()

def normalize_columns(df):
    return (df - df.mean()) / df.std()

pipeline = Pipeline([clean_data, normalize_columns])
result = pipeline(pd.DataFrame({'A': [1, 2, None, 4]}))
```

## Help

### Help is much appreciated just open a pull request 😗
