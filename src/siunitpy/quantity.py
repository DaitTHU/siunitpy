import operator
from copy import copy
from typing import Callable, Generic, TypeVar

from .baseunit import BaseUnit
from .dimension import Dimension
from .identity import Zero, zero
from .unit_analysis import _unit_init
from .utilcollections.abc import Linear
from .variable import Variable

T = TypeVar('T', bound=Linear)


class Unit(BaseUnit):
    def __init__(self, symbol: str, dim=None, factor=None) -> None:
        if dim is None:
            super().__init__(*_unit_init(symbol))
        else:  # constructor of base class, internal use only
            super().__init__(symbol, dim, factor)  # type: ignore

    @classmethod
    def move(cls, unit):
        '''transform a str/Unit object to a Unit object.'''
        if isinstance(unit, cls):
            return unit
        if isinstance(unit, str):
            return cls(unit)
        raise TypeError(f"{type(unit) = } must be 'str' or 'Unit'.")
    
    


DIMENSIONLESS = Unit('')


def _dimension_consistency(left: 'Quantity', right: 'Quantity'):
    try:
        if left.unit.dimension == right.unit.dimension:
            return
        raise ValueError(f"dimension {left.dimension} != {right.dimension}.")
    except AttributeError:
        raise TypeError(f"'{type(right) = }' must be 'Quantity'.")


def _comparison(op: Callable[[Variable, Variable], bool]):
    def __op(self: 'Quantity', other: 'Quantity'):
        _dimension_consistency(self, other)
        return op(self.standard_variable, other.standard_variable)
    return __op


def _unary(op: Callable):
    def __op(self: 'Quantity'):
        return Quantity(op(self.variable), self.unit)
    return __op


def _addsub(op: Callable, iop: Callable):
    '''operator: a + b, a - b, where a, b have to share
    the same dimension.
    '''

    def __op(self: 'Quantity', other: 'Quantity'):
        if self.isdimensionless() and not isinstance(other, Quantity):
            return Quantity(op(self.variable, other), self.unit)
        _dimension_consistency(self, other)
        other_var = other.variable * other.unit.factor / self.unit.factor
        return Quantity(op(self.variable, other_var), self.unit)

    def __iop(self: 'Quantity', other: 'Quantity'):
        if self.isdimensionless() and not isinstance(other, Quantity):
            self._variable = iop(self.variable, other)
            return self
        _dimension_consistency(self, other)
        self._variable = iop(self.variable, other.variable *
                             other.unit.factor / self.unit.factor)
        return self

    return __op, __iop


def _muldiv(op: Callable, iop: Callable, *, unitop=None, inverse: bool = False):
    '''operator: a * b, a / b, 

    when a or b is not a `Quantity` object, which will be treated as a
    dimensionless Quantity.
    '''
    if unitop is None:
        unitop = op

    def __op(self: 'Quantity', other: 'Quantity'):
        if not isinstance(other, Quantity):
            return Quantity(op(self.variable, other), self.unit)
        new_variable = op(self.variable, other.variable)
        new_unit: Unit = unitop(self.unit, other.unit)
        if new_unit.isdimensionless():
            new_variable *= new_unit.factor
            new_unit = DIMENSIONLESS
        else:
            new_unit, factor = new_unit.simplify_with_factor()
            new_variable *= factor
        return Quantity(new_variable, new_unit)

    def __iop(self: 'Quantity', other: 'Quantity'):
        if not isinstance(other, Quantity):
            self._variable = iop(self.variable, other)
            return self
        self._variable = iop(self.variable, other.variable)
        self._unit = unitop(self.unit, other.unit)
        if self.unit.isdimensionless():
            self._variable *= self.unit.factor
            self._unit = DIMENSIONLESS
        else:
            self._unit, factor = self.unit.simplify_with_factor()
            self._variable *= factor
        return self

    if inverse:
        def unary(unit: Unit): return unit.inverse()  # type: ignore
    else:
        def unary(unit): return unit

    def __rop(self: 'Quantity', other):
        '''other is not a `Quantity` object.'''
        return Quantity(op(other, self._variable), unary(self.unit))

    return __op, __iop, __rop


