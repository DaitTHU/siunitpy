from .dimension import Dimension
from .dimensionconst import DimensionConst
from .unitdata import SymbolData, UnitData
from .utilcollections.utils import firstof

__all__ = [
    '_PI', '_WEIN_ZERO',
    '_PREFIX', '_PREFIX_FULLNAME',
    '_BASIC_SI',
    '_UNIT', '_UNIT_FULLNAME', '_UNIT_STD'
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


_PREFIX: dict[str, SymbolData] = {
    # whole unit
    'Q': SymbolData('quetta', 1e30),
    'R': SymbolData('ronna', 1e27),
    'Y': SymbolData('yotta', 1e24),
    'Z': SymbolData('zetta', 1e21),
    'E': SymbolData('exa', 1e18),
    'P': SymbolData('peta', 1e15),
    'T': SymbolData('tera', 1e12),
    'G': SymbolData('giga', 1e9),
    'M': SymbolData('mega', 1e6),
    'k': SymbolData('kilo', 1e3),
    'h': SymbolData('hecto', 1e2),
    'da': SymbolData('deka', 1e1),
    '': SymbolData('', 1),
    # sub unit
    'd': SymbolData('deci', 1e-1),
    'c': SymbolData('centi', 1e-2),
    'm': SymbolData('milli', 1e-3),
    'µ': SymbolData('micro', 1e-6),
    'n': SymbolData('nano', 1e-9),
    'p': SymbolData('pico', 1e-12),
    'f': SymbolData('femto', 1e-15),
    'a': SymbolData('atto', 1e-18),
    'z': SymbolData('zepto', 1e-21),
    'y': SymbolData('yocto', 1e-24),
    'r': SymbolData('ronto', 1e-27),
    'q': SymbolData('quecto', 1e-30),
}

_PREFIX_FULLNAME: dict[str, str] = {v.fullname: k for k, v in _PREFIX.items()}


_SPECIAL_DIMENSIONLESS: dict[str, float] = {
    '': 1, '%': 1e-2, '‰': 1e-3, '‱': 1e-4,
}

_LOGARITHMIC_RATIO: dict[str, str] = {
    'Np': 'neper', 'B': 'bel'
}

_BASIC_SI = ('m', 'kg', 's', 'A', 'K', 'mol', 'cd')

# unit library, classified by dimension
# it should appear and be used only in this file
__UNIT_LIB: dict[Dimension, dict[str, SymbolData]] = {
    DimensionConst.DIMENSIONLESS: {
        '': SymbolData('', 1),
        'rad': SymbolData('radian', 1),
        'sr': SymbolData('steradian', 1),
        '°': SymbolData('degree', _DEGREE),
        '′': SymbolData('arcminute', _ARCMIN),
        '″': SymbolData('arcsecond', _ARCSEC),
    },
    DimensionConst.LENGTH: {
        'm': SymbolData('meter', 1),
        'Å': SymbolData('angstrom', 1e-10),  # ångström
        'au': SymbolData('astronomical-unit', _AU),
        'pc': SymbolData('parsec', _PC)
    },
    DimensionConst.MASS: {
        'g': SymbolData('gram', 1e-3),
        't': SymbolData('ton', 1000),
        'u': SymbolData('amu', _DALTON),
        'Da': SymbolData('dalton', _DALTON),
        'eVpcc': SymbolData('electronvolt/c²', _EVPCC),  # for convience
    },
    DimensionConst.TIME: {
        's': SymbolData('second', 1),
        'min': SymbolData('minute', 60),
        'h': SymbolData('hour', 3600),
        'd': SymbolData('day', 86400),
        'yr': SymbolData('year', 31536000),         # simple year: 1 yr = 365 d
        # Julian year: 1 a = 365.25 d
        'a': SymbolData('Julian-year', 31557600),
    },
    DimensionConst.ELECTRIC_CURRENT: {
        'A': SymbolData('ampere', 1),
    },
    DimensionConst.THERMODYNAMIC_TEMPERATURE: {
        'K': SymbolData('kelvin', 1),
        # TODO: remove degree Celsius(°C), Fahrenheit(°F).
        '°C': SymbolData('degree-Celsius', 1),
        '°F': SymbolData('degree-Fahrenheit', 5 / 9),
        '°R': SymbolData('degree-Rankine', 1.8)
    },
    DimensionConst.AMOUNT_OF_SUBSTANCE: {
        'mol': SymbolData('mole', 1),
    },
    DimensionConst.LUMINOUS_INTENSITY: {
        'cd': SymbolData('candela', 1),
        'lm': SymbolData('lumen', 1),
    },
    # derived
    DimensionConst.AREA: {
        'b': SymbolData('barn', 1e-28),
        'ha': SymbolData('hectare', 10000),
    },
    DimensionConst.VOLUME: {
        'L': SymbolData('liter', 1e-3),
    },
    DimensionConst.FREQUENCY: {
        'Hz': SymbolData('hertz', 1),
        'Bq': SymbolData('becquerel', 1),
        'Ci': SymbolData('curie', 3.7e10),
    },
    DimensionConst.FORCE: {
        'N': SymbolData('newton', 1),
    },
    DimensionConst.PRESSURE: {
        'Pa': SymbolData('pascal', 1),
        'bar': SymbolData('bar', 10000),
        'atm': SymbolData('standard-atmosphere', _ATM),
        'mmHg': SymbolData('millimeter-of-mercury', _MMHG),
        'Torr': SymbolData('torr', _MMHG),
    },
    DimensionConst.ENERGY: {
        'J': SymbolData('joule', 1),
        'Wh': SymbolData('watthour', 3600),
        'eV': SymbolData('electronvolt', _ELC),
        'cal': SymbolData('calorie', 4.1868),
    },
    DimensionConst.POWER: {'W': SymbolData('watt', 1), },
    DimensionConst.MOMENTUM: {'eVpc': SymbolData('electronvolt/c', _EVPC), },
    DimensionConst.CHARGE: {'C': SymbolData('coulomb', 1), },
    DimensionConst.VOLTAGE: {'V': SymbolData('volt', 1), },
    DimensionConst.CAPATITANCE: {'F': SymbolData('farad', 1), },
    DimensionConst.RESISTANCE: {'Ω': SymbolData('ohm', 1), },
    DimensionConst.CONDUCTANCE: {'S': SymbolData('siemens', 1), },
    DimensionConst.MAGNETIC_FLUX: {'Wb': SymbolData('weber', 1), },
    DimensionConst.MAGNETIC_INDUCTION: {'T': SymbolData('tesla', 1), },
    DimensionConst.INDUCTANCE: {'H': SymbolData('henry', 1), },
    DimensionConst.ILLUMINANCE: {'lx': SymbolData('lux', 1), },
    DimensionConst.KERMA: {
        'Gy': SymbolData('gray', 1),
        'Sv': SymbolData('sievert', 1),
    },
    DimensionConst.EXPOSURE: {'R': SymbolData('rontgen', 2.58e-4), },
    DimensionConst.CATALYTIC_ACTIVITY: {'kat': SymbolData('katal', 1), },
}

_UNIT: dict[str, UnitData] = {
    unit: UnitData(dim, val)
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
__IRREGULAR_UNIT_DIM: set[Dimension] = {
    DimensionConst.DIMENSIONLESS,
    DimensionConst.AREA, DimensionConst.VOLUME,
    DimensionConst.MOMENTUM, DimensionConst.EXPOSURE
}
_UNIT_STD: dict[Dimension, str] = {
    dim: firstof(unit_val, default='')
    for dim, unit_val in __UNIT_LIB.items()
    if dim not in __IRREGULAR_UNIT_DIM
}
_UNIT_STD[DimensionConst.MASS] = 'kg'
