"""
Unittests for the battery cell simulations
"""

__all__ = ["TestBaseCycler", "TestDischargeCycler", "TestDischargeRest", "TestCharge", "TestChargeDischarge", "TestCustomCycler"]
__author__ = "Moin Ahmed"
__copyright__ = "Copyright by BMSLogic 2024. All Rights Reserved."
__status__ = "Deployed"

import unittest

import numpy as np

import bmslogic.simulations.cell.cell as slv
from bmslogic.simulations.cell import pycyclers


class TestBaseCycler(unittest.TestCase):
    """Class to Test the properties and methods of the BaseCycler class.

    Args:
        unittest (): Python's unititest Testcasses
    """

    def test_constructor(self):
        cycler: slv.BaseCycler = slv.BaseCycler()
        self.assertEqual(0.0, cycler.time_elapsed)
        self.assertEqual(2.5, cycler.V_min)
        self.assertEqual(0.0, cycler.rest_time)
        self.assertEqual(1, cycler.num_cycles)


class TestDischargeCycler(unittest.TestCase):
    # Creation of an instance for unittesting.
    discharge_current: float = 1.5
    V_min: float = 2.5
    soc_lib_min: float = 0.0
    soc_lib: float = 0.0
    dc: slv.Discharge = slv.Discharge(
        current=discharge_current, V_min=V_min, soc_lib_min=soc_lib_min, soc_lib=soc_lib)

    def test_properties(self):
        """
        Tests the properties of the Discharge class.
        """
        self.assertEqual(self.V_min, self.dc.V_min)
        self.assertEqual(0.0, self.dc.time_elapsed)
        self.assertEqual(2.5, self.dc.V_min)
        self.assertEqual(0.0, self.dc.rest_time)
        self.assertEqual(1, self.dc.num_cycles)

    def test_methods_get_current(self):
        """
        Tests the method get_current of the Discharge class.
        """
        self.assertEqual(-self.discharge_current,
                         self.dc.get_current(cycling_step="discharge", t=0))


class TestDischargeRest(unittest.TestCase):
    # Creation of an instance for unittesting.
    discharge_current: float = 1.5
    V_min: float = 2.5
    soc_lib_min: float = 0.0
    soc_lib: float = 0.0
    rest_time: float = 3600  # in s
    cycler: slv.DischargeRest = slv.DischargeRest(current=discharge_current, V_min=V_min,
                                                  soc_lib_min=soc_lib_min, soc_lib=soc_lib,
                                                  rest_time=rest_time)

    def test_properties(self):
        self.assertEqual(self.V_min, self.cycler.V_min)
        self.assertEqual(self.rest_time, self.cycler.rest_time)
        self.assertEqual(0.0, self.cycler.time_elapsed)

    def test_method_get_current(self):
        self.assertEqual(-self.discharge_current,
                         self.cycler.get_current(cycling_step="discharge", t=0))
        self.assertEqual(0.0, self.cycler.get_current(
            cycling_step="rest", t=1))


class TestCharge(unittest.TestCase):
    """contains the unittests for the Charge instance.

    Parameters
    ----------
    unittest : Python's built-in unittest package.
        Use of unittest's TestCases.
    """
    # Creation of an instance for unittesting.
    charge_current: float = 1.5
    V_max: float = 4.2
    soc_lib_min: float = 0.0
    soc_lib: float = 0.0

    dc: slv.Discharge = slv.Charge(
        current=charge_current, V_max=V_max, soc_lib_max=soc_lib_min, soc_lib=soc_lib)

    def test_properties(self):
        """Tests the properties of the Charge class.
        """
        self.assertEqual(self.V_max, self.dc.V_max)
        self.assertEqual(0.0, self.dc.time_elapsed)
        self.assertEqual(0.0, self.dc.rest_time)
        self.assertEqual(1, self.dc.num_cycles)

    def test_methods_get_current(self):
        """Tests the method get_current of the Charge class.
        """
        self.assertEqual(self.charge_current, self.dc.get_current(
            cycling_step="charge", t=0))


class TestChargeDischarge(unittest.TestCase):
    charge_current: float = 1.5
    discharge_current: float = 1.5
    soc_lib_min: float = 0.0
    soc_lib_max: float = 1.0
    V_min: float = 2.5
    V_max: float = 4.2
    rest_time: float = 3600  # in seconds

    cycler: slv.ChargeDischarge = slv.ChargeDischarge(charge_current=charge_current, discharge_current=discharge_current,
                                                      V_min=V_min, V_max=V_max,
                                                      soc_min=soc_lib_min, soc_max=soc_lib_max, soc=0.0,
                                                      rest_time=rest_time)

    def test_properties(self):
        self.assertEqual(self.V_max, self.cycler.V_max)
        self.assertEqual(self.V_min, self.cycler.V_min)
        self.assertEqual(0.0, self.cycler.time_elapsed)
        self.assertEqual(self.rest_time, self.cycler.rest_time)
        self.assertEqual(1, self.cycler.num_cycles)

    def test_method_get_current(self):
        self.assertEqual(self.charge_current,
                         self.cycler.get_current("charge", 0))
        self.assertEqual(-self.discharge_current,
                         self.cycler.get_current("discharge", 0))


class TestCustomCycler(unittest.TestCase):
    t: np.ndarray = np.linspace(0, 3600, 3601)
    I: np.ndarray = -1.656 * np.ones(len(t))

    soc_lib_min: float = 0.0
    soc_lib_max: float = 1.0
    V_min: float = 2.5
    V_max: float = 4.2
    soc_lib: float = 0.0

    cycler: slv.CustomCycler = slv.CustomCycler(t_array=t, current_array=I,
                                                V_min=V_min, V_max=V_max,
                                                soc_lib_min=soc_lib_min, soc_lib_max=soc_lib_max,
                                                soc_lib=soc_lib)

    def test_properties(self):
        self.assertTrue(np.array_equal(self.t, self.cycler.t_array))
        self.assertTrue(np.array_equal(self.I, self.cycler.current_array))
        self.assertEqual(self.V_max, self.cycler.V_max)
        self.assertEqual(self.V_min, self.cycler.V_min)

    def test_method_get_current(self):
        self.assertEqual(-1.656, self.cycler.get_current("custom", 0))
        self.assertEqual(-1.656, self.cycler.get_current("custom", 100))


class TestHPPCCyler(unittest.TestCase):
    def test_constructor(self):
        with self.assertRaises(ValueError):
            pycyclers.HPPCCycler(t1=500.0, t2=100, i_app=1.5, charge_or_discharge='whatever',
                                 V_min=2.5, V_max=4.2, soc_lib_min=0.0, soc_lib_max=1.0, soc_lib=1.0)

    def test_properties(self):
        cycler: pycyclers.HPPCCycler = pycyclers.HPPCCycler(t1=1, t2=1, i_app=1.5,
                                                            charge_or_discharge='discharge',
                                                            V_min=2.5, V_max=4.2, soc_lib_min=0.0,
                                                            soc_lib_max=1.0, soc_lib=1.0, hppc_steps=2)
        t_array_actual: np.ndarray = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                                               1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
                                               2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0,
                                               3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0])
        I_array_actual: np.ndarray = np.array([0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.5,
                                               -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5,
                                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.5,
                                               -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5])
        self.assertTrue(np.isclose(t_array_actual, cycler.t_array).all())
        self.assertTrue(np.isclose(I_array_actual, cycler.current_array).all())


class TestDSTCycler(unittest.TestCase):
    def test_properties(self):
        pass
