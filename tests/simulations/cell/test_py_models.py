"""
Contains the unittests for the battery cell models
"""

__all__ = ["TestSPModel", "TestESP", "TestP2DM", "TestLumped"]

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2023 by Moin Ahmed. All Rights Reserved."
__status__ = "Deployed"

import unittest

import numpy as np

from bmslogic.simulations.cell import models
from bmslogic.simulations.cell import battery_components


"""
Below are the tests for the battery models
"""


class TestSPModel(unittest.TestCase):
    # Below are the parameters that are used for the test cases below
    k_p = 6.67e-11
    S_p = 1.1167
    max_conc_p = 51410.0
    c_e = 1000

    k_n = 1.76e-11
    S_n = 0.7824
    max_conc_n = 31833

    def test_m(self):
        soc_init_p = 0.6
        soc_init_n = 0.7

        testmodel = models.PySPM()
        self.assertEqual(-0.2893183331034342, testmodel.m(-1.656, self.k_p, self.S_p, self.max_conc_p,
                                                          soc_init_p, self.c_e))
        self.assertEqual(-2.7018597575301726, testmodel.m(-1.656, self.k_n, self.S_n, self.max_conc_n,
                                                          soc_init_n, self.c_e))

    def test_V(self):
        T = 298.15
        soc_init_p = 0.4956
        soc_init_n = 0.7568
        R_cell = 0.00148861
        I = -1.656

        testmodel = models.PySPM()
        OCP_p = 4.176505962016067
        OCP_n = 0.07464309895951012

        m_p = testmodel.m(-1.656, self.k_p, self.S_p,
                          self.max_conc_p, soc_init_p, self.c_e)
        m_n = testmodel.m(-1.656, self.k_n, self.S_n,
                          self.max_conc_n, soc_init_n, self.c_e)
        self.assertEqual(-0.28348389244322414, testmodel.m(-1.656, self.k_p, self.S_p, self.max_conc_p,
                                                           soc_init_p, self.c_e))
        self.assertEqual(-2.8860250955114384, testmodel.m(-1.656, self.k_n, self.S_n, self.max_conc_n,
                                                          soc_init_n, self.c_e))

        self.assertEqual(4.032392212009281,
                         testmodel.calc_cell_terminal_voltage(OCP_p, OCP_n, m_p, m_n, R_cell, T=T, I=I))


class TestESP(unittest.TestCase):
    def test_molar_flux(self):
        I = -1.656
        S = 0.7824
        self.assertEqual(2.1936265167099342e-05,
                         models.PySPMe.molar_flux_electrode(I=I, S=S, electrode_type='n'))
        self.assertEqual(-2.1936265167099342e-05,
                         models.PySPMe.molar_flux_electrode(I=I, S=S, electrode_type='p'))

    def test_method_a_s(self):
        epsilon: float = 0.5
        particle_radius: float = 10e-6
        self.assertEqual(1.5e5, models.PySPMe.a_s(
            epsilon=epsilon, R=particle_radius))

    def test_i_0(self):
        k: float = 1.764e-11
        c_s_max: float = 31833
        c_e: float = 1000
        soc_surf: float = 0.5
        self.assertEqual(8.878634015491551e-06, models.PySPMe.i_0(k=k,
                         c_s_max=c_s_max, c_e=c_e, soc_surf=soc_surf))

    def test_m(self):
        i_app: float = 1.5
        S: float = 0.5
        k: float = 1.764e-11
        c_s_max: float = 31833
        c_e: float = 1000
        soc_surf: float = 0.5
        self.assertEqual(3.501920615656027, models.PySPMe.m(i_app=i_app, k=k, S=S, c_s_max=c_s_max, c_e=c_e,
                                                            soc_surf=soc_surf))

    def test_calc_terminal_voltage(self):
        ocp_p: float = 4.2
        ocp_n: float = 0.15
        m_p: float = 3.0
        m_n: float = 1.0

        l_p: float = 7.35E-05
        l_sep: float = 2.00E-05
        l_n: float = 7.00E-05
        kappa_eff_avg: float = 0.2
        k_f_avg: float = 1
        t_c: float = 0.38
        c_e_n: float = 1100
        c_e_p: float = 900

        i_app: float = -1.656
        R_cell: float = 0.5
        temp: float = 298.15

        self.assertEqual(3.3009664058697896,
                         models.PySPMe.calc_terminal_voltage(ocp_p=ocp_p, ocp_n=ocp_n, m_p=m_p, m_n=m_n,
                                                             l_p=l_p, l_sep=l_sep, l_n=l_n,
                                                             kappa_eff_avg=kappa_eff_avg, k_f_avg=k_f_avg, t_c=t_c,
                                                             c_e_n=c_e_n, c_e_p=c_e_p, R_cell=R_cell,
                                                             i_app=i_app, temp=temp))


