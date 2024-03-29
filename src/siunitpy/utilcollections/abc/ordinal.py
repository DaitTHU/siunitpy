from typing import Protocol, TypeVar, runtime_checkable

__all__ = ['Ordinal', 'Cardinal']

T_co = TypeVar('T_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)


@runtime_checkable
class Ordinal(Protocol[T_co, T_contra]):
    __slots__ = ()
    def __lt__(self, other: T_contra) -> bool: ...
    def __eq__(self, other: T_contra) -> bool: ...
    def __le__(self, other: T_contra) -> bool: ...


@runtime_checkable
class Cardinal(Protocol[T_co, T_contra]):
    __slots__ = ()
    def __lt__(self, other: T_contra) -> bool: ...
    def __eq__(self, other: T_contra) -> bool: ...
    def __le__(self, other: T_contra) -> bool: ...
    def __add__(self, other: T_contra) -> T_co: ...
    def __sub__(self, other: T_contra) -> T_co: ...
