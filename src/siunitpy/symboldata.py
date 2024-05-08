from .dimension import Dimension
from .dimensionconst import DimensionConst
from .utilcollections.constclass import ConstClass

__all__ = ['SymbolData', 'PrefixData', 'BaseData']


class UnitSystem(ConstClass):
    SI: str
    CGS: str
    NATURAL: str


class SymbolData:
    '''Immutable, used in dict, where the key is the symbol (of a prefix/unit), 
    and the value is the data of the symbol, containing fullname and value.
    '''
    __slots__ = ('_fullname', '_factor', )

    def __init__(self, fullname: str, factor: float) -> None:
        self._fullname = fullname
        self._factor = factor

    @property
    def fullname(self): return self._fullname
    @property
    def factor(self): return self._factor

    def __hash__(self) -> int: return hash((self.fullname, self.factor))

    def __eq__(self, other) -> bool:
        return isinstance(other, SymbolData) and \
            self.fullname == other.fullname and self.factor == other.factor


class PrefixData(SymbolData):
    '''subclass of `SymbolData`, used for prefix.
    '''
    __slots__ = ()


class BaseData(SymbolData):
    '''subclass of `SymbolData`, used for unit-base (i.e. without prefix).

    Some unique unit should never be prefixed, as reflected in `never_prefix`.
    '''
    __slots__ = ('_dimension', '_never_prefix')

    def __init__(self, fullname: str, value: float,
                 dimension: Dimension = DimensionConst.DIMENSIONLESS, *,
                 never_prefix=False):
        super().__init__(fullname, value)
        self._dimension = dimension
        self._never_prefix = never_prefix

    @property
    def never_prefix(self): return self._never_prefix
    @property
    def dimension(self): return self._dimension
    @dimension.setter
    def dimension(self, dim): self._dimension = dim
