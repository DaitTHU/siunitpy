'''The `UnitElement` class encapsulates the smallest individual components 
that make up a unit of measurement. It is the basic unit from which more 
complex units can be constructed. Each `UnitElement` object contains two 
essential string attributes: `base` and `prefix`.

The `base` attribute refers to the fundamental unit of measurement, 
such as "meter" in the International System of Units (SI). 
It is the core element that provides the fundamental meaning of the unit.

The `prefix` attribute is an optional component that modifies the 
`base` unit. It represents a multiplier or divisor of the base unit, 
allowing for the expression of larger or smaller quantities. 
For example, the prefix "kilo-" indicates a multiplication by 1,000, 
making the unit "kilometer" represent 1,000 meters.

The combination of a `base` and a `prefix` within a `UnitElement` object 
allows for the creation of a wide range of units, each with its own 
specific magnitude and application. This class is designed to provide 
a structured way to manage and manipulate units of measurement in a 
programmatic context, ensuring consistency and accuracy in scientific 
or engineering calculations.
'''

from .unit_archive import (_PREFIX_DATA, _PREFIX_FULLNAME, _UNIT_DATA,
                           _UNIT_FULLNAME)

_PREFIX_ALIAS = {'u': 'µ', 'K': 'k'}
_PREFIX_MAXLEN = max(map(len, _PREFIX_DATA))
_PREFIX_FULLNAME_MINLEN = min(filter(None, map(len, _PREFIX_FULLNAME)))
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
    '''The `UnitElement` class represents the fundamental components of a unit, 
    namely the elements that comprise it. These elements are the building 
    blocks used to form a complete unit.

    Each `UnitElement` is characterized by two primary attributes: 
    `base` and `prefix`, both of which are of the `str` (string) data type. 
    The `base` represents the core unit, while the `prefix` serves as a 
    multiplier that modifies the magnitude of the base unit. Together, 
    they define the complete unit and its scale.
    '''
    __slots__ = ('_base', '_prefix')

    def __new__(cls, base: str, prefix: str | None = None):
        if isinstance(prefix, str):
            self = super().__new__(cls)
            self._base, self._prefix = base, prefix  # internal use only
        elif base in _UNITELEMENT_BASE:
            self = _UNITELEMENT_BASE[base]  # singleton
        else:
            self = super().__new__(cls)
            self._base, self._prefix = _resolve_element(base)
        return self

    @property
    def base(self) -> str: return self._base
    @property
    def prefix(self) -> str: return self._prefix
    @property
    def symbol(self) -> str: return self.prefix + self.base
    @property
    def prefix_fullname(self) -> str: return _PREFIX_DATA[self.prefix].fullname
    @property
    def base_fullname(self) -> str: return _UNIT_DATA[self.base].fullname
    @property
    def fullname(self) -> str: return self.prefix_fullname + self.base_fullname
    @property
    def prefix_factor(self) -> float: return _PREFIX_DATA[self.prefix].factor
    @property
    def base_factor(self) -> float: return _UNIT_DATA[self.base].factor
    @property
    def factor(self) -> float: return self.prefix_factor * self.base_factor
    @property
    def dimension(self): return _UNIT_DATA[self.base].dimension

    def deprefix(self): return UnitElement(self.base, '')

    def __str__(self) -> str: return self.symbol

    def __repr__(self) -> str:
        return '{}({}-{})'.format(self.prefix, self.base)

    def __hash__(self) -> int: return hash((self.prefix, self.base))

    def __eq__(self, other: 'UnitElement') -> bool:
        return self.symbol == other.symbol

    def __le__(self, other: 'UnitElement') -> bool:
        # TODO: the order of unit-element
        if self.prefix_factor == other.prefix_factor:
            if self.dimension == other.dimension:
                return self.base < other.base
            return self.dimension.astuple() < other.dimension.astuple()
        return self.prefix_factor < other.prefix_factor


_UNITELEMENT_BASE = {
    base: UnitElement(base, '') for base in _UNIT_DATA
}


class UnitSymbolError(ValueError):
    pass
