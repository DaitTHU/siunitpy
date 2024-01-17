import operator
from copy import copy
from typing import Callable, Generic, Iterable, TypeVar

from .dimension import Dimension
from .templatelib import Linear
from .unit import Unit, UnitDimensionError
from .unitconst import UnitConst
from .variable import Variable

__all__ = ['Quantity']

T = TypeVar('T')


def _comparison(op: Callable[[float, float], bool]):
    def __op(self, other):
        self.addable(other, assertTrue=True)
        return op(self.variable * self.unit.value, other.variable * other.unit.value)
    return __op


def _unary_op(op: Callable):
    def __op(self: 'Quantity'):
        return Quantity(op(self.variable), self.unit)
    return __op


def _addsub(op: Callable, iop: Callable):
    '''operator: a + b, a - b, where a, b have to share
    the same dimension.
    '''

    def __op(self: 'Quantity', other: 'Quantity'):
        if self.is_dimensionless() and not isinstance(other, Quantity):
            return Quantity(op(self.variable, other), self.unit)
        self.addable(other, assertTrue=True)
        other_var = other.variable * other.unit.value_over(self.unit)
        return Quantity(op(self.variable, other_var), self.unit)

    def __iop(self: 'Quantity', other: 'Quantity'):
        if self.is_dimensionless() and not isinstance(other, Quantity):
            self._variable = iop(self.variable, other)
            return self
        self.addable(other, assertTrue=True)
        self._variable = iop(self.variable, other.variable *
                             other.unit.value_over(self.unit))
        return self

    return __op, __iop


def _muldiv(op: Callable, iop: Callable, unitop: Callable[[Unit, Unit], Unit],
            pm: Callable[[Unit], Unit]):
    '''operator: a * b, a / b, 

    when a or b is not a `Quantity` object, which will be treated as a
    dimensionless Quantity.
    '''

    def __op(self: 'Quantity', other: 'Quantity'):
        if not isinstance(other, Quantity):
            return Quantity(op(self.variable, other), self.unit)
        new_value = op(self.value, other.value)
        new_unit = unitop(self.unit, other.unit)
        if new_unit.parallel(UnitConst.DIMENSIONLESS):
            new_value *= new_unit.value
            new_unit = UnitConst.DIMENSIONLESS
        else:
            new_unit, factor = new_unit.simplify()
            new_value *= factor
        return Quantity(new_value, new_unit)

    def __iop(self: 'Quantity', other: 'Quantity'):
        if not isinstance(other, Quantity):
            self._variable = iop(self.value, other)
            return self
        self._variable = iop(self.value, other.value)
        self._unit = unitop(self.unit, other.unit)
        if self.unit.parallel(UnitConst.DIMENSIONLESS):
            self._variable *= self.unit.value
            self._unit = UnitConst.DIMENSIONLESS
        else:
            self._unit, factor = self.unit.simplify()
            self._variable *= factor
        return self

    def __rop(self: 'Quantity', other):
        '''other is not a `Quantity` object.'''
        return Quantity(op(other, self._variable), pm(self.unit))

    return __op, __iop, __rop


def _unit_deprefix(unit: Unit) -> tuple[Unit, float]: return unit.deprefix()
def _unit_to_basic(unit: Unit) -> tuple[Unit, float]: return unit.to_basic()
def _unit_simplify(unit: Unit) -> tuple[Unit, float]: return unit.simplify()


