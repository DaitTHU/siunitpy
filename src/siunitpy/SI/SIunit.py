from ..constant import Constant
from ..unitconst import UnitConst
from ..utilcollections.constclass import ConstClass

__all__ = ['si']


def _base(unit: str):
    return lambda prefix: Constant.one(prefix + unit)


class si(ConstClass):
    '''This constclass provides common units, like m, kg, ...
    Units in the `si` can be multiplied to ordinary data types, 
    like `int`, `float`, `Decimal`, `Fraction`, ..., and convert
    them to `Quantity` objects.
    >>> 1 * si.m                            # 1 m
    >>> 0.511 * si.MeV                      # 0.511 MeV
    >>> Decimal('6.02214076e23') / si.mol   # 6.02214076e23 /mol 
    >>> Fraction(5, 9) * si.celsius         # 5/9 °C

    However, for types like `list`, `Vector`, `numpy.ndarray`, ...
    that overloaded `__mul__` operator, it generally won't get what
    was intended:
    >>> [1] * si.m                  # [1] m
    >>> [1] * si.kg / si.m**3       # TypeError
    >>> Vector([1]) * si.m          # [Quantity(value=1, unit=m)]
    >>> numpy.array([1, 2]) * si.m
    # [Quantity(value=1, unit=m) Quantity(value=2, unit=m)]

    that really sucks. To avoid this dilemma, you have to place
    it on the left side:
    >>> si.m * np.array([1, 2])     # [1 2] m

    And remember, do NOT use `list`:
    >>> si.kg / si.m**3 * [1]       # still TypeError
    '''
    one = Constant.one(UnitConst.DIMENSIONLESS)
    m = Constant.one(UnitConst.METER)
    kg = Constant.one(UnitConst.KILOGRAM)
    s = Constant.one(UnitConst.SECOND)
    A = Constant.one(UnitConst.AMPERE)
    K = Constant.one(UnitConst.KELVIN)
    mol = Constant.one(UnitConst.MOLE)
    cd = Constant.one(UnitConst.CANDELA)
    # derived
    Hz = Constant.one(UnitConst.HERTZ)
    rad = Constant.one(UnitConst.RADIAN)
    sr = Constant.one(UnitConst.STERADIAN)
    N = Constant.one(UnitConst.NEWTON)
    Pa = Constant.one(UnitConst.PASCAL)
    J = Constant.one(UnitConst.JOULE)
    W = Constant.one(UnitConst.WATT)
    C = Constant.one(UnitConst.COULOMB)
    V = Constant.one(UnitConst.VOLT)
    F = Constant.one(UnitConst.FARAD)
    ohm = Constant.one(UnitConst.OHM)
    S = Constant.one(UnitConst.SIEMENS)
    Wb = Constant.one(UnitConst.WEBER)
    T = Constant.one(UnitConst.TESLA)
    H = Constant.one(UnitConst.HENRY)
    # celsius = Constant.one(UnitConst.DEGREE_CELSIUS)
    lm = Constant.one(UnitConst.LUMEN)
    lx = Constant.one(UnitConst.LUX)
    Bq = Constant.one(UnitConst.BECQUEREL)
    Gy = Constant.one(UnitConst.GRAY)
    Sv = Constant.one(UnitConst.SIEVERT)
    kat = Constant.one(UnitConst.KATAL)
    # common prefixed SI unit
    fm, pm, nm, um, mm, cm, km = map(_base('m'), 'fpnumck')
    mg, g = map(_base('g'), 'm ')
    fs, ps, ns, us, ms = map(_base('s'), 'fpnum')
    minute = Constant.one('min')
    h = Constant.one('h')
    mA = Constant.one('mA')
    mK = Constant.one('mK')
    mmol = Constant.one('mmol')
    kHz, MHz, GHz, THz = map(_base('Hz'), 'kMGT')
    kPa, MPa, GPa = map(_base('Pa'), 'kMG')
    mJ, kJ, MJ = map(_base('J'), 'mkM')
    mW, kW, MW = map(_base('W'), 'mkM')
    mV, kV = map(_base('V'), 'mk')
    kohm = Constant.one('kΩ')
    nSv, uSv, mSv = map(_base('Sv'), 'num')
    # NOT in SI unit
    mL, L = map(_base('L'), 'm ')
    bar = Constant.one('bar')
    atm = Constant.one('atm')
    mmHg = Constant.one('mmHg')
    Wh, kWh = map(_base('Wh'), ' k')
    meV, eV, keV, MeV, GeV, TeV = map(_base('eV'), 'm kMGT')
    cal, kcal = map(_base('cal'), ' k')
