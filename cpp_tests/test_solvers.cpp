#include "gtest/gtest.h"

#include "owl.h"
#include "solvers.h"

#include "example_parameters.cpp"

TEST(BaseConcSolverTest, Constructor)
{
    char electrode_type = 'p';
    BaseConcSolver solver_instance = BaseConcSolver('p');
    EXPECT_EQ(solver_instance.get_electrodeType(), electrode_type);

    char electrode_type_n = 'n';
    BaseConcSolver solver_instance_n = BaseConcSolver('n');
    EXPECT_EQ(solver_instance_n.get_electrodeType(), electrode_type_n);
}

TEST(PolynomialApproxTest, Constructor)
{
    char electrode_type = 'p';
    double c_init = 3600;
    std::string solver_type = "higher";
    PolynomialApprox solver_instance = PolynomialApprox(electrode_type, c_init, solver_type);
}

TEST(PolynomialApprox, Solve)
{
    double R = 1.25e-5;       // electrode particle radius in [m]
    double c_max = 31833;     // max. electrode concentration [mol/m3]
    double D = 3.9e-14;       // electrode diffusivity [m2/s]
    double S = 0.7824;        // electrode electrochemical active area [m2]
    double SOC_init = 0.7568; // initial electrode SOC

    double dt = 0.1;
    double t_prev = 0.0;
    double I_app = -1.65;

    char electrode_type = 'n';
    std::string solver_type = "higher";
    PolynomialApprox solver_instance = PolynomialApprox(electrode_type, c_max * SOC_init, solver_type);

    solver_instance.solve(dt, t_prev, I_app, R, S, D);
    EXPECT_EQ(solver_instance.get_c_surf() / c_max, 0.7504676658078573);
    solver_instance.solve(dt, t_prev, I_app, R, S, D);
    EXPECT_EQ(solver_instance.get_c_surf() / c_max, 0.750422969925152);
}

TEST(CNSolverTest, Constructor)
{
    double c_init = 0.45 * 51410;
    char electrode_type = 'p';
    double num_spatial_pts = 100;

    CNSolver solver_instance = CNSolver(c_init, electrode_type, num_spatial_pts);

    EXPECT_EQ(solver_instance.get_electrode_type(), electrode_type);
    EXPECT_EQ(solver_instance.get_spatial_pts(), num_spatial_pts);
    EXPECT_EQ(solver_instance.get_c_s_surf(), c_init);
    // EXPECT_EQ(solver_instance.get_c_surf(), c_init);

    OWL::ArrayXD c_prev = c_init * OWL::Ones(num_spatial_pts);
    std::vector<double> c_prev_ = c_prev.getArray();
    EXPECT_EQ(solver_instance.get_c_prev(), c_prev_);
}

TEST(CNSolverTest, MethodCalcA)
{
    double c_init = 0.45 * 51410;
    char electrode_type = 'p';
    double num_spatial_pts = 100;

    double dt = 0.1;
    double R = 8.5e-6;
    double D = 1e-14;

    CNSolver solver_instance = CNSolver(c_init, electrode_type, num_spatial_pts);

    EXPECT_NEAR(solver_instance.calc_A(dt, R, D), 0.138408304, 1e-6);
}

TEST(CNSolverTest, MethodCalcB)
{
    double c_init = 0.45 * 51410;
    char electrode_type = 'p';
    double num_spatial_pts = 100;

    double dt = 0.1;
    double R = 8.5e-6;
    double D = 1e-14;

    CNSolver solver_instance = CNSolver(c_init, electrode_type, num_spatial_pts);

    EXPECT_NEAR(solver_instance.calc_B(dt, R, D), 5.88235e-9, 1e-14);
}

TEST(CNSolverTest, MethodArrayR)
{
    double c_init = 0.45 * 51410;
    char electrode_type = 'p';
    double num_spatial_pts = 5;

    double dt = 0.1;
    double D = 1e-14;

    CNSolver solver_instance = CNSolver(c_init, electrode_type, num_spatial_pts);
    double R = 10.0;
    std::vector<double> expected = {0.0, 2.5, 5.0, 7.5, 10.0};

    std::vector<double> result = solver_instance.get_array_R(R);

    ASSERT_EQ(result.size(), expected.size());
    for (size_t i = 0; i < result.size(); ++i)
    {
        ASSERT_DOUBLE_EQ(result[i], expected[i]);
    }
}

