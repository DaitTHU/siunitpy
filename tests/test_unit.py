import unittest
import sys
from siunitpy import Unit

@unittest.skipIf(sys.version_info < (3, 9), 'only support 3.9+.')
class TestUnit(unittest.TestCase):
    def test_init(self):
        pass

    def test_getitem(self):
        pass

    def test_setitem(self):
        pass
        

    