import sys
import unittest

from src.siunitpy import Dimension, DimensionConst


@unittest.skipIf(sys.version_info < (3, 9), 'only support 3.9+.')
class TestDimension(unittest.TestCase):
    def test_init(self):
        v = Dimension(1, 0, -1, 0, 0, 0, 0)
        self.assertEqual(
            repr(v), 'Dimension(L=1, M=0, T=-1, I=0, H=0, N=0, J=0)')
        self.assertEqual(str(v), '(1, 0, -1, 0, 0, 0, 0)')
        self.assertEqual(v.L, 1)
        self.assertEqual(v.mass, 0)
        self.assertEqual(v.time, -1)

    def test_operation(self):
        dl = DimensionConst.LENGTH
        dm = DimensionConst.MASS
        dt = DimensionConst.TIME
        dv = DimensionConst.VILOCITY
        df = DimensionConst.FORCE
        self.assertEqual(str(-df), '(-1, -1, 2, 0, 0, 0, 0)')
        self.assertEqual(dl - dt, dv)
        self.assertEqual(dm + dl - dt * 2, df)
