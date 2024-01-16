import numbers
from abc import ABC
from typing import Generic, TypeVar

__all__ = ['Linear']

F = TypeVar('F')  # number field


class Linear(ABC):
    '''Linear defines the operations following linear algebra.
    '''
    pass

Linear.register(numbers.Number)
try:
    import numpy as np
    Linear.register(np.ndarray)
except ImportError:
    pass
