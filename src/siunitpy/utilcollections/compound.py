from fractions import Fraction
from itertools import chain
from typing import Generator, Generic, Iterable, Iterator, TypeVar

from .utils import Number, _inplace
from .utils import common_rational as frac

__all__ = ['Compound']

K = TypeVar('K')
_ZERO = Fraction(0)


class Compound(Generic[K]):
    __slots__ = ('_elements',)

    def __init__(self, elements: dict[K, Fraction] |
                 Generator[tuple[K, Number], None, None] = {}, /, *,
                 copy=True):
        if not copy and isinstance(elements, dict):
            self._elements = elements
        elif isinstance(elements, dict):
            self._elements = {k: frac(v) for k, v in elements.items() if v}
        elif isinstance(elements, Iterable):
            self._elements = {k: frac(v) for k, v in elements if v}
        else:
            raise TypeError(f"{type(elements) = } is not 'Iterable'.")

    def __contains__(self, key: K) -> bool: return key in self._elements

    def __getitem__(self, key: K) -> Fraction:
        return self._elements.get(key, _ZERO)

    def __setitem__(self, key: K, value: Fraction) -> None:
        if value == 0:
            self._elements.pop(key, _ZERO)
        else:
            self._elements[key] = value

    def __delitem__(self, key: K) -> None: del self._elements[key]

    def __iter__(self) -> Iterator[K]: return iter(self._elements)

    def __repr__(self) -> str:
        mid = ', '.join(f'{repr(k)}: {v}' for k, v in self._elements.items())
        return '{' + mid + '}'  # f'{{{mid}}}' is confusing

    def __str__(self) -> str:
        mid = ', '.join(f'{k}: {v}' for k, v in self._elements.items())
        return '{' + mid + '}'

    def __len__(self) -> int: return len(self._elements)

    def copy(self): return self.__class__(self._elements.copy(), copy=False)

    def keys(self): return self._elements.keys()

    def values(self): return self._elements.values()

    def items(self): return self._elements.items()

    def pos_items(self):
        '''filter items whose value > 0.'''
        return filter(lambda item: item[1] > 0, self._elements.items())

    def neg_items(self):
        '''filter items whose value < 0.'''
        return filter(lambda item: item[1] < 0, self._elements.items())

    def pop(self, key) -> Fraction: return self._elements.pop(key)

    def clear(self): self._elements.clear()

    def __eq__(self, other: 'Compound') -> bool:
        return self._elements == other._elements

    def __pos__(self):
        return self.__class__({k: +v for k, v in self.items()}, copy=False)

    def __neg__(self):
        return self.__class__({k: -v for k, v in self.items()}, copy=False)

    def __add__(self, other):
        return self.__class__((k, self[k] + other[k]) for k in chain(self, other))

    def __sub__(self, other):
        return self.__class__((k, self[k] - other[k]) for k in chain(self, other))

    def __mul__(self, other):
        if other == 0:
            return self.__class__()
        return self.__class__((k, v * other) for k, v in self.items())

    def __truediv__(self, other):
        return self.__class__((k, v / other) for k, v in self.items())

    __iadd__ = _inplace(__add__)
    __isub__ = _inplace(__sub__)
    __imul__ = _inplace(__mul__)
    __itruediv__ = _inplace(__truediv__)
    __rmul__ = __mul__
