from ..constant import Constant, constant
from ..value_archive import *
from ..utilcollections.constclass import ConstClass
from .SIunit import si

__all__ = ['SI']


class SI(ConstClass):
    '''The `SI` constclass offers common fundamental physical constants,
    like speed of light (c), Planck const (h)... which are all
    immutable `Quantity` objects with proper units.

    For example, accessing the standard acceleration of gravity (g) 
    can be done as follows:
    >>> SI.g
    9.80665 m/s²

    These constants can be directly incorporated into your formulas or code.
    '''

    # exact constants defined by SI

    nu133Cs = Constant(9_192_631_770, si.Hz)
    '''hyperfine transition frequency of Cs-133'''
    c = Constant(C, 'm/s')
    '''speed of light in vacuum'''
    h = Constant(6.626_070_15e-34, 'J.s')
    '''Planck constant'''
    e = Constant(ELC, si.C)
    '''elementary charge'''
    kB = Constant(1.380_649e-23, 'J/K')
    '''Boltzmann constant'''
    NA = Constant(6.022_140_76e23, 'mol-1')
    '''Avogadro constant'''
    Kcd = Constant(683, 'lm/W')
    '''luminous efficacy'''

    hbar = constant(h / (2 * PI))
    '''reduced Planck constant'''
    g = Constant(GRAVITY, 'm/s2')
    '''standard acceleration of gravity'''
    T0 = Constant(KELVIN_ZERO, si.K)
    '''standard temperature'''

    # universal

    G = Constant(6.674_30e-11, 'm3/kg.s2', relative_uncertainty=2.2e-5)
    '''Newtonian constant of gravitation'''
    mP = constant((hbar * c / G).nthroot(2), simplify=True)
    '''Planck mass'''
    TP = constant(mP * c**2 / kB, simplify=True)
    '''Planck temperature'''
    lP = constant(hbar / (mP * c), simplify=True)
    '''Planck length'''
    tP = constant(lP / c)
    '''Planck time'''

    # electromagnetic constants

    mu0 = Constant(1.256_637_061_27e-6, 'H/m', relative_uncertainty=1.6e-10)
    '''vacuum magnetic permeability'''
    epsilon0 = constant(1 / (mu0 * c**2), 'F/m')
    '''vacuum electric permittivity'''
    Z0 = constant(mu0 * c, simplify=True)
    '''characteristic impedance of vacuum'''
    ke = constant(1 / (4 * PI * epsilon0))
    '''Coulomb constant'''
    KJ = constant(2 * e / h, 'Hz/V')
    '''Josephson constant'''
    Phi0 = constant(1 / KJ, simplify=True)
    '''magnetic flux quantum'''
    G0 = constant(2 * e**2 / h, simplify=True)
    '''conductance quantum'''
    RK = constant(h / e**2, simplify=True)
    '''von Klitzing constant'''

    # atomic and nuclear

    me = Constant(9.109_383_7139e-31, si.kg, relative_uncertainty=3.1e-10)
    '''electron mass'''
    mmu = Constant(1.883_531_627e-28, si.kg, relative_uncertainty=2.2e-8)
    '''muon mass'''
    mtau = Constant(3.167_54e-27, si.kg, relative_uncertainty=6.8e-5)
    '''tau mass'''
    mp = Constant(1.672_621_925_95e-27, si.kg, relative_uncertainty=3.1e-10)
    '''proton mass'''
    mn = Constant(1.674_927_500_56e-27, si.kg, relative_uncertainty=5.1e-10)
    '''neutron mass'''
    md = Constant(3.343_583_7768e-27, si.kg, relative_uncertainty=3.1e-10)
    '''deuteron mass'''
    mt = Constant(5.007_356_7512e-27, si.kg, relative_uncertainty=3.1e-10)
    '''triton mass'''
    mh = Constant(5.006_412_7862e-27, si.kg, relative_uncertainty=3.1e-10)
    '''helion mass'''
    malpha = Constant(6.644_657_3450e-27, si.kg, relative_uncertainty=3.1e-10)
    '''alpha partcle mass'''

    alpha = constant(e**2 / (2 * epsilon0 * h * c), simplify=True)
    '''fine-structure constant'''
    alphainv = constant(1 / alpha)
    '''inverse fine-structure constant'''
    a0 = constant(hbar / (alpha * me * c), relative_uncertainty=1.5e-10)
    '''Bohr radius'''
    lambdaC = constant(h / (me * c), simplify=True)
    '''Compton wavelength'''
    Rinf = constant(alpha**2 / (2 * lambdaC), relative_uncertainty=1.9e-12)
    '''Rydberg constant'''
    Eh = constant(2 * h * c * Rinf)
    '''Hartree energy'''  # = alpha**2 * me * c**2
    re = constant(alpha**2 * a0)
    '''classical electron radius'''
    sigmae = constant(8 * PI / 3 * re**2)
    '''Thomson cross section'''
    muB = constant(e * hbar / (2 * me), 'J/T')
    '''Bohr magneton'''
    muN = constant(e * hbar / (2 * mp), 'J/T')
    '''nuclear magneton'''
    mue = Constant(-9.284_764_7043e-24, 'J/T', relative_uncertainty=3.0e-10)
    '''electron magnetic moment'''
    ge = constant(2 * mue / muB, relative_uncertainty=1.7e-13)
    '''electron g-factor'''

    # physico-chemical

    mu = Constant(1.660_539_068_92e-27, si.kg, relative_uncertainty=3.1e-10)
    '''atomic mass constant'''
    Mu = constant(mu * NA)
    '''molar mass constant'''
    R = constant(kB * NA)
    '''molar gas constant'''
    F = constant(NA * e)
    '''Faraday constant'''

    sigma = constant(PI**2/60 * kB**4 / (hbar**3 * c**2), 'W/m2.K4')
    '''Stefan-Boltzmann constant'''
    c1L = constant((2 * h * c**2).ito('W.m2/sr'))
    '''first radiation constant for spectral radiance'''
    c1 = constant(c1L * PI * si.sr)
    '''first radiation constant'''
    c2 = constant(h * c / kB)
    '''second radiation constant'''
    b = constant(c2 / WEIN_ZERO)
    '''Wien wavelength displacement law constant'''
    b_ = constant(WEIN_F_ZERO * c / c2, 'Hz/K')
    '''Wien frequency displacement law constant'''

    Vm = constant((R * T0 / si.ssp).ito('m3/mol'))
    '''molar volume of ideal gas (273.15 K, 100 kPa)'''
    Vmatm = constant((R * T0 / si.atm).ito('m3/mol'))
    '''molar volume of ideal gas (273.15 K, 101.325 kPa)'''
    n0 = constant(NA / Vm)
    '''Loschmidt constant (273.15 K, 100 kPa)'''
    n0atm = constant(NA / Vmatm)
    '''Loschmidt constant (273.15 K, 101.32 kPa)'''
