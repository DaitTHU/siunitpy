import operator
from copy import copy
from typing import Any, Callable, Generic, Iterable, TypeVar

try:
    from numpy import log
except ImportError:
    from math import log

from .identity import Zero, zero
from .utilcollections import Interval
from .utilcollections.abc import Cardinal, Linear

__all__ = ['Variable']

T = TypeVar('T', bound=Linear)


def move(obj: T | None | Zero) -> T | Zero:
    return zero if obj is None else obj


def is_zero(value: Any, precision: Any = 0) -> bool:
    '''`value` is a non-negative number/array.'''
    if value is zero:
        return True
    if isinstance(value, Iterable):
        try:
            return all(value <= precision)  # numpy.ndarray
        except TypeError:
            if isinstance(precision, Iterable):
                return all(v <= p for v, p in zip(value, precision))
            return all(v <= precision for v in value)  # list
    if isinstance(precision, Iterable):
        raise TypeError("precision must have the same type as value.")
    return value <= precision  # float


def _hypotenuse(a, b): return (a**2 + b**2)**0.5


def _comparison(op: Callable[[T, T], bool]):
    def __op(self: 'Variable', other):
        if not isinstance(other, Variable):
            return op(self.value, other)
        return op(self.value, other.value)
    return __op


def _unary(op: Callable):
    def __op(self: 'Variable'):
        return Variable(op(self.value), self.uncertainty)
    return __op


def _addsub(op: Callable, iop: Callable):
    '''operator: a + b, a - b.'''

    def __op(self: 'Variable', other: 'Variable'):
        if not isinstance(other, Variable):
            return Variable(op(self.value, other), self.uncertainty)
        return Variable(op(self.value, other.value),
                        _hypotenuse(self.uncertainty, other.uncertainty))

    def __iop(self: 'Variable', other: 'Variable'):
        if not isinstance(other, Variable):
            self._value = iop(self.value, other)
            return self
        self._value = iop(self.value, other.value)
        self._uncertainty = _hypotenuse(self.uncertainty, other.uncertainty)
        return self

    return __op, __iop


def _muldiv(op: Callable, iop: Callable):
    '''operator: a * b, a / b.'''

    def __op(self: 'Variable', other: 'Variable'):
        if not isinstance(other, Variable):
            return Variable(op(self.value, other), op(self.uncertainty, other))
        r = _hypotenuse(self.relative_uncertainty, other.relative_uncertainty)
        return Variable(op(self.value, other.value), relative_uncertainty=r)

    def __iop(self: 'Variable', other: 'Variable'):
        if not isinstance(other, Variable):
            self._value = iop(self.value, other)
            self._uncertainty = op(self.uncertainty, abs(other))
            return self
        self._value = iop(self.value, other.value)
        self.relative_uncertainty = \
            _hypotenuse(self.relative_uncertainty, other.relative_uncertainty)
        return self

    def __rop(self: 'Variable', other):
        '''when other is not a `Variable` object.'''
        return Variable(op(other, self.value),
                        relative_uncertainty=self.relative_uncertainty)

    return __op, __iop, __rop


class Variable(Generic[T]):
    __slots__ = ("_value", "_uncertainty")

    def __init__(self, value: T, /, uncertainty: T | Zero = zero, *,
                 relative_uncertainty: T | Zero = zero) -> None:
        self._value = value
        if uncertainty is not zero:
            self.uncertainty = uncertainty
        else:
            self.relative_uncertainty = relative_uncertainty

    @property
    def value(self) -> T: return self._value
    @value.setter
    def value(self, value: T) -> None: self._value = value

    @property
    def uncertainty(self) -> T | Zero: return self._uncertainty

    @uncertainty.setter
    def uncertainty(self, uncertainty: T | Zero) -> None:
        self._uncertainty = abs(move(uncertainty))

    @property
    def relative_uncertainty(self) -> T | Zero:
        return self._uncertainty / self.value

    @relative_uncertainty.setter
    def relative_uncertainty(self, relative_uncertainty: T | Zero) -> None:
        self._uncertainty = abs(self.value * move(relative_uncertainty))

    @property
    def confidence_interval(self) -> Interval[T]:
        if not isinstance(self.value, Cardinal):
            raise TypeError('interval ends must be cardinal.')
        if isinstance(self.uncertainty, Zero):
            return Interval(self.value, self.value)
        return Interval.neighborhood(self.value, self.uncertainty)

    def __repr__(self) -> str:
        return '{}({}, uncertainty={})'.format(
            self.__class__.__name__, self.value, self.uncertainty
        )

    def __str__(self) -> str:
        if self.is_exact():
            return str(self.value)
        return f'{self.value} ± {self.uncertainty}'

    def __format__(self, format_spec: str) -> str:
        if self.is_exact():
            return format(self.value, format_spec)
        return f'{self.value:{format_spec}} ± {self.uncertainty:{format_spec}}'

    def is_exact(self, precision=zero) -> bool:
        if precision is zero:
            precision = 0
        return is_zero(self.uncertainty, precision)

    def clear_uncertainty(self) -> None: self._uncertainty = zero

    def copy(self) -> 'Variable':
        return Variable(copy(self.value), copy(self.uncertainty))

    def almost_equal(self, other: 'Variable') -> bool:
        return self.confidence_interval.intersect(other.confidence_interval)

    def same_as(self, other: 'Variable') -> bool:
        return self.value == other.value and self.uncertainty == other.uncertainty

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
        operator.matmul, operator.imatmul)
    __floordiv__, __ifloordiv__, __rfloordiv__ = _muldiv(
        operator.floordiv, operator.ifloordiv)
    __truediv__, __itruediv__, __rtruediv__ = _muldiv(
        operator.truediv, operator.itruediv)

    def __pow__(self, other: T):
        if not isinstance(other, Variable):
            rel_uncert = self.relative_uncertainty * other
        else:
            rel_uncert = _hypotenuse(self.relative_uncertainty * other.value,
                                     log(self.value) * other.uncertainty)  # type: ignore
        return Variable(self.value ** other, relative_uncertainty=rel_uncert)

    def __ipow__(self, other: T):
        if self.is_exact():
            self._value **= other
            return self
        old_value = copy(self.value)
        self._value *= other - 1
        self._uncertainty *= self.value * other
        self._value *= old_value
        return self

    def __rpow__(self, other): return other ** self.value
