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