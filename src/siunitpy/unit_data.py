from .dimension import Dimension
from .dimensionconst import DimensionConst
from .utilcollections.utils import _first

__all__ = [
    '_PI', '_WEIN_ZERO',
    '_SUPERSCRIPT', '_SUBSCRIPT',
    '_PREFIX_FACTOR', '_PREFIX_FULLNAME',
    '_BASIC_SI',
    '_SPECIAL_DIMENSIONLESS', '_UNITS', '_UNIT_STD'
]

# math constants
_PI = 3.1415926535897932384626
_WEIN_ZERO = 4.965114231744277  # x = 5 * (1 - exp(-x))
# physical constants
_C = 299792458              # speed of light
_ELC = 1.602176634e-19      # elementary charge
# unit value definition
_DEGREE = _PI / 180
_ARCMIN = _DEGREE / 60
_ARCSEC = _ARCMIN / 60
_EV = _ELC                  # elctron volt
_DALTON = 1.660539040e-27   # 1 Dalton = m(12C) / 12
_EVPC = _EV / _C            # eV/c
_EVPCC = _EVPC / _C         # eV/c2
_AU = 149597870700          # astronomical unit
_PC = _AU / _ARCSEC         # parsec
_ATM = 101325               # standard atmosphere
_SSP = 100000               # standard state pressure
_MMHG = _ATM / 760          # mmHg = 1 atm / 760


_SUPERSCRIPT = '⁰¹²³⁴⁵⁶⁷⁸⁹'
_SUBSCRIPT = '₀₁₂₃₄₅₆₇₈₉'

_PREFIX_FACTOR: dict[str, float] = {
    'Q': 1e30, 'R': 1e27, 'Y': 1e24, 'Z': 1e21, 'E': 1e18, 'P': 1e15,
    'T': 1e12, 'G': 1e9, 'M': 1e6, 'k': 1000,  # 'h': 100, 'da': 10,
    '': 1, 'd': 1e-1, 'c': 1e-2, 'm': 1e-3, 'u': 1e-6,
    'µ': 1e-6,  # u+00b5, micro
    # 'μ': 1e-6,  # u+03bc, Greek letter
    'n': 1e-9, 'p': 1e-12, 'f': 1e-15, 'a': 1e-18, 'z': 1e-21,
    'y': 1e-24, 'r': 1e-27, 'q': 1e-30,
}

_PREFIX_FULLNAME: dict[str, str] = {
    'quetta': 'Q', 'ronna': 'R', 'yotta': 'Y', 'zetta': 'Z', 'exa': 'E',
    'peta': 'P', 'tera': 'T', 'giga': 'G', 'mega': 'M', 'kilo': 'k',
    'hecto': 'h', 'deca': 'da',
    'deci': 'd', 'centi': 'c', 'milli': 'm', 'micro': 'u', 'nano': 'n',
    'pico': 'p', 'femto': 'f', 'atto': 'a', 'zepto': 'z', 'yocto': 'y',
    'ronto': 'r', 'quecto': 'q',
}

_SPECIAL_DIMENSIONLESS: dict[str, float] = {
    '': 1, '%': 1e-2, '‰': 1e-3, '‱': 1e-4,
    '°': _DEGREE,
    "'": _ARCMIN, '′': _ARCMIN,
    '"': _ARCSEC, '″': _ARCSEC,
}

_BASIC_SI = ('m', 'kg', 's', 'A', 'K', 'mol', 'cd')

# unit library, classified by dimension
_UNIT_LIB: dict[Dimension, dict[str, float]] = {
    DimensionConst.DIMENSIONLESS: {
        'rad': 1, 'sr': 1, 'deg': _DEGREE,
    },
    DimensionConst.LENGTH: {
        'm': 1, 'Å': 1e-10,  # ångström
        'au': _AU, 'pc': _PC
    },
    DimensionConst.MASS: {
        'g': 1e-3, 't': 1000, 'u': _DALTON, 'Da': _DALTON,
        'eVpcc': _EVPCC,  # for convience
    },
    DimensionConst.TIME: {
        's': 1, 'min': 60, 'h': 3600, 'd': 86400,
        'yr': 31536000,  # simple year: 1 yr = 365 days
        'a' : 31557600,  # Julian year: 1 a = 365.25 days
    },
    DimensionConst.ELECTRIC_CURRENT: {
        'A': 1,
    },
    DimensionConst.THERMODYNAMIC_TEMPERATURE: {
        'K': 1,
        # TODO: remove degree Celsius(°C), Fahrenheit(°F).
        '°C': 1, '°F': 5 / 9,
    },
    DimensionConst.AMOUNT_OF_SUBSTANCE: {
        'mol': 1,
    },
    DimensionConst.LUMINOUS_INTENSITY: {
        'cd': 1, 'lm': 1,
    },
    # derived
    DimensionConst.AREA: {
        'barn': 1e-28, 'ha': 10000,
    },
    DimensionConst.VOLUME: {
        'L': 1e-3,
    },
    DimensionConst.FREQUENCY: {
        'Hz': 1, 'Bq': 1, 'Ci': 3.7e10,
    },
    DimensionConst.FORCE: {
        'N': 1,
    },
    DimensionConst.PRESSURE: {
        'Pa': 1, 'bar': 10000, 'atm': _ATM,
        'mmHg': _MMHG, 'Torr': _MMHG,
    },
    DimensionConst.ENERGY: {
        'J': 1, 'Wh': 3600,
        'eV': _ELC, 'cal': 4.1868,
    },
    DimensionConst.POWER: {'W': 1, },
    DimensionConst.MOMENTUM: {'eVpc': _EVPC, },
    DimensionConst.CHARGE: {'C': 1, },
    DimensionConst.VOLTAGE: {'V': 1, },
    DimensionConst.CAPATITANCE: {'F': 1, },
    DimensionConst.RESISTANCE: {
        'Ω': 1, 'ohm': 1,
    },
    DimensionConst.CONDUCTANCE: {'S': 1, },
    DimensionConst.MAGNETIC_FLUX: {'Wb': 1, },
    DimensionConst.MAGNETIC_INDUCTION: {'T': 1, },
    DimensionConst.INDUCTANCE: {'H': 1, },
    DimensionConst.ILLUMINANCE: {'lx': 1, },
    DimensionConst.KERMA: {
        'Gy': 1, 'Sv': 1,
    },
    DimensionConst.EXPOSURE: {'Rontgen': 2.58e-4, },
    DimensionConst.CATALYTIC_ACTIVITY: {'kat': 1, },
}

# unit dictonary, quick to find unit through string-hash
_UNITS: dict[str, tuple[Dimension, float]] = {
    unit: (dim, value)
    for dim, unit_val in _UNIT_LIB.items()
    for unit, value in unit_val.items()
}

# 1 simple unit to 1 dimension
__IRREGULAR_UNIT_DIM = set((
    DimensionConst.DIMENSIONLESS,
    DimensionConst.AREA, DimensionConst.VOLUME,
    DimensionConst.MOMENTUM, DimensionConst.EXPOSURE
))
# values() = {m kg s A K mol cd Hz N Pa J W C V F Ω S Wb T H lx Gy kat}
_UNIT_STD: dict[Dimension, str] = {
    dim: _first(unit_val, '') for dim, unit_val in _UNIT_LIB.items()
    if dim not in __IRREGULAR_UNIT_DIM
}
_UNIT_STD[DimensionConst.MASS] = 'kg'