class Quantity(Generic[T]):
    __slots__ = ('_variable', '_unit')

    def __init__(self, value: T | Variable[T], /,
                 unit: str | Unit = DIMENSIONLESS,
                 uncertainty: T | Zero = zero) -> None:
        if not isinstance(unit, (str, Unit)):
            raise TypeError(f"{type(unit) = } is not 'str' or 'Unit'.")
        if isinstance(value, Variable):
            self._variable = value
        else:
            self._variable = Variable(value, uncertainty)
        self._unit = Unit.move(unit)

    @classmethod
    def one(cls, unit: str | Unit): return cls(1, unit)  # type: ignore

    @property
    def variable(self) -> Variable[T]: return self._variable
    @property
    def value(self) -> T: return self.variable.value
    @property
    def uncertainty(self) -> T | Zero: return self.variable.uncertainty
    @property
    def relative_uncertainty(self): return self.variable.relative_uncertainty
    @property
    def unit(self) -> Unit: return self._unit
    @property
    def dimension(self) -> Dimension: return self.unit.dimension
    @property
    def standard_variable(self): return self.variable * self.unit.factor
    @property
    def standard_value(self): return self.value * self.unit.factor

    def __repr__(self) -> str:
        return '{}(value={}, uncertainty={}, unit={})'.format(
            self.__class__.__name__, self.value, self.uncertainty, self.unit
        )

    def __str__(self) -> str:
        if self.unit.isdimensionless():
            return str(self.variable)
        return f'{self.variable} {self.unit}'

    def __format__(self, format_spec):
        if self.unit.isdimensionless():
            return format(self.variable, format_spec)
        return f'{self.variable:{format_spec}} {self.unit}'

    def isexact(self) -> bool: return self._variable.isexact()

    def isdimensionless(self) -> bool:
        return self.unit.isdimensionless()

    def copy(self) -> 'Quantity':
        return Quantity(copy(self.variable), self.unit)

    def to(self, new_unit: str | Unit, *, assert_dim=True):
        '''unit transform.

        if `assert_dim`, raise Error when not dimensionally consistent.'''
        new_unit = Unit.move(new_unit)
        if assert_dim and self.dimension != new_unit.dimension:
            raise ValueError(
                f'dimension {self.unit.dimension} != {new_unit.dimension}.')
        return Quantity(self.standard_variable / new_unit.factor, new_unit)

    def ito(self, new_unit: str | Unit, *, assert_dim=True):
        '''inplace unit transform.

        if `assert_dim`, raise Error when not dimensionally consistent.
        '''
        new_unit = Unit.move(new_unit)
        if assert_dim and self.dimension != new_unit.dimension:
            raise ValueError(
                f'dimension {self.unit.dimension} != {new_unit.dimension}.')
        self._variable *= self.unit.factor / new_unit.factor
        self._unit = new_unit
        return self

    def deprefix_unit(self, *, inplace=False):
        '''remove the prefix of the unit.'''
        old_unit_factor = self.unit.factor
        new_unit = self.unit.deprefix()
        factor = old_unit_factor / new_unit.factor
        if not inplace:
            return Quantity(self.variable * factor, new_unit)
        self._unit = new_unit
        self._variable *= factor
        return self

    def tobase_unit(self, *, inplace=False) -> 'Quantity':
        '''transform unit to the combination of `_BASIC_SI` unit with 
        the same dimension.
        '''
        old_unit_factor = self.unit.factor
        new_unit = self.unit.tobase()
        factor = old_unit_factor / new_unit.factor
        if not inplace:
            return Quantity(self.variable * factor, new_unit)
        self._unit = new_unit
        self._variable *= factor
        return self

    def simplify_unit(self, *, inplace=False) -> 'Quantity':
        '''try if the complex unit can be simplified as u, u⁻¹, u², u⁻², 
        where u represents a single `_BASIC_SI` unit. 
        '''
        old_unit_factor = self.unit.factor
        new_unit = self.unit.simplify()
        factor = old_unit_factor / new_unit.factor
        if not inplace:
            return Quantity(self.variable * factor, new_unit)
        self._unit = new_unit
        self._variable *= factor
        return self

    def remove_uncertainty(self) -> 'Quantity':
        '''set uncertainty zero.'''
        return Quantity(self.value, self.unit)

    __eq__ = _comparison(operator.eq)  # type: ignore
    __ne__ = _comparison(operator.ne)  # type: ignore
    __gt__ = _comparison(operator.gt)
    __lt__ = _comparison(operator.lt)
    __ge__ = _comparison(operator.ge)
    __le__ = _comparison(operator.le)

    __pos__ = _unary(operator.pos)
    __neg__ = _unary(operator.neg)

    __add__, __iadd__ = _addsub(operator.add, operator.iadd)
    __sub__, __isub__ = _addsub(operator.sub, operator.isub)

    __mul__, __imul__, __rmul__ = _muldiv(operator.mul, operator.imul)
    __matmul__, __imatmul__, __rmatmul__ = _muldiv(
        operator.matmul, operator.imatmul, unitop=operator.mul)
    __truediv__, __itruediv__, __rtruediv__ = _muldiv(
        operator.truediv, operator.itruediv, inverse=True)

    def __pow__(self, other):
        return Quantity(self.variable**other, self.unit**other)

    def __ipow__(self, other):
        self._variable **= other
        self._unit **= other
        return self

    def __rpow__(self, other):
        if not self.isdimensionless():
            raise ValueError("Quantity must be dimensionless as exponent.")
        return other ** self.value

    def nthroot(self, n: int):
        '''n-th root of Quantity. e.g. square root when n = 2.'''
        return Quantity(self.variable.nthroot(n), self._unit.nthroot(n))

    __array_priority__ = 1000000000000

    # def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
    #     pass
