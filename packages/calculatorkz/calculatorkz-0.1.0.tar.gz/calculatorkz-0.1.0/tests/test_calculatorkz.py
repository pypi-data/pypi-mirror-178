from math import exp, log
from calculatorkz.calculatorkz import Calculator

import unittest

class TestStringMethods(unittest.TestCase):

    def test_addition(self):
        a = 9
        b = 2
        obj = Calculator(a, b)
        self.assertEqual(obj.add(), sum([a, b]))

    def test_n_root(self):
        a = 9
        b = 2
        obj = Calculator(a, b)
        self.assertEqual(round(obj.n_root(),3), round(exp(log(a)/b),3))

if __name__ == '__main__':
    unittest.main()