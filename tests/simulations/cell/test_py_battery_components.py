"""
Contains the unittests for the Python battery component objects.
"""

__all__ = ['TestElectrode', 'TestElectrolyte', 'TestBatteryCell', 'TestECMBatteryCell']
__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by Moin Ahmed. All Rights Reserved."
__status__ = "Deployed"

import typing
import unittest

from bmslogic.simulations.cell import battery_components
from bmslogic.parameter_sets.test import funcs
from bmslogic.simulations.cell import custom_warnings_exceptions

from tests.path_definations import TEST_ELECTROLYTE_ERROR_DIR


class TestElectrode(unittest.TestCase):
    L = 7.000000e-05
    A = 5.960000e-02
    max_conc = 51410
    epsilon = 0.49
    kappa = 3.8
    S = 1.1167
    R = 8.5e-6
    T_ref = 298.15
    D_ref = 1e-14
    k_ref = 6.67e-11
    Ea_D = 29000
    Ea_R = 58000
    brugg = 1.5
    T = 298.15
    SOC_init = 0.59
    SOC = SOC_init
    soc_min, soc_max = 0.4956, 0.989011
    electrode_type = 'none'

    elec = battery_components.PyElectrode(L=L, A=A, max_conc=max_conc, epsilon=epsilon, kappa=kappa, S=S, R=R, T_ref=T_ref,
                                          D_ref=D_ref, k_ref=k_ref, Ea_D=Ea_D, Ea_R=Ea_R, brugg=brugg, T=T, SOC_init=SOC_init,
                                          soc_min=soc_min, soc_max=soc_max,
                                          alpha=0.5,
                                          func_OCP=funcs.OCP_ref_p, func_dOCPdT=funcs.dOCPdT_p)

    def test_Electrode_constructor(self):
        """
        This test methods ensures that the Electrode object is created correctly, i.e., the csv is read correctly
        and assigned to relevant instance attributes.
        """
        self.assertEqual(self.L, self.elec.L)

    def test_electrode_properties(self):
        self.assertAlmostEqual(172941.17647058822, self.elec.a_s)

    def test_invalid_SOC_init(self):
        """
        This test method checks if the constructor raises an InvalidSOCException when invalid SOC_init is passed.
        """
        T = 298.15
        # Check with a SOC below lower threshold
        SOC_init = -1
        with self.assertRaises(custom_warnings_exceptions.InvalidSOCException) as e:
            battery_components.PyElectrode(L=self.L, A=self.A, max_conc=self.max_conc, epsilon=self.epsilon,
                                           kappa=self.kappa, S=self.S, R=self.R, T_ref=self.T_ref,
                                           D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R,
                                           brugg=self.brugg, T=T,
                                           SOC_init=SOC_init, soc_min=self.soc_min, soc_max=self.soc_max,
                                           alpha=0.5, func_OCP=funcs.OCP_ref_p, func_dOCPdT=13)
        # Check with a SOC above upper threshold
        SOC_init = 1.2
        with self.assertRaises(custom_warnings_exceptions.InvalidSOCException) as e:
            battery_components.PyElectrode(L=self.L, A=self.A, max_conc=self.max_conc, epsilon=self.epsilon,
                                           kappa=self.kappa, S=self.S, R=self.R, T_ref=self.T_ref,
                                           D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R,
                                           brugg=self.brugg, T=T,
                                           SOC_init=SOC_init, soc_min=self.soc_min, soc_max=self.soc_max,
                                           alpha=0.5, func_OCP=funcs.OCP_ref_p, func_dOCPdT=13)

    def test_SOC_setter(self):
        """
        This test method checks if the SOC attribute of the Electrode object can be changes correctly.
        """
        T = 298.15
        SOC_init = 0.59
        self.assertEqual(self.elec.SOC, SOC_init)
        # Now change the SOC
        new_SOC = 0.71
        self.elec.SOC = new_SOC
        self.assertEqual(self.elec.SOC, new_SOC)
        # Now change it to invalid SOC, i.e, SOC < 0
        new_SOC = -1
        with self.assertRaises(custom_warnings_exceptions.InvalidSOCException):
            self.elec.SOC = new_SOC
        # Now change it to another invalid SOC, i.e, SOC > 1
        new_SOC = 1.1
        with self.assertRaises(custom_warnings_exceptions.InvalidSOCException):
            self.elec.SOC = new_SOC

    def test_invalid_func_OCP_input(self):
        """
        This test method checks if the constructor raises a TypeError when an invalid function is passed for the
        func_OCP parameter.
        """
        T = 298.15
        SOC_init = 0.59
        with self.assertRaises(TypeError) as context_manager:
            # Create an instance of Electrode object using a value (instead of a valid function) for func_OCP parameter.
            elec = battery_components.PyElectrode(L=self.L, A=self.A, max_conc=self.max_conc, epsilon=self.epsilon,
                                                  kappa=self.kappa, S=self.S, R=self.R, T_ref=self.T_ref,
                                                  D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R,
                                                  brugg=self.brugg, T=T,
                                                  SOC_init=self.SOC_init,
                                                  soc_min=self.soc_min, soc_max=self.soc_max,
                                                  alpha=0.5, func_OCP=13, func_dOCPdT=funcs.dOCPdT_p)

    def test_invalid_func_dOCPdT_input(self):
        """
        This test method checks if the constructor raises a TypeError when an invalid function is passed for the
        func_dOCPdT parameter.
        """
        T = 298.15
        SOC_init = 0.59
        with self.assertRaises(TypeError):
            # Create an instance of the Electrode object using a value (instead of a valid function) for func_dOCPdT
            # parameter.
            elec = battery_components.PyElectrode(L=self.L, A=self.A, max_conc=self.max_conc, epsilon=self.epsilon,
                                                  kappa=self.kappa, S=self.S, R=self.R, T_ref=self.T_ref,
                                                  D_ref=self.D_ref, k_ref=self.k_ref, Ea_D=self.Ea_D, Ea_R=self.Ea_R,
                                                  brugg=self.brugg, T=T,
                                                  SOC_init=self.SOC_init,
                                                  soc_min=self.soc_min, soc_max=self.soc_max,
                                                  alpha=0.5, func_OCP=funcs.OCP_ref_p, func_dOCPdT=13)
            

