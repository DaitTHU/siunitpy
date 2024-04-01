'''Identity
---
this module introduces additive identity (0) and multiplicative identity (1).

There are multiple ways to represent 0 (or 1), like `0`, `0.0`, `np.array([0])`.
However, as zeros, they have many properties in common, 
like 0 + a = a, 0 * a = 0... 
Therefore it's useful to unify them into the same object,
which is especially useful when you set 0 (or 1) as the default value
for complicated type situations, rather than None.

There should be and only one singleton representing zero and one.
'''

__all__ = ['Zero', 'zero', 'One', 'one']


class Zero:
    '''acting as something like 0.'''
    __slots__ = ()
    def __str__(self): return '0'
    def __abs__(self): return self
    def __pos__(self): return self
    def __neg__(self): return self
    def __add__(self, other): return other
    def __radd__(self, other): return other
    def __sub__(self, other): return -other
    def __rsub__(self, other): return other
    def __mul__(self, other): return self
    def __rmul__(self, other): return self
    def __truediv__(self, other): return self
    def __rtruediv__(self, other): raise ZeroDivisionError
    def __floordiv__(self, other): return self
    def __rfloordiv__(self, other): raise ZeroDivisionError
    # TODO: 0**0 = 1
    def __pow__(self, other): return self
    def __rpow__(self, other): return one


class One:
    '''acting as something like 1.'''
    __slots__ = ()
    def __str__(self): return '1'
    def __abs__(self): return self
    def __pos__(self): return self
    def __mul__(self, other): return other
    def __rmul__(self, other): return other
    def __rtruediv__(self, other): return other
    def __rfloordiv__(self, other): return other
    def __pow__(self, other): return self
    def __rpow__(self, other): return other


# singleton
zero = Zero()
one = One()
