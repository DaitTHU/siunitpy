from typing import Optional, overload

from .unit_archive import (_PREFIX_DATA, _PREFIX_FULLNAME, _UNIT_DATA,
                           _UNIT_FULLNAME)

_PREFIX_ALIAS = {'u': 'µ'}
_PREFIX_MAXLEN = max(map(len, _PREFIX_DATA))
_PREFIX_FULLNAME_MINLEN = min(len(p) for p in _PREFIX_FULLNAME if p)
_PREFIX_FULLNAME_MAXLEN = max(map(len, _PREFIX_FULLNAME))


def _resolve_element(unit: str) -> tuple[str, str]:
    '''resolve a unexponented element unit str.'''
    if unit in _UNIT_DATA:
        return unit, ''
    for prefix_len in range(1, _PREFIX_MAXLEN):
        prefix, base = unit[:prefix_len], unit[prefix_len:]
        if prefix in _PREFIX_ALIAS:
            prefix = _PREFIX_ALIAS[prefix]
        if prefix in _PREFIX_DATA and base in _UNIT_DATA:
            if _UNIT_DATA[base].never_prefix:
                continue
            return base, prefix
    # fullname case
    if unit in _UNIT_FULLNAME:
        return _UNIT_FULLNAME[unit], ''
    for prefix_len in range(_PREFIX_FULLNAME_MINLEN, _PREFIX_FULLNAME_MAXLEN):
        prefix, base = unit[:prefix_len], unit[prefix_len:]
        if prefix in _PREFIX_FULLNAME and base in _UNIT_FULLNAME:
            if _UNIT_DATA[_UNIT_FULLNAME[base]].never_prefix:
                continue
            return _UNIT_FULLNAME[base], _PREFIX_FULLNAME[prefix]
    raise UnitSymbolError(f"'{unit}' is not a valid element unit.")


class UnitElement:
    '''UnitElement is the minimum part of the unit, i.e. the elements of unit. 
    The combination of unit-elements forms units. 

    UnitElement has the unit-base and prefix, which are both 'str'.
    '''
    __slots__ = ('_base', '_prefix')

    @overload
    def __init__(self, unit: str) -> None: ...
    @overload
    def __init__(self, base: str, prefix: str) -> None: ...

    def __init__(self, unit: str, prefix: Optional[str] = None):  # type: ignore
        if isinstance(prefix, str):
            self._base, self._prefix = unit, prefix
        else:
            self._base, self._prefix = _resolve_element(unit)

    @property
    def base(self) -> str: return self._base
    @property
    def prefix(self) -> str: return self._prefix
    @property
    def symbol(self) -> str: return self.prefix + self.base

    @property
    def fullname(self) -> str:
        return _PREFIX_DATA[self.prefix].fullname + _UNIT_DATA[self.base].fullname

    @property
    def value(self) -> float:
        return _PREFIX_DATA[self.prefix].factor * _UNIT_DATA[self.base].value

    @property
    def dimension(self): return _UNIT_DATA[self.base].dimension

    def deprefix(self): return UnitElement(self.base, '')

    def __str__(self) -> str: return self.symbol

    def __repr__(self) -> str: 
        return '{}({}-{})'.format(self.prefix, self.base)
    
    def __hash__(self) -> int: return hash((self.prefix, self.base))

    def __eq__(self, other: 'UnitElement') -> bool:
        return self.symbol == other.symbol
    
    def __le__(self, other: 'UnitElement'):
        # TODO: the order of unit-element
        pass


class UnitSymbolError(ValueError):
    pass
