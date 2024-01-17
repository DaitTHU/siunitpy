import numbers
from abc import ABC, abstractmethod
from decimal import Decimal
from fractions import Fraction
from typing import NoReturn, TypeVar

__all__ = ['Linear', 'LinearType']


class Linear(ABC):
    '''Linear defines the operations following linear algebra.
    '''
    __slots__ = ()
    @abstractmethod
    def __abs__(self) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __eq__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __ne__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __gt__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __lt__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __ge__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __le__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __add__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __sub__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __mul__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __truediv__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __pow__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __iadd__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __isub__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __imul__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __itruediv__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __ipow__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __radd__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __rsub__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __rmul__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __rtruediv__(self, other) -> NoReturn: raise NotImplementedError
    @abstractmethod
    def __rpow__(self, other) -> NoReturn: raise NotImplementedError


Linear.register(int)
Linear.register(float)
Linear.register(Decimal)  # Decimal is not Real
Linear.register(Fraction)
try:
    import numpy as np
    Linear.register(np.ndarray)
except ImportError:
    pass

LinearType = TypeVar('LinearType', int, float, Fraction,
                     Decimal, np.ndarray, Linear)
