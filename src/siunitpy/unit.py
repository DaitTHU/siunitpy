import operator
from fractions import Fraction
from itertools import product
from math import prod
from typing import Callable, Optional, Union, overload

from .dimension import Dimension
from .dimensionconst import DimensionConst
from .unit_analysis import _combine, _combine_fullname, _resolve
from .unit_archive import _BASIC_SI, _PREFIX, _UNIT, _UNIT_STD
from .unitelement import UnitElement
from .utilcollections.compound import Compound
from .utilcollections.utils import _inplace

__all__ = ['Unit', 'UnitDimensionError', '_DIMENSIONLESS_UNIT']

_ONE, _TWO = Fraction(1), Fraction(2)


def _nthroot(a, b): return a ** (1 / b)


def _vector_add(op: Callable, valop: Callable):
    '''vector addition: v + u, v - u.'''

    def __op(self: 'Unit', other: 'Unit'):
        return Unit(op(self._elements, other._elements),
                    dimension=op(self.dimension, other.dimension),
                    value=valop(self.value, other.value))

    return __op, _inplace(__op)


def _scalar_mul(op: Callable, valop: Callable):
    '''scalar multiplication: c * v, v / c.'''

    def __op(self: 'Unit', c):
        if c == 0:
            return _DIMENSIONLESS_UNIT
        return Unit(op(self._elements, c),
                    dimension=op(self.dimension, c),
                    value=valop(self.value, c))

    return __op, _inplace(__op)


class Unit:
    __slots__ = ('_elements', '_dimension', '_value', '_symbol', '_fullname')

    @overload
    def __init__(self, symbol: str) -> None: ...

    @overload
    def __init__(self, elements: Compound[UnitElement],
                 dimension: Dimension, value: float) -> None:
        '''The constructor is designed for private use, 
        please do NOT call it.
        '''

    def __init__(self, symbol: str | Compound[UnitElement], /,  # type: ignore
                 dimension: Optional[Dimension] = None,
                 value: float = 1) -> None:
        if isinstance(symbol, str):
            self._elements = _resolve(symbol)
            dim_gen = (u.dimension * e for u, e in self._elements.items())
            self._dimension = sum(dim_gen, start=DimensionConst.DIMENSIONLESS)
            if self.dimension == DimensionConst.DIMENSIONLESS:  # like "C²/F·J"
                self._elements.clear()
            self._value = prod(u.value**e for u, e in self._elements.items())
            if isinstance(self.value, float) and self.value.is_integer():
                self._value = int(self.value)
            self._symbol = _combine(self._elements)
            self._fullname = _combine_fullname(self._elements)
            return
        elif dimension is None:
            raise TypeError(f"{type(symbol) = } must be 'str'.")
        # developer mode, make sure type(symbol) is Compound
        if dimension == DimensionConst.DIMENSIONLESS:  # like 'C2/F·J'
            self._elements: Compound[UnitElement] = Compound()
        else:
            self._elements = symbol  # no copy
        self._dimension = dimension
        self._value = value
        self._symbol = _combine(self._elements)
        self._fullname = _combine_fullname(self._elements)

    @property
    def symbol(self) -> str: return self._symbol
    @property
    def fullname(self) -> str: return self._fullname
    @property
    def dimension(self) -> Dimension: return self._dimension
    @property
    def value(self) -> float: return self._value

    def __repr__(self) -> str:
        return self.__class__.__name__ + f'({self.symbol}, ' \
            f'dim={self.dimension}, value={self.value})'

    def __str__(self) -> str: return self.symbol

    def __hash__(self) -> int: return hash(self.symbol)

    @classmethod
    def move(cls, unit: Union['Unit', str]) -> 'Unit':
        '''type(unit) must be str or Unit'''
        return Unit(unit) if isinstance(unit, str) else unit

    def deprefix(self) -> tuple['Unit', float]:
        '''return a new unit that remove all the prefix, 
        and pop out the factor.
        '''
        elements = self._elements.copy()
        factor = 1
        for unit in self._elements:
            if unit in _UNIT:  # not prefixed
                continue
            e = elements.pop(unit)
            factor *= _PREFIX[unit.prefix].factor ** e
            if unit.basic:  # not a single prefix
                elements[unit.deprefix()] += e
        deprefixed_unit = \
            Unit(elements, self.dimension, self.value / factor)
        return deprefixed_unit, factor

    def to_basic(self) -> tuple['Unit', float]:
        '''return a combination of `_BASIC_SI` unit with the same dimension, 
        whose value = 1, thus the factor is self.value.
        '''
        elements = Compound({UnitElement(unit): e for unit, e in
                             zip(_BASIC_SI, self.dimension) if e}, move_dict=True)
        basic_unit = Unit(elements, self.dimension, 1)
        return basic_unit, self.value

    def simplify(self) -> tuple['Unit', float]:
        '''if the complex unit can be simplified as m, m-1, m2, m-2, 
        where m represents a `_BASIC_SI` unit. 
        e.g. 
        '''
        if len(self._elements) < 2:
            return self, 1
        if self.dimension in _UNIT_STD:
            return Unit(_UNIT_STD[self.dimension]), self.value
        for (dim, symbol), expo in product(_UNIT_STD.items(), (-_ONE, _TWO, -_TWO)):
            if dim * expo != self.dimension:
                continue
            elements = Compound({UnitElement(symbol): expo}, move_dict=True)
            return Unit(elements, self.dimension, self.value), self.value
        return self, 1

    def __eq__(self, other: 'Unit') -> bool:
        '''e.g. N == kg·m/s2'''
        return self.dimension == other.dimension \
            and self.value == other.value

    def same_as(self, other: 'Unit') -> bool:
        '''e.g. N and kg.m/s2 are not the same element.'''
        return self._elements == other._elements

    def parallel(self, other: 'Unit', /, *, assertTrue=False) -> bool:
        '''parallel means dimension is the same
        if assertTrue, raise Error when dimension unparallel.
        '''
        try:
            if self.dimension == other.dimension:
                return True
        except AttributeError:
            raise TypeError("parameter must be 'Unit' or 'Quantity'.")
        if assertTrue:
            raise UnitDimensionError(
                f"dimension {self.dimension} != {other.dimension}.")
        return False

    def value_over(self, other: 'Unit', /) -> float:
        '''return self.value / other.value.'''
        return self.value / other.value

    def __pos__(self): return self

    def __neg__(self):
        '''reverse the unit'''
        return Unit(-self._elements, -self.dimension, 1 / self.value)

    __add__, __iadd__ = _vector_add(operator.add, operator.mul)
    __sub__, __isub__ = _vector_add(operator.sub, operator.truediv)

    __mul__, __imul__ = _scalar_mul(operator.mul, operator.pow)
    __rmul__ = __mul__
    __truediv__, __itruediv__ = _scalar_mul(operator.truediv, _nthroot)


_DIMENSIONLESS_UNIT = Unit('')


class UnitDimensionError(Exception):
    pass
