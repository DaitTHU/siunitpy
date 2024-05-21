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


def unit_rop_warn():
    import warnings
    unit_rop_warning_message = "To directly assign a unit to a value to make \
it a Quantity object, please use expression 'value @ unit', the expression \
'value * unit' or 'value / unit' may produce unintended results."
    warnings.warn(unit_rop_warning_message, SyntaxWarning, stacklevel=3)


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
        raise TypeError(f"unit must be 'str' or 'Unit', not {type(unit)}.")

    def __rmul__(self, other):
        '''only used when type(other) is not Unit (and not Quantity).
        value * unit = Quantity(value, unit)
        '''
        if isinstance(other, Variable):
            return Quantity(other, self)
        if isinstance(other, Quantity):
            return Quantity(other.variable, other.unit * self)
        unit_rop_warn()
        return Quantity(other, self)

    def __rtruediv__(self, other):
        '''value / unit = Quantity(value, unit.inverse())
        '''
        if isinstance(other, Variable):
            return Quantity(other, self.inverse())
        if isinstance(other, Quantity):
            return Quantity(other.variable, other.unit / self)
        unit_rop_warn()
        return Quantity(other, self.inverse())

    def __rmatmul__(self, other):
        '''operator `@` means 'at', i.e. directly assign the unit to `other`.
        value @ unit = Quantity(value, unit)
        '''
        return Quantity(other, self)  # type(other) is not Quantity

    __array_priority__ = 100000000000


DIMENSIONLESS = Unit('')


def assert_dimension_consistency(left, right):
    # assert hasattr(left, 'dimension') and hasattr(right, 'dimension')
    if left.dimension != right.dimension:
        raise ValueError(f"dimension {left.dimension} != {right.dimension}.")


def _comparison(op: Callable[[Variable, Variable], bool]):
    '''construct operator: a == b, a != b, a > b, ...

    if a is dimensionless, b can be non-quantity. 
    Otherwise, a and b should meet dimension consistency.
    '''

    def __op(self: 'Quantity', other: 'Quantity'):
        if self.isdimensionless() and not isinstance(other, Quantity):
            return op(self.standard_variable, other)
        assert_dimension_consistency(self, other)
        return op(self.standard_variable, other.standard_variable)
    return __op


def _addsub(op: Callable, iop: Callable):
    '''construct operator: a + b, a - b.

    if a is dimensionless, b can be non-quantity. 
    Otherwise, a and b should meet dimension consistency.
    '''

    def __op(self: 'Quantity', other: 'Quantity'):
        if self.isdimensionless() and not isinstance(other, Quantity):
            return Quantity(op(self.standard_variable, other))
        assert_dimension_consistency(self, other)
        other_var = other.variable * (other.unit.factor / self.unit.factor)
        return Quantity(op(self.variable, other_var), self.unit)

    def __iop(self: 'Quantity', other: 'Quantity'):
        if self.isdimensionless() and not isinstance(other, Quantity):
            self._variable *= self.unit.factor
            self._variable = iop(self._variable, other)
            self._unit = DIMENSIONLESS
            return self
        assert_dimension_consistency(self, other)
        other_var = other.variable * (other.unit.factor / self.unit.factor)
        self._variable = iop(self._variable, other_var)
        return self

    def __rop(self: 'Quantity', other):
        '''type(other) is not Quantity.'''
        if not self.isdimensionless():
            raise ValueError(f'{self.dimension} is not dimensionless, '
                             'cannot +/- non-quantity value.')
        return Quantity(op(other, self.standard_variable))

    return __op, __iop, __rop


def _muldiv(op: Callable, iop: Callable, *, unitop=None, inverse=False):
    '''operator: a * b, a / b, a @ b

    when a or b is not a `Quantity` object, which will be treated as a
    dimensionless Quantity.
    '''
    # unitop: unit [op] unit, [op] = * or /
    if unitop is None:
        unitop = op

    # opunit: quantity [op] unit, [op] = *, / or @
    if op is operator.matmul:
        # quantity @ unit, directly assign the unit
        def opunit(selfunit, unit): return unit
    else:
        def opunit(selfunit, unit): return unitop(selfunit, unit)

    def __op(self: 'Quantity', other: 'Quantity'):
        if isinstance(other, Unit):
            return Quantity(self.variable, opunit(self.unit, other))
        if not isinstance(other, Quantity):
            return Quantity(op(self.variable, other), self.unit)
        result = Quantity(op(self.variable, other.variable),
                          unitop(self.unit, other.unit))
        return result

    def __iop(self: 'Quantity', other: 'Quantity'):
        if isinstance(other, Unit):
            self._unit = opunit(self.unit, other)
            return self
        if not isinstance(other, Quantity):
            self._variable = iop(self._variable, other)
            return self
        self._variable = iop(self._variable, other.variable)
        self._unit = unitop(self._unit, other.unit)
        return self

    # unary operator of unit when non-quantity [op] quantity
    if inverse:
        def unary(unit: Unit): return unit.inverse()  # type: ignore
    else:
        def unary(unit): return unit

    def __rop(self: 'Quantity', other):
        '''other is not a `Quantity` object.'''
        if isinstance(other, Unit):
            return Quantity(self.variable, opunit(self.unit, other))
        return Quantity(op(other, self._variable), unary(self.unit))

    return __op, __iop, __rop


