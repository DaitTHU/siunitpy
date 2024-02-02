'''Continued Fraction by Dait, 2023/9/5
ref: https://en.wikipedia.org/wiki/Continued_fraction

r = a0 + _________1__________
         a1 + _______1_______
              a2 + ____1_____
                   ... + 1/an

which can be represented by abbreviated notation

r = [a0; a1, a2, ..., an]
'''

from fractions import Fraction
from itertools import accumulate
from typing import Iterable, Iterator, SupportsIndex

__all__ = ['ContinuedFraction']


def _frac2cfrac(fraction: Fraction) -> Iterator[int]:
    '''
    an term can be calculated using the following recursive formula

    `an = floor(Nn / Nn+1)`

    where `N0 = r`, `N1 = 1`, `Nn+1 = Nn-1 mod Nn`.

    From which it can be understood that the sequence stops if `Nn+1 = 0`.
    '''
    p, q = fraction.as_integer_ratio()
    while q:
        yield p // q
        p, q = q, p % q


def _float2cfrac(number: float, len_limit: int, coefficient_limit: int):
    for _ in range(len_limit):
        integer_part = int(number)
        if integer_part > coefficient_limit:
            break
        yield integer_part
        try:
            number = 1 / (number - integer_part)
        except ZeroDivisionError:
            break


class ContinuedFraction:
    '''ContinuedFraction is an expression obtained through an 
    iterative process of representing a number as the sum of 
    its integer part and the reciprocal of another number, 
    then writing this other number as the sum of its integer 
    part and another reciprocal, and so on.

    `r = a0 + 1/(a1 + 1/(a2 + 1/(... + 1/an)))`

    which can be represented by abbreviated notation

    `r = [a0; a1, a2, ..., an]`

    which, the coefficients, is excactly a tuple.

    Construct
    ---
    You can use a `Iterable[int]` or a `Fraction` to construct
    a ContinuedFraction object
    >>> ContinuedFraction([1, 1, 1, 1])
    >>> ContinuedFraction(Fraction(355, 113))

    rather than transfer a float to Fraction, use `from_float`
    >>> ContinuedFraction.from_float(2.718281828)

    Moreover, you can set the len_limit and coefficient_limit.
    '''
    __slots__ = ('_coefficients',)

    def __init__(self, coefficients: Fraction | Iterable[int],
                 *, copy_tuple: bool = True) -> None:
        if isinstance(coefficients, Fraction):
            coefficients = _frac2cfrac(coefficients)
        elif not copy_tuple and isinstance(coefficients, tuple):
            self._coefficients = coefficients
            return
        self._coefficients = tuple(coefficients)

    @property
    def coefficients(self): return self._coefficients

    @classmethod
    def from_float(cls, number: float, *, len_limit: int = 10,
                   coefficient_limit: int = 1000000):
        '''due to flaot precision, coefficients[10:] may have error.'''
        coefficients = _float2cfrac(number, len_limit, coefficient_limit)
        return cls(coefficients)

    def __repr__(self) -> str:
        return self.__class__.__name__ \
            + repr(self.coefficients).replace(',', ';', 1)

    def __str__(self) -> str:
        return ' + 1/'.join(map(str, self.coefficients))

    def __len__(self) -> int: return len(self.coefficients)

    def __iter__(self) -> Iterator[int]: return iter(self.coefficients)

    def __hash__(self) -> int: return hash(self.coefficients)

    def __getitem__(self, i: SupportsIndex): return self.coefficients[i]

    def __eq__(self, other) -> bool:
        if isinstance(other, ContinuedFraction):
            return self.coefficients == other.coefficients
        raise TypeError(f"comparing ContinuedFraction with {type(other)}.")

    def __int__(self) -> int: return self.coefficients[0]

    def truncate(self, end_index: SupportsIndex):
        return ContinuedFraction(self.coefficients[:end_index], copy_tuple=False)

    def to_fraction(self) -> Fraction:
        p, q = 0, 1
        for coef in reversed(self.coefficients):
            p, q = q, coef * q + p
        return Fraction(q, p)  # reverse again at last

    def reciprocal(self):
        '''get 1/fraction.'''
        coef = self.coefficients[1:] if self.coefficients[0] == 0 \
            else (0,) + self.coefficients
        return ContinuedFraction(coef, copy_tuple=False)

    def represent(self, width: int = -1) -> None:
        '''print

        a0 + _________1__________
             a1 + _______1_______
                  a2 + ____1_____
                       ... + 1/an
        '''
        if len(self.coefficients) <= 1:
            return print(self.coefficients[0])
        coefs = [str(c) + ' + ' for c in self.coefficients[:-1]]
        coefs[-1] += '1/' + str(self.coefficients[-1])
        clens = list(accumulate(map(len, coefs)))
        width = max(width, clens[-1])
        for coef, clen in zip(coefs, clens):
            line = f'{1:_^{clens[-1] - clen}}'
            print((coef + line if len(line) > 1 else coef).rjust(width))
