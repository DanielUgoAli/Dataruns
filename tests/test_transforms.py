"""
Quick test for the transforms module.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import pandas as pd

# Test basic functionality
def test_transforms():
    print("Starting transform tests...")
    try:
        print("Importing transforms...")
        from dataruns.core.transforms import StandardScaler, MinMaxScaler, DropNA
        print("Imports successful!")
        
        # Create test data
        data = pd.DataFrame({
            'a': [1, 2, 3, 4, 5],
            'b': [2, 4, 6, 8, 10]
        })
        print(f"Test data created: {data.shape}")
        
        # Test StandardScaler
        print("Testing StandardScaler...")
        scaler = StandardScaler()
        scaled = scaler.fit_transform(data)
        print(f"StandardScaler test passed ✓ (shape: {scaled.shape})")
        
        # Test MinMaxScaler
        print("Testing MinMaxScaler...")
        minmax = MinMaxScaler()
        minmax_scaled = minmax.fit_transform(data)
        print(f"MinMaxScaler test passed ✓ (shape: {minmax_scaled.shape})")
        
        # Test DropNA
        print("Testing DropNA...")
        data_with_na = data.copy()
        data_with_na.iloc[0, 0] = np.nan
        print(f"Data with NA: {data_with_na.isnull().sum().sum()} missing values")
        dropna = DropNA()
        clean_data = dropna.transform(data_with_na)
        print(f"DropNA test passed ✓ (shape: {clean_data.shape})")
        
        print("All basic tests passed! ✓✓✓")
        return True
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_transforms()