class Quantity(Generic[T]):
    __slots__ = ('_variable', '_unit')

    def __init__(self, value: T | Variable[T], /,
                 unit: str | Unit = DIMENSIONLESS,
                 uncertainty: T | Zero = zero) -> None:
        if isinstance(value, Variable):
            self._variable = value
        else:
            self._variable = Variable(value, uncertainty)
        self._unit = Unit.move(unit)

    @classmethod
    def one(cls, unit: str | Unit): return cls(1, unit)  # type: ignore

    @property
    def variable(self) -> Variable[T]: return self._variable
    @variable.setter
    def variable(self, variable: Variable[T]): self._variable = variable
    @property
    def value(self) -> T: return self.variable.value
    @value.setter
    def value(self, value: T): self._variable.value = value
    @property
    def uncertainty(self) -> T | Zero: return self.variable.uncertainty

    @uncertainty.setter
    def uncertainty(self, uncertainty: T | Zero):
        self._variable.uncertainty = uncertainty

    @property
    def relative_uncertainty(self): return self.variable.relative_uncertainty

    @relative_uncertainty.setter
    def relative_uncertainty(self, relative_uncertainty: T | Zero):
        self._variable.relative_uncertainty = relative_uncertainty

    @property
    def unit(self) -> Unit: return self._unit
    @unit.setter
    def unit(self, unit: str | Unit): self._unit = Unit.move(unit)
    @property
    def dimension(self) -> Dimension: return self.unit.dimension
    @property
    def standard_variable(self): return self.variable * self.unit.factor
    @property
    def standard_value(self): return self.value * self.unit.factor

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f'{cls}({self.variable}, {self.unit})'

    def __str__(self) -> str:
        if self.unit is DIMENSIONLESS:
            return str(self.variable)
        return f'{self.variable} {self.unit}'

    def __format__(self, format_spec):
        if self.unit is DIMENSIONLESS:
            return format(self.variable, format_spec)
        return f'{self.variable:{format_spec}} {self.unit}'

    def isexact(self) -> bool: return self._variable.isexact()

    def isdimensionless(self) -> bool:
        return self.unit.isdimensionless()

    def copy(self) -> 'Quantity':
        return Quantity(copy(self.variable), self.unit)

    def _to(self, new_unit: Unit, factor: float, inplace: bool):
        '''internal use only.'''
        if inplace:
            self._variable *= factor
            self._unit = new_unit
            return self
        return Quantity(self.variable * factor, new_unit)

    def to(self, new_unit: str | Unit, *, inplace=False, assert_dim=True):
        '''unit transform.
        if `assert_dim`, raise Error when not dimensionally consistent.
        '''
        new_unit = Unit.move(new_unit)
        if assert_dim and self.dimension != new_unit.dimension:
            raise ValueError(
                f'dimension {self.dimension} != {new_unit.dimension}.')
        return self._to(new_unit, self.unit.factor / new_unit.factor, inplace)

    def ito(self, new_unit: str | Unit, *, assert_dim=True):
        '''abbreviation of inplace unit transform.'''
        return self.to(new_unit, inplace=True, assert_dim=assert_dim)

    def deprefix_unit(self, *, inplace=False):
        '''remove all the prefix of the unit.'''
        new_unit, factor = self.unit.deprefix_with_factor()
        return self._to(new_unit, factor, inplace)

    def tobase_unit(self, *, inplace=False) -> 'Quantity':
        '''transform unit to a combination of base SI unit 
        (i.e. m, kg, s, A, K, mol, cd) 
        with the same dimension.
        '''
        new_unit, factor = self.unit.tobase_with_factor()
        return self._to(new_unit, factor, inplace)

    def simplify_unit(self, *, inplace=False) -> 'Quantity':
        '''try if the complex unit can be simplified as a single unit
        (i.e. `u`, `u⁻¹`, `u²`, `u⁻²`).
        
        see `Unit.simplify.__doc__` for more infomation about `u`.
        '''
        if self.isdimensionless():
            return self._to(DIMENSIONLESS, self.unit.factor, inplace)
        new_unit, factor = self.unit.simplify_with_factor()
        return self._to(new_unit, factor, inplace)

    def remove_uncertainty(self) -> 'Quantity':
        '''set uncertainty zero.'''
        return Quantity(self.value, self.unit)

    __eq__ = _comparison(operator.eq)  # type: ignore
    __ne__ = _comparison(operator.ne)  # type: ignore
    __gt__ = _comparison(operator.gt)
    __lt__ = _comparison(operator.lt)
    __ge__ = _comparison(operator.ge)
    __le__ = _comparison(operator.le)

    def __pos__(self): return Quantity(+self.variable, self.unit)
    def __neg__(self): return Quantity(-self.variable, self.unit)

    __add__, __iadd__, __radd__ = _addsub(operator.add, operator.iadd)
    __sub__, __isub__, __rsub__ = _addsub(operator.sub, operator.isub)

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
