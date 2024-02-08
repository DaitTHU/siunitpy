from typing import Optional, overload

from .unit_data import _PREFIX, _PREFIX_FULLNAME, _UNIT, _UNIT_FULLNAME

_EMPTY_STR = ''
_PREFIX_ALIAS = {'u': 'µ'}
_PREFIX_MAXLEN = max(map(len, _PREFIX))
_PREFIX_FULLNAME_MINLEN = min(map(len, _PREFIX_FULLNAME))
_PREFIX_FULLNAME_MAXLEN = max(map(len, _PREFIX_FULLNAME))
_UNIT_ALIAS = {'eVpc': 'eV/c', 'eVpcc': 'eV/c²'}


def _resolve_single(unit: str) -> tuple[str, str]:
    '''resolve a single, unexponented unit str.'''
    if unit in _UNIT:
        return unit, _EMPTY_STR
    for prefix_len in range(_PREFIX_MAXLEN):
        prefix, basic = unit[:prefix_len + 1], unit[prefix_len + 1:]
        if prefix in _PREFIX_ALIAS:
            prefix = _PREFIX_ALIAS[prefix]
        if prefix in _PREFIX and basic in _UNIT:
            return basic, prefix
    # fullname case
    if unit in _UNIT_FULLNAME:
        return _UNIT_FULLNAME[unit], _EMPTY_STR
    for prefix_len in range(_PREFIX_FULLNAME_MINLEN, _PREFIX_FULLNAME_MAXLEN):
        prefix, basic = unit[:prefix_len + 1], unit[prefix_len + 1:]
        if prefix in _PREFIX_FULLNAME and basic in _UNIT_FULLNAME:
            return _UNIT_FULLNAME[basic], _PREFIX_FULLNAME[prefix]
    raise UnitSymbolError(f"'{unit}' is not a valid unit.")


class UnitElement:
    __slots__ = ('_basic', '_prefix')

    @overload
    def __init__(self, unit: str) -> None: ...
    @overload
    def __init__(self, basic: str, prefix: str) -> None: ...

    def __init__(self, unit: str, prefix: Optional[str] = None):  # type: ignore
        if isinstance(prefix, str):
            self._basic, self._prefix = unit, prefix
            return
        self._basic, self._prefix = _resolve_single(unit)
        if self._basic in _UNIT_ALIAS:
            self._basic = _UNIT_ALIAS[self._basic]

    @property
    def basic(self): return self._basic
    @property
    def prefix(self): return self._prefix
    @property
    def symbol(self): return self.prefix + self.basic

    @property
    def fullname(self):
        return _PREFIX[self.prefix].fullname + _UNIT[self.basic].fullname

    @property
    def value(self):
        return _PREFIX[self.prefix].factor * _UNIT[self.basic].factor

    @property
    def dimension(self): return _UNIT[self.basic].dimension

    def deprefix(self): return UnitElement(self.basic, '')


class UnitSymbolError(ValueError):
    pass
