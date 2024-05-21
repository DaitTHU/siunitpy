from .dimension import Dimension
from .dimensionconst import DimensionConst
from .symboldata import BaseData, PrefixData
from .utilcollections.utils import firstof
from .value_archive import *

__all__ = [
    '_PREFIX_DATA', '_PREFIX_FULLNAME',
    '_BASE_SI',
    '_UNIT_DATA', '_UNIT_FULLNAME', '_UNIT_STD'
]

_PREFIX_DATA: dict[str, PrefixData] = {
    # whole unit
    'Q': PrefixData('quetta', 1e30),
    'R': PrefixData('ronna', 1e27),
    'Y': PrefixData('yotta', 1e24),
    'Z': PrefixData('zetta', 1e21),
    'E': PrefixData('exa', 1e18),
    'P': PrefixData('peta', 1e15),
    'T': PrefixData('tera', 1e12),
    'G': PrefixData('giga', 1e9),
    'M': PrefixData('mega', 1e6),
    'k': PrefixData('kilo', 1e3),
    'h': PrefixData('hecto', 1e2),
    'da': PrefixData('deka', 1e1),
    '': PrefixData('', 1),
    # sub unit
    'd': PrefixData('deci', 1e-1),
    'c': PrefixData('centi', 1e-2),
    'm': PrefixData('milli', 1e-3),
    'µ': PrefixData('micro', 1e-6),
    'n': PrefixData('nano', 1e-9),
    'p': PrefixData('pico', 1e-12),
    'f': PrefixData('femto', 1e-15),
    'a': PrefixData('atto', 1e-18),
    'z': PrefixData('zepto', 1e-21),
    'y': PrefixData('yocto', 1e-24),
    'r': PrefixData('ronto', 1e-27),
    'q': PrefixData('quecto', 1e-30),
}

_PREFIX_FULLNAME: dict[str, str] = {v.fullname: k for k, v in _PREFIX_DATA.items()}
'''{prefix fullname: symbol}'''


_SPECIAL_DIMENSIONLESS: dict[str, float] = {
    '': 1, '%': 1e-2, '‰': 1e-3, '‱': 1e-4,
}

_LOGARITHMIC_RATIO: dict[str, str] = {
    'Np': 'neper', 'B': 'bel'
}

_BASE_SI = ('s', 'm', 'kg', 'A', 'K', 'mol', 'cd')

