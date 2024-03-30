from decimal import Decimal
from fractions import Fraction
from typing import Callable, Iterable, TypeVar, overload

__all__ = [
    'superscript', 'common_rational',
    'unzip', 'firstof', 'neg_after',
    '_inplace',
]

T = TypeVar('T')
T_1, T_2, T_3 = TypeVar('T_1'), TypeVar('T_2'), TypeVar('T_3')
K, V = TypeVar('K'), TypeVar('V')

from typing import TypeAlias

Number: TypeAlias = int | float | Decimal | Fraction


_SUPERSCRIPT = '⁰¹²³⁴⁵⁶⁷⁸⁹'
_SUBSCRIPT = '₀₁₂₃₄₅₆₇₈₉'


def superscript(ratio: Fraction | int) -> str:
    '''turn a number (Fraction/int) into superscript, 
    like 2 -> ², -1 -> ⁻¹, 3/4 -> ³ᐟ⁴, etc.'''
    if ratio.numerator < 0:
        return '⁻¹' if ratio == -1 else '⁻' + superscript(-ratio)
    if ratio == 1:
        return ''  # omit
    if ratio.denominator == 1:
        return _sup_int(ratio.numerator)
    return _sup_int(ratio.numerator) + 'ᐟ' + _sup_int(ratio.denominator)


def _sup_int(number: int) -> str:
    return ''.join(_SUPERSCRIPT[int(digit)] for digit in str(number))


def common_rational(number: Number) -> Fraction:
    '''CommonRational is common rational numbers, common means it's
    integer or fraction with small numerator and denominator, like
    1, -42, 2/3...
    '''
    if isinstance(number, Fraction):
        return number
    frac = Fraction(number)
    return frac.limit_denominator() if isinstance(number, float) else frac


@overload
def unzip(iterable: Iterable[tuple[T_1, T_2]]
          ) -> tuple[tuple[T_1], tuple[T_2]]: ...


@overload
def unzip(iterable: Iterable[tuple[T_1, T_2, T_3]]
          ) -> tuple[tuple[T_1], tuple[T_2], tuple[T_3]]: ...


def unzip(iterable: Iterable):
    '''
    >>> a = list(zip([1, 2, 3], ['a', 'b', 'c']))
    [(1, 'a'), (2, 'b'), (3, 'c')]
    >>> list(unzip(a))
    [(1, 2, 3), ('a', 'b', 'c')]
    '''
    return tuple(zip(*iterable))


def firstof(iterable: Iterable[T], /, default: T) -> T:
    '''return the first item of an iterable.'''
    for item in iterable:
        return item
    return default


def neg_after(ls: list, idx: int) -> None:
    '''negate items in-place after an index (exclusive) in the list.'''
    for i in range(idx + 1, len(ls)):
        ls[i] = -ls[i]


def _inplace(op: Callable[[T_1, T_2], T_1]) -> Callable[[T_1, T_2], T_1]:
    '''The easiest way to generate __iop__ using __op__. In this way:
    >>> b = a
    >>> b += c  # a no change
    '''

    def iop(self: T_1, other: T_2) -> T_1:
        self = op(self, other)
        return self
    return iop
