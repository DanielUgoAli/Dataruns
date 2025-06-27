from typing import Optional, Callable

import numpy as np
import pandas as pd


# This class is used to wrap functions and provide a consistent interface.
class Function:
    """
    Function class used to wrap functions and provide a consistent interface.
    """ 
    def __init__(self, func: Optional[Callable | list[Callable]] = None):
        if isinstance(func, list):
            for f in func:
                if not callable(f):
                    raise TypeError("Function must be callable")
                self.func = func
                self.__name__ = ', '.join(getattr(f, '__name__', f.__class__.__name__) for f in func)
        else:
            if not callable(func):
                raise TypeError("Function must be callable")
            self.func = func
            self.__name__ = getattr(func, '__name__', func.__class__.__name__)

    def __call__(self, *args, **kwargs):
        if isinstance(self.func, list):
            for f in self.func:
                result = f(*args, **kwargs)
            return result
        else: 
            return self.func(*args, **kwargs)
    
    def __repr__(self):
        return f"Function[{self.__name__}]"

    