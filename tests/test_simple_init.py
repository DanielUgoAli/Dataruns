"""
Simple test to verify init files work.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_basic_imports():
    """Test basic package imports."""
    print("Testing basic imports...")
    
    try:
        # Test core module
        from dataruns.core import Pipeline, StandardScaler
        print("✓ Core module imports work")
        
        # Test source module  
        from dataruns.source import CSVSource
        print("✓ Source module imports work")
    
        
        # Test main package
        import dataruns
        print(f"✓ Main package imports work - version {dataruns.__version__}")
        
        return True
        
    except Exception as e:
        print(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_functionality():
    """Test basic functionality."""
    print("\nTesting basic functionality...")
    
    try:
        import numpy as np
        import pandas as pd
        from dataruns.core import Pipeline, StandardScaler
        
        # Create test data
        data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        
        # Test transform
        scaler = StandardScaler()
        scaled = scaler.fit_transform(data)
        print(f"✓ StandardScaler works - output shape: {scaled.shape}")
        
        # Test pipeline
        pipeline = Pipeline(scaler)
        result = pipeline(data)
        print(f"✓ Pipeline works - output shape: {result.shape}")
        
        return True
        
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("SIMPLE INIT FILES TEST")
    print("=" * 30)
    
    test1 = test_basic_imports()
    test2 = test_functionality()
    
    if test1 and test2:
        print("\n✓✓✓ ALL TESTS PASSED!")
    else:
        print("\n✗ SOME TESTS FAILED")
