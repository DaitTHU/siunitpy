# TODO: optimize __setitem__ and __delitem_

import operator
from typing import (Callable, Generator, Iterable, Sequence, SupportsIndex,
                    TypeVar)

__all__ = ['ElementWiseList']

T = TypeVar('T')


def _unary(op: Callable):
    '''4 unary operation: +v, -v, not v, ~v'''

    def __op(self): return ElementWiseList(op(x) for x in self)
    return __op


def _length_equal(left, right):
    try:
        return isinstance(right, Sequence) and len(left) == len(right)
    except TypeError:
        raise TypeError('object to operator must be sequence.')


def _comparison(op: Callable):
    def __op(self, other):
        if _length_equal(self, other):
            return ElementWiseList(op(x, y) for x, y in zip(self, other))
        else:
            return ElementWiseList(op(x, other) for x in self)
    return __op


def _binary(op: Callable):
    '''binary operation: all are elementwise
    - comparison: v > u, v == 0... (return ElementWiseList[bool], not bool)
    - other binary operation: v + u, 2 * v...
    '''

    def __op(self, other):
        if _length_equal(self, other):
            return ElementWiseList(op(x, y) for x, y in zip(self, other))
        else:
            return ElementWiseList(op(x, other) for x in self)

    def __iop(self, other):
        if _length_equal(self, other):
            for i in range(len(self)):
                self[i] = op(self[i], other[i])
        else:
            for i in range(len(self)):
                self[i] = op(self[i], other)
        return self

    def __rop(self, other):
        if len(self) == len(other):
            return ElementWiseList(op(y, x) for x, y in zip(self, other))
        else:
            return ElementWiseList(op(other, x) for x in self)

    return __op, __iop, __rop


class ElementWiseList(list[T]):

    def __init__(self, iterable: Iterable[T] = (), /) -> None:
        '''Construct a `ElementWiseList`

        If no argument is given, the constructor creates a new empty List:
        >>> ElementWiseList()  # []

        The argument must be an iterable if specified:
        >>> ElementWiseList([0, 1, 2, 3])  # [0, 1, 2, 3] 
        >>> ElementWiseList(range(4))      # [0, 1, 2, 3]

        If you want to packup multiple non-iterable elements, 
        use classmethod `cls.packup(*args)`:
        >>> ElementWiseList.packup(0, 1, 2, 3)  # [0, 1, 2, 3]
        '''
        super().__init__(iterable)

    @classmethod
    def packup(cls, *args: T): return cls(args)

    def __getitem__(self, index):
        cls = self.__class__
        getter = super().__getitem__
        # get item
        if isinstance(index, SupportsIndex):
            return getter(index)
        # get sub-sequence
        if isinstance(index, slice):
            return cls(getter(index))
        # not an index
        if not isinstance(index, Iterable):
            raise TypeError(f'Inappropriate index type: {type(index)}')
        # boolean indexing
        if all(isinstance(idx, bool) for idx in index):
            return cls(getter(i) for i, idx in enumerate(index) if idx)
        # advanced indexing
        return cls(getter(idx) for idx in index)

    def __setitem__(self, index, value):
        setter = super().__setitem__
        # set element
        if isinstance(index, SupportsIndex):
            return setter(index, value)
        # set sub-sequence
        if isinstance(index, slice):
            if isinstance(value, Iterable):
                return setter(index, value)
            for idx in range(len(self))[index]:
                setter(idx, value)
            return
        # not an index
        if not isinstance(index, Iterable):
            raise TypeError(f'Inappropriate index type: {type(index)}')
        elif isinstance(index, Generator):
            index = tuple(index)
        # boolean indexing
        if all(isinstance(idx, bool) for idx in index):
            if isinstance(value, Iterable):
                for i, (idx, val) in enumerate(zip(index, value)):
                    if idx:
                        setter(i, val)
            else:
                for i, idx in enumerate(index):
                    if idx:
                        setter(i, value)
            return
        # advanced indexing
        if isinstance(value, Iterable):
            for idx, val in zip(index, value):
                setter(idx, val)
        else:
            for idx in index:
                setter(idx, value)

    def __delitem__(self, index):
        killer = super().__delitem__
        # delete item or sub-sequence
        if isinstance(index, (SupportsIndex, slice)):
            return killer(index)
        # not an index
        if not isinstance(index, Iterable):
            raise TypeError(f'Inappropriate index type: {type(index)}')
        elif isinstance(index, Generator):
            index = tuple(index)
        # boolean indexing
        if all(isinstance(idx, bool) for idx in index):
            for i, idx in reversed(list(enumerate(index))):
                if idx:
                    killer(i)
            return
        # advanced indexing
        for idx in sorted(index, reverse=True):
            killer(idx)

    @classmethod
    def cat(cls, left: Iterable, /, *rights):
        '''concatenat Lists, same as `sum(list)`'''
        result = list(left)
        for right in rights:
            result.extend(right)
        return cls(result)

    def repeat(self, repeat_time: int, /):
        return ElementWiseList(super().__mul__(repeat_time))

    def irepeat(self, repeat_time: int, /):
        '''inplacement repeat, same as `list` `*=`'''
        self = super().__imul__(repeat_time)
        return self

    def erepeat(self, repeat_time: int, /):
        '''element repeat, 
        >>> ElementWiseList([0, 1]).erepeat(3)
        [0, 0, 0, 1, 1, 1]
        '''
        return self.__class__(item for self_clone in zip(*([self] * repeat_time))
                              for item in self_clone)

    @classmethod
    def zeros(cls, length: int, /): return cls([0]).irepeat(length)

    @classmethod
    def ones(cls, length: int, /): return cls([1]).irepeat(length)

    def copy(self): return self.__class__(self)

    __pos__ = _unary(operator.pos)
    __neg__ = _unary(operator.neg)
    __not__ = _unary(operator.not_)
    __invert__ = _unary(operator.invert)
    __abs__ = _unary(operator.abs)
    # comparison
    __eq__ = _comparison(operator.eq)  # type: ignore
    __ne__ = _comparison(operator.ne)  # type: ignore
    __gt__ = _comparison(operator.gt)  # type: ignore
    __lt__ = _comparison(operator.lt)  # type: ignore
    __ge__ = _comparison(operator.ge)  # type: ignore
    __le__ = _comparison(operator.le)  # type: ignore
    # operation
    __add__, __iadd__, __radd__ = _binary(operator.add)
    __sub__, __isub__, __rsub__ = _binary(operator.sub)
    __mul__, __imul__, __rmul__ = _binary(operator.mul)
    __matmul__, __imatmul__, __rmatmul__ = _binary(operator.matmul)
    __pow__, __ipow__, __rpow__ = _binary(operator.pow)
    __floordiv__, __ifloordiv__, __rfloordiv__ = _binary(operator.floordiv)
    __truediv__, __itruediv__, __rtruediv__ = _binary(operator.truediv)
    __mod__, __imod__, __rmod__ = _binary(operator.mod)
    # bit
    __and__, __iand__, __rand__ = _binary(operator.and_)
    __or__, __ior__, __ror__ = _binary(operator.or_)
    __xor__, __ixor__, __rxor__ = _binary(operator.xor)
    __lshift__, __ilshift__, __rlshift__ = _binary(operator.lshift)
    __rshift__, __irshift__, __rrshift__ = _binary(operator.rshift)
