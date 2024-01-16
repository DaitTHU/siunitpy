import operator
from copy import copy
from math import sqrt
from typing import Callable, Generic, Iterable, Optional, Sequence, TypeVar

from .templatelib import Interval

__all__ = ['Value']

T = TypeVar('T')


def _nthroot(a: T, b) -> T:
    '''same as a ** (1/b).'''
    if b == 2 and isinstance(a, float):
        return sqrt(a)
    return a ** (1 / b)  # type: ignore


def _hypotenuse(a: Optional[T], b: Optional[T]) -> Optional[T]:
    if a is None:
        return b
    if b is None:
        return a
    # if isinstance(a, Sequence) or isinstance(b, Sequence):
    return sqrt(a**2 + b**2)


def _comparison(op: Callable[[T, T], bool]):
    def __op(self: 'Value', other: 'Value'):
        return op(self.value, other.value)
    return __op


def _unary_op(op: Callable):
    def __op(self: 'Value'):
        return Value(op(self.value), self.uncertainty)
    return __op


def _addsub(op: Callable, iop: Callable):
    '''operator: a + b, a - b.'''

    def __op(self: 'Value', other: 'Value'):
        if not isinstance(other, Value):
            return Value(op(self.value, other), self.uncertainty)
        return Value(op(self.value, other.value),
                     _hypotenuse(self.uncertainty, other.uncertainty))

    def __iop(self: 'Value', other: 'Value'):
        if not isinstance(other, Value):
            self._value = iop(self.value, other)
            return self
        self._value = iop(self.value, other.value)
        self._uncertainty = _hypotenuse(self.uncertainty, other.uncertainty)
        return self

    return __op, __iop


def _muldiv(op: Callable, iop: Callable):
    '''operator: a * b, a / b.'''

    def __op(self: 'Value', other: 'Value'):
        if not isinstance(other, Value):
            return Value(op(self.value, other), op(self.uncertainty, abs(other)))
        new_value = op(self.value, other.value)
        new_uncertainty = new_value * \
            _hypotenuse(self.uncertainty / self.value,
                        other.uncertainty / other.value)
        return Value(new_value, new_uncertainty)

    def __iop(self: 'Value', other: 'Value'):
        if not isinstance(other, Value):
            self._value = iop(self.value, other)
            self._uncertainty = op(self.uncertainty, abs(other))
            return self
        self._value = iop(self.value, other.value)
        self._uncertainty = self.value * \
            _hypotenuse(self.uncertainty / self.value,
                        other.uncertainty / other.value)
        return self

    def __rop(self: 'Value', other):
        '''when other is not a `Value` object.'''
        new_value = op(other, self.value)
        new_uncertainty = abs(new_value / self.value) * self.uncertainty
        return Value(new_value, new_uncertainty)

    return __op, __iop, __rop


class Value(Generic[T]):
    __slots__ = ("_value", "_uncertainty")

    def __init__(self, value: T, /, uncertainty: Optional[T] = None) -> None:
        self._value = value
        self.uncertainty = uncertainty

    @property
    def value(self) -> T: return self._value
    @property
    def uncertainty(self) -> Optional[T]: return self._uncertainty

    @uncertainty.setter
    def uncertainty(self, uncertainty: Optional[T]):
        if uncertainty is not None \
                and not isinstance(uncertainty, type(self.value)):
            raise TypeError("value and uncertainty must have the same type.")
        if isinstance(uncertainty, Sequence):
            if any(u < 0 for u in uncertainty):
                raise ValueError("uncertainty must be positive.")
        elif uncertainty < 0:
            raise ValueError("uncertainty must be positive.")
        self._uncertainty = uncertainty

    @property
    def confidence_interval(self) -> Interval[T]:
        if self.uncertainty is None:
            return Interval(self.value, self.value)
        return Interval(self.value - self.uncertainty, self.value + self.uncertainty)

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

    def is_exact(self) -> bool:
        return self.uncertainty is None

    def copy(self) -> 'Value':
        return Value(copy(self.value), copy(self.uncertainty))

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

    __mul__, __imul__, __rmul__ = _muldiv(operator.mul, operator.imul)
    __matmul__, __imatmul__, __rmatmul__ = _muldiv(
        operator.matmul, operator.imatmul)
    __floordiv__, __ifloordiv__, __rfloordiv__ = _muldiv(
        operator.floordiv, operator.ifloordiv)
    __truediv__, __itruediv__, __rtruediv__ = _muldiv(
        operator.truediv, operator.itruediv)

    def __pow__(self, other: T):
        new_value = self.value ** other
        new_uncertainty = new_value * self.uncertainty / self.value
        return Value(new_value, new_uncertainty)

    def __ipow__(self, other: T):
        old_value = copy(self._value)
        self._value **= other
        self.uncertainty *= self.value * other / old_value
        return self

    def __rpow__(self, other): return other ** self.value

    def nthroot(self, n: int):
        '''n-th root of Value. e.g. square root when n = 2.'''
        value = _nthroot(self._value, n)
        uncertainty = self.uncertainty * value / (n * self.value)
        return Value(value, uncertainty)
