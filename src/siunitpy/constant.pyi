from typing import Generic, NoReturn, TypeVar, overload

from .dimension import Dimension
from .quantity import Quantity
from .unit import Unit
from .unitconst import UnitConst
from .variable import Variable

__all__ = ['Constant', 'constant']

T = TypeVar('T')


class Constant(Quantity[T]):
    @overload
    def __init__(self, value: T, /,
                 unit: str | Unit = UnitConst.DIMENSIONLESS,
                 uncertainty: T | None = None) -> None:
        '''set value, unit, and uncertainty.'''
    @overload
    def __init__(self, variable: Variable[T], /,
                 unit: str | Unit = UnitConst.DIMENSIONLESS) -> None:
        '''set variable and unit.'''


def constant(quantity: Quantity[T]) -> Constant[T]: ...
