from fractions import Fraction
from typing import Iterable, Iterator, SupportsIndex, overload

__all__ = ['ContinuedFraction']


class ContinuedFraction:
    @overload
    def __init__(self, fraction: Fraction) -> None: ...

    @overload
    def __init__(self, coefficients: Iterable[int],  
                 *, _move_tuple: bool = False) -> None: ...

    @classmethod
    def from_float(cls, number: float, *, len_limit: int = 10,
                   coefficient_limit: int = 1000000) -> ContinuedFraction: ...

    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[int]: ...
    def __hash__(self) -> int: ...
    def __getitem__(self, i: SupportsIndex) -> int: ...
    def __eq__(self, other: ContinuedFraction) -> bool: ...
    def __int__(self) -> int: ...
    def truncate(self, end_index: SupportsIndex) -> ContinuedFraction: ...
    def to_fraction(self) -> Fraction: ...
    def reciprocal(self) -> ContinuedFraction: ...
    def represente(self, width: int | None = None) -> None: ...
