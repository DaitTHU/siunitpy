from typing import TypeVar

try:
    import numpy as np
    ValueType = TypeVar('ValueType', bound=float | np.ndarray)
except ImportError:
    ValueType = TypeVar('ValueType', bound=float)


