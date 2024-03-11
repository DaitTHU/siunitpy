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
    TIME = Dimension(T=1)
    LENGTH = Dimension(L=1)
    MASS = Dimension(M=1)
    ELECTRIC_CURRENT = Dimension(I=1)
    THERMODYNAMIC_TEMPERATURE = Dimension(H=1)
    AMOUNT_OF_SUBSTANCE = Dimension(N=1)
    LUMINOUS_INTENSITY = Dimension(J=1)
    # straight derived
    PLANE_ANGLE = DIMENSIONLESS
    SOLID_ANGLE = DIMENSIONLESS
    AREA = LENGTH * 2
    VOLUME = LENGTH * 3
    FREQUENCY = -TIME
    # kinematics and dynamic
    VILOCITY = LENGTH - TIME
    ACCELERATOR = VILOCITY - TIME
    FORCE = MASS + ACCELERATOR
    PRESSURE = FORCE - AREA
    STRESS = PRESSURE
    ENERGY = FORCE + LENGTH
    WORK = ENERGY
    HEAT = ENERGY
    POWER = ENERGY - TIME
    HEAT_FLOW_RATE = POWER
    MOMENTUM = MASS + VILOCITY
    # electrodynamics
    CHARGE = ELECTRIC_CURRENT + TIME
    VOLTAGE = POWER - ELECTRIC_CURRENT
    ELECTROMOTIVE_FORCE = VOLTAGE
    CAPATITANCE = CHARGE - VOLTAGE
    RESISTANCE = VOLTAGE - ELECTRIC_CURRENT
    CONDUCTANCE = -RESISTANCE
    MAGNETIC_FLUX = VOLTAGE + TIME
    MAGNETIC_FLUX_DENSITY = MAGNETIC_FLUX - AREA
    MAGNETIC_INDUCTION = MAGNETIC_FLUX_DENSITY
    INDUCTANCE = MAGNETIC_FLUX - ELECTRIC_CURRENT
    # luminous
    LUMINOUS_FLUX = LUMINOUS_INTENSITY + SOLID_ANGLE
    ILLUMINANCE = LUMINOUS_INTENSITY - AREA
    # nuclear radiation
    ACTIVITY = FREQUENCY  # of a radionuclide
    KERMA = ENERGY - MASS
    DOSE = KERMA
    EXPOSURE = CHARGE - MASS
    # chemistry
    CATALYTIC_ACTIVITY = AMOUNT_OF_SUBSTANCE - TIME