TEST(CNSolverTest, ArrayR)
{
    double c_init = 0.45 * 51410;
    char electrode_type = 'p';
    CNSolver solver_instance = CNSolver(c_init, electrode_type, 5);

    double dt = 0.1;
    double R = 2.0;
    double D = 1.0;

    std::vector<double> result = solver_instance.get_array_R(R);

    EXPECT_EQ(result.size(), 5);
    EXPECT_EQ(result[0], 0);
    EXPECT_EQ(result[1], 0.5);
    EXPECT_EQ(result[2], 1.0);
    EXPECT_EQ(result[3], 1.5);
    EXPECT_EQ(result[4], 2.0);
}

TEST(CNSolverTest, LHS_diag_elements)
{
    double c_init = 0.45 * 51410;
    char electrode_type = 'p';
    CNSolver solver_instance = CNSolver(c_init, electrode_type, 5);

    double dt = 0.1;
    double R = 2.0;
    double D = 1.0;

    std::vector<double> result = solver_instance.get_diag_elements(dt, R, D);

    double expected_A = dt * D / std::pow(solver_instance.get_dr(R), 2);
    OWL::ArrayXD expected_array = (1 + expected_A) * OWL::Ones(solver_instance.get_spatial_pts());
    std::vector<double> expected_result = expected_array.getArray();
    expected_result[0] = 1 + 3 * expected_A;
    expected_result[expected_result.size() - 1] = 1 + expected_A;

    ASSERT_EQ(result.size(), expected_result.size());
    for (size_t i = 0; i < result.size(); ++i)
    {
        EXPECT_DOUBLE_EQ(result[i], expected_result[i]);
    }
}

TEST(CNSolverTest, LHS_l_diag_elements)
{
    double c_init = 0.45 * 51410;
    char electrode_type = 'p';
    int spatial_pts = 5;
    CNSolver solver_instance = CNSolver(c_init, electrode_type, spatial_pts);

    double dt = 0.1;
    double R = 2.0;
    double D = 1.0;

    std::vector<double> result = solver_instance.get_l_diag_elements(dt, R, D);

    double A = solver_instance.calc_A(dt, R, D);
    double B = solver_instance.calc_B(dt, R, D);
    std::vector<double> array_R = solver_instance.get_array_R(R);
    EXPECT_EQ(result.size(), spatial_pts - 1);
    for (int i = 0; i < spatial_pts - 2; i++)
    {

        EXPECT_EQ(result[i], -(A / 2 - B / array_R[i + 1]));
    }
    EXPECT_EQ(result.back(), -A);
}

TEST(CNSolverTest, LHS_u_diag_elements)
{
    double c_init = 0.45 * 51410;
    char electrode_type = 'p';
    int spatial_pts = 5;
    CNSolver solver_instance = CNSolver(c_init, electrode_type, spatial_pts);

    double dt = 0.1;
    double R = 2.0;
    double D = 1.0;

    std::vector<double> result = solver_instance.get_u_diag_elements(dt, R, D);

    double A = solver_instance.calc_A(dt, R, D);
    double B = solver_instance.calc_B(dt, R, D);
    std::vector<double> array_R = solver_instance.get_array_R(R);
    EXPECT_EQ(result.size(), spatial_pts - 1);
    EXPECT_EQ(result[0], -3 * A);
    for (int i = 1; i < spatial_pts - 1; i++)
    {

        EXPECT_EQ(result[i], -(A / 2 + B / array_R[i]));
    }
}

TEST(CNSolverTest, solve)
{
    double R = 1.25e-5;       // electrode particle radius in [m]
    double c_max = 31833;     // max. electrode concentration [mol/m3]
    double D = 3.9e-14;       // electrode diffusivity [m2/s]
    double S = 0.7824;        // electrode electrochemical active area [m2]
    double SOC_init = 0.7568; // initial electrode SOC

    double dt = 0.1;
    double I_app = -1.65;
    double spatial_pts = 100;

    CNSolver solver_instance = CNSolver(c_max * SOC_init, 'n', spatial_pts);

    EXPECT_EQ(solver_instance.get_c_s_surf(), 24091.2144);
    solver_instance.solve(dt, I_app, R, S, D);
    EXPECT_NEAR(solver_instance.get_c_s_surf(), 24062.50442622, 1e-6);
    solver_instance.solve(dt, I_app, R, S, D);
    EXPECT_NEAR(solver_instance.get_c_s_surf(), 24043.33453948, 1e-6);
}

