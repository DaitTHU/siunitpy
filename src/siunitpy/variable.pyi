from typing import Any, Generic, Optional, overload, TypeVar

from utilcollections import Interval
from utilcollections.abc import Linear

__all__ = ['Variable']

T = TypeVar('T', bound=Linear[Any, Any])
T_co = TypeVar('T_co', bound=Linear[Any, Any], covariant=True)
T_contra = TypeVar('T_contra', bound=Linear[Any, Any], contravariant=True)


class Variable(Generic[T]):
    def __init__(self, value: T, /, uncertainty: Optional[T] = None) -> None:
        '''define a variable with uncertainty. Uncertainty is None
        meaning the value is exact.'''

    @property
    def value(self) -> T: ...
    @property
    def uncertainty(self) -> T | None: ...
    @uncertainty.setter
    def uncertainty(self, uncertainty: T | None) -> None: ...
    @property
    def relative_uncertainty(self) -> T | None: ...
    @relative_uncertainty.setter
    def relative_uncertainty(self, rel_unc: T | None) -> None: ...
    @property
    def confidence_interval(self) -> Interval[T]: ... # type: ignore
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __format__(self, format_spec: str) -> str: ...
    def is_exact(self) -> bool: ...
    def copy(self) -> Variable[T]: ...
    def almost_equal(self, other: Variable[T]) -> bool: ...
    def same_as(self, other: Variable[T]) -> bool: ...
    def __eq__(self, other: Variable[T]) -> bool: ...
    def __ne__(self, other: Variable[T]) -> bool: ...
    def __gt__(self, other: Variable[T]) -> bool: ...
    def __lt__(self, other: Variable[T]) -> bool: ...
    def __ge__(self, other: Variable[T]) -> bool: ...
    def __le__(self, other: Variable[T]) -> bool: ...
    def __pos__(self) -> Variable[T]: ...
    def __neg__(self) -> Variable[T]: ...
    def __add__(self, other: T | Variable[T]) -> Variable[T]: ...
    def __sub__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __mul__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __matmul__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __floordiv__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __truediv__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __pow__(self, other) -> Variable[T]: ...
    def __iadd__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __isub__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __imul__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __imatmul__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __ifloordiv__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __itruediv__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __ipow__(self, other) -> Variable[T]: ...
    def __radd__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __rsub__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __rmul__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __rmatmul__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __rfloordiv__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __rtruediv__(self, other: float | T | Variable[T]) -> Variable[T]: ...
    def __rpow__(self, other) -> Variable[T]: ...
