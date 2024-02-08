import operator
from fractions import Fraction
from itertools import chain
from typing import Callable, Generic, Iterable, Iterator, TypeVar

from .utils import _inplace

__all__ = ['Compound']

K = TypeVar('K')
_ZERO = Fraction(0)


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
    that make up the whole compound, and whose values are the corresponding 
    contributions, which can be either postive or negative, but never zero.

    Its function is similar to `defaultdict`. 
    For keys not in the compound, the default values are 0. 

    Moreover, when the value of one key in the compound becomes 0, 
    the key will be automatically deleted. 
    Because elements with zero contribution should not be taken into account.
    '''
    __slots__ = ('_elements',)

    def __init__(self, elements: dict[K, Fraction], *, move_dict=False):
        '''elements should be a rvalue and guarantee no zero value.'''
        if not isinstance(elements, dict):
            raise TypeError('elements must be dict.')
        if move_dict:
            self._elements = elements
            return
        self._elements = {k: Fraction(v) for k, v in elements.items() if v}

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

    def __str__(self) -> str: return str(self._elements)

    def __len__(self) -> int: return len(self._elements)

    def copy(self): return Compound(self._elements.copy())

    def keys(self): return self._elements.keys()

    def values(self): return self._elements.values()

    def items(self): return self._elements.items()

    def pop(self, key) -> Fraction: return self._elements.pop(key)

    def clear(self): self._elements.clear()

    def __eq__(self, other: 'Compound') -> bool:
        return self._elements == other._elements

    __pos__ = _unary(operator.pos)  # like copy()
    __neg__ = _unary(operator.neg)

    __add__, __iadd__ = _vector_add(operator.add)
    __sub__, __isub__ = _vector_add(operator.sub)

    __mul__, __imul__ = _scalar_mul(operator.mul)
    __rmul__ = __mul__
    __truediv__, __itruediv__ = _scalar_mul(operator.truediv)
    # __floordiv__, __ifloordiv__ = _scalar_mul(operator.floordiv)
