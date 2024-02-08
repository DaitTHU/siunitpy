from .dimension import Dimension
from .dimensionconst import DimensionConst
from .utilcollections.utils import firstof

__all__ = [
    '_PI', '_WEIN_ZERO',
    '_PREFIX', '_PREFIX_MAXLEN', '_PREFIX_FULLNAME',
    '_PREFIX_FULLNAME_MINLEN', '_PREFIX_FULLNAME_MAXLEN',
    '_SPECIAL_DIMENSIONLESS', '_BASIC_SI',
    '_UNIT_DIMVAL', '_UNIT_FULLNAME', '_UNIT_STD'
]

# math constants
_PI = 3.1415926535897932384626
_WEIN_ZERO = 4.965114231744277  # solution of: x = 5 * (1 - exp(-x))
# physical constants
_C = 299792458              # speed of light
_ELC = 1.602176634e-19      # elementary charge
# unit value definition
_DEGREE = _PI / 180
_ARCMIN = _DEGREE / 60
_ARCSEC = _ARCMIN / 60
_EV = _ELC                  # elctron volt
_DALTON = 1.660539040e-27   # 1 Dalton = mass(12C) / 12
_EVPC = _EV / _C            # eV/c
_EVPCC = _EVPC / _C         # eV/c2
_AU = 149597870700          # astronomical unit
_PC = _AU / _ARCSEC         # parsec
_ATM = 101325               # standard atmosphere
_SSP = 100000               # standard state pressure
_MMHG = _ATM / 760          # 1 mmHg = 1 atm / 760


class Factor:
    '''used as dict-value, can be represent a unit or prefix.'''
    __slots__ = ('_fullname', '_factor')

    def __init__(self, fullname: str, factor: float) -> None:
        self._fullname = fullname
        self._factor = factor

    @property
    def fullname(self): return self._fullname
    @property
    def factor(self): return self._factor


_PREFIX: dict[str, Factor] = {
    # whole unit
    'Q': Factor('quetta', 1e30),
    'R': Factor('ronna', 1e27),
    'Y': Factor('yotta', 1e24),
    'Z': Factor('zetta', 1e18),
    'E': Factor('exa', 1e18),
    'P': Factor('peta', 1e15),
    'T': Factor('tera', 1e12),
    'G': Factor('giga', 1e9),
    'M': Factor('mega', 1e6),
    'k': Factor('kilo', 1e3),
    'h': Factor('hecto', 1e2),
    'da': Factor('deka', 1e1),
    '': Factor('', 1),
    # sub unit
    'd': Factor('deci', 1e-1),
    'c': Factor('centi', 1e-2),
    'm': Factor('milli', 1e-3),
    'µ': Factor('micro', 1e-6),
    'n': Factor('nano', 1e-9),
    'p': Factor('pico', 1e-12),
    'f': Factor('femto', 1e-15),
    'a': Factor('atto', 1e-18),
    'z': Factor('zepto', 1e-21),
    'y': Factor('yocto', 1e-24),
    'r': Factor('ronto', 1e-27),
    'q': Factor('quecto', 1e-30),
}
_PREFIX_MAXLEN = max(map(len, _PREFIX))

_PREFIX_FULLNAME: dict[str, str] = {v.fullname: k for k, v in _PREFIX.items()}
_PREFIX_FULLNAME_MINLEN = min(map(len, _PREFIX_FULLNAME))
_PREFIX_FULLNAME_MAXLEN = max(map(len, _PREFIX_FULLNAME))


_SPECIAL_DIMENSIONLESS: dict[str, float] = {
    '': 1, '%': 1e-2, '‰': 1e-3, '‱': 1e-4,
    '°': _DEGREE,
    "'": _ARCMIN, '′': _ARCMIN,
    '"': _ARCSEC, '″': _ARCSEC,
}

_BASIC_SI = ('m', 'kg', 's', 'A', 'K', 'mol', 'cd')

