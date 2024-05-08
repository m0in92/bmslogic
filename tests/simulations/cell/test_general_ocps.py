"""
Unittests for testing the accuracy the package's open-circuit potential vs. state-of-charge relationships.
"""

__all__ = ["TestPositiveElectrode", "TestNegativeElectrode"]
__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."

import unittest

from bmslogic.simulations.cell.cell import LCO, NMC, LFP, LMO, NCA, graphite


class TestPositiveElectrode(unittest.TestCase):
    """unittests for checking the accuracy of the builtin battery cell open-circuit potential.
    """
    def test_LCO(self):
        self.assertEqual(4.285360210873217, LCO(soc=0.4))

    def test_NMC(self):
        self.assertEqual(4.284634512069273, NMC(soc=0.4))

    def test_LMO(self):
        self.assertEqual(4.11498733610216, LMO(soc=0.4))

    def test_NCA(self):
        self.assertEqual(3.9724133989368675, NCA(soc=0.4))

    def test_LFP(self):
        self.assertEqual(3.4201900441811737, LFP(soc=0.4))


class TestNegativeElectrode(unittest.TestCase):
    """unittests for checking the accuracy of the builtin battery cell open-circuit potential.
    """
    def test_negative_electrode(self):
        self.assertEqual(0.11527367325125464, graphite(soc=0.4))
