from .dimension import Dimension


class SymbolData:
    '''used as dict-value, can be represent a unit or prefix.'''
    __slots__ = ('_fullname', '_factor')

    def __init__(self, fullname: str, factor: float) -> None:
        self._fullname = fullname
        self._factor = factor

    @property
    def fullname(self): return self._fullname
    @property
    def factor(self): return self._factor


class UnitData:
    '''a unit symbol (str) moreover need dimension.'''
    __slots__ = ('_dimension', '_fullname', '_factor')

    def __init__(self, dimension: Dimension, symbol_data: SymbolData) -> None:
        self._dimension = dimension
        self._fullname = symbol_data.fullname
        self._factor = symbol_data.factor

    @property
    def dimension(self): return self._dimension
    @property
    def fullname(self): return self._fullname
    @property
    def factor(self): return self._factor
