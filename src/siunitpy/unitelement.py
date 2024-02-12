from typing import Optional, overload

from .unit_archive import _PREFIX, _PREFIX_FULLNAME, _UNIT, _UNIT_FULLNAME

_EMPTY_STR = ''
_PREFIX_ALIAS = {'u': 'µ'}
_PREFIX_MAXLEN = max(map(len, _PREFIX))
_PREFIX_FULLNAME_MINLEN = min(len(p) for p in _PREFIX_FULLNAME if p)
_PREFIX_FULLNAME_MAXLEN = max(map(len, _PREFIX_FULLNAME))
_UNIT_ALIAS = {}


def _resolve_single(unit: str) -> tuple[str, str]:
    '''resolve a single, unexponented unit str.'''
    if unit in _UNIT:
        return unit, _EMPTY_STR
    for prefix_len in range(1, _PREFIX_MAXLEN):
        prefix, basic = unit[:prefix_len], unit[prefix_len:]
        if prefix in _PREFIX_ALIAS:
            prefix = _PREFIX_ALIAS[prefix]
        if prefix in _PREFIX and basic in _UNIT:
            if _UNIT[basic].never_prefix:
                continue
            return basic, prefix
    # fullname case
    if unit in _UNIT_FULLNAME:
        return _UNIT_FULLNAME[unit], _EMPTY_STR
    for prefix_len in range(_PREFIX_FULLNAME_MINLEN, _PREFIX_FULLNAME_MAXLEN):
        prefix, basic = unit[:prefix_len], unit[prefix_len:]
        if prefix in _PREFIX_FULLNAME and basic in _UNIT_FULLNAME:
            if _UNIT[_UNIT_FULLNAME[basic]].never_prefix:
                continue
            return _UNIT_FULLNAME[basic], _PREFIX_FULLNAME[prefix]
    raise UnitSymbolError(f"'{unit}' is not a valid unit.")


class UnitElement:
    __slots__ = ('_base', '_prefix')

    @overload
    def __init__(self, unit: str) -> None: ...
    @overload
    def __init__(self, base: str, prefix: str) -> None: ...

    def __init__(self, unit: str, prefix: Optional[str] = None):  # type: ignore
        if isinstance(prefix, str):
            self._base, self._prefix = unit, prefix
        else:
            self._base, self._prefix = _resolve_single(unit)

    @property
    def base(self) -> str: return self._base
    @property
    def prefix(self) -> str: return self._prefix
    @property
    def symbol(self) -> str: return self.prefix + self.base

    @property
    def fullname(self) -> str:
        return _PREFIX[self.prefix].fullname + _UNIT[self.base].fullname

    @property
    def value(self) -> float:
        return _PREFIX[self.prefix].value * _UNIT[self.base].factor

    @property
    def dimension(self): return _UNIT[self.base].dimension

    def deprefix(self): return UnitElement(self.base, _EMPTY_STR)

    def __str__(self) -> str: return self.symbol

    def __repr__(self) -> str: 
        return self.__class__.__name__ + f'({self.prefix}, {self.base})'
    
    def __hash__(self) -> int: return hash(self.symbol)


class UnitSymbolError(ValueError):
    pass
