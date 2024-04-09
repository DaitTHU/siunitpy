from ..constant import OneUnit
from ..unitconst import UnitConst
from ..utilcollections.constclass import ConstClass

__all__ = ['si']


def _base(unit: str):
    return lambda prefix: OneUnit(prefix + unit)


class si(ConstClass):
    '''This constclass provides common units, like m, kg, ...
    Units in the `si` can be multiplied to ordinary data types, 
    like `int`, `float`, `Decimal`, `Fraction`, ..., and convert
    them to `Quantity` objects.
    >>> 1 * si.m                            # 1 m
    >>> 0.511 * si.MeV                      # 0.511 MeV

    However, for `numpy.ndarray` that overloaded `__mul__` operator, 
    it generally won't get what was intended:
    >>> numpy.array([1, 2]) * si.m
    # [Variable(1, uncertainty=0) Variable(2, uncertainty=0)] m

    So use @ operand (meaning at) instead:
    >>> numpy.array([1, 2]) @ si.m
    # [1, 2] m
    '''
    I = one = OneUnit(UnitConst.DIMENSIONLESS)
    m = OneUnit(UnitConst.METER)
    kg = OneUnit(UnitConst.KILOGRAM)
    s = OneUnit(UnitConst.SECOND)
    A = OneUnit(UnitConst.AMPERE)
    K = OneUnit(UnitConst.KELVIN)
    mol = OneUnit(UnitConst.MOLE)
    cd = OneUnit(UnitConst.CANDELA)
    # derived
    Hz = OneUnit(UnitConst.HERTZ)
    rad = OneUnit(UnitConst.RADIAN)
    sr = OneUnit(UnitConst.STERADIAN)
    N = OneUnit(UnitConst.NEWTON)
    Pa = OneUnit(UnitConst.PASCAL)
    J = OneUnit(UnitConst.JOULE)
    W = OneUnit(UnitConst.WATT)
    C = OneUnit(UnitConst.COULOMB)
    V = OneUnit(UnitConst.VOLT)
    F = OneUnit(UnitConst.FARAD)
    ohm = OneUnit(UnitConst.OHM)
    S = OneUnit(UnitConst.SIEMENS)
    Wb = OneUnit(UnitConst.WEBER)
    T = OneUnit(UnitConst.TESLA)
    H = OneUnit(UnitConst.HENRY)
    # celsius = OneUnit(UnitConst.DEGREE_CELSIUS)
    lm = OneUnit(UnitConst.LUMEN)
    lx = OneUnit(UnitConst.LUX)
    Bq = OneUnit(UnitConst.BECQUEREL)
    Gy = OneUnit(UnitConst.GRAY)
    Sv = OneUnit(UnitConst.SIEVERT)
    kat = OneUnit(UnitConst.KATAL)
    # common prefixed SI unit
    fm, pm, nm, um, mm, cm, km = map(_base('m'), 'fpnumck')
    mg, g = map(_base('g'), 'm ')
    fs, ps, ns, us, ms = map(_base('s'), 'fpnum')
    minute = OneUnit('min')
    h = OneUnit('h')
    mA = OneUnit('mA')
    mK = OneUnit('mK')
    mmol = OneUnit('mmol')
    kHz, MHz, GHz, THz = map(_base('Hz'), 'kMGT')
    kPa, MPa, GPa = map(_base('Pa'), 'kMG')
    mJ, kJ, MJ = map(_base('J'), 'mkM')
    mW, kW, MW = map(_base('W'), 'mkM')
    mV, kV = map(_base('V'), 'mk')
    kohm = OneUnit('kΩ')
    nSv, uSv, mSv = map(_base('Sv'), 'num')
    # NOT in SI unit
    mL, L = map(_base('L'), 'm ')
    bar = OneUnit('bar')
    atm = OneUnit('atm')
    mmHg = OneUnit('mmHg')
    Wh, kWh = map(_base('Wh'), ' k')
    meV, eV, keV, MeV, GeV, TeV = map(_base('eV'), 'm kMGT')
    cal, kcal = map(_base('cal'), ' k')
