import sys
import unittest

from src.siunitpy import Dimension, DimensionConst, Unit, UnitConst


@unittest.skipIf(sys.version_info < (3, 9), 'only support 3.9+.')
class TestUnit(unittest.TestCase):
    def test_init(self):
        u0 = Unit('kg.m/s2')
        self.assertEqual(repr(u0), 'Unit(kg·m/s², dim=T⁻²LM, value=1)')
        self.assertEqual(u0.symbol, 'kg·m/s²')
        self.assertEqual(u0.dimension, DimensionConst.FORCE)
        self.assertEqual(u0.value, 1)
        u1 = Unit('kilogram.meter/second2')
        self.assertEqual(repr(u1), repr(u0))
        u2 = Unit('MeV/c2')
        self.assertEqual(u2.symbol, 'MeV/c²')
        self.assertEqual(u2.dimension, DimensionConst.MASS)
        self.assertEqual(u2.value, 1.7826619216278976e-30)
        u3 = Unit('megaelectronvolt/speed-of-light2')
        self.assertEqual(repr(u3), repr(u3))
        u4 = Unit('T.W/m2.K4')
        self.assertEqual(u4.symbol, 'T·W/m²·K⁴')
        self.assertEqual(u4.dimension, Dimension(-5, 0, 2, -1, -4, 0, 0))
        self.assertEqual(u4.value, 1)

    def test_operation(self):
        u0 = Unit("MeV/c")
        u1, factor1 = u0.deprefix_with_factor()
        self.assertEqual(u1.symbol, "eV/c")
        self.assertEqual(factor1, 1000_000)
        u2, factor2 = u0.to_basic_with_factor()
        self.assertEqual(u2.symbol, "m·kg/s")
        self.assertEqual(factor2, 5.3442859926783075e-22)
        self.assertEqual(u0.value_over(Unit(u2.symbol)), factor2)
        u3, factor3 = Unit("V/mA").simplify_with_factor()
        self.assertEqual(u3.symbol, "Ω")
        self.assertEqual(factor3, 1000)
        um = UnitConst.METER
        ukg = UnitConst.KILOGRAM
        us = UnitConst.SECOND
        self.assertEqual((ukg + um - us * 2).symbol, "kg·m/s²")

    def test_comparison(self):
        u0 = UnitConst.NEWTON
        u1 = Unit('kg.m/s2')
        u2 = Unit('N')
        self.assertEqual(u0 == u1, True)
        self.assertEqual(u0.same_as(u1), False)
        self.assertEqual(u0.same_as(u2), True)
