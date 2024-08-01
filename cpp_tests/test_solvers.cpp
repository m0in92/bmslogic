#include "gtest/gtest.h"

#include "extern/owl.h"
#include "solvers.h"

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