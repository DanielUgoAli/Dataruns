from typing import Callable, Optional, List
from .types import Function

import numpy as np
import pandas as pd


# Version 2.0.0(Future)
# Introduces Function for formal representation for functions
# Improves function handling within main pipeline setup
# Adds apply method for easy use.

# Version 1.0.dev
# Initial version with am advanced version of pipeline functionality and function handling.
# Introduces Pipeline class for chaining functions
# and a builder class for creating pipelines.
# Adds a precompiled pipeline for performance improvements.

# version 0.alpha
# Initial version with basic pipeline functionality and handling of functions.
# Introduces Pipeline class for chaining functions

# Funtion class has been moved to types.py

# This file contains the core pipeline class and the pipeline builder class
class Pipeline:
    """
    Core Pipeline used for implementing a number of 
    functions/transforms in one go on given input.
    """
    def __init__(self, *functions: Optional[Callable | list[Callable]]):
        if len(functions) == 0:
            raise ValueError("No functions provided at all")
        # Convert all functions to Function instances
        self.functions = [f if isinstance(f, Function) else Function(f) for f in functions]

    def __call__(self, data: Optional[np.ndarray | pd.DataFrame]):
        if data is None:
            raise ValueError("Data cannot be None")
        if isinstance(data, dict):
            raise TypeError("Data cannot be a dictionary")
        if isinstance(data, list):
            data = np.array(data)
            
        result = data
        for function in self.functions:
            result = function(result)
        return result


    def __repr__(self):
        format_string = f"{self.__class__.__name__}("
        for function in self.functions:
            format_string += f"\n    {function}"
        format_string += "\n)"
        return format_string



class Make_Pipeline:
    """
    Used For building Pipelines.
    """
    def __init__(self):
        self.functions = []
        self.pipeline = None

    def add(self, *function):
        """
        Add a function to the pipeline
        """
        if len(function) == 1:
            function = function[0]
        elif len(function) > 1:
            function = list(function)
        elif len(function) == 0:
            raise ValueError("No function provided at all")
        
        self.functions.append(function)
        return self

    def build(self) -> Pipeline:
        """
        Build and return the pipeline with added functions
        """
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
    ⚠️ Experimental

    Decorator to speed up function execution by caching results.
    Also a function wrapper for the pipeline.
    """

    pass
