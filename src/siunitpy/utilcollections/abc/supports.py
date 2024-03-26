from typing import Protocol, TypeVar, runtime_checkable

__all__ = ['SupportsNeg']

T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)


@runtime_checkable
class SupportsNeg(Protocol[T_co]):
    def __neg__(self) -> T_co: ...


if __name__ == '__main__':
    assert issubclass(int, SupportsNeg)
