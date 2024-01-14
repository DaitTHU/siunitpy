import operator
from itertools import chain
from typing import TypeVar, Generic, Iterator, Iterable, Callable
from fractions import Fraction

from .utils import _inplace

__all__ = ['Compound']

K = TypeVar('K')


def _unary(op: Callable[[Fraction], Fraction]):
    def __op(self):
        return Compound({key: op(val) for key, val in self.items()})
    return __op


def _vector_add(op: Callable[[Fraction, Fraction], Fraction]):
    def __op(self, other):
        dict_gen = ((key, op(self[key], other[key])) 
                    for key in chain(self, other))
        return Compound({key: val for key, val in dict_gen if val})
    return __op, _inplace(__op)


def _scalar_mul(op: Callable[[Fraction, Fraction | int], Fraction]):
    def __op(self, other):
        if other == 0:
            return Compound({})
        return Compound({key: op(val, other) 
                            for key, val in self.items()})
    return __op, _inplace(__op)


class Compound(Generic[K]):
    '''The class `Compound` is a `dict` whose keys are all the elements 
    that make up a whole, and whose values are the corresponding 
    contributions, which can of course be negative.

    Its function is similar to `defaultdict`. The keys have a default 
    value of 0. Moreover, when the value of the key in the `Compound` is 0, 
    it will be automatically deleted, because elements with a contribution 
    of 0 should not be taken into account.
    '''
    __slots__ = ('_elements',)

    def __init__(self, elements: dict[K, Fraction]):
        '''elements should be a rvalue and guarantee no zero value.'''
        self._elements = elements

    def __contains__(self, key: K) -> bool: return key in self._elements

    def __getitem__(self, key: K) -> Fraction:
        return self._elements[key] if key in self._elements else Fraction(0)

    def __setitem__(self, key: K, value: Fraction) -> None:
        if value == 0:
            if key in self._elements:
                del self._elements[key]
        else:
            self._elements[key] = value

    def __delitem__(self, key: K) -> None: del self._elements[key]

    def __iter__(self) -> Iterator[K]: return iter(self._elements)

    def __str__(self) -> str: return str(self._elements)

    def __len__(self) -> int: return len(self._elements)

    def copy(self): return Compound(self._elements.copy())

    def keys(self): return self._elements.keys()

    def values(self): return self._elements.values()

    def items(self): return self._elements.items()

    def pop(self, key) -> Fraction: return self._elements.pop(key)

    def __eq__(self, other) -> bool:
        return self._elements == other._elements

    __pos__ = _unary(operator.pos)  # like copy()
    __neg__ = _unary(operator.neg)

    __add__, __iadd__ = _vector_add(operator.add)
    __sub__, __isub__ = _vector_add(operator.sub)

    __mul__, __imul__ = _scalar_mul(operator.mul)
    __rmul__ = __mul__
    __truediv__, __itruediv__ = _scalar_mul(operator.truediv)
    #__floordiv__, __ifloordiv__ = _scalar_mul(operator.floordiv)