class TestElectrolyte(unittest.TestCase):
    L = 2e-5
    c_init = 1000.0
    kappa = 0.2875
    epsilon = 0.724
    brugg = 1.5
    test_electrolyte = battery_components.PyElectrolyte(L=L, conc=c_init, kappa=kappa, brugg=brugg, epsilon_sep=epsilon)

    def test_constructor(self):
        """
        This test checks if the constructor of the Electrolyte class is able to read the parameters from the csv file
        and assign the class attributes correctly.
        """
        self.assertEqual(self.c_init, self.test_electrolyte.conc)
        self.assertEqual(self.L, self.test_electrolyte.L)
        self.assertEqual(self.kappa, self.test_electrolyte.kappa)
        self.assertEqual(self.epsilon, self.test_electrolyte.epsilon_sep)
        self.assertEqual(self.brugg, self.test_electrolyte.brugg)

    def test_property(self):
        self.assertEqual(0.1771110665373567, self.test_electrolyte.kappa_sep_eff)

    def test_constructur_raises(self):
        with self.assertRaises(TypeError) as context:
            battery_components.PyElectrolyte(TEST_ELECTROLYTE_ERROR_DIR)


class TestBatteryCell(unittest.TestCase):
    T = 298.15
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    test_cell = battery_components.PyBatteryCell.read_from_parametersets(parameter_set_name='test',
                                                         soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                         temp_init=T)
    test_cell_sp = battery_components.PyBatteryCell.read_from_parametersets(parameter_set_name="test_single_particle_only",
                                                            soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                            temp_init=T)

    def test_negative_electrode_parameters(self):
        """
        This test method test the constructor of the BatteryCell class.
        """
        self.assertEqual(self.test_cell.elec_n.L, 7.35e-05)
        self.assertEqual(self.test_cell.elec_n.A, 5.960000e-02)
        self.assertEqual(self.test_cell.elec_n.max_conc, 31833)
        self.assertEqual(self.test_cell.elec_n.epsilon, 0.59)
        self.assertEqual(self.test_cell.elec_n.kappa, 100)
        self.assertEqual(self.test_cell.elec_n.S, 0.7824)
        self.assertEqual(self.test_cell.elec_n.R, 12.5e-6)
        self.assertEqual(self.test_cell.elec_n.T_ref, 298.15)
        self.assertEqual(self.test_cell.elec_n.D_ref, 3.9e-14)
        self.assertEqual(self.test_cell.elec_n.k_ref, 1.76e-11)
        self.assertEqual(self.test_cell.elec_n.Ea_D, 35000)
        self.assertEqual(self.test_cell.elec_n.Ea_R, 20000)
        self.assertEqual(self.test_cell.elec_n.brugg, 1.5)
        self.assertEqual(self.test_cell.elec_n.T, 298.15)
        self.assertEqual(self.test_cell.elec_n.SOC, self.SOC_init_n)
        self.assertEqual(0.01890232, self.test_cell.elec_n.soc_min)
        self.assertEqual(0.7568, self.test_cell.elec_n.soc_max)
        self.assertEqual(0.7568, self.test_cell.elec_n.SOC)
        self.assertEqual(self.test_cell.elec_n.electrode_type, 'n')

    def test_positive_electrode(self):
        """
        Tests the attributes of the battery cell's positive electrode.
        """
        self.assertEqual(0.0596, self.test_cell.elec_p.A)
        self.assertEqual(7e-5, self.test_cell.elec_p.L)
        self.assertEqual(3.8, self.test_cell.elec_p.kappa)
        self.assertEqual(0.49, self.test_cell.elec_p.epsilon)
        self.assertEqual(1.1167, self.test_cell.elec_p.S)
        self.assertEqual(51410, self.test_cell.elec_p.max_conc)
        self.assertEqual(8.5e-6, self.test_cell.elec_p.R)
        self.assertEqual(6.67e-11, self.test_cell.elec_p.k_ref)
        self.assertEqual(1e-14, self.test_cell.elec_p.D_ref)
        self.assertEqual(5.8e4, self.test_cell.elec_p.Ea_R)
        self.assertEqual(2.9e4, self.test_cell.elec_p.Ea_D)
        self.assertEqual(0.5, self.test_cell.elec_p.alpha)
        self.assertEqual(1.5, self.test_cell.elec_p.brugg)
        self.assertEqual(0.4956, self.test_cell.elec_p.soc_min)
        self.assertEqual(0.989011, self.test_cell.elec_p.soc_max)
        self.assertEqual(0.4956, self.test_cell.elec_p.SOC)

    def test_electrolyte_parameters(self):
        self.assertEqual(self.test_cell.electrolyte.conc, 1000)
        self.assertEqual(self.test_cell.electrolyte.L, 2e-5)
        self.assertEqual(self.test_cell.electrolyte.kappa, 0.2875)
        self.assertEqual(self.test_cell.electrolyte.epsilon_sep, 0.724)
        self.assertEqual(self.test_cell.electrolyte.brugg, 1.5)
        self.assertEqual(0.38, self.test_cell.electrolyte.t_c)
        self.assertEqual(3.5e-10, self.test_cell.electrolyte.D_e)
        self.assertEqual(0.385, self.test_cell.electrolyte.epsilon_n)
        self.assertEqual(0.485, self.test_cell.electrolyte.epsilon_p)

        # tests for the test parameter named "test_single_particle_only"
        self.assertEqual(1000, self.test_cell.electrolyte.conc)
        self.assertEqual(2e-5, self.test_cell.electrolyte.L)
        self.assertEqual(0.2875, self.test_cell.electrolyte.kappa)
        self.assertEqual(0.724, self.test_cell.electrolyte.epsilon_sep)
        self.assertEqual(1.5, self.test_cell.electrolyte.brugg)
        self.assertEqual(None, self.test_cell_sp.electrolyte.t_c)
        self.assertEqual(None, self.test_cell_sp.electrolyte.D_e)
        self.assertEqual(None, self.test_cell_sp.electrolyte.epsilon_n)
        self.assertEqual(None, self.test_cell_sp.electrolyte.epsilon_p)

    def test_battery_cell_parameters(self):
        # below tests for the battery cell parameters
        self.assertEqual(self.test_cell.rho, 1626)
        self.assertEqual(self.test_cell.Vol, 3.38e-5)
        self.assertEqual(self.test_cell.C_p, 750)
        self.assertEqual(self.test_cell.h, 1)
        self.assertEqual(self.test_cell.A, 0.085)
        self.assertEqual(self.test_cell.cap, 1.65)
        self.assertEqual(self.test_cell.V_max, 4.2)
        self.assertEqual(self.test_cell.V_min, 2.5)

    def test_R_cell(self):
        self.assertEqual(0.0028230038442483246, self.test_cell.R_cell)

    def test_temp(self):
        """
        This test method checks if the temperature is properly assigned to the object after the temperature
        parameter is changed.
        :return:
        """
        T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        test_cell = battery_components.PyBatteryCell.read_from_parametersets(parameter_set_name='test',
                                                             soc_init_p=SOC_init_p,
                                                             soc_init_n=SOC_init_n,
                                                             temp_init=T)

        self.assertEqual(test_cell.T, T)
        self.assertEqual(test_cell.elec_p.T, T)
        self.assertEqual(test_cell.elec_n.T, T)
        # change T and check if the battery and electrode temperature changes as well.
        new_T = 313.15
        test_cell.T = new_T
        self.assertEqual(test_cell.T, new_T)
        self.assertEqual(test_cell.elec_p.T, new_T)
        self.assertEqual(test_cell.elec_n.T, new_T)

    def test_temp_amb(self):
        """
        test_T_amb test if the ambient temperature stays constant even after temperature parameter change.
        """
        orig_T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        test_cell = battery_components.PyBatteryCell.read_from_parametersets(parameter_set_name='test',
                                                             soc_init_p=SOC_init_p,
                                                             soc_init_n=SOC_init_n,
                                                             temp_init=orig_T)

        self.assertEqual(test_cell.T_amb, orig_T)
        # Now change to new T but T_amb should not change
        new_T = 313.15
        test_cell.T = new_T
        self.assertEqual(test_cell.T_amb, orig_T)

    def test_get_electrode_soc_from_lib_soc(self):
        soc_p_0, soc_n_0 = self.test_cell._get_electrode_soc_from_lib_soc(soc_lib=0.0,
                                                                          soc_p_min=0.4956, soc_p_max=0.989011,
                                                                          soc_n_min=0.01890232, soc_n_max=0.7568)
        self.assertEqual(0.989011, soc_p_0)
        self.assertEqual(0.01890232, soc_n_0)

        soc_p_1, soc_n_1 = self.test_cell._get_electrode_soc_from_lib_soc(soc_lib=1.0,
                                                                          soc_p_min=0.4956, soc_p_max=0.989011,
                                                                          soc_n_min=0.01890232, soc_n_max=0.7568)
        self.assertEqual(0.4956, soc_p_1)
        self.assertEqual(0.7568, soc_n_1)


