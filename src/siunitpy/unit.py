import operator
from fractions import Fraction
from itertools import product
from typing import Callable, Optional, overload

from .dimension import Dimension
from .dimensionconst import DimensionConst
from .unit_analysis import _combine, _combine_fullname, _unit_init
from .unit_archive import _BASIC_SI, _PREFIX_DATA, _UNIT_DATA, _UNIT_STD
from .unitelement import UnitElement
from .utilcollections.compound import Compound
from .utilcollections.utils import _inplace

__all__ = ['Unit']

_ONE, _TWO = Fraction(1), Fraction(2)
_SIMPLE_EXPONENT = (-_ONE, _TWO, -_TWO)


def _vector_add(op: Callable, valop: Callable):
    '''vector addition: v + u, v - u.'''

    def __op(self: 'Unit', other: 'Unit'):
        return Unit(op(self._elements, other._elements),
                    dimension=valop(self.dimension, other.dimension),
                    value=valop(self.value, other.value))

    return __op, _inplace(__op)


def _scalar_mul(op: Callable, valop: Callable):
    '''scalar multiplication: c * v, v / c.'''

    def __op(self: 'Unit', c):
        if c == 0:
            return _UNIT_SIMPLE['']
        return Unit(op(self._elements, c),
                    dimension=valop(self.dimension, c),
                    value=valop(self.value, c))

    return __op, _inplace(__op)


class Unit:
    __slots__ = ('_elements', '_dimension', '_value')

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
            self._elements, self._dimension, self._value = _unit_init(symbol)
            return
        elif dimension is None:
            raise TypeError(f"{type(symbol) = } must be 'str'.")
        # developer mode, make sure type(symbol) is Compound
        if dimension == DimensionConst.DIMENSIONLESS and value == 1:
            self._elements: Compound[UnitElement] = Compound()
        elif isinstance(symbol, Compound):
            self._elements = symbol  # no copy
        else:
            raise TypeError("Constructor takes only one argument.")
        self._dimension = dimension
        self._value = value

    @property
    def symbol(self) -> str: return _combine(self._elements)
    @property
    def fullname(self) -> str: return _combine_fullname(self._elements)
    @property
    def dimension(self) -> Dimension: return self._dimension
    @property
    def value(self) -> float: return self._value

    def __repr__(self) -> str:
        return '{}({}, dim={}, value={})'.format(
            self.__class__.__name__, self.symbol, self.dimension, self.value
        )

    def __str__(self) -> str: return self.symbol

    @staticmethod
    def simple(symbol):
        if symbol in _UNIT_SIMPLE:
            return _UNIT_SIMPLE[symbol]
        return Unit(symbol)

    @classmethod
    def move(cls, unit):
        '''transform a str/Unit object to a Unit object.'''
        if isinstance(unit, cls):
            return unit
        if isinstance(unit, str):
            return cls(unit)
        raise TypeError(f"{type(unit) = } must be 'str' or 'Unit'.")

    def deprefix_with_factor(self):
        elements = self._elements
        factor = 1
        for unit in self._elements:
            if unit.symbol in _UNIT_DATA:  # not prefixed
                continue
            if elements is self._elements:
                elements = self._elements.copy()
            e = elements.pop(unit)
            factor *= _PREFIX_DATA[unit.prefix].value ** e
            if unit.base:  # not a single prefix
                elements[unit.deprefix()] += e
        return Unit(elements, self.dimension, self.value / factor), factor

    def deprefix(self):
        '''return a new unit that remove all the prefix.'''
        return self.deprefix_with_factor()[0]

    def tobasic_with_factor(self):
        elements = Compound({UnitElement(unit): e for unit, e in
                             zip(_BASIC_SI, self.dimension) if e}, move_dict=True)
        return Unit(elements, self.dimension, 1), self.value

    def tobasic(self):
        '''return a combination of basic SI unit 
        (i.e. m, kg, s, A, K, mol, cd) 
        with the same dimension.
        '''
        return self.tobasic_with_factor()[0]

    def simplify_with_factor(self):
        if len(self._elements) < 2:
            return self, 1
        if self.dimension in _UNIT_STD:
            return Unit(_UNIT_STD[self.dimension]), self.value
        for (dim, symbol), expo in product(_UNIT_STD.items(), _SIMPLE_EXPONENT):
            if dim**expo != self.dimension:
                continue
            elements = Compound({UnitElement(symbol): expo}, move_dict=True)
            return Unit(elements, self.dimension, 1), self.value
        return self, 1

    def simplify(self):
        '''if the complex unit can be simplified as m, m⁻¹, m², m⁻², 
        where m represents a standard SI unit. 

        e.g. the standard unit of voltage is V.
        '''
        return self.simplify_with_factor()[0]

    def __hash__(self) -> int:
        return hash((self.dimension, self.value))

    def __eq__(self, other: 'Unit') -> bool:
        '''e.g. N == kg·m/s2'''
        return self.dimension == other.dimension and self.value == other.value

    def sameas(self, other: 'Unit') -> bool:
        '''e.g. N and kg.m/s2 are not the same element.'''
        return self._elements == other._elements

    def parallel(self, other: 'Unit', /) -> bool:
        '''two units parallel means their dimensions are the same.'''
        try:
            if self.dimension == other.dimension:
                return True
        except AttributeError:
            raise TypeError(f"{type(other) = } must be 'Unit' or 'Quantity'.")
        return False

    def isdimensionless(self) -> bool:
        return self.dimension == DimensionConst.DIMENSIONLESS

    def valueover(self, other: 'Unit', /) -> float:
        '''return self.value / other.value.'''
        return self.value / other.value

    def inverse(self):
        '''inverse of the unit'''
        return Unit(-self._elements, self.dimension.inverse(), 1 / self.value)

    __mul__, __imul__ = _vector_add(operator.add, operator.mul)
    __truediv__, __itruediv__ = _vector_add(operator.sub, operator.truediv)
    __pow__, __ipow__ = _scalar_mul(operator.mul, operator.pow)

    def __rtruediv__(self, other):
        '''only used in 1/unit.'''
        if other is not 1:
            raise ValueError('only 1 or Unit object can divide Unit object.')
        return self.inverse()

    def nthroot(self, n):
        '''inverse operation of power.'''
        return Unit(self._elements / n, self.dimension.nthroot(n), self.value**(1 / n))


_UNIT_SIMPLE: dict[str, Unit] = {
    symbol: Unit(symbol) for symbol in _UNIT_DATA
}

DIMENSIONLESS = Unit.simple('')
