from typing import Generic, TypeVar, overload

from .dimension import Dimension
from .unit import Unit
from .unitconst import UnitConst

__all__ = ['Quantity']

T = TypeVar('T')


class Quantity(Generic[T]):
    '''`Quantity` object is used for representing a physical quantity, 
    which has 3 parameters:
    - `value`      : the value of the quantity under the `unit`, whose
                     type can be `int`, `float`, `Decimal`, `Fraction`,
                     and even `numpy.ndarray`.
    - `unit`       : the unit of the quantity, a `Unit` object.
    - `uncertainty`: the uncertainty of the quantity, which is usually
                     a `float` when `value` is a single number.

    Construct
    ---
    >>> Quantity(42)
    >>> Quantity('m')
    >>> Quantity(1.6e-19, 'C')
    >>> Quantity()
    '''
    def __init__(self, value: T, /, unit: str | Unit = UnitConst.DIMENSIONLESS, uncertainty: T = 0):
        '''set value, unit, and uncertainty.'''
    @classmethod
    def A(cls, unit: str | Unit) -> Quantity[int]: ...
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
    def is_exact(self) -> bool: ...
    def copy(self) -> 'Quantity': ...

    
