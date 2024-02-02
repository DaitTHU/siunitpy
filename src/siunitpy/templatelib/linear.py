import numbers
from abc import ABC, abstractmethod
from typing import TypeVar, Protocol, runtime_checkable, Any

__all__ = ['Linear']

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)


@runtime_checkable
class Linear(Protocol[T_contra, T_co]):
    '''Linear defines the operations following linear algebra.
    '''
    __slots__ = ()
    @abstractmethod
    def __abs__(self) -> T_co: ...
    @abstractmethod
    def __eq__(self, other: T_contra) -> bool: ...
    @abstractmethod
    def __ne__(self, other: T_contra) -> bool: ...
    @abstractmethod
    def __gt__(self, other: T_contra) -> bool: ...
    @abstractmethod
    def __lt__(self, other: T_contra) -> bool: ...
    @abstractmethod
    def __ge__(self, other: T_contra) -> bool: ...
    @abstractmethod
    def __le__(self, other: T_contra) -> bool: ...
    @abstractmethod
    def __add__(self, other: T_contra) -> T_co: ...
    @abstractmethod
    def __sub__(self, other: T_contra) -> T_co: ...
    @abstractmethod
    def __mul__(self, other: T_contra | float) -> T_co: ...
    @abstractmethod
    def __truediv__(self, other: T_contra) -> T_co: ...
    @abstractmethod
    def __pow__(self, other: T_contra) -> T_co: ...
    # @abstractmethod
    # def __iadd__(self, other: T_contra) -> T_co: ...
    # @abstractmethod
    # def __isub__(self, other: T_contra) -> T_co: ...
    # @abstractmethod
    # def __imul__(self, other: T_contra) -> T_co: ...
    # @abstractmethod
    # def __itruediv__(self, other: T_contra) -> T_co: ...
    # @abstractmethod
    # def __ipow__(self, other: T_contra) -> T_co: ...
    @abstractmethod
    def __radd__(self, other: T_contra) -> T_co: ...
    @abstractmethod
    def __rsub__(self, other: T_contra) -> T_co: ...
    @abstractmethod
    def __rmul__(self, other: T_contra) -> T_co: ...
    @abstractmethod
    def __rtruediv__(self, other: T_contra) -> T_co: ...
    @abstractmethod
    def __rpow__(self, other: T_contra) -> T_co: ...


