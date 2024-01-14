import operator
from copy import copy
from typing import Callable, Iterable

from .dimension import Dimension
from .templatelib.utils import _hypotenuse, _nthroot
from .unit import Unit
from .unitconst import UnitConst

__all__ = ['Quantity']


def _comparison(op: Callable[[float, float], bool]):
    def __op(self, other):
        self.addable(other, assertTrue=True)
        return op(self.value * self.unit.value,
                  other.value * other.unit.value)
    return __op


def _unary_op(op: Callable):
    def __op(self: 'Quantity'):
        return Quantity(op(self.value), self.unit, self.uncertainty)
    return __op


def _addsub(op: Callable, iop: Callable):
    '''operator: a + b, a - b, where a, b have to share
    the same dimension.
    '''

    def __op(self: 'Quantity', other: 'Quantity'):
        if self.is_dimensionless() and not isinstance(other, Quantity):
            return Quantity(op(self.value, other), self.unit, self.uncertainty)
        self.addable(other, assertTrue=True)
        other_value = other.value * other.unit.value_over(self.unit)
        return Quantity(op(self.value, other_value), self.unit,
                        _hypotenuse(self.uncertainty, other.uncertainty))

    def __iop(self: 'Quantity', other: 'Quantity'):
        if self.is_dimensionless() and not isinstance(other, Quantity):
            self._value = iop(self.value, other)
            return self
        self.addable(other, assertTrue=True)
        other_value = other.value * other.unit.value_over(self.unit)
        self._value = iop(self.value, other_value)
        self._uncertainty = _hypotenuse(
            self.uncertainty, other.uncertainty)
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
            return Quantity(op(self.value, other), self.unit,
                            op(self.uncertainty, abs(other)))
        new_value = op(self.value, other.value)
        new_unit = unitop(self.unit, other.unit)
        if new_unit.parallel(UnitConst.DIMENSIONLESS):
            new_value *= new_unit.value
            new_unit = UnitConst.DIMENSIONLESS
        else:
            new_unit, factor = new_unit.simplify()
            new_value *= factor
        new_uncertainty = new_value * \
            _hypotenuse(self.uncertainty / self.value,
                        other.uncertainty / other.value)
        return Quantity(new_value, new_unit, new_uncertainty)

    def __iop(self: 'Quantity', other: 'Quantity'):
        if not isinstance(other, Quantity):
            self._value = iop(self.value, other)
            self._uncertainty = op(self.uncertainty, abs(other))
            return self
        self._value = iop(self.value, other.value)
        self._unit = unitop(self.unit, other.unit)
        if self.unit.parallel(UnitConst.DIMENSIONLESS):
            self._value *= self.unit.value
            self._unit = UnitConst.DIMENSIONLESS
        else:
            self._unit, factor = self.unit.simplify()
            self._value *= factor
        self._uncertainty = self.value * \
            _hypotenuse(self.uncertainty / self.value,
                        other.uncertainty / other.value)
        return self

    def __rop(self: 'Quantity', other):
        '''other is not a `Quantity` object.'''
        new_value = op(other, self.value)
        new_uncertainty = new_value * self.uncertainty / self.value
        return Quantity(new_value, pm(self.unit), new_uncertainty)

    return __op, __iop, __rop


def _unit_deprefix(unit: Unit) -> tuple[Unit, float]: return unit.deprefix()
def _unit_to_basic(unit: Unit) -> tuple[Unit, float]: return unit.to_basic()
def _unit_simplify(unit: Unit) -> tuple[Unit, float]: return unit.simplify()


class Quantity:
    
    __slots__ = ('_value', '_unit', '_uncertainty')

    def __init__(self, value: float, /,
                 unit: str | Unit = UnitConst.DIMENSIONLESS,
                 uncertainty: float = 0) -> None:
        if not isinstance(unit, (str, Unit)):
            raise TypeError(f"{type(unit) = } is not 'str' or 'Unit'.")
        self._value = value
        self._unit = Unit.move(unit)
        self._uncertainty = uncertainty

    @classmethod
    def one(cls, unit: str | Unit): return cls(1, unit, 0)

    @property
    def value(self) -> float: return self._value
    @property
    def unit(self) -> Unit: return self._unit
    @property
    def dimension(self) -> Dimension: return self._unit.dimension
    @property
    def uncertainty(self) -> float: return self._uncertainty

    def __repr__(self) -> str:
        return self.__class__.__name__ \
            + f'(value={repr(self.value)}, unit={self.unit}, '\
            f'uncertainty={self.uncertainty})'

    def __str__(self) -> str:
        value = str(self.value)
        if not self.is_exact():
            value += f' ± {self.uncertainty}'
        if self.unit == UnitConst.DIMENSIONLESS:
            return value
        return f'{value} {self.unit}'

    def is_exact(self) -> bool:
        if isinstance(self.uncertainty, Iterable):
            return all(unc == 0 for unc in self.uncertainty)
        return self.uncertainty == 0

    def is_dimensionless(self) -> bool:
        return self.unit == UnitConst.DIMENSIONLESS

    def copy(self) -> 'Quantity':
        return Quantity(copy(self.value), self.unit, copy(self.uncertainty))

    def to(self, new_unit: str | Unit, *, assertDimension=True):
        '''unit transform.
        if assertDimension, raise Error when dimension unparallel.'''
        new_unit = Unit.move(new_unit)
        if assertDimension:
            self.unit.parallel(new_unit, assertTrue=True)
        factor = self.unit.value_over(new_unit)
        return Quantity(self.value * factor, new_unit,
                        self.uncertainty * factor)

    def ito(self, new_unit: str | Unit, *, assertDimension=True):
        '''inplace unit transform'''
        new_unit = Unit.move(new_unit)
        if assertDimension:
            self.unit.parallel(new_unit, assertTrue=True)
        factor = self.unit.value_over(new_unit)
        self._value *= factor
        self._uncertainty *= factor
        self._unit = new_unit
        return self

    def __change_unit(self, unit_fun: Callable[[Unit], tuple[Unit, float]]):
        new_unit, factor = unit_fun(self.unit)
        return Quantity(self.value * factor, new_unit, self.uncertainty * factor)

    def __ichange_unit(self, unit_fun: Callable[[Unit], tuple[Unit, float]]):
        self._unit, factor = unit_fun(self.unit)
        self._value *= factor
        self._uncertainty *= factor
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

    def addable(self, other, /, *, assertTrue=False) -> bool:
        if not isinstance(other, Quantity):
            raise TypeError(f"type of '{other}' is not Quantity.")
        return self.unit.parallel(other.unit, assertTrue=assertTrue)
    
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
    # __floordiv__, __ifloordiv__, __rfloordiv__ = _muldiv(
    #    operator.floordiv, operator.ifloordiv, operator.sub, operator.neg)
    __truediv__, __itruediv__, __rtruediv__ = _muldiv(
        operator.truediv, operator.itruediv, operator.sub, operator.neg)

    def __pow__(self, other):
        new_value = self.value ** other
        new_uncertainty = new_value * self.uncertainty / self.value
        return Quantity(new_value, self.unit * other, new_uncertainty)

    def __ipow__(self, other):
        old_value = copy(self._value)
        self._value **= other
        self._unit *= other
        self._uncertainty *= self.value * other / old_value
        return self

    def nthroot(self, n: int):
        value = _nthroot(self._value, n)
        unit = self._unit / n
        uncertainty = self.uncertainty * value / (n * self.value)
        return Quantity(value, unit, uncertainty)