class Quantity(Generic[T]):
    __slots__ = ('_variable', '_unit')

    def __init__(self, value: T | Variable[T], /,
                 unit: str | Unit = UnitConst.DIMENSIONLESS,
                 uncertainty: T | None = None) -> None:
        if not isinstance(unit, (str, Unit)):
            raise TypeError(f"{type(unit) = } is not 'str' or 'Unit'.")
        if isinstance(value, Variable):
            self._variable: Variable[T] = value  # ignore the 3rd arg
        else:
            self._variable = Variable(value, uncertainty)
        self._unit = Unit.move(unit)

    @classmethod
    def one(cls, unit: str | Unit): return cls(1, unit)

    @property
    def variable(self) -> Variable[T]: return self._variable
    @property
    def value(self) -> T: return self.variable.value
    @property
    def uncertainty(self) -> T | None: return self.variable.uncertainty
    @property
    def unit(self) -> Unit: return self._unit
    @property
    def dimension(self) -> Dimension: return self.unit.dimension

    def __repr__(self) -> str:
        return self.__class__.__name__ \
            + f'(value={repr(self.value)}, uncertainty={self.uncertainty}, '\
            f'unit={self.unit})'

    def __str__(self) -> str:
        if self.unit == UnitConst.DIMENSIONLESS:
            return str(self.variable)
        return f'{self.variable} {self.unit}'

    def __format__(self, format_spec):
        if self.unit == UnitConst.DIMENSIONLESS:
            return format(self.variable, format_spec)
        return f'{self.variable:{format_spec}} {self.unit}'

    def is_exact(self) -> bool: return self._variable.is_exact()

    def is_dimensionless(self) -> bool:
        return self.unit == UnitConst.DIMENSIONLESS

    def copy(self) -> 'Quantity':
        return Quantity(copy(self.variable), self.unit)

    def to(self, new_unit: str | Unit, *, assertDimension=True):
        '''unit transform.
        if assertDimension, raise Error when dimension unparallel.'''
        new_unit = Unit.move(new_unit)
        if assertDimension:
            self.unit.parallel(new_unit, assertTrue=True)
        factor = self.unit.value_over(new_unit)
        return Quantity(self.variable * factor, new_unit)

    def ito(self, new_unit: str | Unit, *, assertDimension=True):
        '''inplace unit transform'''
        new_unit = Unit.move(new_unit)
        if assertDimension:
            self.unit.parallel(new_unit, assertTrue=True)
        self._variable *= self.unit.value_over(new_unit)
        self._unit = new_unit
        return self

    def __change_unit(self, unit_fun: Callable[[Unit], tuple[Unit, float]]):
        new_unit, factor = unit_fun(self.unit)
        return Quantity(self.variable * factor, new_unit)

    def __ichange_unit(self, unit_fun: Callable[[Unit], tuple[Unit, float]]):
        self._unit, factor = unit_fun(self.unit)
        self._variable *= factor
        return self

    def deprefix_unit(self) -> 'Quantity':
        return self.__change_unit(_unit_deprefix)

    def ideprefix_unit(self) -> 'Quantity':
        return self.__ichange_unit(_unit_deprefix)

    def to_basic_unit(self) -> 'Quantity':
        return self.__change_unit(_unit_to_basic)

    def ito_basic_unit(self) -> 'Quantity':
        return self.__ichange_unit(_unit_to_basic)

    def simplify_unit(self) -> 'Quantity':
        return self.__change_unit(_unit_simplify)

    def isimplify_unit(self) -> 'Quantity':
        return self.__ichange_unit(_unit_simplify)

    def addable(self, other: 'Quantity', /, *, assertTrue=False) -> bool:
        try:
            return self.unit.parallel(other.unit, assertTrue=assertTrue)
        except AttributeError:
            raise TypeError(f"type of '{other}' must be 'Quantity'.")

    def remove_uncertainty(self) -> 'Quantity':
        return Quantity(self.value, self.unit)

    __eq__ = _comparison(operator.eq)
    __ne__ = _comparison(operator.ne)
    __gt__ = _comparison(operator.gt)
    __lt__ = _comparison(operator.lt)
    __ge__ = _comparison(operator.ge)
    __le__ = _comparison(operator.le)

    __pos__ = _unary_op(operator.pos)
    __neg__ = _unary_op(operator.neg)

    __add__, __iadd__ = _addsub(operator.add, operator.iadd)
    __sub__, __isub__ = _addsub(operator.sub, operator.isub)

    __mul__, __imul__, __rmul__ = _muldiv(
        operator.mul, operator.imul, operator.add, operator.pos)
    __matmul__, __imatmul__, __rmatmul__ = _muldiv(
        operator.matmul, operator.imatmul, operator.add, operator.pos)
    __floordiv__, __ifloordiv__, __rfloordiv__ = _muldiv(
        operator.floordiv, operator.ifloordiv, operator.sub, operator.neg)
    __truediv__, __itruediv__, __rtruediv__ = _muldiv(
        operator.truediv, operator.itruediv, operator.sub, operator.neg)

    def __pow__(self, other):
        return Quantity(self.variable ** other, self.unit * other)

    def __ipow__(self, other):
        self._variable **= other
        self._unit *= other
        return self

    def __rpow__(self, other):
        if not self.is_dimensionless():
            raise UnitDimensionError(
                "Quantity must be dimensionless as exponent.")
        return other ** self.value

    def nthroot(self, n: int):
        '''n-th root of Quantity. e.g. square root when n = 2.'''
        return Quantity(self.variable**(1 / n), self._unit / n)

    __array_priority__ = 1000000000000

    # def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
    #     pass
