"""
Test for calculating the different functionalites that aid in the simulations
"""

import unittest

from bmslogic.calc_helpers.constants import Constants


class TestPhysicsConstants(unittest.TestCase):
    def test_constructor(self):
        self.assertEqual(96487, Constants.F) 
        self.assertEqual(8.3145, Constants.R) 
        self.assertEqual(273.15, Constants.T_abs) 
        self.assertEqual(9.81, Constants.g)