TEST(ElectrolyteFVMSOlverTest, Constructor)
{
    double L_n = 8e-5;
    double L_sep = 2.5e-5;
    double L_p = 8.8e-5;
    double epsilon_e_n = 0.385;
    double epsilon_e_sep = 0.785;
    double epsilon_e_p = 0.485;
    double D_e = 3.5e-10; // [mol/m3]
    double brugg = 4.0;
    double a_s_n = 5.78e3;
    double a_s_p = 7.28e3;
    double c_e_init = 1000; // [mol/m3]
    double transference = 0.354;

    ElectrolyteFVMCoordinates coords = ElectrolyteFVMCoordinates(L_n, L_sep, L_p, 10, 10, 10);
    ElectrolyteFVMSolver solver_instance = ElectrolyteFVMSolver(coords, c_e_init, transference, epsilon_e_n, epsilon_e_sep, epsilon_e_p,
                                                                a_s_n, a_s_p, D_e, brugg);

    EXPECT_EQ(solver_instance.get_epsilon_e_n(), epsilon_e_n);
    EXPECT_EQ(solver_instance.get_epsilon_e_sep(), epsilon_e_sep);
    EXPECT_EQ(solver_instance.get_epsilon_e_p(), epsilon_e_p);

    EXPECT_EQ(solver_instance.get_a_s_n(), a_s_n);
    EXPECT_EQ(solver_instance.get_a_s_p(), a_s_p);

    EXPECT_EQ(solver_instance.get_D_e(), D_e);
    EXPECT_EQ(solver_instance.get_t_c(), transference);
}

/**
 * @brief Tests for the getter method for the vector containing the electrolyte concentrations.
 *
 */
TEST(ElectrolyteFVMSolverTest, vector_c_e)
{
    double L_n = 8e-5;
    double L_sep = 2.5e-5;
    double L_p = 8.8e-5;
    double epsilon_e_n = 0.385;
    double epsilon_e_sep = 0.785;
    double epsilon_e_p = 0.485;
    double D_e = 3.5e-10; // [mol/m3]
    double brugg = 4.0;
    double a_s_n = 5.78e3;
    double a_s_p = 7.28e3;
    double c_e_init = 1000; // [mol/m3]
    double transference = 0.354;

    ElectrolyteFVMCoordinates coords = ElectrolyteFVMCoordinates(L_n, L_sep, L_p, 10, 10, 10);
    ElectrolyteFVMSolver solver_instance = ElectrolyteFVMSolver(coords, c_e_init, transference, epsilon_e_n, epsilon_e_sep, epsilon_e_p,
                                                                a_s_n, a_s_p, D_e, brugg);

    size_t N = 30;
    std::vector<double> expected(N, c_e_init);
    EXPECT_EQ(solver_instance.get_vector_c_e(), expected);
}

TEST(ElectrolyteFVMSolverTest, diag_elements)
{
    double L_n = 8e-5;
    double L_sep = 2.5e-5;
    double L_p = 8.8e-5;
    double epsilon_e_n = 0.385;
    double epsilon_e_sep = 0.785;
    double epsilon_e_p = 0.485;
    double D_e = 3.5e-10; // [mol/m3]
    double brugg = 4.0;
    double a_s_n = 5.78e3;
    double a_s_p = 7.28e3;
    double c_e_init = 1000; // [mol/m3]
    double transference = 0.354;

    double dt = 0.1; // in [s]

    ElectrolyteFVMCoordinates coords = ElectrolyteFVMCoordinates(L_n, L_sep, L_p, 10, 10, 10);
    ElectrolyteFVMSolver solver_instance = ElectrolyteFVMSolver(coords, c_e_init, transference, epsilon_e_n, epsilon_e_sep, epsilon_e_p,
                                                                a_s_n, a_s_p, D_e, brugg);

    std::vector<double> expected = {0.39701519956054687, 0.40903039912109374, 0.40903039912109374, 0.40903039912109374, 0.40903039912109374,
                                    0.40903039912109374, 0.40903039912109374, 0.40903039912109374, 0.40903039912109374, 0.5643918250813804,
                                    3.447111405166663, 5.03801240699999, 5.03801240699999, 5.03801240699999, 5.03801240699999,
                                    5.03801240699999,
                                    5.03801240699999, 5.03801240699999, 5.03801240699999, 3.45052361212832, 0.6631374097584988,
                                    0.5350149282509039,
                                    0.5350149282509039, 0.5350149282509039, 0.5350149282509039, 0.5350149282509039, 0.5350149282509039,
                                    0.5350149282509039, 0.5350149282509039, 0.510007464125452};
    std::vector<double> result = solver_instance.get_calc_diag(dt);
    for (size_t i = 0; i < expected.size(); i++)
    {
        EXPECT_NEAR(result[i], expected[i], 1e-8);
    }
}