class TestECMBatteryCell(unittest.TestCase):

    @staticmethod
    def func_ocv(soc: float) -> float:
        return 2.5 + 1.7 * soc

    @staticmethod
    def func_docvdtemp(soc: float):
        return 1.0

    @staticmethod
    def func_eta(soc: float, temp: float) -> float:
        return 1.0

    test_cell_Thevenin = battery_components.PyECMBatteryCell(R0_ref=0.225, R1_ref=0.001, C1=0.03, temp_ref=298.15, Ea_R1=400, Ea_R0=400,
                                             rho=1626, vol=3.38e-5, c_p=750, h=1, area=0.085,
                                             func_eta=func_eta, func_ocv=func_ocv, func_docvdtemp=func_docvdtemp,
                                             soc_init=0.1, temp_init=298.15,
                                             cap=1.65, v_max=4.2, v_min=2.5)

    test_cell_ESC = battery_components.PyECMBatteryCell(R0_ref=0.225, R1_ref=0.001, C1=0.03, temp_ref=298.15, Ea_R1=400, Ea_R0=400,
                                        rho=1626, vol=3.38e-5, c_p=750, h=1, area=0.085,
                                        func_eta=func_eta, func_ocv=func_ocv, func_docvdtemp=func_docvdtemp,
                                        soc_init=0.1, temp_init=298.15,
                                        cap=1.65, v_max=4.2, v_min=2.5,
                                        M_0=4.4782e-4, M=0.0012)

    def test_battery_cell_parameters_for_Thevenin_simulations(self):
        self.assertEqual(self.test_cell_Thevenin.rho, 1626)
        self.assertEqual(self.test_cell_Thevenin.vol, 3.38e-5)
        self.assertEqual(self.test_cell_Thevenin.c_p, 750)
        self.assertEqual(self.test_cell_Thevenin.h, 1)
        self.assertEqual(self.test_cell_Thevenin.area, 0.085)
        self.assertEqual(self.test_cell_Thevenin.cap, 1.65)
        self.assertEqual(self.test_cell_Thevenin.v_max, 4.2)
        self.assertEqual(self.test_cell_Thevenin.v_min, 2.5)

        self.assertTrue(isinstance(self.test_cell_Thevenin.func_ocv, typing.Callable))
        self.assertEqual(2.5, self.test_cell_Thevenin.func_ocv(soc=0.0))
        self.assertEqual(3.35, self.test_cell_Thevenin.func_ocv(soc=0.5))
        self.assertEqual(4.2, self.test_cell_Thevenin.func_ocv(soc=1.0))

        self.assertTrue(isinstance(self.test_cell_Thevenin.func_eta, typing.Callable))

        self.assertTrue(isinstance(self.test_cell_Thevenin.func_docvdtemp, typing.Callable))

        self.assertTrue(self.test_cell_Thevenin.M is None)
        self.assertTrue(self.test_cell_Thevenin.M_0 is None)

    def test_battery_cell_parameters_for_ESC_simulations(self):
        self.assertEqual(self.test_cell_ESC.rho, 1626)
        self.assertEqual(self.test_cell_ESC.vol, 3.38e-5)
        self.assertEqual(self.test_cell_ESC.c_p, 750)
        self.assertEqual(self.test_cell_ESC.h, 1)
        self.assertEqual(self.test_cell_ESC.area, 0.085)
        self.assertEqual(self.test_cell_ESC.cap, 1.65)
        self.assertEqual(self.test_cell_ESC.v_max, 4.2)
        self.assertEqual(self.test_cell_ESC.v_min, 2.5)

        self.assertTrue(isinstance(self.test_cell_ESC.func_ocv, typing.Callable))
        self.assertEqual(2.5, self.test_cell_ESC.func_ocv(soc=0.0))
        self.assertEqual(3.35, self.test_cell_ESC.func_ocv(soc=0.5))
        self.assertEqual(4.2, self.test_cell_ESC.func_ocv(soc=1.0))

        self.assertTrue(isinstance(self.test_cell_ESC.func_eta, typing.Callable))

        self.assertTrue(isinstance(self.test_cell_ESC.func_docvdtemp, typing.Callable))

        self.assertEqual(4.4782e-4, self.test_cell_ESC.M_0)
        self.assertEqual(0.0012, self.test_cell_ESC.M)

    def test_read_from_parameterset(self):
        b_cell: battery_components.PyECMBatteryCell = battery_components.PyECMBatteryCell.read_from_parametersets(parameter_set_name='test',
                                                                                  soc_init=1.0, temp_init=298.15)
        self.assertEqual(0.005, b_cell.R0_ref)
        self.assertTrue(0.001, b_cell.R1_ref)
        self.assertTrue(0.03, b_cell.C1)
        self.assertTrue(298.15, b_cell.temp_ref)
        self.assertTrue(400, b_cell.Ea_R0)
        self.assertTrue(400, b_cell.Ea_R1)

        self.assertTrue(1626, b_cell.rho)
        self.assertTrue(3.38e-5, b_cell.vol)
        self.assertTrue(750, b_cell.c_p)
        self.assertTrue(0.085, b_cell.h)
        self.assertTrue(1, b_cell.area)
        self.assertTrue(1.65, b_cell.cap)
        self.assertTrue(4.2, b_cell.v_max)
        self.assertTrue(2.5, b_cell.v_min)

        self.assertEqual(1.0, b_cell.func_eta(0.5, 298.15))
        self.assertEqual(3.7913774209371964, b_cell.func_ocv(0.5))
        self.assertEqual(-0.0002942358440153894, b_cell.func_docvdtemp(0.5))
