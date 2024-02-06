from typing import Any, TypeVar, overload

from .dimension import Dimension
from .quantity import Quantity
from .unit import Unit
from .unitconst import UnitConst
from .utilcollections.abc import Linear
from .variable import Variable

__all__ = ['Constant', 'constant']

T = TypeVar('T', bound=Linear[Any, Any])


class Constant(Quantity[T]):
    '''Constant objects are just immutable Quantity objects.'''
    @overload
    def __init__(self, value: T, /,
                 unit: str | Unit = UnitConst.DIMENSIONLESS,
                 uncertainty: T | None = None) -> None:
        '''set value, unit, and uncertainty.'''
    @overload
    def __init__(self, variable: Variable[T], /,
                 unit: str | Unit = UnitConst.DIMENSIONLESS) -> None:
        '''set variable and unit.'''
    @classmethod
    def one(cls, unit: str | Unit) -> Constant[int]: ...  # type: ignore
    @property
    def variable(self) -> Variable[T]: ...
    @property
    def value(self) -> T: ...
    @property
    def unit(self) -> Unit: ...
    @property
    def dimension(self) -> Dimension: ...
    @property
    def uncertainty(self) -> T: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __format__(self, format_spec: str) -> str: ...
    def is_exact(self) -> bool: ...
    def is_dimensionless(self) -> bool: ...
    def copy(self) -> Constant: ...

    def to(self, new_unit: str | Unit, *,
           assertDimension=True) -> Constant[T]: ...

    def deprefix_unit(self) -> Quantity[T]:
        '''remove the prefix of the unit.'''

    def to_basic_unit(self) -> Quantity[T]:
        '''transform unit to the combination of `_BASIC_SI` unit with 
        the same dimension.
        '''

    def simplify_unit(self) -> Quantity[T]:
        '''try if the complex unit can be simplified as u, u⁻¹, u², u⁻², 
        where u represents a single `_BASIC_SI` unit. 
        '''

    def addable(self, other: Quantity, /, *, assertTrue=False) -> bool:
        '''check if self is addable with other, i.e. same dimension.'''

    def remove_uncertainty(self) -> Quantity[T]:
        '''set uncertainty zero.'''

    def __eq__(self, other: Quantity[T]) -> bool: ...
    def __ne__(self, other: Quantity[T]) -> bool: ...
    def __gt__(self, other: Quantity[T]) -> bool: ...
    def __lt__(self, other: Quantity[T]) -> bool: ...
    def __ge__(self, other: Quantity[T]) -> bool: ...
    def __le__(self, other: Quantity[T]) -> bool: ...
    def __pos__(self) -> Quantity[T]: ...
    def __neg__(self) -> Quantity[T]: ...
    def __add__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __sub__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __mul__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __matmul__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __floordiv__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __truediv__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __pow__(self, other) -> Quantity[T]: ...
    def __iadd__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __isub__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __imul__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __imatmul__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __ifloordiv__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __itruediv__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __ipow__(self, other) -> Quantity[T]: ...
    def __radd__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __rsub__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __rmul__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __rmatmul__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __rfloordiv__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __rtruediv__(self, other: T | Quantity[T]) -> Quantity[T]: ...
    def __rpow__(self, other) -> Quantity[T]: ...
    def nthroot(self, n: int) -> Quantity[T]: ...


def constant(quantity: Quantity[T]) -> Constant[T]: ...
