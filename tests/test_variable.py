import sys
import unittest

from src.siunitpy import Variable
from src.siunitpy.identity import zero
from src.siunitpy.utilcollections import Interval


@unittest.skipIf(sys.version_info < (3, 9), 'only support 3.9+.')
class TestVariable(unittest.TestCase):
    def test_init(self):
        v0 = Variable(100)
        self.assertEqual(v0.value, 100)
        self.assertEqual(v0.uncertainty, zero)
        self.assertEqual(v0.confidence_interval, Interval(100, 100))
        self.assertEqual(repr(v0), 'Variable(100, uncertainty=0)')
        self.assertEqual(str(v0), '100')
        v1 = Variable(10.0, 0.1)
        self.assertEqual(v1.uncertainty, 0.1)
        self.assertEqual(v1.confidence_interval, Interval(9.9, 10.1))
        self.assertEqual(repr(v1), 'Variable(10.0, uncertainty=0.1)')
        self.assertEqual(str(v1), '10.0 ± 0.1')

    def test_operation(self):
        v0 = Variable(100.0)
        v1 = Variable(100.0, 1e-3)
        self.assertEqual(v0 == v1, True)
        v2 = Variable(99.0, 1e-3)
        self.assertEqual(v0 > v2, True)
        self.assertEqual(v0 <= v2, False)
        self.assertEqual(-v2, Variable(-99, 1))
        v3 = v0 + v1
        self.assertEqual(v3.value, 200)
        self.assertEqual(v3.uncertainty, 1e-3)




