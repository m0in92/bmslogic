"""
Contains unittests for the Python-based battery cell solvers.
"""

__all__ = ["TestSPSolverBasic", "TestSPSolverMethods",
           "TestSPSolerIsothermal", "TestSPSolverNonIsothermal", "TestESPSolver"]

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."
__status__ = "Deployed"

import unittest
import numpy as np

from bmslogic.simulations.cell.custom_warnings_exceptions import *
from bmslogic.simulations.cell.battery_components import PyBatteryCell
from bmslogic.simulations.cell.cyclers import PyDischarge
from bmslogic.simulations.cell.solvers.battery import PySPSolver, PyEnhancedSPSolver


class TestSPSolverBasic(unittest.TestCase):
    """
    Basic test to ensure its basic functionalities.
    """
    T = 298.15
    N = 5
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    t = np.arange(0, 4000, 0.1)
    I = -1.656 * np.ones(len(t))
    test_cell = PyBatteryCell.read_from_parametersets(parameter_set_name='test',
                                                      soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                      temp_init=T)
    test_solver = PySPSolver(b_cell=test_cell, N=N,
                             isothermal=True, degradation=False)

    def test_constructor(self):
        self.assertEqual(self.N, self.test_solver.N)
        self.assertEqual(self.test_cell, self.test_solver.b_cell)
        self.assertTrue(self.test_solver.bool_isothermal)
        self.assertFalse(self.test_solver.bool_degradation)

    def test_invalid_constructor_arguments(self):
        with self.assertRaises(TypeError):
            PySPSolver(b_cell=self.test_cell, isothermal=13, degradation=False)
        with self.assertRaises(TypeError):
            PySPSolver(b_cell=self.test_cell, isothermal=True, degradation=13)


class TestSPSolverMethods(unittest.TestCase):
    N = 5
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    I = 1.656
    T = 298.15
    V_min = 4.0
    SOC_min = 0.1
    SOC_LIB = 0.9
    test_cell = PyBatteryCell.read_from_parametersets(parameter_set_name='test',
                                                      soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                      temp_init=T)

    def test_solve(self):
        dc = PyDischarge(discharge_current=self.I, v_min=self.V_min,
                         SOC_LIB_min=self.SOC_min, SOC_LIB=self.SOC_LIB)
        test_solver = PySPSolver(
            b_cell=self.test_cell, isothermal=True, degradation=False)

        with self.assertRaises(TypeError) as context:
            test_solver.solve(cycler_instance=0)