TEST(ElectrolyteFVMSolverTest, lower_diag_elements)
{
    double L_n = 8e-5;
    double L_sep = 2.5e-5;
    double L_p = 8.8e-5;
    double epsilon_e_n = 0.385;
    double epsilon_e_sep = 0.785;
    double epsilon_e_p = 0.485;
    double D_e = 3.5e-10; // [mol/m3]
    double brugg = 4.0;
    double a_s_n = 5.78e3;
    double a_s_p = 7.28e3;
    double c_e_init = 1000; // [mol/m3]
    double transference = 0.354;

    double dt = 0.1; // in [s]

    ElectrolyteFVMCoordinates coords = ElectrolyteFVMCoordinates(L_n, L_sep, L_p, 10, 10, 10);
    ElectrolyteFVMSolver solver_instance = ElectrolyteFVMSolver(coords, c_e_init, transference, epsilon_e_n, epsilon_e_sep, epsilon_e_p,
                                                                a_s_n, a_s_p, D_e, brugg);

    std::vector<double> expected = {-0.01201519956054687, -0.012015199560546868, -0.012015199560546875, -0.012015199560546865,
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
                                    -0.02500746412545197};
    std::vector<double> result = solver_instance.get_calc_lower_diag(dt);
    for (size_t i = 0; i < expected.size(); i++)
    {
        EXPECT_NEAR(result[i], expected[i], 1e-8);
    }
}

TEST(ElectrolyteFVMSolverTest, upper_diag_elements)
{
    double L_n = 8e-5;
    double L_sep = 2.5e-5;
    double L_p = 8.8e-5;
    double epsilon_e_n = 0.385;
    double epsilon_e_sep = 0.785;
    double epsilon_e_p = 0.485;
    double D_e = 3.5e-10; // [mol/m3]
    double brugg = 4.0;
    double a_s_n = 5.78e3;
    double a_s_p = 7.28e3;
    double c_e_init = 1000; // [mol/m3]
    double transference = 0.354;

    double dt = 0.1; // in [s]

    ElectrolyteFVMCoordinates coords = ElectrolyteFVMCoordinates(L_n, L_sep, L_p, 10, 10, 10);
    ElectrolyteFVMSolver solver_instance = ElectrolyteFVMSolver(coords, c_e_init, transference, epsilon_e_n, epsilon_e_sep, epsilon_e_p,
                                                                a_s_n, a_s_p, D_e, brugg);

    std::vector<double> expected = {-0.01201519956054687, -0.012015199560546868, -0.012015199560546875, -0.012015199560546865,
                                    -0.012015199560546865, -0.012015199560546875, -0.012015199560546875, -0.012015199560546865,
                                    -0.012015199560546865, -0.1673766255208336, -2.126506203499995, -2.126506203499995,
                                    -2.126506203499995, -2.126506203499995, -2.126506203499995, -2.126506203499995,
                                    -2.126506203499995,
                                    -2.126506203499995, -2.126506203499995, -0.539017408628325, -0.02500746412545197,
                                    -0.02500746412545197, -0.02500746412545197, -0.02500746412545197, -0.02500746412545197,
                                    -0.02500746412545197, -0.02500746412545197, -0.02500746412545197, -0.02500746412545197};
    std::vector<double> result = solver_instance.get_calc_upper_diag(dt);
    for (size_t i = 0; i < expected.size(); i++)
    {
        EXPECT_NEAR(result[i], expected[i], 1e-8);
    }
}