# unit library, classified by dimension
# internal use only in this file
__UNIT_LIB: dict[Dimension, dict[str, BaseData]] = {
    DimensionConst.DIMENSIONLESS: {
        '': BaseData('', 1),
        'rad': BaseData('radian', 1),
        'sr': BaseData('steradian', 1),
        '°': BaseData('degree', DEGREE, never_prefix=True),
        '′': BaseData('arcminute', ARCMIN, never_prefix=True),
        '″': BaseData('arcsecond', ARCSEC, never_prefix=True),
    },
    DimensionConst.LENGTH: {
        'm': BaseData('meter', 1),
        'Å': BaseData('angstrom', 1e-10),  # ångström
        'au': BaseData('astronomical-unit', AU),
        'pc': BaseData('parsec', PC),
        'ly': BaseData('light-year', LIGHT_YEAR)
    },
    DimensionConst.MASS: {
        'g': BaseData('gram', 1e-3),
        't': BaseData('ton', 1000),
        'u': BaseData('amu', DALTON),
        'Da': BaseData('dalton', DALTON),
    },
    DimensionConst.TIME: {
        's': BaseData('second', 1),
        'min': BaseData('minute', MINUTE),
        'h': BaseData('hour', HOUR),
        'd': BaseData('day', DAY),
        'yr': BaseData('year', SIMPLE_YEAR),
        'a': BaseData('Julian-year', JULIAN_YEAR),
    },
    DimensionConst.ELECTRIC_CURRENT: {
        'A': BaseData('ampere', 1),
    },
    DimensionConst.THERMODYNAMIC_TEMPERATURE: {
        'K': BaseData('kelvin', 1),
        '°C': BaseData('degree-Celsius', 1, never_prefix=True),
        '°F': BaseData('degree-Fahrenheit', 5/9, never_prefix=True),
        '°R': BaseData('degree-Rankine', 1.8, never_prefix=True)
    },
    DimensionConst.AMOUNT_OF_SUBSTANCE: {
        'mol': BaseData('mole', 1),
    },
    DimensionConst.LUMINOUS_INTENSITY: {
        'cd': BaseData('candela', 1),
        'lm': BaseData('lumen', 1),
    },
    # derived
    DimensionConst.AREA: {
        'b': BaseData('barn', 1e-28),
        'ha': BaseData('hectare', 10000, never_prefix=True),
    },
    DimensionConst.VOLUME: {
        'L': BaseData('liter', 1e-3),
    },
    DimensionConst.FREQUENCY: {
        'Hz': BaseData('hertz', 1),
        'Bq': BaseData('becquerel', 1),
        'Ci': BaseData('curie', 3.7e10),
    },
    DimensionConst.VILOCITY: {
        'c': BaseData('speed-of-light', C, never_prefix=True),
    },
    DimensionConst.ACCELERATOR: {
        'gal': BaseData('Gal', 0.01),
    },
    DimensionConst.FORCE: {
        'N': BaseData('newton', 1),
        'gf': BaseData('gram-fore', GRAVITY / 1000)
    },
    DimensionConst.PRESSURE: {
        'Pa': BaseData('pascal', 1),
        'bar': BaseData('bar', SSP),
        'atm': BaseData('standard-atmosphere', ATM),
        'mHg': BaseData('meter-of-mercury', MMHG * 1000),
        'Torr': BaseData('torr', MMHG),  # Torricelli
    },
    DimensionConst.ENERGY: {
        'J': BaseData('joule', 1),
        'Wh': BaseData('watthour', HOUR),
        'eV': BaseData('electronvolt', EV),
        'cal': BaseData('calorie', CAL),
        'g-TNT': BaseData('gram-of-TNT', KCAL),
        't-TNT': BaseData('ton-of-TNT', KCAL * 1e6),
    },
    DimensionConst.POWER: {'W': BaseData('watt', 1), },
    # DimensionConst.MOMENTUM
    DimensionConst.CHARGE: {'C': BaseData('coulomb', 1), },
    DimensionConst.VOLTAGE: {'V': BaseData('volt', 1), },
    DimensionConst.CAPATITANCE: {'F': BaseData('farad', 1), },
    DimensionConst.RESISTANCE: {'Ω': BaseData('ohm', 1), },
    DimensionConst.CONDUCTANCE: {'S': BaseData('siemens', 1), },
    DimensionConst.MAGNETIC_FLUX: {'Wb': BaseData('weber', 1), },
    DimensionConst.MAGNETIC_INDUCTION: {'T': BaseData('tesla', 1), },
    DimensionConst.INDUCTANCE: {'H': BaseData('henry', 1), },
    DimensionConst.ILLUMINANCE: {'lx': BaseData('lux', 1), },
    DimensionConst.KERMA: {
        'Gy': BaseData('gray', 1),
        'Sv': BaseData('sievert', 1),
    },
    DimensionConst.EXPOSURE: {'R': BaseData('roentgen', 2.58e-4), },
    DimensionConst.CATALYTIC_ACTIVITY: {'kat': BaseData('katal', 1), },
}

# add dimension property
for dim, unit_dict in __UNIT_LIB.items():
    for basedata in unit_dict.values():
        basedata.dimension = dim

_UNIT_DATA: dict[str, BaseData] = {
    unit: basedata
    for unit_dict in __UNIT_LIB.values()  # concatenate all dict
    for unit, basedata in unit_dict.items()
}

_UNIT_FULLNAME: dict[str, str] = {
    basedata.fullname: unit for unit, basedata in _UNIT_DATA.items()
}
'''{unit fullname: symbol}'''

# unit standard, every dimension has one SI basic/standard unit
# values() = {m kg s A K mol cd Hz N Pa J W C V F Ω S Wb T H lx Gy kat}
__IRREGULAR_UNIT_DIM: set[Dimension] = {
    DimensionConst.DIMENSIONLESS,
    DimensionConst.AREA, DimensionConst.VOLUME,
    DimensionConst.VILOCITY, DimensionConst.ACCELERATOR, DimensionConst.MOMENTUM,
    DimensionConst.EXPOSURE
}
_UNIT_STD: dict[Dimension, str] = {
    dim: firstof(unit_val, default='')
    for dim, unit_val in __UNIT_LIB.items()
    if dim not in __IRREGULAR_UNIT_DIM
}
'''standard unit for dimension'''
_UNIT_STD[DimensionConst.MASS] = 'kg'
