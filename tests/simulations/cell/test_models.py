"""
contains the tests for the model related equations
"""

__all__ = ["TestGeneralEquations", "TestESPModel", "TestROMSEI"]

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."
__status__ = "Deployed"

import unittest

import numpy as np

from bmslogic.simulations.cell.cell import calc_cap, calc_i_0, molar_flux_to_current
from bmslogic.simulations.cell.cell import calc_cap, calc_i_0, molar_flux_to_current, ROMSEI
from bmslogic.simulations.cell.cell import Thevenin1RC, ESC
from bmslogic.simulations.cell.cell import ESPModel_molar_flux_electrode, ESPModel_a_s, ESPModel_i_0, ESPModel_m, ESPModel_calc_terminal_voltage


class TestGeneralEquations(unittest.TestCase):
    def test_calc_soc(self) -> None:
        """calculates the soc from the Columb counting.
        """
        result: float = 0.027777777777777e-3
        self.assertAlmostEqual(result, calc_cap(
            cap_prev=0.0, Q=1.5, I=1.5, dt=0.1))

    def test_cal_i_0(self) -> None:
        result: float = 5.418867e-5
        self.assertAlmostEqual(result, calc_i_0(
            k=6.6667e-11, c_s_max=51410, soc=0.4952, c_e=1000), places=11)

    def test_molar_flux_to_current(self) -> None:
        # this represents the flux during discharge of the positive electrode
        molar_flux: float = -1.656 / (96487 * 1.1167)
        self.assertEqual(molar_flux * 96487 * 1.1167, molar_flux_to_current(
            molar_flux=molar_flux, S=1.1167, electrode_type="p"))
        # this represents the flux during charge of the positive electrode
        molar_flux: float = 1.656 / (96487 * 1.1167)
        self.assertEqual(molar_flux * 96487 * 1.1167, molar_flux_to_current(
            molar_flux=molar_flux, S=1.1167, electrode_type="p"))

        # this represents the flux during discharge of the negative electrode
        molar_flux: float = -1.656 / (96487 * 1.1167)
        self.assertEqual(molar_flux * 96487 * 1.1167, -molar_flux_to_current(
            molar_flux=molar_flux, S=1.1167, electrode_type="n"))
        # this represents the flux during charge of the negative electrode
        molar_flux: float = 1.656 / (96487 * 1.1167)
        self.assertEqual(molar_flux * 96487 * 1.1167, -molar_flux_to_current(
            molar_flux=molar_flux, S=1.1167, electrode_type="n"))


class TestThevenin1RC(unittest.TestCase):
    eta: float = 1.0
    cap = 1.0
    i_app = 2.0
    soc_prev = 0.5
    dt = 0.5

    R0: float = 0.1
    R1: float = 0.1
    C1: float = 1000
    i_R1_prev = 0.0

    gamma: float = 523.8311
    h_prev: float = 0.0
    s_prev: float = 0.0
    m: float = 4.4782e-4
    m_0: float = 0.0012

    ocv: float = 3.8

    def test_classmethod_soc_next(self):
        model: Thevenin1RC = Thevenin1RC()
        self.assertAlmostEqual(0.4997222222222222, model.soc_next(dt=self.dt, i_app=self.i_app,
                                                                  soc_prev=self.soc_prev, Q=self.cap, eta=self.eta))


class TestESC(unittest.TestCase):
    eta = 1.0
    cap = 1
    i_app = 2
    soc_prev = 0.5
    dt = 0.5

    R0: float = 0.1
    R1: float = 0.1
    C1: float = 1000
    i_R1_prev = 0.0

    gamma: float = 523.8311
    h_prev: float = 0.0
    s_prev: float = 0.0
    m: float = 4.4782e-4
    m_0: float = 0.0012

    ocv: float = 3.8

    def test_classmethod_sign(self):
        negative_float = -100.0
        zero_float = 0.0
        positive_float = 100.0

        negative_int = -100
        zero_int = 0
        positive_int = 100

        model: ESC = ESC()

        self.assertEqual(-1, model.sign(num=negative_float))
        self.assertEqual(0, model.sign(num=zero_float))
        self.assertEqual(1, model.sign(num=positive_float))

        self.assertEqual(-1, model.sign(num=negative_int))
        self.assertEqual(0, model.sign(num=zero_int))
        self.assertEqual(1, model.sign(num=positive_int))

    def test_classmethod_soc_next(self):
        self.assertAlmostEqual(0.4997222222222222, ESC().soc_next(dt=self.dt, i_app=self.i_app,
                                                                  soc_prev=self.soc_prev, Q=self.cap, eta=self.eta))

    def test_classmethod_i_R1_next(self):
        self.assertAlmostEqual(9.975041612e-3, ESC().i_R1_next(dt=self.dt, i_app=self.i_app, i_R1_prev=self.i_R1_prev,
                                                               R1=self.R1, C1=self.C1))

    def test_classmethod_h_next(self):
        self.assertEqual(-0.13541757898977902,
                         ESC().h_next(dt=self.dt, i_app=self.i_app, eta=self.eta, gamma=self.gamma, cap=self.cap,
                                      h_prev=self.h_prev))

    def test_classmethod_v(self):
        self.assertEqual(3.6011999999999995, ESC().V(i_app=self.i_app, ocv=self.ocv, R0=self.R0, R1=self.R1,
                                                     i_R1=self.i_R1_prev, m=self.m, h=self.h_prev, s_prev=self.s_prev,
                                                     m_0=self.m_0))

    def test_classmethod_s(self):
        s_prev = 100
        zero_float = 0.0
        zero_int = 0

        positive_float = 1.0
        positive_int = 1

        self.assertEqual(100, ESC().s(i_app=zero_float, s_prev=s_prev))
        self.assertEqual(100, ESC().s(i_app=zero_int, s_prev=s_prev))

        self.assertEqual(1, ESC().s(i_app=positive_float, s_prev=s_prev))
        self.assertEqual(1, ESC().s(i_app=positive_int, s_prev=s_prev))


