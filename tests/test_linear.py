import sys
import unittest
from decimal import Decimal
from fractions import Fraction

from src.siunitpy.utilcollections.abc import Linear


@unittest.skipIf(sys.version_info < (3, 9), 'only support 3.9+.')
class TestLinear(unittest.TestCase):
    def test_compatibility(self):
        a = int(1)
        self.assertTrue(isinstance(a, Linear))
        b = float(0.1)
        self.assertTrue(isinstance(b, Linear))
        c = Decimal(3.14)
        self.assertTrue(isinstance(c, Linear))
        d = Fraction(22, 7)
        self.assertTrue(isinstance(d, Linear))
        try:
            import numpy as np
            e = np.array([0, 1, 2, 3])
            self.assertTrue(isinstance(e, Linear))
        except ImportError:
            pass

