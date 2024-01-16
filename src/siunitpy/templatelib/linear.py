import numbers
from abc import ABC, abstractmethod
from decimal import Decimal
from fractions import Fraction

__all__ = ['Linear']


class Linear(ABC):
    '''Linear defines the operations following linear algebra.
    '''
    __slots__ = ()
    @abstractmethod
    def __eq__(self, other): raise NotImplementedError
    @abstractmethod
    def __ne__(self, other): raise NotImplementedError
    @abstractmethod
    def __gt__(self, other): raise NotImplementedError
    @abstractmethod
    def __lt__(self, other): raise NotImplementedError
    @abstractmethod
    def __ge__(self, other): raise NotImplementedError
    @abstractmethod
    def __le__(self, other): raise NotImplementedError
    # @abstractmethod
    # def __abs__(self): raise NotImplementedError
    @abstractmethod
    def __add__(self, othre): raise NotImplementedError
    @abstractmethod
    def __sub__(self, other): raise NotImplementedError
    @abstractmethod
    def __mul__(self, other): raise NotImplementedError
    @abstractmethod
    def __truediv__(self, other): raise NotImplementedError
    @abstractmethod
    def __pow__(self, other): raise NotImplementedError


Linear.register(int)
Linear.register(float)
Linear.register(Decimal)  # Decimal is not Real
Linear.register(Fraction)
try:
    import numpy as np
    Linear.register(np.ndarray)
except ImportError:
    pass
