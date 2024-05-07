"""
Contain unittests for the python-based electrode concentration solvers.
"""

__all__ = ["TestPolyApprox", "TestEignFuncForPositiveElectrode",
           "TestEigenFuncExpForIncorrectElectrode"]

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."
__status__ = "Deployed"

import unittest

from bmslogic.simulations.cell.solvers.electrode_conc import PyPolynomialApproximation, PyEigenFuncExp


# Electrode parameters below
R = 1.25e-5  # electrode particle radius in [m]
c_max = 31833  # max. electrode concentration [mol/m3]
D = 3.9e-14  # electrode diffusivity [m2/s]
S = 0.7824  # electrode electrochemical active area [m2]
SOC_init = 0.7568  # initial electrode SOC

poly_solver1 = PyPolynomialApproximation(
    c_init=SOC_init*c_max, electrode_type='n', type='two')
poly_solver2 = PyPolynomialApproximation(
    c_init=SOC_init*c_max, electrode_type='n', type='higher')

# Simulation parameters below
t_prev = 0  # previous time [s]
dt = 0.1  # in s

# solve for SOC wrt to time
lst_time_poly, lst_poly_solver1, lst_poly_solver2 = [], [], []
SOC_poly1 = SOC_init
while SOC_poly1 > 0:
    SOC_poly1 = poly_solver1(dt=dt, t_prev=t_prev,
                             i_app=-1.65, R=R, S=S, D_s=D, c_smax=c_max)
    SOC_poly2 = poly_solver2(dt=dt, t_prev=t_prev,
                             i_app=-1.65, R=R, S=S, D_s=D, c_smax=c_max)
    lst_time_poly.append(t_prev)
    lst_poly_solver1.append(SOC_poly1)
    lst_poly_solver2.append(SOC_poly2)
    print(SOC_poly2)

    t_prev += dt  # update the time


class TestPolyApprox(unittest.TestCase):
    def test_constructor(self):
        pass

    def test_solve(self):
        self.assertEqual(0.7127702012060186, lst_poly_solver1[0])
        self.assertEqual(0.7127537226189332, lst_poly_solver1[1])

        self.assertEqual(0.7504676658078573, lst_poly_solver2[0])
        self.assertEqual(0.750422969925152, lst_poly_solver2[1])