class TestSPSolverIsothermal(unittest.TestCase):
    """
    Test the values of the simulation in a isothermal simulation. The test are conducted in a single discharge step
    cycle.
    """
    N = 5
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    I = 1.656
    T = 298.15
    V_min = 4.0
    SOC_min = 0.1
    SOC_LIB = 0.9
    test_cell = PyBatteryCell.read_from_parametersets(parameter_set_name='test',
                                                      soc_init_p=SOC_init_p,
                                                      soc_init_n=SOC_init_n,
                                                      temp_init=T)
    test_solver = PySPSolver(
        b_cell=test_cell, isothermal=True, degradation=False)
    dc = PyDischarge(discharge_current=I, v_min=V_min,
                     SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
    sol = test_solver.solve(cycler_instance=dc)

    def test_terminal_potential(self):
        """
        Test the battery cell terminal voltage.
        """
        self.assertEqual(4.017944458468085, self.sol.V[0])
        self.assertEqual(4.0178735493136415, self.sol.V[1])
        self.assertEqual(4.01780271676398, self.sol.V[2])
        self.assertEqual(4.017731960073281, self.sol.V[3])
        self.assertEqual(4.017661278502599, self.sol.V[4])

    def test_cell_temperature(self):
        """
        Test the battery cell temperatures.
        """
        self.assertEqual(298.15, self.sol.T[0])
        self.assertEqual(298.15, self.sol.T[1])
        self.assertEqual(298.15, self.sol.T[2])
        self.assertEqual(298.15, self.sol.T[3])
        self.assertEqual(298.15, self.sol.T[4])

    def test_poly_solver(self):
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        I = 1.656
        V_min = 3.5
        SOC_min = 0.1
        SOC_LIB = 0.9
        T = 298.15
        test_cell = PyBatteryCell.read_from_parametersets(parameter_set_name='test',
                                                          soc_init_p=SOC_init_p,
                                                          soc_init_n=SOC_init_n,
                                                          temp_init=T)
        dc = PyDischarge(discharge_current=I, v_min=V_min,
                         SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
        test_solver = PySPSolver(b_cell=self.test_cell, isothermal=True, degradation=False,
                                 electrode_SOC_solver="poly", type='two')
        sol = test_solver.solve(cycler_instance=dc)
        print(sol.V[0])
        self.assertEqual(3.9248673125333613, sol.V[0])


class TestSPSolverNonIsothermal(unittest.TestCase):
    """
    Test the values of the simulation in a non-isothermal simulation. The test are conducted in a single discharge step
    cycle.
    """
    N = 5
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    I = 1.656
    T = 298.15
    V_min = 4.0
    SOC_min = 0.1
    SOC_LIB = 0.9
    test_cell = PyBatteryCell.read_from_parametersets(parameter_set_name='test',
                                                      soc_init_p=SOC_init_p,
                                                      soc_init_n=SOC_init_n,
                                                      temp_init=T)
    test_solver = PySPSolver(
        b_cell=test_cell, isothermal=False, degradation=False)
    dc = PyDischarge(discharge_current=I, v_min=V_min,
                     SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
    sol = test_solver.solve(cycler_instance=dc)

    def test_terminal_potential(self):
        """
        Test the battery cell terminal voltage.
        """
        self.assertEqual(4.017944458468085, self.sol.V[0])
        self.assertEqual(4.017873715136176, self.sol.V[1])
        self.assertEqual(4.017803045441758, self.sol.V[2])
        self.assertEqual(4.017732448639317, self.sol.V[3])
        self.assertEqual(4.017661923990237, self.sol.V[4])

    def test_cell_temperature(self):
        """
        Test the battery cell temperatures.
        """
        self.assertEqual(298.15007654854116, self.sol.T[0])
        self.assertEqual(298.15015162076287, self.sol.T[1])
        self.assertEqual(298.1502252195381, self.sol.T[2])
        self.assertEqual(298.1502973477614, self.sol.T[3])
        self.assertEqual(298.1503680083491, self.sol.T[4])


class TestESPSolver(unittest.TestCase):
    """
    This class contains the test cases for initializing and performing simulations using solver for single particle model
    with electrolyte dynamics
    """
    T = 298.15
    N = 5
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    t = np.arange(0, 4000, 0.1)
    I = -1.656 * np.ones(len(t))
    test_cell = PyBatteryCell.read_from_parametersets(parameter_set_name='test',
                                                         soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                         temp_init=T)

    def test_constructor(self):
        test_solver = PyEnhancedSPSolver(b_cell=self.test_cell, isothermal=True, degradation=False)

        self.assertEqual(self.test_cell.elec_p.a_s, test_solver.b_cell.elec_p.a_s)
        self.assertEqual(True, test_solver.bool_isothermal)
        self.assertEqual(False, test_solver.bool_degradation)
        self.assertEqual('poly', test_solver.electrode_SOC_solver)

        self.assertEqual(7.35e-5 / 10, test_solver.electrolyte_co_ords.dx_n)
        self.assertEqual(2.0e-5 / 10, test_solver.electrolyte_co_ords.dx_s)

        self.assertEqual([], test_solver.sol_init.lst_V)

        c_init: np.ndarray = 1000 * np.ones(30)
        c_init = c_init[np.newaxis, :]
        self.assertTrue(np.array_equal(c_init, test_solver.sol_init.electrolyte_conc[1:]))

    def test_constructor_with_insufficient_parameters(self):
        b_cell: PyBatteryCell = PyBatteryCell.read_from_parametersets(parameter_set_name="test_single_particle_only",
                                                                            soc_init_p=self.SOC_init_p,
                                                                            soc_init_n=self.SOC_init_n,
                                                                            temp_init=self.T)
        with self.assertRaises(InsufficientParameters):
            test_solver = PyEnhancedSPSolver(b_cell=b_cell, isothermal=True, degradation=False)

