import time
from functools import wraps
from typing import Callable, Any, Dict, Hashable, Optional, Tuple

# This file contains the core pipeline class and the pipeline builder class
class Pipeline:
    """
        Core Pipeline used for implementing an arbitrary number of 
        functions/transforms in one go on given input.

        Returns
        ----------
        Value of implemented functions
    """

    def __init__(self, *args):
        self.functions = args

    def __call__(self, data):
        for function in self.functions:
            data = function(data)
        return data

    def __repr__(self):
        # String representation of the pipeline functions
        format_string = self.__class__.__name__ + "("
        for function in self.functions:
            # Get name from function or class
            name = getattr(function, '__name__', None) or function.__class__.__name__
            format_string += f"\n    {name}()"
        format_string += "\n)"
        return format_string



class make_pipeline:
    def __init__(self):
        self.functions = []
        self.pipeline = None

    def add(self, *function):
        """Add a function to the pipeline"""
        if len(function) == 1:
            function = function[0]
        elif len(function) > 1:
            function = list(function)
        elif len(function) == 0:
            raise ValueError("No function provided at all")
        
        self.functions.append(function)
        return self

    def build(self) -> Pipeline:
        """Build and return the pipeline with added functions"""
        # Flatten the list of functions if any were added as lists
        flattened_functions = []
        for func in self.functions:
            if isinstance(func, list):
                flattened_functions.extend(func)
            else:
                flattened_functions.append(func) 
                
        # Create and return new pipeline with flattened functions
        self.pipeline = Pipeline(*flattened_functions)
        return self.pipeline

    def __repr__(self):
        return f"PipelineBuilder({self.functions})"


class SpeedUp:
    """ 
    -------
    ⚠️ Experimental

    -------

    Wrapper to make pipeline execution really really fast.
    
    This decorator speeds up functions in the pipeline by:
    - Caching results to avoid redundant computations
    - Measuring execution time for performance monitoring
    
    It can be applied to individual functions or entire pipeline instances.

    Usage
    -----
    # For individual functions:
    @SpeedUp
    def slow_function(x):
        # Slow computation
        return x
        
    # For an entire pipeline:
    pipeline = Pipeline(func1, func2, func3)
    fast_pipeline = SpeedUp(pipeline)
    """
    
    def __init__(self, func_or_pipeline: Callable):
        # Check if we're wrapping a Pipeline or a function
        if isinstance(func_or_pipeline, Pipeline):
            # Handle Pipeline case
            self.is_pipeline = True
            self.pipeline = func_or_pipeline
            # Create a new pipeline with all functions wrapped by SpeedUp
            speedy_functions = [SpeedUp(func) for func in func_or_pipeline.functions]
            self.speedy_pipeline = Pipeline(*speedy_functions)
            # Set name for logging
            self.__name__ = "Pipeline"
        else:
            # Handle normal function case
            self.is_pipeline = False
            wraps(func_or_pipeline)(self)
            self.func = func_or_pipeline
            
        # Common attributes
        self.cache: Dict[Hashable, Any] = {}
        self.cache_hits = 0
        self.total_calls = 0
        
    def __call__(self, *args, **kwargs):
        self.total_calls += 1
        
        if self.is_pipeline:
            # For Pipeline objects, we delegate to the speedy pipeline
            # but still track overall pipeline performance
            start_time = time.time()
            result = self.speedy_pipeline(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Log pipeline execution time
            if execution_time > 0.1:
                print(f"⚡ Pipeline: {execution_time:.4f}s (containing {len(self.pipeline.functions)} functions)")
                
            return result
        else:
            # Original function wrapping logic
            try:
                # Convert args and kwargs to a hashable representation
                key = self._make_cache_key(args, kwargs)
                
                # Return cached result if available
                if key in self.cache:
                    self.cache_hits += 1
                    return self.cache[key]
            except:
                # If arguments aren't hashable, skip caching
                key = None
                
            # Measure execution time
            start_time = time.time()
            result = self.func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Store result in cache if possible
            if key is not None:
                self.cache[key] = result
                
            # Log execution time for slow operations
            if execution_time > 0.1:  # Only log slower operations
                hit_rate = (self.cache_hits / self.total_calls * 100) if self.total_calls > 0 else 0
                print(f"⚡ {self.func.__name__}: {execution_time:.4f}s (cache hit rate: {hit_rate:.1f}%)")
                
            return result
    
    def _make_cache_key(self, args: Tuple, kwargs: Dict) -> Hashable:
        """Create a hashable key from function arguments"""
        kw_key = tuple(sorted((k, self._make_hashable(v)) for k, v in kwargs.items()))
        return (tuple(self._make_hashable(arg) for arg in args), kw_key)
    
    def _make_hashable(self, obj: Any) -> Hashable:
        """Convert common unhashable types to hashable representations"""
        if isinstance(obj, dict):
            return tuple(sorted((k, self._make_hashable(v)) for k, v in obj.items()))
        elif isinstance(obj, (list, set)):
            return tuple(self._make_hashable(x) for x in obj)
        else:
            return obj
