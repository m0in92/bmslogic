#include "gtest/gtest.h"

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
    PolynomialApprox solver_instance = PolynomialApprox(electrode_type, c_max*SOC_init, solver_type);
    
    solver_instance.solve(dt, t_prev, I_app, R, S, D);
    EXPECT_EQ(solver_instance.get_c_surf() / c_max, 0.7504676658078573);
    solver_instance.solve(dt, t_prev, I_app, R, S, D);
    EXPECT_EQ(solver_instance.get_c_surf() / c_max, 0.750422969925152);
}