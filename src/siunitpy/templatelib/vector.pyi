from typing import Iterable, Sequence, SupportsIndex, TypeVar, overload

T, S = TypeVar('T'), TypeVar('S')


class Vector(list[T]):
    '''Vector inherits most of the function of Python built-in `list`, 
    but makes its operator overloading more **elementwise**. It acts
    like 1-D array in numpy.

    Constructor
    ---
    You can construct a `Vector` object using iterable like `list`:
    >>> Vector()                    # [], new empty Vector
    >>> Vector([0, 1, 2, 3])        # [0, 1, 2, 3]
    >>> Vector(range(4))            # [0, 1, 2, 3]

    You can also use classmethod `Vector.packup(*args)` 
    to write one less parenthesis.
    >>> Vector.packup(0, 1, 2, 3)   # [0, 1, 2, 3]

    Get items or sub-Vector
    ---
    You can get an item or sub-Vector from a `Vector` exactly like `list`:
    >>> v = Vector(range(4))    # [0, 1, 2, 3]
    >>> v[3]                    # 3
    >>> v[-1]                   # 3
    >>> v[:2]                   # [0, 1]

    Moreover, you can use advanced indexing and boolean indexing like numpy:
    >>> v[0, -1, 2]             # [0, 3, 2]
    >>> v[True, False, True]    # [0, 2]

    Set items
    ---
    >>> u = v.copy()
    >>> u[:2] = range(1, 3)     # [1, 2, 2, 3]
    >>> u[u > 1] = 0            # [1, 0, 0, 0]

    Operation
    ---
    The operator is elementwise, meaning it acts on each element:
    >>> -v          # [0, -1, -2, -3]
    >>> u = v + 1   # [1, 2, 3, 4], like boardcast in numpy
    >>> u * v       # [0, 2, 6, 12]

    Meanwhile, `list` operator `+`, `+=`, `*`, `*=` and comparison 
    (like `==`, `>`) are overloaded. As replacement, see WARNING.

    WARNING
    ---
    This inheritance violates *the Liskov Substitution principle*. 
    If you want to replace `list` with `Vector`, you should make 5 
    types of adjustments:
    >>> a.extend(b)                 # list extend:  a += b
    >>> Vector.cat(a, b, ..., z)    # list concatenat: a + b + ... + z
    >>> a.repeat(3)                 # list repeat: a * 3
    >>> a.irepeat(3)                # list inplace repeat: a *= 3
    >>> Vector.equal(a, b)          # list comparison: a == b

    Comparison: `Vector` staticmethod `equal`.
    '''
    
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, iterable: Iterable[T]) -> None: ...
    @classmethod
    def packup(cls, *args: T) -> Vector[T]: ...
    @overload
    def __getitem__(self, index: SupportsIndex) -> T: ...
    @overload
    def __getitem__(self, slice: slice) -> Vector[T]: ...
    @overload
    def __getitem__(self, bool_index: Iterable[bool]) -> Vector[T]: ...
    @overload
    def __getitem__(self, index_list: Iterable[SupportsIndex]) -> Vector[T]: ...
    @overload
    def __setitem__(self, index: SupportsIndex, value: T) -> None: ...
    @overload
    def __setitem__(self, key: slice | Iterable[bool] | Iterable[SupportsIndex], value: Vector[T]) -> None: ...
    def __delitem__(self, key: SupportsIndex | slice | Iterable[bool] | Iterable[SupportsIndex]) -> None: ...
    @classmethod
    def cat(cls, left: Iterable[T], /, *rights: tuple[Iterable[T]]) -> Vector[T]: ...
    def repeat(self, repeat_time: int, /) -> Vector[T]: ...
    def irepeat(self, repeat_time: int, /) -> Vector[T]: ...
    def erepeat(self, repeat_time: int, /) -> Vector[T]: ...
    @staticmethod
    def zeros(length: int, /) -> Vector[int]: ...
    @staticmethod
    def ones(length: int, /) -> Vector[int]: ...
    def copy(self) -> Vector[T]: ...
    # elementwise unary operation
    def __pos__(self) -> Vector[T]: ...
    def __neg__(self) -> Vector[T]: ...
    def __not__(self) -> Vector[T]: ...
    def __invert__(self) -> Vector[T]: ...
    def __abs__(self) -> Vector[T]: ...
    @staticmethod
    def set_match_check(*, enable: bool) -> None: ...
    @staticmethod
    def match_length(left: Sequence, right: Sequence) -> bool: ...
    # elementwise comparison operation
    def __eq__(self, other: T | Vector[T]) -> Vector[bool]: ...
    def __ne__(self, other: T | Vector[T]) -> Vector[bool]: ...
    def __gt__(self, other: T | Vector[T]) -> Vector[bool]: ...
    def __lt__(self, other: T | Vector[T]) -> Vector[bool]: ...
    def __ge__(self, other: T | Vector[T]) -> Vector[bool]: ...
    def __le__(self, other: T | Vector[T]) -> Vector[bool]: ...
    # vector comparison
    @staticmethod
    def equal(left, right: Vector[T]) -> bool: ...
    # @staticmethod
    # def ne(left, right: Vector[T]) -> bool: ...
    # @staticmethod
    # def gt(left, right: Vector[T]) -> bool: ...
    # @staticmethod
    # def lt(left, right: Vector[T]) -> bool: ...
    # @staticmethod
    # def ge(left, right: Vector[T]) -> bool: ...
    # @staticmethod
    # def le(left, right: Vector[T]) -> bool: ...
    # elementwise binary operation
    def __add__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __sub__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __mul__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __matmul__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __pow__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __floordiv__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __truediv__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __mod__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __and__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __or__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __xor__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __lshift__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __rshift__(self, other: T | Vector[T]) -> Vector[T]: ...
    # inplace
    def __iadd__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __isub__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __imul__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __imatmul__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __ipow__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __ifloordiv__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __itruediv__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __imod__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __iand__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __ior__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __ixor__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __ilshift__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __irshift__(self, other: T | Vector[T]) -> Vector[T]: ...
    # right
    def __radd__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __rsub__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __rmul__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __rmatmul__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __rpow__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __rfloordiv__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __rtruediv__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __rmod__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __rand__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __ror__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __rxor__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __rlshift__(self, other: T | Vector[T]) -> Vector[T]: ...
    def __rrshift__(self, other: T | Vector[T]) -> Vector[T]: ...
    





