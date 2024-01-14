# TODO: optimize __setitem__ and __delitem_

#from __future__ import annotations

import operator
from typing import Callable, Iterable, Sequence, TypeVar

__all__ = ['Vector', 'VectorMatchError']

T = TypeVar('T')


def _unary(op: Callable):
    '''unary operation: +v, -v, not v, ~v...'''

    def __op(self): return Vector(op(x) for x in self)
    return __op


def _comparison(op: Callable):
    def __op(self, other):
        if Vector.match_length(self, other):
            return Vector(op(x, y) for x, y in zip(self, other))
        else:
            return Vector(op(x, other) for x in self)
    return __op


def _binary(op: Callable):
    '''binary operation: all are elementwise
    - comparison: v > u, v == 0... (return Vector, not bool)
    - other binary operation: v + u, 2 * v...
    '''

    def __op(self, other):
        if Vector.match_length(self, other):
            return Vector(op(x, y) for x, y in zip(self, other))
        else:
            return Vector(op(x, other) for x in self)

    def __iop(self, other):
        if Vector.match_length(self, other):
            for i in range(len(self)):
                self[i] = op(self[i], other[i])
        else:
            for i in range(len(self)):
                self[i] = op(self[i], other)
        return self

    def __rop(self, other):
        if Vector.match_length(self, other):
            return Vector(op(y, x) for x, y in zip(self, other))
        else:
            return Vector(op(other, x) for x in self)
        
    return __op, __iop, __rop


class Vector(list[T]):
    

    def __init__(self, iterable: Iterable[T] = (), /) -> None:
        '''Construct a `Vector`

        If no argument is given, the constructor creates a new empty Vector:
        >>> Vector()  # []

        The argument must be an iterable if specified:
        >>> Vector([0, 1, 2, 3])  # [0, 1, 2, 3] 
        >>> Vector(range(4))      # [0, 1, 2, 3]

        If you want to packup multiple non-iterable elements as a `Vector`, 
        use classmethod `Vector.packup(*args)`:
        >>> Vector.packup(0, 1, 2, 3)  # [0, 1, 2, 3]
        '''
        super().__init__(iterable)

    @classmethod
    def packup(cls, *args: T):
        return cls(args)

    def __getitem__(self, index):
        getter = super().__getitem__
        # get item
        if isinstance(index, int):
            return getter(index)
        # get sub-Vector
        if isinstance(index, slice):
            return Vector(getter(index))
        # not an index
        if not isinstance(index, Iterable):
            raise TypeError(f'Inappropriate index type: {type(index)}')
        # boolean indexing
        if all(isinstance(idx, bool) for idx in index):
            return Vector(getter(i) for i, idx in enumerate(index) if idx)
        # advanced indexing
        return Vector(getter(idx) for idx in index)

    def __setitem__(self, index, value):
        setter = super().__setitem__
        # set element
        if isinstance(index, int):
            return setter(index, value)
        # set sub-Vector
        if isinstance(index, slice):
            if isinstance(value, Iterable):
                return setter(index, value)
            for idx in range(len(self))[index]:
                setter(idx, value)
            return
        # not an index
        if not isinstance(index, Iterable):
            raise TypeError(f'Inappropriate index type: {type(index)}')
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
        # delete item or sub-Vector
        if isinstance(index, (int, slice)):
            return killer(index)
        # not an index
        if not isinstance(index, Iterable):
            raise TypeError(f'Inappropriate index type: {type(index)}')
        # boolean indexing
        if all(isinstance(idx, bool) for idx in index):
            for i, idx in enumerate(index):
                if idx:
                    killer(i)
            return
        # advanced indexing
        for idx in index:
            killer(idx)

    @classmethod
    def cat(cls, left: Iterable, /, *rights):
        '''concatenat Vectors, same as `sum(list)`'''
        result = list(left)
        for right in rights:
            result.extend(right)
        return cls(result)

    def repeat(self, repeat_time: int, /):
        return Vector(super().__mul__(repeat_time))

    def irepeat(self, repeat_time: int, /):
        '''inplacement repeat, same as `list` `*=`'''
        self = super().__imul__(repeat_time)
        return self

    def erepeat(self, repeat_time: int, /):
        '''element repeat, 
        >>> Vector(range(2)).erepeat(3)
        [0, 0, 0, 1, 1, 1]
        '''
        return Vector(item for self_clone in zip(*([self] * repeat_time))
                      for item in self_clone)

    @staticmethod
    def zeros(length: int, /): return Vector([0]).irepeat(length)

    @staticmethod
    def ones(length: int, /): return Vector([1]).irepeat(length)

    def copy(self): return Vector(self)

    __pos__ = _unary(operator.pos)
    __neg__ = _unary(operator.neg)
    __not__ = _unary(operator.not_)
    __invert__ = _unary(operator.invert)
    __abs__ = _unary(operator.abs)

    @staticmethod
    def set_match_check(*, enable: bool) -> None:
        '''If enabled, the match check mode will automatically check 
        whether the two lengths are matched whenever the `Vector` are 
        operated with the `Sequence`, and will raise `VectorMatchError`
        if the lengths do not match.

        If disabled, the check process will be omitted, but it may be
        dangerous.
        '''
        VectorMatch._match_check = enable

    @staticmethod
    def match_length(left, right) -> bool:
        '''see staticmethod Vector.set_match_check.'''
        if not isinstance(right, Sequence):
            return False
        if VectorMatch._match_check and len(left) != len(right):
            raise VectorMatchError(
                f'Length ({len(left)}, {len(right)}) do not match.')
        return True

    # comparison
    __eq__ = _comparison(operator.eq)
    __ne__ = _comparison(operator.ne)
    __gt__ = _comparison(operator.gt)
    __lt__ = _comparison(operator.lt)
    __ge__ = _comparison(operator.ge)
    __le__ = _comparison(operator.le)
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

    @staticmethod
    def equal(left, right) -> bool:
        '''since `v == u` returns a `Vector`, the `Vector.equal(v, u)` assumes 
        the function of determining whether `v`, `u` are equal or not.

        similarly, we got `Vector.gt`, `Vector.lt`, `Vector.ge`, `Vector.le`.
        '''
        return list.__eq__(left, right)

    gt, lt, ge, le = (staticmethod(op) for op in
                      (list.__gt__, list.__lt__, list.__ge__, list.__le__))


class VectorMatch:
    _match_check = True


class VectorMatchError(Exception):
    pass



