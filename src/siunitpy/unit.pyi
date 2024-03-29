from fractions import Fraction
from typing import Iterable

from .dimension import Dimension

__all__ = ['Unit']


class Unit:
    '''`Unit` is a immutable object:
    - `symbol`: string expression of the unit.
    - `dimension`: `Dimension`, dimension of the unit.
    - `value`: 1 unit = ? standard-unit.

    Construct
    ---
    define unit combination:
    >>> vilocity_unit = Unit('m/s')
    >>> force_unit = Unit('kg.m/s2')

    for more detail construct rules, see constructor doc.

    Comparison
    ---
    If 2 unit share the same dimension and value, it equals.
    >>> Unit('N') == force_unit  # True

    For element comparison, please use `a.same_as(b)`

    For just dimension comparison, use `a.parallel(b)`

    Transformation
    ---

    '''
    def __init__(self, symbol: str) -> None:
        '''construct from string symbol. 

        Rules
        ---
        - unit should be linked from basic units, which are called elements,
          like `'kg'`, `'s'`, `'meV'`...
        - the linker should be one of: `'/'`, `'.'`, `'·'`, where `'/'` 
          represents division, while `'.'` and `'·'` represent multiplication.
        - the exponents of the elements should be written after the elements,
          like `'m2'`, `'m-1'`, `'m³'`, `'m^+114514'` are all acceptable.
        - The standard form has only one `'/'`, and all subsequent elements 
          are represented as denominators, which does not cause any ambiguity.
          Therefore, `Unit('kg/m/s') == Unit('kg/m.s')`.
        - following these basic rules you can easily get used to it, and 
          properly using it will give you proper result.

        Example
        ---
        - legal expression example:

        >>> Unit('kg.m/s2')
        >>> Unit('MeV/c2')
        >>> Unit('T.W/m2.K4')

        - illegal expression example: 

        >>> Unit('x')   # UnitSymbolError: 'x' is not a valid unit.
        >>> Unit('m+m') # UnitSymbolError: 'm+m' is not a valid element unit.
        '''
    
    @property
    def symbol(self) -> str: ...
    @property
    def fullname(self) -> str: ...
    @property
    def dimension(self) -> Dimension: ...
    @property
    def value(self) -> float: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __hash__(self) -> int: ...
    @staticmethod
    def simple(symbol: str) -> Unit: ...
    @classmethod
    def move(cls, unit: Unit | str) -> Unit: ...
    def deprefix_with_factor(self) -> tuple[Unit, float]: ...
    def to_basic_with_factor(self) -> tuple[Unit, float]: ...
    def simplify_with_factor(self) -> tuple[Unit, float]: ...
    def deprefix(self) -> Unit: ...
    def to_basic(self) -> Unit: ...
    def simplify(self) -> Unit: ...
    def __eq__(self, other: Unit) -> bool: ...
    def same_as(self, other: Unit) -> bool: ...
    def parallel(self, other: Unit, /) -> bool: ...
    def is_dimensionless(self) -> bool: ...
    def value_over(self, other: Unit, /) -> float: ...
    def __pos__(self): ...
    def __neg__(self): ...
    def __add__(self, other: Unit) -> Unit: ...
    def __sub__(self, other: Unit) -> Unit: ...
    def __mul__(self, other: int | Fraction) -> Unit: ...
    def __truediv__(self, other: int | Fraction) -> Unit: ...
    def __iadd__(self, other: Unit) -> Unit: ...
    def __isub__(self, other: Unit) -> Unit: ...
    def __imul__(self, other: int | Fraction) -> Unit: ...
    def __itruediv__(self, other: int | Fraction) -> Unit: ...
    def __rmul__(self, other: int | Fraction) -> Unit: ...

