import sys
from fractions import Fraction
from typing import Iterable, Iterator, Literal, SupportsIndex

__all__ = ['Dimension']

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing import TypeVar
    Self = TypeVar('Self', bound='Dimension')


class Dimension:
    '''`Dimension` is like a 7-len `namedtuple`, the field is
    - `T`: time
    - `L`: length
    - `M`: mass
    - `I`: electric current
    - `H`: thermodynamic temperature (ASCII substitute for Greek letter `Θ`)
    - `N`: amount of substance
    - `J`: luminous intensity

    It's a kind of immutable sequence.

    Get base quantity
    ---
    You can get base quantity property like mass by index, initial 
    or fullname.
    >>> force_dim[0]    # 1
    >>> force_dim.M     # 1
    >>> force_dim.time  # -2

    Operation
    ---
    very straight-forward:
    >>> force_dim.inverse()                     # T⁻²LM
    >>> power_dim = force_dim * vilocity_dim    # T⁻³L²M
    >>> vilocity_dim**2                         # T⁻²L²
    '''

    def __init__(self, T=0, L=0, M=0, I=0, H=0, N=0, J=0) -> None:
        '''construct a `Dimension` object using 7 int/Fraction arguments, 
        default 0.
        >>> time_dim = Dimension(T=1)
        >>> vilocity_dim = Dimension(-1, 1)

        You can also use classmethod `Dimension.unpack` to construct a 
        `Dimension` object from a iterable:
        >>> force_dim = Dimension.unpack([-2, 1, 1])
        '''

    @classmethod
    def unpack(cls, iterable: Iterable[int] |
               dict[Literal['T', 'L', 'M', 'I', 'H', 'N', 'J'], int], /) -> Self: ...

    def astuple(self) -> tuple[Fraction]: ...
    def __getitem__(self, key: SupportsIndex |
                    Literal['T', 'L', 'M', 'I', 'H', 'N', 'J']) -> Fraction: ...

    def __iter__(self) -> Iterator[Fraction]: ...
    @property
    def T(self) -> Fraction: '''time'''
    @property
    def L(self) -> Fraction: '''length'''
    @property
    def M(self) -> Fraction: '''mass'''
    @property
    def I(self) -> Fraction: '''electric current'''
    @property
    def H(self) -> Fraction: '''thermodynamic temperature'''
    @property
    def N(self) -> Fraction: '''amount of substance'''
    @property
    def J(self) -> Fraction: '''luminous intensity'''
    @property
    def time(self) -> Fraction: ...
    @property
    def length(self) -> Fraction: ...
    @property
    def mass(self) -> Fraction: ...
    @property
    def electric_current(self) -> Fraction: ...
    @property
    def thermodynamic_temperature(self) -> Fraction: ...
    @property
    def amount_of_substance(self) -> Fraction: ...
    @property
    def luminous_intensity(self) -> Fraction: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __len__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: Dimension) -> bool: ...
    def isdimensionless(self) -> bool: ...
    def iscomposedof(self, composition: str) -> bool: ...
    def isgeometric(self) -> bool: ...
    def iskinematic(self) -> bool: ...
    def isdynamic(self) -> bool: ...
    def inverse(self) -> Self: ...
    def __mul__(self, other: Dimension) -> Self: ...
    def __truediv__(self, other: Dimension) -> Self: ...
    def __imul__(self, other: Dimension) -> Self: ...
    def __itruediv__(self, other: Dimension) -> Self: ...
    def __rtruediv__(self, one: Literal[1]) -> Self: ...
    def __pow__(self, n: int | float | Fraction) -> Self: ...
    def __ipow__(self, n: int | float | Fraction) -> Self: ...
    def nthroot(self, n: int | float | Fraction) -> Self: ...
    @staticmethod
    def product(dim_iter: Iterable[Dimension]) -> Dimension: ...
