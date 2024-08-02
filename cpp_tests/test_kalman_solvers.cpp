#include "gtest/gtest.h"

#include "kalman_solvers.h"

TEST(SPKFPolynomialApprox, Constructor)
{
    double c_init = 3200;
    double cov_x = 10;
    double cov_v = 20;
    double cov_w = 30;
    SPKFPolynomialApprox solver_instance = SPKFPolynomialApprox('n', c_init, 1e-8, 1.1, 1e-10,
                                                                cov_x, cov_w, cov_v);

    EXPECT_EQ(solver_instance.get_spkf_solver().get_x().get_vec()[0], c_init);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_w().get_vec()[0], 0.0);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_w().get_vec()[0], 0.0);

    EXPECT_EQ(solver_instance.get_spkf_solver().get_x().get_cov()(0, 0), cov_x);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_w().get_cov()(0, 0), cov_w);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_v().get_cov()(0, 0), cov_v);
}

TEST(SPKFPolynomialApprox, AugmentsStatesAndAugmentedCov)
{
    double c_init = 3200;
    double cov_x = 10;
    double cov_v = 20;
    double cov_w = 30;
    SPKFPolynomialApprox solver_instance = SPKFPolynomialApprox('n', c_init, 1e-8, 1.1, 1e-10,
                                                                cov_x, cov_w, cov_v);

    // Check the values from the augmented vector
    EXPECT_EQ(solver_instance.get_spkf_solver().get_aug_vec()(0), c_init);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_aug_vec()(1), 0.0);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_aug_vec()(2), 0.0);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_aug_vec().size(), 3);

    // Check the values of the augmented covariance matrix
    EXPECT_EQ(solver_instance.get_spkf_solver().get_aug_cov()(0, 0), cov_x);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_aug_cov()(0, 1), 0.0);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_aug_cov()(0, 1), 0.0);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_aug_cov()(1, 0), 0.0);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_aug_cov()(1, 1), cov_w);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_aug_cov()(1, 2), 0.0);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_aug_cov()(2, 0), 0.0);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_aug_cov()(2, 1), 0.0);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_aug_cov()(2, 2), cov_v);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_aug_cov().rows(), 3);
    EXPECT_EQ(solver_instance.get_spkf_solver().get_aug_cov().cols(), 3);

    // Check the values of the square of the augmented covariance matrix.
    Eigen::Matrix<double, 3, 3> sqrt_matrix = solver_instance.get_spkf_solver().calc_sqrt_matrix(solver_instance.get_spkf_solver().get_aug_cov());
    EXPECT_NEAR(sqrt_matrix(0, 0), 3.1622776601683795, 1e-6);
    EXPECT_NEAR(sqrt_matrix(0, 1), 0.0, 1e-6);
    EXPECT_NEAR(sqrt_matrix(0, 2), 0.0, 1e-6);
    EXPECT_NEAR(sqrt_matrix(1, 0), 0.0, 1e-6);
    EXPECT_NEAR(sqrt_matrix(1, 1), 5.47723, 1e-3);
    EXPECT_NEAR(sqrt_matrix(1, 2), 0.0, 1e-6);
    EXPECT_NEAR(sqrt_matrix(2, 0), 0.0, 1e-6);
    EXPECT_NEAR(sqrt_matrix(2, 1), 0.0, 1e-6);
    EXPECT_NEAR(sqrt_matrix(2, 2), 4.47214, 1e-3);
}
