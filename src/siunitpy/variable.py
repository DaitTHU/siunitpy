import operator
import sys
from copy import copy
from math import sqrt
from typing import Any, Callable, Generic, Optional, Sequence, TypeVar

from .utilcollections import Interval
from .utilcollections.abc import Linear, Cardinal

if sys.version_info >= (3, 11):
    from typing import Self
else:
    Self = TypeVar('Self', bound='Variable')

__all__ = ['Variable']

T = TypeVar('T', bound=Linear[Any, Any])


def _hypotenuse(a: T | None, b: T | None) -> T | None:
    '''TODO: add np.ndarray()'''
    if a is None:
        return b
    if b is None:
        return a
    if isinstance(a, float) and isinstance(b, float):
        return sqrt(a**2 + b**2)  # type: ignore
    return None


def _comparison(op: Callable[[T, T], bool]):
    def __op(self: 'Variable', other):
        if not isinstance(other, Variable):
            return op(self.value, other)
        return op(self.value, other.value)
    return __op


def _unary_op(op: Callable):
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
            return Variable(op(self.value, other), None if self.is_exact()
                            else op(self.uncertainty, other))
        new_var = Variable(op(self.value, other.value))
        new_var.relative_uncertainty = _hypotenuse(
            self.relative_uncertainty, other.relative_uncertainty)
        return new_var

    def __iop(self: 'Variable', other: 'Variable'):
        if not isinstance(other, Variable):
            self._value = iop(self.value, other)
            self._uncertainty = None if self.is_exact() \
                else op(self.uncertainty, abs(other))
            return self
        self._value = iop(self.value, other.value)
        self.relative_uncertainty = _hypotenuse(
            self.relative_uncertainty, other.relative_uncertainty)
        return self

    def __rop(self: 'Variable', other):
        '''when other is not a `Value` object.'''
        new_value = op(other, self.value)
        return Variable(new_value, None if self.is_exact() else
                        new_value * self.relative_uncertainty)

    return __op, __iop, __rop


class Variable(Generic[T]):
    __slots__ = ("_value", "_uncertainty")

    def __init__(self, value: T, /, uncertainty: Optional[T] = None) -> None:
        self._value = value
        self.uncertainty = uncertainty

    @property
    def value(self) -> T: return self._value
    @property
    def uncertainty(self) -> T | None: return self._uncertainty

    @uncertainty.setter
    def uncertainty(self, uncertainty: Optional[T]) -> None:
        if uncertainty is None:
            self._uncertainty = None
            return
        if not isinstance(uncertainty, type(self.value)):
            raise TypeError("value and uncertainty must have the same type.")
        self._uncertainty = abs(uncertainty)

    @property
    def relative_uncertainty(self) -> T | None:
        return None if self.is_exact() else self.uncertainty / self.value

    @relative_uncertainty.setter
    def relative_uncertainty(self, rel_unc: Optional[T]) -> None:
        if rel_unc is None:
            self._uncertainty = None
            return
        self.uncertainty = self.value * rel_unc

    @property
    def confidence_interval(self) -> Interval[T]:  # type: ignore
        if not issubclass(type[T], Cardinal):
            raise TypeError('interval ends must be cardinal.')
        if self.uncertainty is None:
            return Interval(self.value, self.value)
        return Interval.neighborhood(self.value, self.uncertainty)  # type: ignore

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.value)}, " \
            f"uncertainty={repr(self.uncertainty)})"

    def __str__(self) -> str:
        if self.is_exact():
            return str(self.value)
        if isinstance(self.value, Sequence):
            pass
        return f'{self.value} ± {self.uncertainty}'

    def __format__(self, format_spec: str) -> str:
        if self.is_exact():
            return format(self.value, format_spec)
        if isinstance(self.value, Sequence):
            pass
        return f'{self.value:{format_spec}} ± {self.uncertainty:{format_spec}}'

    def is_exact(self) -> bool: return self.uncertainty is None

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

    __pos__ = _unary_op(operator.pos)
    __neg__ = _unary_op(operator.neg)

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
        new_var = Variable(self.value ** other)
        if self.is_exact():
            return new_var
        new_var.relative_uncertainty = other * self.relative_uncertainty
        return new_var

    def __ipow__(self, other: T):
        if self.is_exact():
            self._value **= other
            return self
        old_value = copy(self.value)
        self._value **= other
        self._uncertainty *= self.value * other / old_value
        return self

    def __rpow__(self, other): return other ** self.value
