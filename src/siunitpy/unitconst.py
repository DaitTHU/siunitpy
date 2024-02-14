from .unit import Unit
from .utilcollections.constclass import ConstClass

__all__ = ['UnitConst']


class UnitConst(ConstClass):
    '''`UnitConst` is an constclass containing constant `Unit`
    objects, like dimensionless unit, 7 SI base units
    '''
    DIMENSIONLESS = Unit.simple('')
    METER = Unit('m')
    KILOGRAM = Unit('kg')
    SECOND = Unit('s')
    AMPERE = Unit('A')
    KELVIN = Unit('K')
    MOLE = Unit('mol')
    CANDELA = Unit('cd')
    # derived
    HERTZ = Unit('Hz')
    RADIAN = Unit('rad')
    STERADIAN = Unit('sr')
    NEWTON = Unit('N')
    PASCAL = Unit('Pa')
    JOULE = Unit('J')
    WATT = Unit('W')
    COULOMB = Unit('C')
    VOLT = Unit('V')
    FARAD = Unit('F')
    OHM = Unit('Ω')
    SIEMENS = Unit('S')
    WEBER = Unit('Wb')
    TESLA = Unit('T')
    HENRY = Unit('H')
    # DEGREE_CELSIUS = Unit('°C')
    LUMEN = Unit('lm')
    LUX = Unit('lx')
    BECQUEREL = Unit('Bq')
    GRAY = Unit('Gy')
    SIEVERT = Unit('Sv')
    KATAL = Unit('kat')
