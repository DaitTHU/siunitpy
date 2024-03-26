from typing import Protocol, TypeVar, runtime_checkable

__all__ = ['Linear']

T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)


@runtime_checkable
class Linear(Protocol[T_co, T_contra]):
    '''`Linear` objects follow linear algebra operations.
    '''
    def __lt__(self, other: T_contra, /) -> T_co: ...
    def __le__(self, other: T_contra, /) -> T_co: ...
    def __gt__(self, other: T_contra, /) -> T_co: ...
    def __ge__(self, other: T_contra, /) -> T_co: ...
    def __abs__(self) -> T_co: ...
    def __pos__(self) -> T_co: ...
    def __neg__(self) -> T_co: ...
    def __add__(self, other: T_contra, /) -> T_co: ...
    def __sub__(self, other: T_contra, /) -> T_co: ...
    def __mul__(self, other: T_contra, /) -> T_co: ...
    def __truediv__(self, other: T_contra, /) -> T_co: ...
    def __pow__(self, other: T_contra, /) -> T_co: ...
    def __radd__(self, other: T_contra, /) -> T_co: ...
    def __rsub__(self, other: T_contra, /) -> T_co: ...
    def __rmul__(self, other: T_contra, /) -> T_co: ...
    def __rtruediv__(self, other: T_contra, /) -> T_co: ...
    def __rpow__(self, other: T_contra, /) -> T_co: ...