class TestESPModel(unittest.TestCase):
    def test_molar_flux(self):
        I = -1.656
        S = 0.7824
        self.assertEqual(2.1936265167099342e-05,
                         ESPModel_molar_flux_electrode(i_app=I, S=S, electrode_type="n"))
        self.assertEqual(-2.1936265167099342e-05,
                         ESPModel_molar_flux_electrode(i_app=I, S=S, electrode_type="p"))

    def test_method_a_s(self):
        epsilon: float = 0.5
        particle_radius: float = 10e-6
        self.assertEqual(1.5e5, ESPModel_a_s(
            epsilon=epsilon, R=particle_radius))

    def test_i_0(self):
        k: float = 1.764e-11
        c_s_max: float = 31833
        c_e: float = 1000
        soc_surf: float = 0.5
        self.assertEqual(8.878634015491551e-06, ESPModel_i_0(k=k,
                         c_s_max=c_s_max, c_e=c_e, soc_surf=soc_surf))

    def test_m(self):
        i_app: float = 1.5
        S: float = 0.5
        k: float = 1.764e-11
        c_s_max: float = 31833
        c_e: float = 1000
        soc_surf: float = 0.5
        self.assertEqual(3.501920615656027, ESPModel_m(i_app=i_app, k=k, S=S, c_s_max=c_s_max, c_e=c_e,
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
                         ESPModel_calc_terminal_voltage(ocp_p=ocp_p, ocp_n=ocp_n, m_p=m_p, m_n=m_n,
                                                        L_p=l_p, L_sep=l_sep, L_n=l_n,
                                                        kappa_eff_avg=kappa_eff_avg, k_f_avg=k_f_avg, t_c=t_c,
                                                        c_e_n=c_e_n, c_e_p=c_e_p, R_cell=R_cell,
                                                        i_app=i_app, temp=temp))


class TestROMSEI(unittest.TestCase):
    def test_method_calc_j_i(self) -> None:
        I: float = 1.656  # represents the battery cell charge
        # represents the molar flux to the negative electrode
        j_tot: float = -I / (96487 * 0.7824)
        j_s: float = 0.0
        solver: ROMSEI = ROMSEI()
        self.assertAlmostEqual(-2.193626517e-5,
                               solver.calc_j_i(j_tot=j_tot, j_s=j_s))

    def test_method_cal_eta(self) -> None:
        I: float = 1.656  # represents the battery cell charge
        # represents the molar flux to the negative electrode
        j_tot: float = -I / (96487 * 0.7824)
        j_s: float = 0.0
        temp: float = 298.15

        i_0: float = calc_i_0(k=1.764e-11, c_s_max=31833, soc=0.7522, c_e=1000)
        solver: ROMSEI = ROMSEI()

        j_i: float = solver.calc_j_i(j_tot=j_tot, j_s=j_s)
        self.assertAlmostEqual(-2.193626517e-5, j_i)
        self.assertAlmostEqual(7.666435137e-6, i_0, places=10)
        self.assertAlmostEqual((2 * (8.314) * temp / 96487) * np.arcsinh(
            j_i/(2*i_0)), solver.calc_eta_n(temp=temp, j_i=j_i, i_0=i_0), places=5)

    def test_method_eta_s(self) -> None:
        I: float = 1.656  # represents the battery cell charge
        # represents the molar flux to the negative electrode
        j_tot: float = -I / (96487 * 0.7824)
        j_s: float = 0.0
        temp: float = 298.15

        i_0: float = calc_i_0(k=1.764e-11, c_s_max=31833, soc=0.7522, c_e=1000)
        solver: ROMSEI = ROMSEI()

        j_i: float = solver.calc_j_i(j_tot=j_tot, j_s=j_s)

        eta_n: float = (2 * (8.314) * temp / 96487) * np.arcsinh(j_i/(2*i_0))

        solver: ROMSEI = ROMSEI()
        self.assertAlmostEqual(-0.377814, solver.calc_eta_s(eta_n=eta_n,
                               ocp=0.081566, ocp_s=0.4), places=5)

    def test_method_calc_j_s(self) -> None:
        i_0_s: float = 1.14264e-5
        temp: float = 298.15
        eta_s: float = -0.377814

        solver: ROMSEI = ROMSEI()
        self.assertAlmostEqual(
            1.783e-2, solver.calc_j_s(temp=temp, i_0_s=i_0_s, eta_s=eta_s), places=1)

        i_0_s: float = 1.14264e-15
        self.assertAlmostEqual(-1.783e-12, solver.calc_j_s(temp=temp,
                               i_0_s=i_0_s, eta_s=eta_s), places=14)