TEST(ElectrolyteFVMSolverTest, solver)
{
    double L_n = 8e-5;
    double L_sep = 2.5e-5;
    double L_p = 8.8e-5;
    double epsilon_e_n = 0.385;
    double epsilon_e_sep = 0.785;
    double epsilon_e_p = 0.485;
    double D_e = 3.5e-10; // [mol/m3]
    double brugg = 4.0;
    double a_s_n = 5.78e3;
    double a_s_p = 7.28e3;
    double c_e_init = 1000; // [mol/m3]
    double transference = 0.354;

    double dt = 0.1; // in [s]

    ElectrolyteFVMCoordinates coords = ElectrolyteFVMCoordinates(L_n, L_sep, L_p, 10, 10, 10);
    ElectrolyteFVMSolver solver_instance = ElectrolyteFVMSolver(coords, c_e_init, transference, epsilon_e_n, epsilon_e_sep, epsilon_e_p,
                                                                a_s_n, a_s_p, D_e, brugg);

    OWL::ArrayXD j_p = -1.53693327e-05 * OWL::Ones(10);
    OWL::ArrayXD j_sep = OWL::Zeros(10);
    OWL::ArrayXD j_n = 2.19362652e-05 * OWL::Ones(10);
    OWL::ArrayXD j_n_and_j_sep = OWL::append(j_n, j_sep);
    OWL::ArrayXD j_ = OWL::append(j_n_and_j_sep, j_p);
    std::vector<double> j = j_.getArray();

    std::vector<double> expected = {1000.02127464, 1000.02127464, 1000.02127464, 1000.02127464, 1000.02127464,
                                    1000.02127464, 1000.02127451, 1000.02127015, 1000.02112188, 1000.01607847,
                                    1000.00376418, 1000.00205212, 1000.0010976, 1000.00054825, 1000.00020129,
                                    999.99992864, 999.99962965, 999.99919394, 999.99846067, 999.99715915,
                                    999.9878872, 999.98522759, 999.985103, 999.98509717, 999.98509689,
                                    999.98509688, 999.98509688, 999.98509688, 999.98509688, 999.98509688};
    solver_instance.solve(j, dt);
    std::vector<double> result = solver_instance.get_vector_c_e();
    for (int i = 0; i < expected.size(); i++)
    {
        EXPECT_NEAR(result[i], expected[i], 1e-6);
    }
}

/**
 * @brief Test the results from the isothermal and no degradation single particle simulations using the
 * poly solver.
 *
 * The numbers are the benchmark in-house simulations results.
 *
 */
TEST(SPSolverTest, IsoThermalSolvePolySolver)
{
    double temp = 298.15;
    double soc_n = 0.7568;
    double soc_p = 0.4956;

    double discharge_current = 1.656;
    double V_min = 4.0;
    double SOC_lib_min = 0.0;
    double SOC_lib = 0.0;

    std::function<double(double)> OCP_ref_n_ = OCP_ref_n;
    std::function<double(double)> dOCPdT_n_ = dOCPdT_n;
    std::function<double(double)> OCP_ref_p_ = OCP_ref_p;
    std::function<double(double)> dOCPdT_p_ = dOCPdT_p;

    NElectrode elec_n = NElectrode(L_n, A_n, kappa_n, epsilon_n, max_conc_n, R_n, S_n,
                                   T_ref_n, D_ref_n, k_ref_n, Ea_D_n, Ea_R_n, alpha_n,
                                   brugg_n, soc_n, temp, OCP_ref_n_, dOCPdT_n_);
    PElectrode elec_p = PElectrode(L_p, A_p, kappa_p, epsilon_p, max_conc_p, R_p, S_p,
                                   T_ref_p, D_ref_p, k_ref_p, Ea_D_p, Ea_R_p, alpha_p,
                                   brugg_p, soc_p, temp, OCP_ref_p_, dOCPdT_p_);
    Electrolyte electrolyte = Electrolyte(c_init_e, L_e, kappa_e, epsilon_e, brugg_e);
    BatteryCell b_cell = BatteryCell(elec_p, elec_n, electrolyte, rho, Vol, C_p, h, A, cap, V_max, V_min, R_cell);

    Discharge cycler = Discharge(discharge_current, V_min, SOC_lib_min, SOC_lib);

    BatterySolver solver = BatterySolver(b_cell, true, true, "poly");
    Solution sol = solver.solve(cycler);

    EXPECT_EQ(sol.get_V()[0], 4.0199174566872626);
    EXPECT_EQ(sol.get_V()[1], 4.0198737542938119);
    EXPECT_EQ(sol.get_V()[2], 4.0198300549308437);
    EXPECT_EQ(sol.get_V()[3], 4.0197863584857476);
    EXPECT_EQ(sol.get_V()[4], 4.0197426648461407);

    EXPECT_EQ(sol.get_temp()[0], temp);
    EXPECT_EQ(sol.get_temp()[1], temp);
    EXPECT_EQ(sol.get_temp()[2], temp);
    EXPECT_EQ(sol.get_temp()[3], temp);
    EXPECT_EQ(sol.get_temp()[4], temp);
}

