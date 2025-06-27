"""
Test script to verify all __init__.py files work correctly.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_main_package():
    """Test main dataruns package."""
    print("Testing main dataruns package...")
    try:
        import dataruns
        print(f"✓ Package version: {dataruns.__version__}")
        print(f"✓ Package author: {dataruns.__author__}")
        print(f"✓ Available items: {len(dataruns.__all__)}")
        
        # Test convenience functions
        from dataruns import quick_pipeline, load_csv
        print("✓ Convenience functions imported")
        
        # Test main classes
        from dataruns import Pipeline, StandardScaler, CSVSource
        print("✓ Main classes imported")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_core_module():
    """Test core module."""
    print("\nTesting core module...")
    try:
        from dataruns.core import (
            Pipeline, StandardScaler, TransformComposer,
            list_transforms, create_simple_pipeline
        )
        
        print("✓ Core classes imported")
        
        # Test convenience functions
        transforms = list_transforms()
        print(f"✓ Available transforms: {len(transforms)}")
        
        # Test pipeline creation
        pipeline = create_simple_pipeline(StandardScaler())
        print("✓ Simple pipeline created")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_source_module():
    """Test source module."""
    print("\nTesting source module...")
    try:
        from dataruns.source import (
            CSVSource, XLSsource, SQLiteSource,
            load_data, list_supported_formats, get_source_info
        )
        
        print("✓ Source classes imported")
        
        # Test utility functions
        formats = list_supported_formats()
        print(f"✓ Supported formats: {formats}")
        
        info = get_source_info()
        print(f"✓ Source info available for {len(info)} sources")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """Test integration between modules."""
    print("\nTesting integration...")
    try:
        # Create a simple end-to-end test
        import numpy as np
        import pandas as pd
        from dataruns import Pipeline, StandardScaler, quick_pipeline
        
        # Create test data
        data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50]
        })
        
        # Test pipeline integration
        scaler = StandardScaler()
        pipeline = Pipeline(scaler)
        result = pipeline(data)
        print(f"✓ Pipeline execution successful, result shape: {result.shape}")
        
        # Test quick_pipeline
        quick_pipe = quick_pipeline(StandardScaler())
        result2 = quick_pipe(data)
        print(f"✓ Quick pipeline execution successful, result shape: {result2.shape}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("TESTING ALL __init__.py FILES")
    print("=" * 50)
    
    tests = [
        test_main_package,
        test_core_module, 
        test_source_module,
        test_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"Test {test.__name__} failed with exception: {e}")
            failed += 1
        print("-" * 30)
    
    print(f"\nFINAL RESULTS:")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    
    if failed == 0:
        print("ALL INIT FILES WORKING CORRECTLY! ✓✓✓")
        return True
    else:
        print(f"{failed} TESTS FAILED ✗")
        return False

if __name__ == "__main__":
    main()
