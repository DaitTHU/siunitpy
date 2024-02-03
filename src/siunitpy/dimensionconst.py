from .dimension import Dimension
from .utilcollections.constclass import ConstClass

__all__ = ['DimensionConst']


class DimensionConst(ConstClass):
    '''`DimensionConst` is an constclass containing constant `Dimension`
    objects, like dimensionless, 7 SI base units, and other derived units. 
    Units with different physical meanings sharing the same dimension, 
    like energy and work, have to share the same name `ENERGY`. 
    '''
    DIMENSIONLESS = Dimension()
    LENGTH = Dimension(L=1)
    MASS = Dimension(M=1)
    TIME = Dimension(T=1)
    ELECTRIC_CURRENT = Dimension(I=1)
    THERMODYNAMIC_TEMPERATURE = Dimension(H=1)
    AMOUNT_OF_SUBSTANCE = Dimension(N=1)
    LUMINOUS_INTENSITY = Dimension(J=1)
    # derived
    AREA = LENGTH * 2
    VOLUME = LENGTH * 3
    FREQUENCY = -TIME
    VILOCITY = LENGTH - TIME
    ACCELERATOR = VILOCITY - TIME
    FORCE = MASS + ACCELERATOR
    PRESSURE = FORCE - AREA  # stress
    ENERGY = FORCE + LENGTH  # work
    POWER = ENERGY - TIME
    MOMENTUM = MASS + VILOCITY
    # electirc-magnetic
    CHARGE = ELECTRIC_CURRENT + TIME
    VOLTAGE = POWER - ELECTRIC_CURRENT
    CAPATITANCE = CHARGE - VOLTAGE
    RESISTANCE = VOLTAGE - ELECTRIC_CURRENT
    CONDUCTANCE = -RESISTANCE
    MAGNETIC_FLUX = VOLTAGE + TIME
    MAGNETIC_INDUCTION = MAGNETIC_FLUX - AREA
    INDUCTANCE = MAGNETIC_FLUX - ELECTRIC_CURRENT
    # LUMINOUS_FLUX = LUMINOUS_INTENSITY
    ILLUMINANCE = LUMINOUS_INTENSITY - AREA
    KERMA = ENERGY - MASS  # or dose
    EXPOSURE = CHARGE - MASS
    CATALYTIC_ACTIVITY = AMOUNT_OF_SUBSTANCE - TIME
