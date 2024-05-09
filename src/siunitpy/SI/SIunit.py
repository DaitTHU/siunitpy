from ..unit import Unit, DIMENSIONLESS
from ..utilcollections.constclass import ConstClass

__all__ = ['si']


def _base(unit: str):
    return lambda prefix: Unit(prefix + unit)


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
    I = one = DIMENSIONLESS
    fm, pm, nm, um, mm, cm, m, km = map(_base('m'), 'fpnumc k')
    mg, g, kg = map(_base('g'), 'm k')
    fs, ps, ns, us, ms, s = map(_base('s'), 'fpnum ')
    mA, A = map(_base('A'), 'm ')
    mK, K = map(_base('K'), 'm ')
    mmol, mol = map(_base('mol'), 'm ')
    cd = Unit('cd')
    # derived
    Hz, kHz, MHz, GHz, THz = map(_base('Hz'), ' kMGT')
    rad = Unit('rad')
    sr = Unit('sr')
    N, kN = map(_base('N'), ' k')
    Pa, kPa, MPa, GPa = map(_base('Pa'), ' kMG')
    mJ, J, kJ, MJ = map(_base('J'), 'm kM')
    mW, W, kW, MW = map(_base('W'), 'm kM')
    C = Unit('C')
    mV, V, kV = map(_base('V'), 'm k')
    pF, nF, uF, mF, F = map(_base('F'), 'pnum ')
    ohm, kohm = map(_base('Ω'), ' k')
    S = Unit('S')
    Wb = Unit('Wb')
    T = Unit('T')
    H = Unit('H')
    # celsius = Unit('°C')
    lm = Unit('lm')
    lx = Unit('lx')
    Bq = Unit('Bq')
    Gy = Unit('Gy')
    nSv, uSv, mSv, Sv = map(_base('Sv'), 'num ')
    kat = Unit('kat')
    # common prefixed SI unit
    minute = Unit('min')
    h = Unit('h')
    # NOT in SI unit
    mL, L = map(_base('L'), 'm ')
    bar = Unit('bar')
    atm = Unit('atm')
    mmHg = Unit('mmHg')
    Wh, kWh = map(_base('Wh'), ' k')
    meV, eV, keV, MeV, GeV, TeV = map(_base('eV'), 'm kMGT')
    cal, kcal = map(_base('cal'), ' k')