# unit library, classified by dimension
# it should appear and be used only in this file
__UNIT_LIB: dict[Dimension, dict[str, Factor]] = {
    DimensionConst.DIMENSIONLESS: {
        '': Factor('', 1),
        'rad': Factor('radian', 1),
        'sr': Factor('steradian', 1),
        'deg': Factor('degree', _DEGREE),
    },
    DimensionConst.LENGTH: {
        'm': Factor('meter', 1),
        'Å': Factor('angstrom', 1e-10),  # ångström
        'au': Factor('astronomical-unit', _AU),
        'pc': Factor('parsec', _PC)
    },
    DimensionConst.MASS: {
        'g': Factor('gram', 1e-3),
        't': Factor('ton', 1000),
        'u': Factor('amu', _DALTON),
        'Da': Factor('dalton', _DALTON),
        'eVpcc': Factor('electronvolt/c²', _EVPCC),  # for convience
    },
    DimensionConst.TIME: {
        's': Factor('second', 1),
        'min': Factor('minute', 60),
        'h': Factor('hour', 3600),
        'd': Factor('day', 86400),
        'yr': Factor('year', 31536000),         # simple year: 1 yr = 365 d
        'a': Factor('Julian-year', 31557600),   # Julian year: 1 a = 365.25 d
    },
    DimensionConst.ELECTRIC_CURRENT: {
        'A': Factor('ampere', 1),
    },
    DimensionConst.THERMODYNAMIC_TEMPERATURE: {
        'K': Factor('kelvin', 1),
        # TODO: remove degree Celsius(°C), Fahrenheit(°F).
        '°C': Factor('degree-Celsius', 1),
        '°F': Factor('degree-Fahrenheit', 5 / 9),
        '°R': Factor('degree-Rankine', 1.8)
    },
    DimensionConst.AMOUNT_OF_SUBSTANCE: {
        'mol': Factor('mole', 1),
    },
    DimensionConst.LUMINOUS_INTENSITY: {
        'cd': Factor('candela', 1),
        'lm': Factor('lumen', 1),
    },
    # derived
    DimensionConst.AREA: {
        'b': Factor('barn', 1e-28),
        'ha': Factor('hectare', 10000),
    },
    DimensionConst.VOLUME: {
        'L': Factor('liter', 1e-3),
    },
    DimensionConst.FREQUENCY: {
        'Hz': Factor('hertz', 1),
        'Bq': Factor('becquerel', 1),
        'Ci': Factor('curie', 3.7e10),
    },
    DimensionConst.FORCE: {
        'N': Factor('newton', 1),
    },
    DimensionConst.PRESSURE: {
        'Pa': Factor('pascal', 1),
        'bar': Factor('bar', 10000),
        'atm': Factor('standard-atmosphere', _ATM),
        'mmHg': Factor('millimeter-of-mercury', _MMHG),
        'Torr': Factor('torr', _MMHG),
    },
    DimensionConst.ENERGY: {
        'J': Factor('joule', 1),
        'Wh': Factor('watthour', 3600),
        'eV': Factor('electronvolt', _ELC),
        'cal': Factor('calorie', 4.1868),
    },
    DimensionConst.POWER: {'W': Factor('watt', 1), },
    DimensionConst.MOMENTUM: {'eVpc': Factor('electronvolt/c', _EVPC), },
    DimensionConst.CHARGE: {'C': Factor('coulomb', 1), },
    DimensionConst.VOLTAGE: {'V': Factor('volt', 1), },
    DimensionConst.CAPATITANCE: {'F': Factor('farad', 1), },
    DimensionConst.RESISTANCE: {'Ω': Factor('ohm', 1), },
    DimensionConst.CONDUCTANCE: {'S': Factor('siemens', 1), },
    DimensionConst.MAGNETIC_FLUX: {'Wb': Factor('weber', 1), },
    DimensionConst.MAGNETIC_INDUCTION: {'T': Factor('tesla', 1), },
    DimensionConst.INDUCTANCE: {'H': Factor('henry', 1), },
    DimensionConst.ILLUMINANCE: {'lx': Factor('lux', 1), },
    DimensionConst.KERMA: {
        'Gy': Factor('gray', 1),
        'Sv': Factor('sievert', 1),
    },
    DimensionConst.EXPOSURE: {'R': Factor('rontgen', 2.58e-4), },
    DimensionConst.CATALYTIC_ACTIVITY: {'kat': Factor('katal', 1), },
}

# dimension and value of unit
_UNIT_DIMVAL: dict[str, tuple[Dimension, float]] = {
    unit: (dim, val.factor)
    for dim, unit_val in __UNIT_LIB.items()
    for unit, val in unit_val.items()
}
_UNIT_FULLNAME: dict[str, str] = {
    val.fullname: unit
    for unit_val in __UNIT_LIB.values()
    for unit, val in unit_val.items()
}

# unit standard, every dimension has one SI basic/standard unit
# values() = {m kg s A K mol cd Hz N Pa J W C V F Ω S Wb T H lx Gy kat}
__IRREGULAR_UNIT_DIM = set((
    DimensionConst.DIMENSIONLESS,
    DimensionConst.AREA, DimensionConst.VOLUME,
    DimensionConst.MOMENTUM, DimensionConst.EXPOSURE
))
_UNIT_STD: dict[Dimension, str] = {
    dim: firstof(unit_val, default='') for dim, unit_val in __UNIT_LIB.items()
    if dim not in __IRREGULAR_UNIT_DIM
}
_UNIT_STD[DimensionConst.MASS] = 'kg'