class TestP2DM(unittest.TestCase):
    def test_a_s(self):
        # Typical value for the negative electrode containing graphite
        self.assertEqual(340000.0, models.PyP2DM.a_s(epsilon=0.68, r=6e-6))

        # Typical value for the positive electrode containing NMC
        self.assertEqual(390000.0, models.PyP2DM.a_s(epsilon=0.65, r=5e-6))

    def test_i_0(self):
        # parameter below are from Shangwoo et al
        k_n = 2.3e-10
        k_p = 1.43e-10
        c_s_max_n = 31221
        c_s_max_p = 50179
        c_s_surf_n = 30596.579999999998
        c_s_surf_p = 17562.649999999998
        c_e = 900
        c_e_0 = 1000

        self.assertAlmostEqual(0.09202222696431563,
                               models.PyP2DM.i_0(k=k_n, c_s_surf=c_s_surf_n, c_s_max=c_s_max_n, c_e=c_e, c_e_0=c_e_0))
        self.assertAlmostEqual(0.31328442058013517,
                               models.PyP2DM.i_0(k=k_p, c_s_surf=c_s_surf_p, c_s_max=c_s_max_p, c_e=c_e, c_e_0=c_e_0))

        # Below tests for the exchange current equation using the Numpy arrays
        c_s_surf_n = np.array([30596.58, 30000, 28000, 25000, 24000])
        c_e = np.array([900, 1000, 990, 1000, 800])
        c_e_0 = np.array([1000, 1000, 1000, 1000, 1000])

        actual_i_0_n = np.array([0.09202222696431563, 0.13431208741651982, 0.20969526054264584,
                                 0.27675580843377356, 0.2613039208124068])

        self.assertTrue(np.allclose(actual_i_0_n,
                                    models.PyP2DM.i_0(k=k_n,
                                                      c_s_surf=c_s_surf_n, c_s_max=c_s_max_n,
                                                      c_e=c_e, c_e_0=c_e_0)))

    def test_v_n_minus_v_e(self):
        array_rel_eta_n = np.array(
            [-0.06276411, -0.06191974, -0.06021835, -0.05717165, -0.05351207])
        array_i_0_n = np.array(
            [0.00388174, 0.00388174, 0.00388174, 0.00388174, 0.00388174])
        array_x_n = np.array(
            [8.10e-06, 2.43e-05, 4.05e-05, 5.67e-05, 7.29e-05])

        i_app = 4
        temp = 298.15
        cell_area = 0.06
        a_s_n = 340000
        L_n = 81e-6

        v_e = models.PyP2DM.v_n_minus_v_e(array_i_0_n=array_i_0_n,
                                          array_eta_rel_n=array_rel_eta_n,
                                          array_coord_n=array_x_n,
                                          i_app=i_app, temp=temp, a_s_n=a_s_n, cell_area=cell_area, L_n=L_n)
        self.assertEqual(-0.92599193513242, v_e)

    def test_v_p_minum_v_e(self):
        pass

    def test_calc_eta_from_rel_eta(self):
        array_rel_eta: np.ndarray = np.array([-4.2, -4.2, -4.2, -4.2, -4.2])
        v_terminal: float = 4.16
        v_terminal_e: float = 0.92
        array_actual: np.ndarray = np.array(
            [-0.96, -0.96, -0.96, -0.96, -0.96])

        self.assertTrue(np.allclose(array_actual,
                                    models.PyP2DM.calc_eta_from_rel_eta(rel_eta=array_rel_eta,
                                                                        v_terminal=v_terminal,
                                                                        v_terminal_e=v_terminal_e)))


