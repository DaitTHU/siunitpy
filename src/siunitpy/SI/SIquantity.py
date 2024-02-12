from ..constant import Constant, constant
from ..value_archive import _PI, _WEIN_ZERO, _GRAVITY
from ..utilcollections.constclass import ConstClass
from .SIunit import si

__all__ = ['SI']


class SI(ConstClass):
    '''This constclass provides common physic constants,
    like speed of light c, Planck const h... which are all
    immutable `Quantity` object with proper unit.
    >>> SI.g    # 9.8067 m/s2

    use them directly.
    '''

    ### exact constants defined by SI

    # hyperfine transition frequency of Cs-133
    nu133Cs = Constant(9_192_631_770, 'Hz')
    # speed of light in vacuum
    c = Constant(299_792_458, 'm/s')
    # Planck constant
    h = Constant(6.626_070_15e-34, 'J.s')
    # atomic unit of charge
    e = Constant(1.602_176_634e-19, 'C')
    # Boltzmann constant
    kB = Constant(1.380_649e-23, 'J/K')
    # Avogadro constant
    NA = Constant(6.022_140_76e23, 'mol-1')
    # luminous efficacy
    Kcd = Constant(683, 'lm/W')

    ### exact constants derived from SI

    # molar gas constant
    R = constant(kB * NA)
    # Faraday constant
    F = constant(NA * e)
    # molar Planck constant
    NAh = constant(NA * h)
    # reduced Planck constant
    hbar = constant(h / (2 * _PI))
    # Stefan-Boltzmann constant
    sigma = constant((2 * _PI**5 * kB**4 / (15 * h**3 * c**2)).ito('W/m2.K4'))
    # Wien wavelength displacement law constant
    b = constant(h * c / (kB * _WEIN_ZERO))
    # first radiation constant
    c1 = constant((2 * _PI * h * c**2).ito('W.m2'))
    # first radiation constant for spectral radiance
    c1L = constant(c1 / Constant(_PI, 'sr'))
    # second radiation constant
    c2 = constant(h * c / kB)
    # conductance quantum
    G0 = constant((2 * e**2 / h).simplify_unit(inplace=True))
    # Josephson constant
    KJ = constant((2 * e / h).ito('Hz/V'))
    # magnetic flux quantum
    Phi0 = constant((1 / KJ).simplify_unit(inplace=True))
    # von Klitzing constant
    RK = constant((h / e**2).simplify_unit(inplace=True))

    ### other defined exact constants

    # standard acceleration of gravity
    g = Constant(_GRAVITY, 'm/s2')
    # standard temperature
    T0 = Constant(273.15, 'K')
    # standard pressure
    p0 = constant(si.atm.to('Pa'))
    # molar volume of ideal gas
    Vm = constant((R * T0 / p0).ito('m3/mol'))

    ### constants with uncertainty

    # atomic mass constant
    mu = Constant(1.660_539_066_60e-27, 'kg',
                  0.000_000_000_50e-27)
    # molar mass constant
    Mu = Constant(0.999_999_999_65, 'g/mol',
                  0.000_000_000_30)
    # molar mass of C-12
    M12C = constant(12 * Mu)
    # Newtonian constant of gravitation
    G = Constant(6.67430e-11, 'm3/kg.s2',
                 0.000_15e-11)
    # vacuum electric permittivity
    epsilon0 = Constant(8.854_187_8128e-12, 'F/m',
                        0.000_000_0013e-12)
    # vacuum magnetic permeability
    mu0 = Constant(1.256_637_062_12e-6, 'H/m',
                   0.000_000_000_19e-6)
    # Coulomb constant
    ke = constant(1 / (4 * _PI * epsilon0))
    # magnetic constant
    km = constant(mu0 / (4 * _PI))
    # characteristic impedance of vacuum
    Z0 = constant((mu0 / epsilon0).simplify_unit(inplace=True).nthroot(2))
    # fine-structure constant
    alpha = constant(e**2 / (2 * epsilon0 * h * c))
    # inverse fine-structure constant
    alphainv = constant(1 / alpha)
    # particle mass
    me = Constant(9.109_383_7015e-31, 'kg',
                  0.000_000_0028e-31)
    mp = Constant(1.672_621_923_69e-27, 'kg',
                  0.000_000_000_51e-27)
    mn = Constant(1.674_927_498_04e-27, 'kg',
                  0.000_000_000_95e-27)
    malpha = Constant(6.644_657_3357e-27, 'kg',
                      0.000_000_0020e-27)
    mmu = Constant(1.883_531_627e-28, 'kg',
                   0.000_000_042e-28)
    mtau = Constant(3.167_54e-27, 'kg',
                    0.000_21e-27)
    # electron charge to mass quotient
    e_me = constant(e / me)
    # Compton wavelength
    lambdaC = constant((h / (me * c)).simplify_unit(inplace=True))
    # classical electron radius
    re = constant(alpha * lambdaC / (2 * _PI))
    # Thomson cross section
    sigmae = constant(8 * _PI / 3 * re**2)
    # Bohr radius
    a0 = constant(re / alpha**2)
    # Rydberg constant = alpha**2 / 2 * lambdaC
    Rinf = Constant(10_973_731.568_160, 'm-1',
                    0.000_021)
    # Hartree energy = alpha**2 * me * c**2
    Eh = constant(2 * h * c * Rinf)
    # Bohr magneton = hbar / alpha * me * c
    muB = constant((e_me * hbar / 2).ito('J/T'))
    # nuclear magneton
    muN = constant((e * hbar / (2 * mp)).ito('J/T'))
