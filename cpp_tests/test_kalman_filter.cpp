#include "gtest/gtest.h"
#include "Eigen/Dense"

#include "kalman_filter.h"

TEST(SigmaPointKalmanFilterTest, LowerCholeskydecompositon)
{
    Eigen::Matrix3d mat;
    mat << 4, 12, -16, 12, 37, -43, -16, -43, 98;

    Eigen::MatrixXd sqrt_mat = SigmaPointKalmanFilter().calc_sqrt_matrix(mat);

    EXPECT_EQ(sqrt_mat(0, 0), 2.0);
    EXPECT_EQ(sqrt_mat(0, 1), 0.0);
    EXPECT_EQ(sqrt_mat(0, 2), 0.0);
    EXPECT_EQ(sqrt_mat(1, 0), 6.0);
    EXPECT_EQ(sqrt_mat(1, 1), 1.0);
    EXPECT_EQ(sqrt_mat(1, 2), 0.0);
    EXPECT_EQ(sqrt_mat(2, 0), -8.0);
    EXPECT_EQ(sqrt_mat(2, 1), 5.0);
    EXPECT_EQ(sqrt_mat(2, 2), 3.0);
}
