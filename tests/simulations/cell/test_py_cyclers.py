"""
Contains unittests for the Python-based cyclers objects
"""

__all__ = ["TestDischargeCycler", "TestCustomDischargeCycler"]
__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved"


import numpy as np
import unittest

from bmslogic.simulations.cell.cyclers import PyDischarge, PyCustomDischarge, PyCustomCycler


class TestDischargeCycler(unittest.TestCase):
    discharge_current = 1.5
    V_min = 2.5
    dc: PyDischarge = PyDischarge(discharge_current=discharge_current, v_min=V_min, SOC_LIB_min=0, SOC_LIB=0)

    def test_constructor(self):
        self.assertEqual(-self.discharge_current, self.dc.discharge_current)
        self.assertEqual(self.V_min, self.dc.v_min)
        self.assertEqual(0.0, self.dc.time_elapsed)
        self.assertEqual('discharge', self.dc.cycle_steps[0])

    def test_get_current(self):
        self.assertEqual(-self.discharge_current, self.dc.get_current(step_name=self.dc.cycle_steps[0]))


class TestCustomDischargeCycler(unittest.TestCase):
    def test_constructor(self):
        t_array = np.array([0,1,2])
        I_array = np.array([1,1,1])
        V_min = 2.5
        dc: PyCustomDischarge = PyCustomDischarge(t_array=t_array, I_array=I_array, V_min=V_min)
        self.assertTrue(np.array_equal(t_array, dc.t_array))
        self.assertTrue(np.array_equal(-I_array, dc.I_array))
        self.assertEqual(V_min, dc.V_min)
        self.assertEqual(0.0, dc.time_elapsed)
        self.assertEqual('discharge', dc.cycle_steps[0])
        self.assertEqual(2.0, dc.t_max)

    def test_get_current(self):
        pass


class TestCustomCycler(unittest.TestCase):
    t_array = np.arange(5)
    I_array = np.array([-1.656, 0, -1.656, 0, -2*1.656])
    V_min = 2.5
    V_max = 4.2

    def test_constructor1(self):
        cycler: PyCustomCycler = PyCustomCycler(array_t=self.t_array, array_I=self.I_array, V_min=self.V_min, V_max=self.V_max)
        self.assertEqual(0.0, cycler.time_elapsed)
        self.assertEqual(1.0, cycler.SOC_LIB)

        self.assertTrue(np.array_equal(self.t_array, cycler.array_t))
        self.assertTrue(np.array_equal(self.I_array, cycler.array_I))
        self.assertEqual(self.V_min, cycler.V_min)

        with self.assertRaises(ValueError) as context:
            PyCustomCycler(array_t=self.t_array, array_I=np.array([0]), V_min=self.V_min, V_max=self.V_max)

    def test_constructor2(self):
        cycler: PyCustomCycler = PyCustomCycler(array_t=self.t_array, array_I=self.I_array, V_min=self.V_min, V_max=self.V_max,
                              SOC_LIB=1.0)
        self.assertEqual(0.0, cycler.time_elapsed)
        self.assertEqual(1.0, cycler.SOC_LIB)

        self.assertTrue(np.array_equal(self.t_array, cycler.array_t))
        self.assertTrue(np.array_equal(self.I_array, cycler.array_I))


    def test_get_current_method(self):
        cycler: PyCustomCycler = PyCustomCycler(array_t=self.t_array, array_I=self.I_array, V_min=self.V_min, V_max=self.V_max)
        self.assertEqual(self.I_array[0], cycler.get_current(step_name='discharge', t=0))
        self.assertEqual(self.I_array[0], cycler.get_current(step_name='discharge', t=0.1))
        self.assertEqual(self.I_array[0], cycler.get_current(step_name='discharge', t=0.2))
        self.assertEqual(self.I_array[0], cycler.get_current(step_name='discharge', t=0.3))
        self.assertEqual(self.I_array[0], cycler.get_current(step_name='discharge', t=0.5))
        self.assertEqual(self.I_array[0], cycler.get_current(step_name='discharge', t=0.7))
        self.assertEqual(self.I_array[0], cycler.get_current(step_name='discharge', t=0.9))

        self.assertEqual(self.I_array[1], cycler.get_current(step_name='discharge', t=1))
        self.assertEqual(self.I_array[1], cycler.get_current(step_name='discharge', t=1.5))
        self.assertEqual(self.I_array[1], cycler.get_current(step_name='discharge', t=1.99))

        self.assertEqual(self.I_array[-2], cycler.get_current(step_name='discharge', t=3))
        self.assertEqual(self.I_array[-2], cycler.get_current(step_name='discharge', t=3.5))
        self.assertEqual(self.I_array[-2], cycler.get_current(step_name='discharge', t=3.99))

        self.assertEqual(self.I_array[-1], cycler.get_current(step_name='discharge', t=4.1))