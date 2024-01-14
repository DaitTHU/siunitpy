import unittest
import sys
from siunitpy import Vector

@unittest.skipIf(sys.version_info < (3, 9), 'only support 3.9+.')
class TestVector(unittest.TestCase):
    def test_init(self):
        v0 = Vector()
        self.assertEqual(repr(v0), '[]')
        self.assertEqual(len(v0), 0)
        v1 = Vector([0, 1, 2, 3])
        self.assertEqual(repr(v1), '[0, 1, 2, 3]')
        self.assertEqual(len(v1), 4)
        v2 = Vector(range(4))
        self.assertEqual(repr(v2), '[0, 1, 2, 3]')
        self.assertEqual(len(v2), 4)
        v3 = Vector.packup(0, 1, 2, 3)
        self.assertEqual(repr(v3), '[0, 1, 2, 3]')
        self.assertEqual(len(v3), 4)

    def test_getitem(self):
        v0 = Vector(range(4))
        self.assertEqual(v0[3], 3)
        self.assertEqual(v0[-1], 3)
        self.assertListEqual(v0[:2], Vector([0, 1]))
        self.assertListEqual(v0[0, -1, 2], Vector([0, 3, 2]))
        self.assertListEqual(v0[True, False, True], Vector([0, 2]))

    def test_setitem(self):
        v0 = Vector(range(7))
        

    