"""
Below are the tests for the thermal models
"""


class TestLumped(unittest.TestCase):
    T = 298.15
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    test_cell = battery_components.PyBatteryCell.read_from_parametersets(parameter_set_name='test',
                                                                         soc_init_p=SOC_init_p,
                                                                         soc_init_n=SOC_init_n,
                                                                         temp_init=T)
    t_model = models.PyLumped(b_cell=test_cell)

    def test_reversible_heat_loss(self):
        I = -1.656
        T = 298.15
        self.assertAlmostEqual(0.017761327872963178,
                               self.t_model.reversible_heat(I=I, T=T))

    def test_irreversible_heat_loss(self):
        V = self.test_cell.elec_p.OCP - self.test_cell.elec_n.OCP
        I = -1.656
        T = 298.15
        self.assertEqual(0.0, self.t_model.irreversible_heat(I=I, V=V))
        V = 3.9
        self.assertEqual(0.33428490122165927,
                         self.t_model.irreversible_heat(I, V))

    def test_heat_balance(self):
        self.assertEqual(0.0, self.t_model.heat_flux(298.15))
        self.assertEqual(1.2750000000000001, self.t_model.heat_flux(313.15))


"""
Below are the tests for battery cell degradation models
"""


class TestROMSEI(unittest.TestCase):
    def test_method_calc_j_i(self) -> None:
        I: float = 1.656  # represents the battery cell charge
        # represents the molar flux to the negative electrode
        j_tot: float = -I / (96487 * 0.7824)
        j_s: float = 0.0

        solver: models.PyROMSEI = models.PyROMSEI()
        j_i: float = solver.calc_j_i(j_tot=j_tot, j_s=j_s)
        self.assertAlmostEqual(-2.193626517e-5, j_i, places=12)

    def test_method_calc_eta_n(self) -> None:
        I: float = 1.656  # represents the battery cell charge
        # represents the molar flux to the negative electrode
        j_tot: float = -I / (96487 * 0.7824)
        j_s: float = 0.0
        temp: float = 298.15

        solver: models.PyROMSEI = models.PyROMSEI()
        j_i: float = solver.calc_j_i(j_tot=j_tot, j_s=j_s)
        j_0_i: float = solver.calc_j_0_i(k=1.764e-11, c_s_max=31833,
                                         soc=0.7522, c_e=1000)
        calculated_eta_n: float = solver.calc_eta_n(
            temp=temp, j_i=j_i, j_0_i=j_0_i)
        self.assertAlmostEqual(7.666435137e-6, j_0_i, places=10)
        self.assertAlmostEqual((2 * 8.314 * temp / 96487) * np.arcsinh(j_i / (2 * j_0_i)),
                               calculated_eta_n, places=5)

    def test_method_eta_s(self) -> None:
        I: float = 1.656  # represents the battery cell charge
        # represents the molar flux to the negative electrode
        j_tot: float = -I / (96487 * 0.7824)
        j_s: float = 0.0
        temp: float = 298.15

        solver: models.PyROMSEI = models.PyROMSEI()
        j_0_i: float = solver.calc_j_0_i(k=1.764e-11, c_s_max=31833,
                                         soc=0.7522, c_e=1000)
        j_i: float = solver.calc_j_i(j_tot=j_tot, j_s=j_s)

        eta_n: float = (2 * 8.314 * temp / 96487) * np.arcsinh(j_i/(2*j_0_i))
        calculated_eta_s: float = solver.calc_eta_s(
            eta_n=eta_n, ocp_n=0.081566, ocp_s=0.4)
        self.assertAlmostEqual(-0.377814, calculated_eta_s, places=5)

    def test_method_calc_j_s(self) -> None:
        i_0_s: float = 1.14264e-5
        temp: float = 298.15
        eta_s: float = -0.377814

        solver: models.PyROMSEI = models.PyROMSEI()
        self.assertAlmostEqual(1.783e-2, solver.calc_j_s(temp=temp, j_0_s=i_0_s,
                                                         eta_s=eta_s), places=1)

        i_0_s: float = 1.14264e-15
        self.assertAlmostEqual(-1.783e-12, solver.calc_j_s(temp=temp, j_0_s=i_0_s,
                                                           eta_s=eta_s), places=14)
