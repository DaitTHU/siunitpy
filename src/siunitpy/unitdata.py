from .dimension import Dimension
from .utilcollections.constclass import ConstClass


class UnitSystem(ConstClass):
    SI: str
    CGS: str
    NATURAL: str


class SymbolData:
    '''Immutable, used in dict, where the key is the symbol (of a prefix/unit), 
    and the value is the data of the symbol, containing fullname and value.
    '''
    __slots__ = ('_fullname', '_value', )

    def __init__(self, fullname: str, value: float) -> None:
        self._fullname = fullname
        self._value = value

    @property
    def fullname(self): return self._fullname
    @property
    def value(self): return self._value

    def __hash__(self) -> int: return hash((self.fullname, self.value))

    def __eq__(self, other) -> bool:
        return isinstance(other, SymbolData) and \
            self.fullname == other.fullname and self.value == other.value


class PrefixData(SymbolData):
    '''subclass of `SymbolData`, used for prefix, 
    whose value can also be called factor.
    '''
    __slots__ = ()
    @property
    def factor(self): return self._value


class BaseData(SymbolData):
    '''subclass of `SymbolData`, used for unit.

    Some unique unit should never be prefixed, as reflected in `never_prefix`.
    '''
    __slots__ = ('_never_prefix',)

    def __init__(self, fullname: str, value: float, *, never_prefix=False):
        super().__init__(fullname, value)
        self._never_prefix = never_prefix

    @property
    def never_prefix(self): return self._never_prefix


class UnitData(BaseData):
    '''subclass of `BaseData`, also used for unit. 
    Adds dimension property.
    '''
    __slots__ = ('_dimension',)

    def __init__(self, dimension: Dimension, base_data: BaseData) -> None:
        self._dimension = dimension
        super().__init__(base_data.fullname, base_data.value,
                         never_prefix=base_data.never_prefix)

    @property
    def dimension(self): return self._dimension
