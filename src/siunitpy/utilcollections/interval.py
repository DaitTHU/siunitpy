from typing import Generic, TypeVar

from .abc.ordinal import Cardinal

__all__ = ['Interval']

T = TypeVar('T', bound=Cardinal)


class Interval(Generic[T]):
    __slots__ = ('_lo', '_hi')

    def __init__(self, lo: T, hi: T, /) -> None:
        if lo > hi:
            raise ValueError("lo must be less than or equal to hi.")
        self._lo, self._hi = lo, hi

    @classmethod
    def neighborhood(cls, center: T, radius: T):
        return cls(center - radius, center + radius)

    @property
    def lo(self) -> T: return self._lo
    @property
    def hi(self) -> T: return self._hi
    @property
    def mid(self) -> T: return (self.lo + self.hi) / 2
    @property
    def length(self) -> T: return self.hi - self.lo

    def cover(self, other: 'Interval') -> bool:
        return self.lo <= other.lo and other.hi <= self.hi

    def disjoint(self, other: 'Interval') -> bool:
        return self.hi < other.lo or other.hi < self.lo

    def intersect(self, other: 'Interval') -> bool:
        return not self.disjoint(other)

    def __contains__(self, number: T) -> bool:
        return self.lo <= number and number <= self.hi

    def lohalf(self) -> 'Interval':
        return Interval(self.lo, self.mid)

    def hihalf(self) -> 'Interval':
        return Interval(self.mid, self.hi)

    def __eq__(self, other: 'Interval') -> bool:
        return self.lo == other.lo and self.hi == other.hi
    
    def __hash__(self) -> int: return hash((self.lo, self.hi))
