# Dataruns

A Python library for data extraction, transformation, and pipeline creation.

## Installation

```bash
pip install dataruns
```

## Quick Start

```python
from dataruns.source import CSVSource
from dataruns.core.pipeline import Pipeline
from dataruns.core.transforms import StandardScaler, FillNA, TransformComposer
import pandas as pd

# Extract data
source = CSVSource(file_path='data.csv')
data = source.extract_data()

# Create preprocessing pipeline
preprocessor = TransformComposer(
    FillNA(method='mean'),
    StandardScaler()
)

# Apply transformations
processed_data = preprocessor.fit_transform(data)
```

## Features

- Extract data from CSV, SQLite, and Excel files
- Build custom data processing pipelines
- Comprehensive data transformations (scaling, missing values, column operations)
- Works with pandas DataFrames and numpy arrays

## License

MIT License