'''The `Compound` class extends the functionality of a standard `dict` 
by specializing it for the representation of compounds. 

Each key represents an element that constitutes the compound, and the 
corresponding value denotes the element's contribution, which may be 
positive, negative, or zero, but the class is optimized to automatically 
remove any elements with a zero contribution, as they are not relevant 
to the compound's composition.

In terms of behavior, `Compound` shares similarities with the `defaultdict` 
class. For any key that is not explicitly present in the compound, the 
class assumes a default value of 0. This defaulting mechanism simplifies 
the handling of missing elements.

A distinctive feature of `Compound` is its automated management of keys with 
zero values. When the contribution of an element reaches zero, the class 
removes that key entirely from the compound. This design decision reflects 
the understanding that elements with no contribution should not be 
considered as part of the compound, thus ensuring that the representation 
remains concise and meaningful.
'''

import sys
from fractions import Fraction
from typing import Any, Generic, Iterable, Iterator, TypeVar, overload

from .utils import Number

K = TypeVar('K')

if sys.version_info >= (3, 11):
    from typing import Self
else:
    Self = TypeVar('Self', bound=ElementWiseList[Any])


class Compound(Generic[K]):
    '''`Compound` is similar to `defaultdict` with zero as the default value.

    constructor
    ---
    You can construct a `Compound` object using `dict` or pair `Iterable`:
    >>> Compound({'a': 0, 'b': 1, 'c': 2})
    {'b': 1, 'c': 2} 
    >>> Compound(zip('abc', range(3)))
    {'b': 1, 'c': 2} 

    get/set items
    ---
    getting a missing item will return zero, and 
    setting a item zero will automatically remove it.
    >>> compound['b'] = 0  # 'b' is removed

    operation
    ---
    add/sub between `Compound` objects
    >>> {'b': 1, 'c': 2} + {'c': -1/2, 'd': 3}
    {'b': 1, 'c': 3/2, 'd': 3}
    
    mul/div between `Compound` object and number:
    >>> {'b': 1, 'c': 2} / 2
    {'b': 1/2, 'c': 1}
    '''
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, iterable: Iterable[tuple[K, Number]], /) -> None: ...
    @overload
    def __init__(self, elements: dict[K, Number], /, *, copy=True) -> None: ...
    def __contains__(self, key: K) -> bool: ...
    def __getitem__(self, key: K) -> Fraction: ...
    def __setitem__(self, key: K, value: Fraction) -> None: ...
    def __delitem__(self, key: K) -> None: ...
    def __iter__(self) -> Iterator[K]: ...
    def __str__(self) -> str: ...
    def __len__(self) -> int: ...
    def copy(self) -> Self: ...
    def keys(self) -> Iterable[K]: ...
    def values(self) -> Iterable[Fraction]: ...
    def items(self) -> Iterable[tuple[K, Fraction]]: ...
    def pos_items(self) -> filter[tuple[K, Fraction]]: ...
    def neg_items(self) -> filter[tuple[K, Fraction]]: ...
    def pop(self, key: K) -> Fraction: ...
    def clear(self) -> None: ...
    def __eq__(self, other: Compound[Any]) -> bool: ...
    def __pos__(self) -> Self: ...
    def __neg__(self) -> Self: ...
    def __add__(self, other: Compound[K]) -> Self: ...
    def __sub__(self, other: Compound[K]) -> Self: ...
    def __mul__(self, other: int | Fraction) -> Self: ...
    def __truediv__(self, other: int | Fraction) -> Self: ...
    def __iadd__(self, other: Compound[K]) -> Self: ...
    def __isub__(self, other: Compound[K]) -> Self: ...
    def __imul__(self, other: int | Fraction) -> Self: ...
    def __itruediv__(self, other: int | Fraction) -> Self: ...
    def __rmul__(self, other: int | Fraction) -> Self: ...
