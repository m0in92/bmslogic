"""
Unittests for testing the C++ based battery cell solvers that uses the Python interface
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by Moin Ahmed. All Rights Reserved."
__status__ = "Deployed"

import unittest

import numpy as np

from bmslogic.simulations.cell.cell import EigenSolver, CNSolver, LumpedThermalSolver, ROMSEISolver
from bmslogic.simulations.cell.cell import ElectrolyteFVMCoordinates, ElectrolyteFVMSolver


class TestROMSEISolver(unittest.TestCase):
    k: float = 1.76e-11
    c_e: float = 1000.0
    S: float = 0.7824
    c_s_max: float = 31833
    U_s: float = 0.4
    j_0_s: float = 1.14264e-15
    A: float = 0.0596
    MW: float = 0.16
    rho: float = 1600
    kappa: float = 5e-6
    temp: float = 298.15

    solver: ROMSEISolver = ROMSEISolver(k=1.76e-11, c_e=1000.0, S=0.7824, c_s_max=31833,
                                        U_s=0.4, j_0_s=1.14264e-15, A=0.0596, MW=0.16,
                                        rho=1600, kappa=5e-6)

    def test_properties(self):
        self.assertEqual(self.k, self.solver.k)
        self.assertEqual(self.c_e, self.solver.c_e)
        self.assertEqual(self.S, self.solver.S)
        self.assertEqual(self.c_s_max, self.solver.c_s_max)
        self.assertEqual(self.U_s, self.solver.U_s)
        self.assertEqual(self.j_0_s, self.solver.j_0_s)
        self.assertEqual(self.A, self.solver.A)
        self.assertEqual(self.MW, self.solver.MW)
        self.assertEqual(self.rho, self.solver.rho)
        self.assertEqual(self.kappa, self.solver.kappa)
        self.assertEqual(0.0, self.solver.L_SEI)

    def test_method_calc_current(self):
        # the first test case
        soc: float = 0.01
        ocp: float = 0.64981159
        I_s = self.solver.calc_current(
            soc=soc, ocp=ocp, temp=self.temp, i_app=1.656)
        self.assertAlmostEqual(8.35925983e-12, I_s, places=16)

        # the second case
        soc: float = 0.7568
        ocp: float = 0.07464309895951012
        I_s = self.solver.calc_current(
            soc=soc, ocp=ocp, temp=self.temp, i_app=1.656)
        self.assertAlmostEqual(1.55111785e-07, I_s, places=15)

    def test_method_calc_L(self) -> None:
        J_s: float = -1.55111785e-7 / (96487 * 0.7824)
        delta_L: float = self.solver.calc_delta_L(j_s=J_s, dt=0.1)
        self.assertAlmostEqual(2.049977783e-17, delta_L, places=18)

    def test_method_update_L(self) -> None:
        k: float = 1.76e-11
        c_e: float = 1000.0
        S: float = 0.7824
        c_s_max: float = 31833
        U_s: float = 0.4
        j_0_s: float = 1.14264e-15
        A: float = 0.0596
        MW: float = 0.16
        rho: float = 1600
        kappa: float = 5e-6
        temp: float = 298.15

        solver: ROMSEISolver = ROMSEISolver(k=1.76e-11, c_e=1000.0, S=0.7824, c_s_max=31833,
                                            U_s=0.4, j_0_s=1.14264e-15, A=0.0596, MW=0.16,
                                            rho=1600, kappa=5e-6)
        self.assertEqual(0.0, solver.L_SEI)
        J_s: float = -1.55111785e-7 / (96487 * 0.7824)
        solver.update_L(j_s=J_s, dt=0.1)
        self.assertAlmostEqual(2.049977783e-17, solver.L_SEI, places=18)


class TestLumpedThermalModel(unittest.TestCase):
    h: float = 1.0
    A: float = 0.085
    rho: float = 1626
    vol: float = 3.38e-5
    C_p: float = 750
    temp_init: float = 298.15
    instance: LumpedThermalSolver = LumpedThermalSolver(
        h=h, A=A, rho=rho, vol=vol, C_p=C_p, temp_init=temp_init)

    def test_properties(self):
        instance: LumpedThermalSolver = LumpedThermalSolver(
            h=self.h, A=self.A, rho=self.rho, vol=self.vol, C_p=self.C_p, temp_init=self.temp_init)
        self.assertEqual(298.15, instance.temp())
        self.assertEqual(298.15, instance.temp_prev())
        self.assertEqual(298.15, instance.temp_init())

    def test_method_reversible_heat(self) -> None:
        I: float = -1.656
        T: float = 298.15
        dOCPdT_n: float = -0.00010000003546921532
        dOCPdT_p: float = -0.00013597333594486018
        self.assertAlmostEqual(0.017761327872963178, self.instance.reversible_heat(dOCPdT_p=dOCPdT_p,
                                                                                   dOCPdT_n=dOCPdT_n,
                                                                                   current=I, temp=T))

    def test_irreversible_heat_loss(self):
        V: float = 3.9
        I: float = -1.656
        OCP_p: float = 4.176505962016067
        OCP_n: float = 0.07464309895951012
        self.assertEqual(0.33428490122165927, self.instance.irreversible_heat(OCP_p=OCP_p,
                                                                              OCP_n=OCP_n,
                                                                              current=I,
                                                                              V=V))

    def test_method_heat_transfer(self):
        self.assertEqual(0.0, self.instance.heat_transfer(
            temp=298.15, temp_amb=298.15))
        self.assertEqual(1.2750000000000001, self.instance.heat_transfer(
            temp=313.15, temp_amb=298.15))

    def test_method_solve_temp(self):
        # Note: it is important to specify the instance, otherwise an error is given with the solve_temp method is called.
        self.assertEqual(298.14960637624864, self.instance.solve_temp(dt=0.1, t_prev=0.0, I=-1.656, V=4.2, temp_amb=298.15,
                                                                      OCP_p=4.176505962016067, OCP_n=0.07464309895951012,
                                                                      dOCPdT_p=-0.00013597333594486018, dOCPdT_n=-0.00010000003546921532))
        self.assertEqual(298.15, self.instance.temp_prev())
        self.assertEqual(298.15, self.instance.temp_init())
        self.assertEqual(298.14960637624864, self.instance.temp())


class TestEigenSolver(unittest.TestCase):
    i_app: float = -1.656
    R: float = 8.5e-6
    S: float = 1.1167
    D_s: float = 1e-14
    c_s_max: float = 51410

    dt: float = 0.1

    num_roots: int = 5

    def test_property_root(self):
        electrode_soc = EigenSolver(
            electrode_type='p', soc_init=0.4956, num_roots=self.num_roots)
        self.assertAlmostEqual(
            4.493409457910043, electrode_soc.roots()[0], places=4)
        self.assertAlmostEqual(
            7.725251836937441, electrode_soc.roots()[1], places=4)
        self.assertAlmostEqual(
            10.904121659428089, electrode_soc.roots()[2], places=4)
        self.assertAlmostEqual(
            14.06619391283256, electrode_soc.roots()[3], places=4)
        self.assertAlmostEqual(
            17.220755271929562, electrode_soc.roots()[4], places=4)

        self.assertEqual(0.0, electrode_soc.integ_term())
        self.assertTrue(np.array_equal(np.zeros(self.num_roots),
                        np.array(electrode_soc.vec_u_k())))

    def test_method_j_scaled(self):
        electrode_soc = EigenSolver(
            electrode_type='p', soc_init=0.4956, num_roots=self.num_roots)
        self.assertEqual(0.25411267897180484, electrode_soc.j_scaled(
            i_app=self.i_app, R=self.R, S=self.S, D_s=self.D_s, c_s_max=self.c_s_max))

    def test_update_integ_term(self):
        electrode_soc: EigenSolver = EigenSolver(
            electrode_type='p', soc_init=0.4956, num_roots=self.num_roots)
        electrode_soc.update_integ_term(
            self.dt, self.i_app, self.R, self.S, self.D_s, self.c_s_max)
        self.assertEqual(1.0551391514400201e-05, electrode_soc.integ_term())

    def test_method_du_kdt(self):
        electrode_soc: EigenSolver = EigenSolver(
            electrode_type='p', soc_init=0.4956, num_roots=self.num_roots)
        j_scaled_value: float = electrode_soc.j_scaled(
            i_app=self.i_app, R=self.R, S=self.S, D_s=self.D_s, c_s_max=self.c_s_max)

        # For u_prev = 0.0 and t_prev = 0.0, dudt = 7.03391e-5 for all roots
        self.assertAlmostEqual(7.03391e-5, electrode_soc.du_kdt(root=electrode_soc.roots()[0],
                                                                D=self.D_s,
                                                                R=self.R,
                                                                scaled_j_value=j_scaled_value,
                                                                t=0.0,
                                                                u=0.0), places=8)
        self.assertAlmostEqual(7.03391e-5, electrode_soc.du_kdt(root=electrode_soc.roots()[1],
                                                                D=self.D_s,
                                                                R=self.R,
                                                                scaled_j_value=j_scaled_value,
                                                                t=0.0,
                                                                u=0.0), places=8)
        self.assertAlmostEqual(7.03391e-5, electrode_soc.du_kdt(root=electrode_soc.roots()[2],
                                                                D=self.D_s,
                                                                R=self.R,
                                                                scaled_j_value=j_scaled_value,
                                                                t=0.0,
                                                                u=0.0), places=8)
        self.assertAlmostEqual(7.03391e-5, electrode_soc.du_kdt(root=electrode_soc.roots()[3],
                                                                D=self.D_s,
                                                                R=self.R,
                                                                scaled_j_value=j_scaled_value,
                                                                t=0.0,
                                                                u=0.0), places=8)
        self.assertAlmostEqual(7.03391e-5, electrode_soc.du_kdt(root=electrode_soc.roots()[4],
                                                                D=self.D_s,
                                                                R=self.R,
                                                                scaled_j_value=j_scaled_value,
                                                                t=0.0,
                                                                u=0.0), places=8)

    def test_method_solve_u_k(self):
        """Tests for the solution of the eigen-values using the ODE solver.
        """
        electrode_soc: EigenSolver = EigenSolver(
            electrode_type='p', soc_init=0.4956, num_roots=self.num_roots)
        self.assertAlmostEqual(
            4.493409457910043, electrode_soc.roots()[0], places=4)
        first_u_k: float = electrode_soc.solve_u_k(root=electrode_soc.roots()[0],
                                                   t_prev=0.0,
                                                   dt=0.1,
                                                   u_k_prev=0.0,
                                                   i_app=self.i_app,
                                                   R=self.R,
                                                   S=self.S,
                                                   D_s=self.D_s,
                                                   c_s_max=self.c_s_max)
        self.assertAlmostEqual(7.033278216344374e-06, first_u_k, places=8)

    def test_get_summation(self):
        """Tests for the calculation of the summation term in the Eigen Function Expansion Method.
        """
        electrode_soc: EigenSolver = EigenSolver(
            electrode_type='p', soc_init=0.4956, num_roots=self.num_roots)

        electrode_soc.update_vec_uk(
            dt=0.1, t_prev=0.0, i_app=self.i_app, R=self.R, S=self.S, D_s=self.D_s, c_s_max=self.c_s_max)
        self.assertEqual(0.0, electrode_soc.vec_u_k()[0])
        summation: float = electrode_soc.get_summation_term(dt=0.1, t_prev=0.0,
                                                            i_app=self.i_app, R=self.R,
                                                            S=self.S, D_s=self.D_s, c_s_max=self.c_s_max)
        self.assertAlmostEqual(-0.04220880120875144, summation, places=6)

    def test_method_soc_solver(self):
        electrode_soc: EigenSolver = EigenSolver(
            electrode_type='p', soc_init=0.4956, num_roots=5)
        soc_new: float = electrode_soc.solve(dt=0.1, t_prev=0.0, i_app=self.i_app,
                                             R=self.R, S=self.S, D=self.D_s,
                                             c_s_max=self.c_s_max)
        # self.assertAlmostEqual(0.5042242859771239, soc_new, places=7)
        # soc_new: float = electrode_soc.calc_soc_surf(dt=0.1, t_prev=0.0, i_app=self.i_app,
        #                                              R=self.R, S=self.S, D_s=self.D_s,
        #                                              c_s_max=self.c_s_max)
        # self.assertAlmostEqual(0.5042242859771239, soc_new, places=6)


class TestCNSolver(unittest.TestCase):
    i_app: float = -1.656
    R: float = 8.5e-6
    S: float = 1.1167
    D_s: float = 1e-14
    c_s_max: float = 51410
    soc_init: float = 0.45

    dt: float = 0.1

    def test_constructor(self):
        spatial_pts: int = 100
        solver: CNSolver = CNSolver(
            c_init=self.soc_init * self.c_s_max, electrode_type="p", num_spatial_pts=spatial_pts)

        self.assertEqual(spatial_pts, solver.K)
        self.assertEqual(self.c_s_max * self.soc_init, solver.c_s_surf)

    def test_method_calc_A(self):
        spatial_pts: int = 100
        solver: CNSolver = CNSolver(
            c_init=self.soc_init * self.c_s_max, electrode_type="p", num_spatial_pts=spatial_pts)

        dt: float = 0.1
        R: float = 8.5e-6
        D: float = 1e-14
        self.assertAlmostEqual(0.138408304, solver.calc_A(dt=dt, R=R, D=D))

    def test_method_calc_B(self):
        spatial_pts: int = 100
        solver: CNSolver = CNSolver(
            c_init=self.soc_init * self.c_s_max, electrode_type="p", num_spatial_pts=spatial_pts)

        dt: float = 0.1
        R: float = 8.5e-6
        D: float = 1e-14
        self.assertAlmostEqual(
            5.88235e-9, solver.calc_B(dt=dt, R=R, D=D), places=12)

    def test_property_cs(self):
        spatial_pts: int = 100
        solver: CNSolver = CNSolver(
            c_init=self.soc_init * self.c_s_max, electrode_type="p", num_spatial_pts=spatial_pts)
        self.assertAlmostEqual(0.45, solver.c_s / self.c_s_max)

    def test_method_solver(self):
        R = 1.25e-5  # electrode particle radius in [m]
        c_max = 31833  # max. electrode concentration [mol/m3]
        D = 3.9e-14  # electrode diffusivity [m2/s]
        S = 0.7824  # electrode electrochemical active area [m2]
        SOC_init = 0.7568  # initial electrode SOC

        dt = 0.1
        I_app: float = -1.65
        spatial_pts: int = 100

        solver: CNSolver = CNSolver(
            c_init=SOC_init * c_max, electrode_type="n", num_spatial_pts=spatial_pts)
        self.assertAlmostEqual(24091.2144, solver.c_s)

        solver.solve(dt=dt, I_app=I_app, R=R, S=S, D=D)
        self.assertAlmostEqual(24062.50442622, solver.c_s, places=8)

        solver.solve(dt=dt, I_app=I_app, R=R, S=S, D=D)
        self.assertAlmostEqual(24043.33453948, solver.c_s, places=8)


class TestFVMCoordinates(unittest.TestCase):
    """
    Unittest for the finite volume method co-ordinates
    """

    instance = ElectrolyteFVMCoordinates(L_n=8e-5, L_sep=2.5e-5, L_p=8.8e-5)

    def test_constructor(self):
        self.assertEqual(8e-5, self.instance.L_n)
        self.assertEqual(2.5e-5, self.instance.L_sep)
        self.assertEqual(8.8e-5, self.instance.L_p)
        self.assertEqual(8e-5 / 10, self.instance.dx_n)
        self.assertEqual(2.5e-5 / 10, self.instance.dx_sep)
        self.assertEqual(8.8e-5 / 10, self.instance.dx_p)

    def test_property_array_x_n(self):
        self.assertEqual(8e-5 / 10, self.instance.dx_n)
        self.assertAlmostEqual(4e-6, self.instance.array_x_n[0])
        self.assertAlmostEqual(4e-6 + 1 * 8e-6, self.instance.array_x_n[1])
        self.assertAlmostEqual(4e-6 + 2 * 8e-6, self.instance.array_x_n[2])
        self.assertAlmostEqual(4e-6 + 3 * 8e-6, self.instance.array_x_n[3])
        self.assertAlmostEqual(4e-6 + 4 * 8e-6, self.instance.array_x_n[4])
        self.assertAlmostEqual(4e-6 + 5 * 8e-6, self.instance.array_x_n[5])
        self.assertAlmostEqual(4e-6 + 6 * 8e-6, self.instance.array_x_n[6])
        self.assertAlmostEqual(4e-6 + 7 * 8e-6, self.instance.array_x_n[7])
        self.assertAlmostEqual(4e-6 + 8 * 8e-6, self.instance.array_x_n[8])
        self.assertAlmostEqual(4e-6 + 9 * 8e-6, self.instance.array_x_n[9])
        self.assertAlmostEqual(10, len(self.instance.array_x_n))

    def test_array_xs(self):
        self.assertEqual(2.5e-5 / 10, self.instance.dx_sep)
        self.assertAlmostEqual(8e-5 + 1.25e-6, self.instance.array_x_sep[0])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 1 * self.instance.dx_sep, self.instance.array_x_sep[1])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 2 * self.instance.dx_sep, self.instance.array_x_sep[2])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 3 * self.instance.dx_sep, self.instance.array_x_sep[3])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 4 * self.instance.dx_sep, self.instance.array_x_sep[4])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 5 * self.instance.dx_sep, self.instance.array_x_sep[5])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 6 * self.instance.dx_sep, self.instance.array_x_sep[6])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 7 * self.instance.dx_sep, self.instance.array_x_sep[7])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 8 * self.instance.dx_sep, self.instance.array_x_sep[8])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 9 * self.instance.dx_sep, self.instance.array_x_sep[9])
        self.assertAlmostEqual(10, len(self.instance.array_x_sep))

    def test_array_xp(self):
        self.assertEqual(8.8e-5 / 10, self.instance.dx_p)
        self.assertAlmostEqual(1.05e-4 + 4.4e-6, self.instance.array_x_p[0])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 1 *
                               self.instance.dx_p, self.instance.array_x_p[1])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 2 *
                               self.instance.dx_p, self.instance.array_x_p[2])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 3 *
                               self.instance.dx_p, self.instance.array_x_p[3])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 4 *
                               self.instance.dx_p, self.instance.array_x_p[4])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 5 *
                               self.instance.dx_p, self.instance.array_x_p[5])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 6 *
                               self.instance.dx_p, self.instance.array_x_p[6])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 7 *
                               self.instance.dx_p, self.instance.array_x_p[7])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 8 *
                               self.instance.dx_p, self.instance.array_x_p[8])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 9 *
                               self.instance.dx_p, self.instance.array_x_p[9])
        self.assertAlmostEqual(10, len(self.instance.array_x_p))

    def test_vector_x(self):
        self.assertAlmostEqual(4e-6, self.instance.array_x[0])
        self.assertAlmostEqual(4e-6 + 1 * 8e-6, self.instance.array_x[1])
        self.assertAlmostEqual(4e-6 + 2 * 8e-6, self.instance.array_x[2])
        self.assertAlmostEqual(4e-6 + 3 * 8e-6, self.instance.array_x[3])
        self.assertAlmostEqual(4e-6 + 4 * 8e-6, self.instance.array_x[4])
        self.assertAlmostEqual(4e-6 + 5 * 8e-6, self.instance.array_x[5])
        self.assertAlmostEqual(4e-6 + 6 * 8e-6, self.instance.array_x[6])
        self.assertAlmostEqual(4e-6 + 7 * 8e-6, self.instance.array_x[7])
        self.assertAlmostEqual(4e-6 + 8 * 8e-6, self.instance.array_x[8])
        self.assertAlmostEqual(4e-6 + 9 * 8e-6, self.instance.array_x[9])

        self.assertAlmostEqual(8e-5 + 1.25e-6, self.instance.array_x[10])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 1 *
                               self.instance.dx_sep, self.instance.array_x[11])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 2 *
                               self.instance.dx_sep, self.instance.array_x[12])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 3 *
                               self.instance.dx_sep, self.instance.array_x[13])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 4 *
                               self.instance.dx_sep, self.instance.array_x[14])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 5 *
                               self.instance.dx_sep, self.instance.array_x[15])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 6 *
                               self.instance.dx_sep, self.instance.array_x[16])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 7 *
                               self.instance.dx_sep, self.instance.array_x[17])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 8 *
                               self.instance.dx_sep, self.instance.array_x[18])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 9 *
                               self.instance.dx_sep, self.instance.array_x[19])

        self.assertAlmostEqual(1.05e-4 + 4.4e-6, self.instance.array_x[20])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 1 *
                               self.instance.dx_p, self.instance.array_x[21])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 2 *
                               self.instance.dx_p, self.instance.array_x[22])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 3 *
                               self.instance.dx_p, self.instance.array_x[23])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 4 *
                               self.instance.dx_p, self.instance.array_x[24])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 5 *
                               self.instance.dx_p, self.instance.array_x[25])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 6 *
                               self.instance.dx_p, self.instance.array_x[26])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 7 *
                               self.instance.dx_p, self.instance.array_x[27])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 8 *
                               self.instance.dx_p, self.instance.array_x[28])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 9 *
                               self.instance.dx_p, self.instance.array_x[29])

        self.assertAlmostEqual(30, len(self.instance.array_x))

    def test_array_dx(self):
        self.assertEqual(self.instance.dx_n, self.instance.array_dx[0])
        self.assertEqual(self.instance.dx_n, self.instance.array_dx[5])
        self.assertEqual(self.instance.dx_n, self.instance.array_dx[9])

        self.assertEqual(self.instance.dx_sep, self.instance.array_dx[11])
        self.assertEqual(self.instance.dx_sep, self.instance.array_dx[15])
        self.assertEqual(self.instance.dx_sep, self.instance.array_dx[18])

        self.assertEqual(self.instance.dx_p, self.instance.array_dx[20])
        self.assertEqual(self.instance.dx_p, self.instance.array_dx[25])
        self.assertEqual(self.instance.dx_p, self.instance.array_dx[-1])
        self.assertEqual(30, len(self.instance.array_dx))


class TestElectrolyteFVMSolver(unittest.TestCase):
    L_n: float = 8e-5
    L_sep: float = 2.5e-5
    L_p: float = 8.8e-5
    epsilon_e_n: float = 0.385
    epsilon_e_sep: float = 0.785
    epsilon_e_p: float = 0.485
    D_e: float = 3.5e-10  # [mol/m3]
    brugg: float = 4
    a_s_n: float = 5.78e3
    a_s_p: float = 7.28e3
    c_e_init: float = 1000  # [mol/m3]
    transference: float = 0.354

    coords: ElectrolyteFVMCoordinates = ElectrolyteFVMCoordinates(
        L_n=L_n, L_sep=L_sep, L_p=L_p)
    instance: ElectrolyteFVMSolver = ElectrolyteFVMSolver(fvm_coords=coords, c_e_init=c_e_init, t_c=transference,
                                                          epsilon_e_n=epsilon_e_n, epsilon_e_sep=epsilon_e_sep, epsilon_e_p=epsilon_e_p,
                                                          a_s_n=a_s_n, a_s_p=a_s_p,
                                                          D_e=D_e, brugg=brugg)

    def test_properties(self):
        self.assertEqual(self.transference, self.instance.t_c)
        self.assertEqual(self.c_e_init, self.instance.c_e_init)
        self.assertEqual(self.epsilon_e_n, self.instance.epsilon_e_n)
        self.assertEqual(self.epsilon_e_sep, self.instance.epsilon_e_sep)
        self.assertEqual(self.epsilon_e_p, self.instance.epsilon_e_p)
        self.assertEqual(self.a_s_n, self.instance.a_s_n)
        self.assertEqual(self.a_s_p, self.instance.a_s_p)
        self.assertEqual(self.D_e, self.instance.D_e)
        self.assertEqual(self.brugg, self.instance.brugg)

    def test_property_coords(self):
        self.assertEqual(8e-5 / 10, self.instance.coords.dx_n)
        self.assertEqual(2.5e-5 / 10, self.instance.coords.dx_sep)
        self.assertEqual(8.8e-5 / 10, self.instance.coords.dx_p)

        self.assertAlmostEqual(4e-6, self.instance.coords.array_x_n[0])
        self.assertAlmostEqual(
            4e-6 + 1 * 8e-6, self.instance.coords.array_x_n[1])
        self.assertAlmostEqual(
            4e-6 + 2 * 8e-6, self.instance.coords.array_x_n[2])
        self.assertAlmostEqual(
            4e-6 + 3 * 8e-6, self.instance.coords.array_x_n[3])
        self.assertAlmostEqual(
            4e-6 + 4 * 8e-6, self.instance.coords.array_x_n[4])
        self.assertAlmostEqual(
            4e-6 + 5 * 8e-6, self.instance.coords.array_x_n[5])
        self.assertAlmostEqual(
            4e-6 + 6 * 8e-6, self.instance.coords.array_x_n[6])
        self.assertAlmostEqual(
            4e-6 + 7 * 8e-6, self.instance.coords.array_x_n[7])
        self.assertAlmostEqual(
            4e-6 + 8 * 8e-6, self.instance.coords.array_x_n[8])
        self.assertAlmostEqual(
            4e-6 + 9 * 8e-6, self.instance.coords.array_x_n[9])

        self.assertAlmostEqual(
            8e-5 + 1.25e-6, self.instance.coords.array_x_sep[0])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 1 * self.instance.coords.dx_sep, self.instance.coords.array_x_sep[1])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 2 * self.instance.coords.dx_sep, self.instance.coords.array_x_sep[2])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 3 * self.instance.coords.dx_sep, self.instance.coords.array_x_sep[3])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 4 * self.instance.coords.dx_sep, self.instance.coords.array_x_sep[4])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 5 * self.instance.coords.dx_sep, self.instance.coords.array_x_sep[5])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 6 * self.instance.coords.dx_sep, self.instance.coords.array_x_sep[6])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 7 * self.instance.coords.dx_sep, self.instance.coords.array_x_sep[7])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 8 * self.instance.coords.dx_sep, self.instance.coords.array_x_sep[8])
        self.assertAlmostEqual(
            8e-5 + 1.25e-6 + 9 * self.instance.coords.dx_sep, self.instance.coords.array_x_sep[9])

        self.assertAlmostEqual(
            1.05e-4 + 4.4e-6, self.instance.coords.array_x_p[0])
        self.assertAlmostEqual(
            1.05e-4 + 4.4e-6 + 1 * self.instance.coords.dx_p, self.instance.coords.array_x_p[1])
        self.assertAlmostEqual(
            1.05e-4 + 4.4e-6 + 2 * self.instance.coords.dx_p, self.instance.coords.array_x_p[2])
        self.assertAlmostEqual(
            1.05e-4 + 4.4e-6 + 3 * self.instance.coords.dx_p, self.instance.coords.array_x_p[3])
        self.assertAlmostEqual(
            1.05e-4 + 4.4e-6 + 4 * self.instance.coords.dx_p, self.instance.coords.array_x_p[4])
        self.assertAlmostEqual(
            1.05e-4 + 4.4e-6 + 5 * self.instance.coords.dx_p, self.instance.coords.array_x_p[5])
        self.assertAlmostEqual(
            1.05e-4 + 4.4e-6 + 6 * self.instance.coords.dx_p, self.instance.coords.array_x_p[6])
        self.assertAlmostEqual(
            1.05e-4 + 4.4e-6 + 7 * self.instance.coords.dx_p, self.instance.coords.array_x_p[7])
        self.assertAlmostEqual(
            1.05e-4 + 4.4e-6 + 8 * self.instance.coords.dx_p, self.instance.coords.array_x_p[8])
        self.assertAlmostEqual(
            1.05e-4 + 4.4e-6 + 9 * self.instance.coords.dx_p, self.instance.coords.array_x_p[9])

        self.assertAlmostEqual(10, len(self.instance.coords.array_x_n))
        self.assertAlmostEqual(10, len(self.instance.coords.array_x_sep))
        self.assertAlmostEqual(10, len(self.instance.coords.array_x_p))

    def test_property_array_c_e(self):
        self.assertEqual(1000, self.instance.array_c_e[0])
        self.assertTrue(np.array_equal(
            1000 * np.ones(30), self.instance.array_c_e))

        self.assertEqual(30, len(self.instance.array_c_e))

    def test_property_array_epsilon_e(self):
        self.assertTrue(np.allclose(self.epsilon_e_n *
                        np.ones(10), self.instance.array_epsilon_e[:10]))
        self.assertTrue(np.allclose(self.epsilon_e_sep,
                        self.instance.array_epsilon_e[10:20]))
        self.assertTrue(np.allclose(self.epsilon_e_p *
                        np.ones(10), self.instance.array_epsilon_e[20:30]))

    def test_property_array_D_e(self):
        self.assertTrue(np.allclose(7.689727719e-12 *
                        np.ones(10), self.instance.array_D_eff[:10]))
        self.assertTrue(np.allclose(1.329066377e-10 *
                        np.ones(10), self.instance.array_D_eff[10:20]))
        self.assertTrue(np.allclose(1.936578022e-11 * np.ones(10),
                        self.instance.array_D_eff[20:30], rtol=1e-10))

    def test_property_array_a_s(self):
        self.assertTrue(np.allclose(self.a_s_n * np.ones(10),
                        self.instance.array_a_s[:10]))
        self.assertTrue(np.allclose(
            np.zeros(10), self.instance.array_a_s[10:20]))
        self.assertTrue(np.allclose(self.a_s_p * np.ones(10),
                        self.instance.array_a_s[20:30]))

    def test_method_calc_diag(self):
        L_n: float = 8e-5
        L_sep: float = 2.5e-5
        L_p: float = 8.8e-5

        epsilon_e_n: float = 0.385
        epsilon_e_sep: float = 0.785
        epsilon_e_p: float = 0.485

        D_e: float = 3.5e-10  # [m2/s]
        brugg: float = 4
        t_c: float = 0.354
        c_e_init = 1000  # [mol/m3]

        a_s_n: float = 5.78e3
        a_s_p: float = 7.28e3

        dt: float = 0.1  # [s]

        coords: ElectrolyteFVMCoordinates = ElectrolyteFVMCoordinates(
            L_n=L_n, L_sep=L_sep, L_p=L_p)
        solver: ElectrolyteFVMSolver = ElectrolyteFVMSolver(fvm_coords=coords, c_e_init=c_e_init, t_c=t_c,
                                                            epsilon_e_n=epsilon_e_n, epsilon_e_sep=epsilon_e_sep, epsilon_e_p=epsilon_e_p,
                                                            a_s_n=a_s_n, a_s_p=a_s_p,
                                                            D_e=D_e, brugg=brugg)

        self.assertTrue(np.allclose(np.array(
            [0.39701519956054687, 0.40903039912109374, 0.40903039912109374, 0.40903039912109374, 0.40903039912109374,
             0.40903039912109374, 0.40903039912109374, 0.40903039912109374, 0.40903039912109374, 0.5643918250813804,
             3.447111405166663, 5.03801240699999, 5.03801240699999, 5.03801240699999, 5.03801240699999,
             5.03801240699999,
             5.03801240699999, 5.03801240699999, 5.03801240699999, 3.45052361212832, 0.6631374097584988,
             0.5350149282509039,
             0.5350149282509039, 0.5350149282509039, 0.5350149282509039, 0.5350149282509039, 0.5350149282509039,
             0.5350149282509039, 0.5350149282509039, 0.510007464125452]), np.array(solver.get_calc_diag(dt=dt))))

    def test_method_calc_diags(self):
        L_n: float = 8e-5
        L_sep: float = 2.5e-5
        L_p: float = 8.8e-5

        epsilon_e_n: float = 0.385
        epsilon_e_sep: float = 0.785
        epsilon_e_p: float = 0.485

        D_e: float = 3.5e-10  # [m2/s]
        brugg: float = 4
        t_c: float = 0.354
        c_e_init = 1000  # [mol/m3]

        a_s_n: float = 5.78e3
        a_s_p: float = 7.28e3

        dt: float = 0.1  # [s]

        coords: ElectrolyteFVMCoordinates = ElectrolyteFVMCoordinates(
            L_n=L_n, L_sep=L_sep, L_p=L_p)
        solver: ElectrolyteFVMSolver = ElectrolyteFVMSolver(fvm_coords=coords, c_e_init=c_e_init, t_c=t_c,
                                                            epsilon_e_n=epsilon_e_n, epsilon_e_sep=epsilon_e_sep, epsilon_e_p=epsilon_e_p,
                                                            a_s_n=a_s_n, a_s_p=a_s_p,
                                                            D_e=D_e, brugg=brugg)

        self.assertTrue(np.allclose(np.array(
            [0.39701519956054687, 0.40903039912109374, 0.40903039912109374, 0.40903039912109374, 0.40903039912109374,
             0.40903039912109374, 0.40903039912109374, 0.40903039912109374, 0.40903039912109374, 0.5643918250813804,
             3.447111405166663, 5.03801240699999, 5.03801240699999, 5.03801240699999, 5.03801240699999,
             5.03801240699999,
             5.03801240699999, 5.03801240699999, 5.03801240699999, 3.45052361212832, 0.6631374097584988,
             0.5350149282509039,
             0.5350149282509039, 0.5350149282509039, 0.5350149282509039, 0.5350149282509039, 0.5350149282509039,
             0.5350149282509039, 0.5350149282509039, 0.510007464125452]), np.array(solver.get_calc_diag(dt=dt))))

        self.assertTrue(
            np.allclose(
                np.array([-0.01201519956054687, -0.012015199560546868, -0.012015199560546875, -0.012015199560546865,
                          -0.012015199560546865, -0.012015199560546875,
                          -0.012015199560546875, -0.012015199560546865,
                          -0.012015199560546865, -0.5356052016666676,
                          -2.126506203499995, -2.126506203499995,
                          -2.126506203499995,
                          -2.126506203499995, -2.126506203499995, -2.126506203499995, -2.126506203499995,
                          -2.126506203499995,
                          -2.126506203499995, -0.15312994563304688,
                          -0.02500746412545197, -0.02500746412545197,
                          -0.02500746412545197,
                          -0.02500746412545197, -0.02500746412545197,
                          -0.02500746412545197, -0.02500746412545197,
                          -0.02500746412545197,
                          -0.02500746412545197]),
                np.array(solver.get_calc_lower_diag(dt=dt))))

        self.assertTrue(
            np.allclose(
                np.array([-0.01201519956054687, -0.012015199560546868, -0.012015199560546875, -0.012015199560546865,
                          -0.012015199560546865, -0.012015199560546875, -
                          0.012015199560546875, -0.012015199560546865,
                          -0.012015199560546865, -0.1673766255208336, -
                          2.126506203499995, -2.126506203499995,
                          -2.126506203499995, -2.126506203499995, -2.126506203499995, -2.126506203499995,
                          -2.126506203499995,
                          -2.126506203499995, -2.126506203499995, -
                          0.539017408628325, -0.02500746412545197,
                          -0.02500746412545197, -0.02500746412545197, -
                          0.02500746412545197, -0.02500746412545197,
                          -0.02500746412545197, -0.02500746412545197, -0.02500746412545197, -0.02500746412545197]),
                np.array(solver.get_calc_upper_diag(dt=dt))))

    def test_method_calc_c_e_j(self):
        L_n: float = 8e-5
        L_sep: float = 2.5e-5
        L_p: float = 8.8e-5

        epsilon_e_n: float = 0.385
        epsilon_e_sep: float = 0.785
        epsilon_e_p: float = 0.485

        D_e: float = 3.5e-10  # [m2/s]
        brugg: float = 4
        t_c: float = 0.354
        c_e_init = 1000  # [mol/m3]

        a_s_n: float = 5.78e3
        a_s_p: float = 7.28e3

        dt: float = 0.1  # [s]

        coords: ElectrolyteFVMCoordinates = ElectrolyteFVMCoordinates(
            L_n=L_n, L_sep=L_sep, L_p=L_p)
        solver: ElectrolyteFVMSolver = ElectrolyteFVMSolver(fvm_coords=coords, c_e_init=c_e_init, t_c=t_c,
                                                            epsilon_e_n=epsilon_e_n, epsilon_e_sep=epsilon_e_sep, epsilon_e_p=epsilon_e_p,
                                                            a_s_n=a_s_n, a_s_p=a_s_p,
                                                            D_e=D_e, brugg=brugg)

        j_p = -1.53693327e-05 * np.ones(10)  # [mol/m2/s]
        j_sep = np.zeros(10)  # [mol/m2/s]
        j_n = 2.19362652e-05 * np.ones(10)  # [mol/m2/s]
        j = np.append(np.append(j_n, j_sep), j_p)  # [mol/m2/s]

        self.assertTrue(np.allclose(
            np.array([385.00819074, 385.00819074, 385.00819074, 385.00819074, 385.00819074, 385.00819074, 385.00819074, 385.00819074, 385.00819074, 385.00819074,
                      785., 785., 785., 785., 785., 785., 785., 785., 785., 785., 484.99277199, 484.99277199, 484.99277199, 484.99277199, 484.99277199, 484.99277199, 484.99277199, 484.99277199, 484.99277199, 484.99277199]),
            solver.get_vec_ce_j(c_prev=solver.array_c_e, j=j, dt=dt)))

    def test_method_solve(self):
        L_n: float = 8e-5
        L_sep: float = 2.5e-5
        L_p: float = 8.8e-5

        epsilon_e_n: float = 0.385
        epsilon_e_sep: float = 0.785
        epsilon_e_p: float = 0.485

        D_e: float = 3.5e-10  # [m2/s]
        brugg: float = 4
        t_c: float = 0.354
        c_e_init = 1000  # [mol/m3]

        a_s_n: float = 5.78e3
        a_s_p: float = 7.28e3

        dt: float = 0.1  # [s]

        coords: ElectrolyteFVMCoordinates = ElectrolyteFVMCoordinates(
            L_n=L_n, L_sep=L_sep, L_p=L_p)
        solver: ElectrolyteFVMSolver = ElectrolyteFVMSolver(fvm_coords=coords, c_e_init=c_e_init, t_c=t_c,
                                                            epsilon_e_n=epsilon_e_n, epsilon_e_sep=epsilon_e_sep, epsilon_e_p=epsilon_e_p,
                                                            a_s_n=a_s_n, a_s_p=a_s_p,
                                                            D_e=D_e, brugg=brugg)

        j_p = -1.53693327e-05 * np.ones(10)  # [mol/m2/s]
        j_sep = np.zeros(10)  # [mol/m2/s]
        j_n = 2.19362652e-05 * np.ones(10)  # [mol/m2/s]
        j = np.append(np.append(j_n, j_sep), j_p)  # [mol/m2/s]

        solver.solve(j=j, dt=dt)

        self.assertTrue(np.allclose(
            np.array([1000.02127464, 1000.02127464, 1000.02127464, 1000.02127464, 1000.02127464,
                      1000.02127464, 1000.02127451, 1000.02127015, 1000.02112188, 1000.01607847,
                      1000.00376418, 1000.00205212, 1000.0010976, 1000.00054825, 1000.00020129,
                      999.99992864, 999.99962965, 999.99919394, 999.99846067, 999.99715915,
                      999.9878872, 999.98522759, 999.985103, 999.98509717, 999.98509689,
                      999.98509688, 999.98509688, 999.98509688, 999.98509688, 999.98509688]),
            np.array(solver.array_c_e)))
