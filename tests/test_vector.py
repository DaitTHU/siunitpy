import sys
import unittest

from src.siunitpy.templatelib import Vector


@unittest.skipIf(sys.version_info < (3, 9), 'only support 3.9+.')
class TestVector(unittest.TestCase):
    def test_init(self):
        v0 = Vector()
        self.assertEqual(repr(v0), '[]')
        self.assertEqual(len(v0), 0)
        v1 = Vector([0, 1, 2, 3])
        self.assertEqual(repr(v1), '[0, 1, 2, 3]')
        self.assertEqual(str(v1), '[0, 1, 2, 3]')
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
        self.assertEqual(repr(v0[:2]), '[0, 1]')
        self.assertEqual(repr(v0[0, -1, 2]), '[0, 3, 2]')
        self.assertEqual(repr(v0[True, False, True]), '[0, 2]')

    def test_setitem(self):
        v0 = Vector(range(4))
        v0[:2] = range(1, 3)
        self.assertEqual(repr(v0), '[1, 2, 2, 3]')
        v0[v0 > 1] = 0
        self.assertEqual(repr(v0), '[1, 0, 0, 0]')
        v0[1:] = range(4)
        self.assertEqual(repr(v0), '[1, 0, 1, 2, 3]')

    def test_delitem(self):
        v0 = Vector(range(10))
        del v0[2:5]
        self.assertEqual(repr(v0), '[0, 1, 5, 6, 7, 8, 9]')
        del v0[v0 > 7]
        self.assertEqual(repr(v0), '[0, 1, 5, 6, 7]')
        if sys.version_info >= (3, 12):
            del v0[1, 4, 3]
            self.assertEqual(repr(v0), '[0, 5]')


    def test_operation(self):
        v0 = Vector(range(4))
        self.assertEqual(repr(-v0), '[0, -1, -2, -3]')
        self.assertEqual(repr(v0 * 3), '[0, 3, 6, 9]')
        v1 = v0 - 1
        self.assertEqual(repr(v1), '[-1, 0, 1, 2]')
        self.assertEqual(repr(abs(v1)), '[1, 0, 1, 2]')
        v2 = v0 * (v0 + 1)
        self.assertEqual(repr(v2), '[0, 2, 6, 12]')
        self.assertEqual(repr(v0 == v2 / 2), '[True, True, False, False]')

    def test_inplace_operation(self):
        v0 = Vector(range(4))
        v0 *= 2
        self.assertEqual(repr(v0), '[0, 2, 4, 6]')
        v0 <<= 3
        self.assertEqual(repr(v0), '[0, 16, 32, 48]')
    
    def test_replaced_operation(self):
        v0 = Vector(range(3))
        self.assertEqual(repr(Vector.cat(v0, v0 + 1)), '[0, 1, 2, 1, 2, 3]')
        self.assertEqual(repr(v0.repeat(2)), '[0, 1, 2, 0, 1, 2]')
        self.assertEqual(Vector.equal(v0, range(3)), True)
        v0.extend(v0 - 1)
        self.assertEqual(repr(v0), '[0, 1, 2, -1, 0, 1]')



