import sys
import unittest
from decimal import Decimal
from fractions import Fraction

from src.siunitpy.utilcollections import Interval


@unittest.skipIf(sys.version_info < (3, 9), 'only support 3.9+.')
class TestInterval(unittest.TestCase):
    def test_init(self):
        i1 = Interval(0, 1)
        self.assertEqual(i1.mid, 0.5)
        self.assertEqual(i1.length, 1)
        i2 = Interval(0, 1.5)
        self.assertEqual(i2.length, 1.5)
        