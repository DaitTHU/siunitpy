import operator
from decimal import Decimal
from fractions import Fraction
from math import sqrt
from typing import Callable, Iterable, TypeVar

__all__ = [
    'unzip', 'common_rational',
    '_inplace', '_sum', '_prod', '_first',
    '_nthroot', '_hypotenuse'
]

T, S = TypeVar('T'), TypeVar('S')
K, V = TypeVar('K'), TypeVar('V')


def unzip(iterable: Iterable[tuple[T, S]]) -> tuple[tuple[T], tuple[S]]:
    '''
    >>> a = list(zip([1, 2, 3], ['a', 'b', 'c']))
    [(1, 'a'), (2, 'b'), (3, 'c')]
    >>> list(unzip(a))
    [(1, 2, 3), ('a', 'b', 'c')]
    '''
    return zip(*iterable)  # type: ignore


def common_rational(number: int | float) -> Fraction:
    '''CommonRational is common rational numbers, common means it's
    integer or fraction with small numerator and denominator, like
    1, -42, 2/3...
    '''
    frac = Fraction(number)
    return frac.limit_denominator() if isinstance(number, float) else frac


def _inplace(op: Callable[[T, S], T]) -> Callable[[T, S], T]:
    '''The easiest way to generate __iop__ using __op__. In this way:
    >>> b = a
    >>> b += c  # a no change
    '''

    def iop(self: T, other: S) -> T:
        self = op(self, other)
        return self
    return iop


def __join(op: Callable[[T, T], T],
           left: T | None = None, /, *rights: T) -> T | None:
    for right in rights:
        left = op(left, right)  # type: ignore
    return left


def _sum(iterable: Iterable[T]) -> T | None:
    return __join(operator.add, *iterable)


def _prod(iterable: Iterable[T]) -> T | None:
    return __join(operator.mul, *iterable)


def _first(iterable: Iterable[T], default: T) -> T:
    for item in iterable:
        return item
    return default


def _nthroot(a: T, b) -> T:
    '''same as a ** (1/b).'''
    if b == 2 and isinstance(a, float):
        return sqrt(a)
    return a ** (1 / b) # type: ignore


def _hypotenuse(a: float, b: float) -> float:
    if a == 0:
        return b
    if b == 0:
        return a
    return sqrt(a**2 + b**2)

