"""
Unitest for functionality that defines the external conditions for battery pack applications
"""

import unittest

import numpy as np

from bmslogic.simulations.applications.external_conditions import ExternalConditions


class TestExternalConditions(unittest.TestCase):
    def test_constructor(self):
        waterloo = ExternalConditions(rho=1.225, road_grade=0.3)
        self.assertEqual(1.225, waterloo.rho)
        self.assertEqual(0.3, waterloo.road_grade)
        self.assertEqual(np.arctan(0.3/100), waterloo.road_grade_angle)
        self.assertEqual(0.0, waterloo.road_force)