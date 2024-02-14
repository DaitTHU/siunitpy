from .dimension import Dimension
from .utilcollections.constclass import ConstClass


class UnitSystem(ConstClass):
    SI: str
    CGS: str
    NATURAL: str


class SymbolData:
    '''used as dict-value, can be represent a unit or prefix. Immutable.'''
    __slots__ = ('_fullname', '_value', )

    def __init__(self, fullname: str, value: float) -> None:
        self._fullname = fullname
        self._value = value

    @property
    def fullname(self): return self._fullname
    @property
    def value(self): return self._value


class PrefixData(SymbolData):
    __slots__ = ()
    @property
    def factor(self): return self._value


class BaseData(SymbolData):
    __slots__ = ('_never_prefix',)

    def __init__(self, fullname: str, value: float, *, never_prefix=False):
        super().__init__(fullname, value)
        self._never_prefix = never_prefix

    @property
    def never_prefix(self): return self._never_prefix


class UnitData:
    '''a unit symbol (str) moreover need dimension. Immutable.'''
    __slots__ = ('_dimension', '_base_data')

    def __init__(self, dimension: Dimension, base_data: BaseData) -> None:
        self._dimension = dimension
        self._base_data = base_data

    @property
    def dimension(self): return self._dimension
    @property
    def fullname(self): return self._base_data.fullname
    @property
    def value(self): return self._base_data.value
    @property
    def never_prefix(self): return self._base_data.never_prefix