/**
 * @brief Test the results from the non-isothermal and no degradation single particle simulations using the
 * poly solver.
 *
 * The numbers are the benchmark in-house simulations results.
 *
 */
TEST(SPSolverTest, NonIsoThermalSolvePolySolver)
{
    double temp = 298.15;
    double soc_n = 0.7568;
    double soc_p = 0.4956;

    double discharge_current = 1.656;
    double V_min = 4.0;
    double SOC_lib_min = 0.0;
    double SOC_lib = 0.0;

    std::function<double(double)> OCP_ref_n_ = OCP_ref_n;
    std::function<double(double)> dOCPdT_n_ = dOCPdT_n;
    std::function<double(double)> OCP_ref_p_ = OCP_ref_p;
    std::function<double(double)> dOCPdT_p_ = dOCPdT_p;

    NElectrode elec_n = NElectrode(L_n, A_n, kappa_n, epsilon_n, max_conc_n, R_n, S_n,
                                   T_ref_n, D_ref_n, k_ref_n, Ea_D_n, Ea_R_n, alpha_n,
                                   brugg_n, soc_n, temp, OCP_ref_n_, dOCPdT_n_);
    PElectrode elec_p = PElectrode(L_p, A_p, kappa_p, epsilon_p, max_conc_p, R_p, S_p,
                                   T_ref_p, D_ref_p, k_ref_p, Ea_D_p, Ea_R_p, alpha_p,
                                   brugg_p, soc_p, temp, OCP_ref_p_, dOCPdT_p_);
    Electrolyte electrolyte = Electrolyte(c_init_e, L_e, kappa_e, epsilon_e, brugg_e);
    BatteryCell b_cell = BatteryCell(elec_p, elec_n, electrolyte, rho, Vol, C_p, h, A, cap, V_max, V_min, R_cell);

    Discharge cycler = Discharge(discharge_current, V_min, SOC_lib_min, SOC_lib);

    BatterySolver solver = BatterySolver(b_cell, false, true, "poly");
    Solution sol = solver.solve(cycler);

    EXPECT_EQ(sol.get_V()[0], 4.0199174566872626);
    EXPECT_EQ(sol.get_V()[1], 4.0198742951877362);
    EXPECT_EQ(sol.get_V()[2], 4.0198305958144065);
    EXPECT_EQ(sol.get_V()[3], 4.0197874402091704);
    EXPECT_EQ(sol.get_V()[4], 4.0197437465505015);

    EXPECT_EQ(sol.get_temp()[0], 298.15028422258484);
    EXPECT_EQ(sol.get_temp()[1], 298.15028419862062);
    EXPECT_EQ(sol.get_temp()[2], 298.15056834028428);
    EXPECT_EQ(sol.get_temp()[3], 298.15056829237966);
    EXPECT_EQ(sol.get_temp()[4], 298.15085235315752);
}

/**
 * @brief Test the results from the isothermal and no degradation single particle simulations using the
 * CN solver.
 *
 * The numbers are the benchmark in-house simulations results.
 *
 */
