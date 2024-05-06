import unittest

import numpy as np

from bmslogic.simulations.cell.cell import EigenSolver, LumpedThermalSolver, ROMSEISolver


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
        I_s = self.solver.calc_current(soc=soc, ocp=ocp, temp=self.temp, i_app=1.656)
        self.assertAlmostEqual(8.35925983e-12, I_s, places=16)

        # the second case
        soc: float = 0.7568
        ocp: float = 0.07464309895951012
        I_s = self.solver.calc_current(soc=soc, ocp=ocp, temp=self.temp, i_app=1.656)
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
        soc_new: float = electrode_soc.calc_soc_surf(dt=0.1, t_prev=0.0, i_app=self.i_app,
                                                     R=self.R, S=self.S, D_s=self.D_s,
                                                     c_s_max=self.c_s_max)
        # self.assertAlmostEqual(0.5042242859771239, soc_new, places=7)
        # soc_new: float = electrode_soc.calc_soc_surf(dt=0.1, t_prev=0.0, i_app=self.i_app,
        #                                              R=self.R, S=self.S, D_s=self.D_s,
        #                                              c_s_max=self.c_s_max)
        # self.assertAlmostEqual(0.5042242859771239, soc_new, places=6)



    

