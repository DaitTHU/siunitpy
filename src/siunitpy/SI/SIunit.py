from ..unit import Unit, DIMENSIONLESS
from ..utilcollections.constclass import ConstClass

__all__ = ['si']


def prefix_map(unitbase: str, prefix: str | list[str]):
    return (Unit(p + unitbase) for p in prefix)


class si(ConstClass):
    '''The `si` constclass offers a comprehensive set of common units 
    such as meters (m), kilograms (kg), and more.

    rmul/rtruediv units to `Quantity` objects can change the unit of
    the object, the effect is the same as mul/truediv a '1 unit' quantity.
    >>> Quantity(3.14, 'm') / si.s
    3.14 m/s
    >>> Quantity(2.718, 'J') * si.m
    2.718 J·m

    rmul/rtruediv units to ordinary data types like `int` or `float`
    can convert them into `Quantity` objects.
    >>> 0.511 * si.MeV
    0.511 MeV
    >>> 1 / si.m
    1 /m

    However, when rmul/rtruediv `numpy.ndarray` objects, 
    which overload `__mul__` operation, it may won't get what is intended:
    >>> numpy.array([1, 2]) * si.m
    [Quantity(1, m) Quantity(2, m)]

    So we recommend using @ operand (meaning at) instead:
    >>> numpy.array([1, 2]) @ si.m
    [1 2] m
    '''

    # SI base unit

    one = DIMENSIONLESS
    '''placeholder (used as 1/unit), dimensionless'''
    fs, ps, ns, us, ms, s = prefix_map('s', 'fpnum ')
    '''second, time'''
    fm, pm, nm, um, mm, cm, m, km = prefix_map('m', 'fpnumc k')
    '''metre/meter, length'''
    mg, g, kg = prefix_map('g', 'm k')
    '''gram, mass'''
    mA, A = prefix_map('A', 'm ')
    '''ampere, electric current'''
    mK, K = prefix_map('K', 'm ')
    '''kelvin, thermodynamic temperature'''
    mmol, mol = prefix_map('mol', 'm ')
    '''mole, amount of substance'''
    cd = Unit('cd')
    '''candela, luminous intensity'''

    # SI derived unit

    rad = Unit('rad')
    '''radian, plane angle'''
    sr = Unit('sr')
    '''steradian, solid angle'''
    Hz, kHz, MHz, GHz, THz = prefix_map('Hz', ' kMGT')
    '''hertz, frequency'''
    N, kN = prefix_map('N', ' k')
    '''newton, force/weight'''
    Pa, kPa, MPa, GPa = prefix_map('Pa', ' kMG')
    '''pascal, pressure/stress'''
    mJ, J, kJ, MJ = prefix_map('J', 'm kM')
    '''joule, energy/work/heat'''
    mW, W, kW, MW = prefix_map('W', 'm kM')
    '''watt, power/radiant flux'''
    pC, nC, uC, mC, C = prefix_map('C', 'pnum ')
    '''coulomb, electric charge'''
    mV, V, kV = prefix_map('V', 'm k')
    '''volt, electric potential/voltage/emf'''
    pF, nF, uF, mF, F = prefix_map('F', 'pnum ')
    '''farad, capacitance'''
    mohm, ohm, kohm = prefix_map('Ω', 'm k')
    '''ohm, resistance/impedance/reactance'''
    S = Unit('S')
    '''siemens, electrical conductance'''
    Wb = Unit('Wb')
    '''weber, magnetic flux'''
    T = Unit('T')
    '''tesla, magnetic flux density'''
    H = Unit('H')
    '''henry, inductance'''
    # celsius = Unit('°C')
    # '''degree Celsius, temperature relative to 273.15 K'''
    lm = Unit('lm')
    '''lumen, luminous flux'''
    lx = Unit('lx')
    '''lux, illuminance'''
    Bq, kBq, MBq, GBq = prefix_map('Bq', ' kMG')
    '''becquerel, activity referred to a radionuclide'''
    Gy = Unit('Gy')
    '''gray, absorbed dose'''
    nSv, uSv, mSv, Sv = prefix_map('Sv', 'num ')
    '''sievert, equivalent dose'''
    kat = Unit('kat')
    '''katal, catalytic activity'''

    # other common unit

    min = Unit('min')
    '''minute, time'''
    h = Unit('h')
    '''hour, time'''
    mL, L = prefix_map('L', 'm ')
    '''liter/litre, volume'''
    bar = Unit('bar')
    '''bar, pressure'''
    ssp = Unit('ssp')
    '''standard-state pressure'''
    atm = Unit('atm')
    '''standard atmosphere'''
    mmHg = Unit('mmHg')
    '''millimetre of mercury, 760 mmHg = 1 atm'''
    Wh, kWh = prefix_map('Wh', ' k')
    '''watthour, energy'''
    meV, keV, MeV, GeV, TeV, eV = prefix_map('eV', 'mkMGT ')
    '''electron volt, energy'''
    cal, kcal = prefix_map('cal', ' k')
    '''calorie, energy'''