TEST(SPSolverTest, IsoThermalSPSolverCNSolver)
{
    double temp = 298.15;
    double soc_n = 0.7568;
    double soc_p = 0.4956;

    double discharge_current = 1.656;
    double V_min = 4.0;
    double SOC_lib_min = 0.0;
    double SOC_lib = 0.0;

    std::function<double(double)> OCP_ref_n_ = OCP_ref_n;
    std::function<double(double)> dOCPdT_n_ = dOCPdT_n;
    std::function<double(double)> OCP_ref_p_ = OCP_ref_p;
    std::function<double(double)> dOCPdT_p_ = dOCPdT_p;

    NElectrode elec_n = NElectrode(L_n, A_n, kappa_n, epsilon_n, max_conc_n, R_n, S_n,
                                   T_ref_n, D_ref_n, k_ref_n, Ea_D_n, Ea_R_n, alpha_n,
                                   brugg_n, soc_n, temp, OCP_ref_n_, dOCPdT_n_);
    PElectrode elec_p = PElectrode(L_p, A_p, kappa_p, epsilon_p, max_conc_p, R_p, S_p,
                                   T_ref_p, D_ref_p, k_ref_p, Ea_D_p, Ea_R_p, alpha_p,
                                   brugg_p, soc_p, temp, OCP_ref_p_, dOCPdT_p_);
    Electrolyte electrolyte = Electrolyte(c_init_e, L_e, kappa_e, epsilon_e, brugg_e);
    BatteryCell b_cell = BatteryCell(elec_p, elec_n, electrolyte, rho, Vol, C_p, h, A, cap, V_max, V_min, R_cell);

    Discharge cycler = Discharge(discharge_current, V_min, SOC_lib_min, SOC_lib);

    BatterySolver solver = BatterySolver(b_cell, true, true, "CN");
    Solution sol = solver.solve(cycler);

    EXPECT_EQ(sol.get_V()[0], 4.0292677917381994);
    EXPECT_EQ(sol.get_V()[1], 4.0285675827922987);
    EXPECT_EQ(sol.get_V()[2], 4.0280031299585959);
    EXPECT_EQ(sol.get_V()[3], 4.0275294026515862);
    EXPECT_EQ(sol.get_V()[4], 4.0271190042397649);

    EXPECT_EQ(sol.get_temp()[0], temp);
    EXPECT_EQ(sol.get_temp()[1], temp);
    EXPECT_EQ(sol.get_temp()[2], temp);
    EXPECT_EQ(sol.get_temp()[3], temp);
    EXPECT_EQ(sol.get_temp()[4], temp);
}

TEST(ESPBatterySolverTest, MethodSolveIsothermal)
{
    double temp = 298.15;
    double soc_n = 0.7568;
    double soc_p = 0.4956;

    double discharge_current = 1.656;
    double V_min = 4.0;
    double SOC_lib_min = 0.0;
    double SOC_lib = 0.0;

    std::function<double(double)> OCP_ref_n_ = OCP_ref_n;
    std::function<double(double)> dOCPdT_n_ = dOCPdT_n;
    std::function<double(double)> OCP_ref_p_ = OCP_ref_p;
    std::function<double(double)> dOCPdT_p_ = dOCPdT_p;

    NElectrode elec_n = NElectrode(L_n, A_n, kappa_n, epsilon_n, max_conc_n, R_n, S_n,
                                   T_ref_n, D_ref_n, k_ref_n, Ea_D_n, Ea_R_n, alpha_n,
                                   brugg_n, soc_n, temp, OCP_ref_n_, dOCPdT_n_);
    PElectrode elec_p = PElectrode(L_p, A_p, kappa_p, epsilon_p, max_conc_p, R_p, S_p,
                                   T_ref_p, D_ref_p, k_ref_p, Ea_D_p, Ea_R_p, alpha_p,
                                   brugg_p, soc_p, temp, OCP_ref_p_, dOCPdT_p_);
    Electrolyte electrolyte = Electrolyte(c_init_e, L_e, kappa_e, epsilon_en, epsilon_e, epsilon_ep, D_e, t_c, brugg_e);
    BatteryCell b_cell = BatteryCell(elec_p, elec_n, electrolyte, rho, Vol, C_p, h, A, cap, V_max, V_min, R_cell);

    Discharge cycler = Discharge(discharge_current, V_min, SOC_lib_min, SOC_lib);

    ESPBatterySolver solver = ESPBatterySolver(b_cell, true, false, "poly");
    Solution sol = solver.solve(cycler);

    EXPECT_EQ(sol.get_V()[0], 4.0190579108689812);
    EXPECT_EQ(sol.get_V()[1], 4.0190125310905893);
    EXPECT_EQ(sol.get_V()[2], 4.0189671543528735);
    EXPECT_EQ(sol.get_V()[3], 4.0189217806410218);
    EXPECT_EQ(sol.get_V()[4], 4.0188764100058387);

    EXPECT_EQ(sol.get_temp()[0], temp);
    EXPECT_EQ(sol.get_temp()[1], temp);
    EXPECT_EQ(sol.get_temp()[2], temp);
    EXPECT_EQ(sol.get_temp()[3], temp);
    EXPECT_EQ(sol.get_temp()[4], temp);
}