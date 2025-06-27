"""
Basic tests for the dataruns pipeline functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import pandas as pd

def test_pipeline_basic():
    """Test basic pipeline functionality."""
    print("Testing basic pipeline functionality...")
    
    try:
        from dataruns.core.pipeline import Pipeline
        
        # Simple function
        def double_values(data):
            if isinstance(data, pd.DataFrame):
                return data * 2
            return np.array(data) * 2
        
        # Create pipeline
        pipeline = Pipeline(double_values)
        
        # Test with list
        result = pipeline([1, 2, 3])
        expected = np.array([2, 4, 6])
        assert np.array_equal(result, expected), f"Expected {expected}, got {result}"
        
        # Test with DataFrame
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        result_df = pipeline(df)
        expected_df = df * 2
        pd.testing.assert_frame_equal(result_df, expected_df)
        
        print("Basic pipeline test passed ✓")
        return True
        
    except Exception as e:
        print(f"Basic pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pipeline_chaining():
    """Test pipeline with multiple functions."""
    print("Testing pipeline chaining...")
    
    try:
        from dataruns.core.pipeline import Pipeline
        
        def add_one(data):
            return data + 1
        
        def multiply_by_two(data):
            return data * 2
        
        # Create pipeline with multiple functions
        pipeline = Pipeline(add_one, multiply_by_two)
        
        # Test: (5 + 1) * 2 = 12
        result = pipeline(5)
        expected = 12
        assert result == expected, f"Expected {expected}, got {result}"
        
        # Test with array: ([1, 2, 3] + 1) * 2 = [4, 6, 8]
        result_array = pipeline(np.array([1, 2, 3]))
        expected_array = np.array([4, 6, 8])
        assert np.array_equal(result_array, expected_array), f"Expected {expected_array}, got {result_array}"
        
        print("Pipeline chaining test passed ✓")
        return True
        
    except Exception as e:
        print(f"Pipeline chaining test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_make_pipeline():
    """Test Make_Pipeline builder."""
    print("Testing Make_Pipeline builder...")
    
    try:
        from dataruns.core.pipeline import Make_Pipeline
        
        # Create builder
        builder = Make_Pipeline()
        builder.add(lambda x: x + 10)
        builder.add(lambda x: x * 2)
        
        # Build pipeline
        pipeline = builder.build()
        
        # Test: (5 + 10) * 2 = 30
        result = pipeline(5)
        expected = 30
        assert result == expected, f"Expected {expected}, got {result}"
        
        print("Make_Pipeline test passed ✓")
        return True
        
    except Exception as e:
        print(f"Make_Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_csv_source():
    """Test CSV source functionality if available."""
    print("Testing CSV source...")
    
    try:
        from dataruns.source.datasource import CSVSource
        
        # Create a temporary CSV file for testing
        test_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50],
            'C': ['a', 'b', 'c', 'd', 'e']
        })
        
        test_csv_path = os.path.join(os.path.dirname(__file__), 'temp_test.csv')
        test_data.to_csv(test_csv_path, index=False)
        
        # Test CSVSource
        source = CSVSource(file_path=test_csv_path)
        extracted_data = source.extract_data()
        
        # Verify data
        assert extracted_data.shape == test_data.shape, f"Shape mismatch: expected {test_data.shape}, got {extracted_data.shape}"
        assert list(extracted_data.columns) == list(test_data.columns), "Column names don't match"
        
        # Clean up
        os.remove(test_csv_path)
        
        print("CSV source test passed ✓")
        return True
        
    except Exception as e:
        print(f"CSV source test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("RUNNING DATARUNS CORE TESTS")
    print("=" * 50)
    
    tests = [
        test_pipeline_basic,
        test_pipeline_chaining,
        test_make_pipeline,
        test_csv_source
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
    
    print(f"\nTEST RESULTS:")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    
    if failed == 0:
        print("ALL TESTS PASSED! ✓✓✓")
        return True
    else:
        print(f"{failed} TESTS FAILED ✗")
        return False

if __name__ == "__main__":
    main()
