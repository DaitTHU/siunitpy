from typing import Callable, Generic, Iterable, Optional, Sequence, TypeVar

from templatelib import Interval

__all__ = ['Value']

T = TypeVar('T')


class Value(Generic[T]):
    def __init__(self, value: T, /,
                 uncertainty: Optional[T] = None) -> None: ...

    @property
    def value(self) -> T: ...
    @property
    def uncertainty(self) -> Optional[T]: ...
    @uncertainty.setter
    def uncertainty(self, uncertainty: Optional[T]): ...
    @property
    def confidence_interval(self) -> Interval[T]: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __format__(self, format_spec: str) -> str: ...
    def is_exact(self) -> bool: ...
    def copy(self) -> Value[T]: ...
    def __eq__(self, other: Value[T]) -> bool: ...
    def __ne__(self, other: Value[T]) -> bool: ...
    def __gt__(self, other: Value[T]) -> bool: ...
    def __lt__(self, other: Value[T]) -> bool: ...
    def __ge__(self, other: Value[T]) -> bool: ...
    def __le__(self, other: Value[T]) -> bool: ...
    def __pos__(self) -> Value[T]: ...
    def __neg__(self) -> Value[T]: ...
    def __add__(self, other: T | Value[T]) -> Value[T]: ...
    def __sub__(self, other: T | Value[T]) -> Value[T]: ...
    def __mul__(self, other: T | Value[T]) -> Value[T]: ...
    def __matmul__(self, other: T | Value[T]) -> Value[T]: ...
    def __floordiv__(self, other: T | Value[T]) -> Value[T]: ...
    def __truediv__(self, other: T | Value[T]) -> Value[T]: ...
    def __pow__(self, other) -> Value[T]: ...
    def __iadd__(self, other: T | Value[T]) -> Value[T]: ...
    def __isub__(self, other: T | Value[T]) -> Value[T]: ...
    def __imul__(self, other: T | Value[T]) -> Value[T]: ...
    def __imatmul__(self, other: T | Value[T]) -> Value[T]: ...
    def __ifloordiv__(self, other: T | Value[T]) -> Value[T]: ...
    def __itruediv__(self, other: T | Value[T]) -> Value[T]: ...
    def __ipow__(self, other) -> Value[T]: ...
    def __radd__(self, other: T | Value[T]) -> Value[T]: ...
    def __rsub__(self, other: T | Value[T]) -> Value[T]: ...
    def __rmul__(self, other: T | Value[T]) -> Value[T]: ...
    def __rmatmul__(self, other: T | Value[T]) -> Value[T]: ...
    def __rfloordiv__(self, other: T | Value[T]) -> Value[T]: ...
    def __rtruediv__(self, other: T | Value[T]) -> Value[T]: ...
    def __rpow__(self, other) -> Value[T]: ...
    def nthroot(self, n: int) -> Value[T]: ...
    