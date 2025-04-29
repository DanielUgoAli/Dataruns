from abc import ABC
from typing import Dict, Any, List
from ..core.types import Data

import numpy as np
import pandas as pd


# This file contains the core transform class and the pipeline builder class
# This class is used to represent a transform in the pipeline.



class Transform(ABC):
    """
    Base class for all transforms.
    """
    def __init__(self, data: Data, **kwargs: Any):
        self.data = np.asarray(data) if isinstance(data, (pd.DataFrame, list)) else data
        self._kwargs = kwargs

    def __repr__(self):
        return f"{self.__class__.__name__}()"
    