class TestEigenFuncForPositiveElectrode(unittest.TestCase):
    """
    Tests for the functionality and accuracy of the computed variables in the Eigen Expansion Method.
    """
    i_app = -1.656
    r = 8.5e-6
    s = 1.1167
    d = 1e-14
    max_conc = 51410

    def test_constructor_and_property(self):
        electrode_SOC = PyEigenFuncExp(x_init=0.4956, n=5, electrode_type='p')
        self.assertEqual(0.4956, electrode_SOC.x_init)
        self.assertEqual(5, electrode_SOC.N)
        self.assertEqual('p', electrode_SOC.electrode_type)

        # below confirms the bounds for the eigenvalue equation.
        self.assertEqual(3.141592653589793,
                         electrode_SOC.lambda_bounds()[0][0])
        self.assertEqual(6.283185307179586,
                         electrode_SOC.lambda_bounds()[0][1])

        self.assertEqual(6.283185307179586,
                         electrode_SOC.lambda_bounds()[1][0])
        self.assertEqual(9.42477796076938, electrode_SOC.lambda_bounds()[1][1])

        self.assertEqual(9.42477796076938, electrode_SOC.lambda_bounds()[2][0])
        self.assertEqual(12.566370614359172,
                         electrode_SOC.lambda_bounds()[2][1])

        self.assertEqual(12.566370614359172,
                         electrode_SOC.lambda_bounds()[3][0])
        self.assertEqual(15.707963267948966,
                         electrode_SOC.lambda_bounds()[3][1])

        self.assertEqual(15.707963267948966,
                         electrode_SOC.lambda_bounds()[4][0])
        self.assertEqual(18.84955592153876,
                         electrode_SOC.lambda_bounds()[4][1])

        # below confirms the eigenvalues
        self.assertEqual(electrode_SOC.lambda_roots[0], 4.493409457910043)
        self.assertEqual(electrode_SOC.lambda_roots[1], 7.725251836937441)
        self.assertEqual(electrode_SOC.lambda_roots[2], 10.904121659428089)
        self.assertEqual(electrode_SOC.lambda_roots[3], 14.06619391283256)
        self.assertEqual(electrode_SOC.lambda_roots[4], 17.220755271929562)

    def test_j_scaled_calc(self):
        electrode_SOC = PyEigenFuncExp(x_init=0.4956, n=5, electrode_type='p')
        self.assertEqual(0.25411267897180484, electrode_SOC.j_scaled(i_app=self.i_app, R=self.r, S=self.s,
                                                                     D_s=self.d, c_smax=self.max_conc))

    def test_integ_term_first_iteration_positive_electrode(self):
        """
        Tests for the integration term for the positive electrode for the first iteration.
        """
        electrode_SOC = PyEigenFuncExp(x_init=0.4956, n=5, electrode_type='p')
        self.assertEqual(0.0, electrode_SOC.integ_term)
        electrode_SOC.update_integ_term(
            dt=0.1, i_app=self.i_app, R=self.r, S=self.s, D_s=self.d, c_smax=self.max_conc)
        self.assertEqual(1.0551391514400201e-05, electrode_SOC.integ_term)

    def test_eigenfunction_calc_first_iteration_positive_electrode(self):
        """
        Tests the calculated values of the eigenfunctions for the first iteration of the positive electrode.
        """
        electrode_SOC = PyEigenFuncExp(x_init=0.4956, n=5, electrode_type='p')
        first_u_k = electrode_SOC.solve_u_k(root_value=electrode_SOC.lambda_roots[0], t_prev=0, u_k_prev=0, dt=0.1,
                                            i_app=self.i_app, R=self.r, S=self.s, D_s=self.d, c_smax=self.max_conc)
        second_u_k = electrode_SOC.solve_u_k(root_value=electrode_SOC.lambda_roots[1], t_prev=0, u_k_prev=0, dt=0.1,
                                             i_app=self.i_app, R=self.r, S=self.s, D_s=self.d, c_smax=self.max_conc)
        third_u_k = electrode_SOC.solve_u_k(root_value=electrode_SOC.lambda_roots[2], t_prev=0, u_k_prev=0, dt=0.1,
                                            i_app=self.i_app, R=self.r, S=self.s, D_s=self.d, c_smax=self.max_conc)
        fourth_u_k = electrode_SOC.solve_u_k(root_value=electrode_SOC.lambda_roots[3], t_prev=0, u_k_prev=0, dt=0.1,
                                             i_app=self.i_app, R=self.r, S=self.s, D_s=self.d, c_smax=self.max_conc)
        fifth_u_k = electrode_SOC.solve_u_k(root_value=electrode_SOC.lambda_roots[4], t_prev=0, u_k_prev=0, dt=0.1,
                                            i_app=self.i_app, R=self.r, S=self.s, D_s=self.d, c_smax=self.max_conc)
        self.assertEqual(7.033278216344374e-06, first_u_k)
        self.assertEqual(7.0313566100936286e-06, second_u_k)
        self.assertEqual(7.028476136909354e-06, third_u_k)
        self.assertEqual(7.024638076156881e-06, fourth_u_k)
        self.assertEqual(7.019844469987686e-06, fifth_u_k)

    #
    def test_SOC_calc_two_iteration_positive_electrode(self):
        """
        Tests for the calculated surface SOC of the positive electrode for the first two iterations.
        """
        electrode_SOC = PyEigenFuncExp(x_init=0.4956, n=5, electrode_type='p')
        SOC_first_iter = electrode_SOC.calc_SOC_surf(dt=0.1, t_prev=0, i_app=self.i_app, R=self.r, S=self.s, D_s=self.d,
                                                     c_smax=self.max_conc)
        self.assertEqual(0.5042242859771239, SOC_first_iter)
        SOC_second_iter = electrode_SOC.calc_SOC_surf(dt=0.1, t_prev=0, i_app=self.i_app, R=self.r, S=self.s,
                                                      D_s=self.d,
                                                      c_smax=self.max_conc)
        self.assertEqual(0.5042699076691792, SOC_second_iter)

    def test_class_call_method(self):
        electrode_SOC = PyEigenFuncExp(x_init=0.4956, n=5, electrode_type='p')
        SOC_first_iter = electrode_SOC(dt=0.1, t_prev=0, i_app=self.i_app, R=self.r, S=self.s, D_s=self.d,
                                       c_smax=self.max_conc)
        self.assertEqual(0.5042242859771239, SOC_first_iter)
        SOC_second_iter = electrode_SOC(dt=0.1, t_prev=0, i_app=self.i_app, R=self.r, S=self.s, D_s=self.d,
                                        c_smax=self.max_conc)
        self.assertEqual(0.5042699076691792, SOC_second_iter)


class TestEigenFuncExpForIncorrectElectrode(unittest.TestCase):
    def test_constuctor(self):
        """
        Test for raised Exceptions in case of incorrect class arguments.
        """
        with self.assertRaises(Exception) as context:
            PyEigenFuncExp(x_init=0.4956, n=5, electrode_type='o')
