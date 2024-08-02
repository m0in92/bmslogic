#include <cmath>
#include <functional>

#include "gtest/gtest.h"
#include "Eigen/Dense"

#include "kalman_filter.h"

[[nodiscard]] Eigen::VectorXd state_equation_(Eigen::VectorXd x_k, Eigen::VectorXd u_k, Eigen::VectorXd w_k)
{
    Eigen::VectorXd result(2);
    result(0) = std::sqrt(5 + x_k(1)) + w_k(0);
    result(1) = std::sqrt(5 + x_k(1)) + w_k(0);
    return result;
}

[[nodiscard]] Eigen::VectorXd output_equation_(Eigen::VectorXd x_k, Eigen::VectorXd u_k, Eigen::VectorXd v_k)
{
    Eigen::VectorXd result(1);
    result << std::pow(x_k(0), 3) + v_k(0);
    return result;
}

TEST(NormalRandomVectorTest, Constructor)
{
    const int SIZE = 2;
    Eigen::Matrix<double, SIZE, 1> vec_x{5, 10};
    Eigen::Matrix<double, SIZE, SIZE> cov_x{{1e-3, 0}, {0, 2e-3}};

    NormalRandomVector x = NormalRandomVector(vec_x, cov_x);

    EXPECT_EQ(x.get_vec()(0), 5);
    EXPECT_EQ(x.get_vec()(1), 10);

    EXPECT_EQ(x.get_cov()(0, 0), 1e-3);
    EXPECT_EQ(x.get_cov()(0, 1), 0.0);
    EXPECT_EQ(x.get_cov()(1, 0), 0.0);
    EXPECT_EQ(x.get_cov()(1, 1), 2e-3);
}

TEST(SigmaPointKalmanFilterTest, ConstructorAugVectorAndAugCov)
{
    Eigen::Matrix<double, 2, 1> vec_x{2, 2};
    Eigen::Matrix<double, 2, 2> cov_x{{2.0, 0.0}, {0.0, 2.0}};
    Eigen::Matrix<double, 1, 1> vec_w{0.0};
    Eigen::Matrix<double, 1, 1> cov_w{{1.0}};
    Eigen::Matrix<double, 1, 1> vec_v{0.0};
    Eigen::Matrix<double, 1, 1> cov_v{{2.0}};

    NormalRandomVector x = NormalRandomVector(vec_x, cov_x);
    NormalRandomVector w = NormalRandomVector(vec_w, cov_w);
    NormalRandomVector v = NormalRandomVector(vec_v, cov_v);

    int y_dim = 1;

    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> state_equation = state_equation;
    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> output_equation = output_equation;
    SigmaPointKalmanFilter solver = SigmaPointKalmanFilter(x, w, v, y_dim, state_equation, output_equation);

    EXPECT_EQ(solver.get_Nx(), 2);
    EXPECT_EQ(solver.get_Nw(), 1);
    EXPECT_EQ(solver.get_Nv(), 1);

    Eigen::VectorXd result_aug_vector = solver.get_aug_vec();
    EXPECT_EQ(result_aug_vector(0), 2.0);
    EXPECT_EQ(result_aug_vector(1), 2.0);
    EXPECT_EQ(result_aug_vector(2), 0.0);
    EXPECT_EQ(result_aug_vector(3), 0.0);

    Eigen::MatrixXd result_aug_cov = solver.get_aug_cov();
    EXPECT_EQ(result_aug_cov(0, 0), 2.0);
    EXPECT_EQ(result_aug_cov(1, 1), 2.0);
    EXPECT_EQ(result_aug_cov(2, 2), 1.0);
    EXPECT_EQ(result_aug_cov(3, 3), 2.0);
}

/**
 * @brief Results from the inhouse benchmark tests.
 *
 */
TEST(SigmaPointKalmanFilterTest, ConstructorSigmaPoints)
{
    Eigen::Matrix<double, 2, 1> vec_x{2, 2};
    Eigen::Matrix<double, 2, 2> cov_x{{2.0, 0.0}, {0.0, 2.0}};
    Eigen::Matrix<double, 1, 1> vec_w{0.0};
    Eigen::Matrix<double, 1, 1> cov_w{{1.0}};
    Eigen::Matrix<double, 1, 1> vec_v{0.0};
    Eigen::Matrix<double, 1, 1> cov_v{{2.0}};

    NormalRandomVector x = NormalRandomVector(vec_x, cov_x);
    NormalRandomVector w = NormalRandomVector(vec_w, cov_w);
    NormalRandomVector v = NormalRandomVector(vec_v, cov_v);

    int y_dim = 1;

    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> state_equation = state_equation;
    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> output_equation = output_equation;
    SigmaPointKalmanFilter solver = SigmaPointKalmanFilter(x, w, v, y_dim, state_equation, output_equation);

    Eigen::MatrixXd result_sigma_pts = solver.get_mat_sigma_pts();

    // first row
    EXPECT_NEAR(result_sigma_pts(0, 0), 2.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(0, 1), 4.4494897427831788, 1e-6);
    EXPECT_NEAR(result_sigma_pts(0, 2), 2.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(0, 3), 2.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(0, 4), 2.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(0, 5), -0.44948974279999998, 1e-6);
    EXPECT_NEAR(result_sigma_pts(0, 6), 2.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(0, 7), 2.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(0, 8), 2.0, 1e-6);

    // second row
    EXPECT_NEAR(result_sigma_pts(1, 0), 2.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(1, 1), 2, 1e-6);
    EXPECT_NEAR(result_sigma_pts(1, 2), 4.4494897428, 1e-6);
    EXPECT_NEAR(result_sigma_pts(1, 3), 2.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(1, 4), 2.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(1, 5), 2.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(1, 6), -0.4494897428, 1e-6);
    EXPECT_NEAR(result_sigma_pts(1, 7), 2.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(1, 8), 2.0, 1e-6);

    // third row
    EXPECT_NEAR(result_sigma_pts(2, 0), 0.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(2, 1), 0.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(2, 2), 0.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(2, 3), 1.7320508076, 1e-6);
    EXPECT_NEAR(result_sigma_pts(2, 4), 0.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(2, 5), 0.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(2, 6), 0.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(2, 7), -1.7320508076, 1e-6);
    EXPECT_NEAR(result_sigma_pts(2, 8), 0.0, 1e-6);

    // fourth row
    EXPECT_NEAR(result_sigma_pts(3, 0), 0.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(3, 1), 0.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(3, 2), 0.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(3, 3), 0.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(3, 4), 2.4494897428, 1e-6);
    EXPECT_NEAR(result_sigma_pts(3, 5), 0.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(3, 6), 0.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(3, 7), 0.0, 1e-6);
    EXPECT_NEAR(result_sigma_pts(3, 8), -2.4494897428, 1e-6);
}

TEST(SigmaPointKalmanFilterTest, TestStep1)
{
    Eigen::Matrix<double, 2, 1> vec_x{2, 2};
    Eigen::Matrix<double, 2, 2> cov_x{{2.0, 0.0}, {0.0, 2.0}};
    Eigen::Matrix<double, 1, 1> vec_w{0.0};
    Eigen::Matrix<double, 1, 1> cov_w{{1.0}};
    Eigen::Matrix<double, 1, 1> vec_v{0.0};
    Eigen::Matrix<double, 1, 1> cov_v{{2.0}};

    NormalRandomVector x = NormalRandomVector(vec_x, cov_x);
    NormalRandomVector w = NormalRandomVector(vec_w, cov_w);
    NormalRandomVector v = NormalRandomVector(vec_v, cov_v);

    int y_dim = 1;

    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> state_equation = state_equation_;
    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> output_equation = output_equation_;
    SigmaPointKalmanFilter solver = SigmaPointKalmanFilter(x, w, v, y_dim, state_equation, output_equation);

    Eigen::VectorXd u(1);
    u(0) = 0.0;
    Eigen::MatrixXd result = solver.calc_and_set_state_prediction(u);

    EXPECT_NEAR(solver.get_x().get_vec()(0), 2.6316999972, 1e-6);
    EXPECT_NEAR(solver.get_x().get_vec()(1), 2.6316999972, 1e-6);

    EXPECT_NEAR(result(0, 0), 2.6457513111, 1e-6);
    EXPECT_NEAR(result(0, 1), 2.6457513111, 1e-6);
    EXPECT_NEAR(result(0, 2), 3.0740022353, 1e-6);
    EXPECT_NEAR(result(0, 3), 4.3778021186, 1e-6);
    EXPECT_NEAR(result(0, 4), 2.6457513111, 1e-6);
    EXPECT_NEAR(result(0, 5), 2.6457513111, 1e-6);
    EXPECT_NEAR(result(0, 6), 2.1331925036, 1e-6);
    EXPECT_NEAR(result(0, 7), 0.9137005035, 1e-6);
    EXPECT_NEAR(result(0, 8), 2.6457513111, 1e-6);

    EXPECT_NEAR(result(1, 0), 2.6457513111, 1e-6);
    EXPECT_NEAR(result(1, 1), 2.6457513111, 1e-6);
    EXPECT_NEAR(result(1, 2), 3.0740022353, 1e-6);
    EXPECT_NEAR(result(1, 3), 4.3778021186, 1e-6);
    EXPECT_NEAR(result(1, 4), 2.6457513111, 1e-6);
    EXPECT_NEAR(result(1, 5), 2.6457513111, 1e-6);
    EXPECT_NEAR(result(1, 6), 2.1331925036, 1e-6);
    EXPECT_NEAR(result(1, 7), 0.9137005035, 1e-6);
    EXPECT_NEAR(result(1, 8), 2.6457513111, 1e-6);
}

TEST(SigmaPointKalmanFilterTest, TestStep2)
{
    Eigen::Matrix<double, 2, 1> vec_x{2, 2};
    Eigen::Matrix<double, 2, 2> cov_x{{2.0, 0.0}, {0.0, 2.0}};
    Eigen::Matrix<double, 1, 1> vec_w{0.0};
    Eigen::Matrix<double, 1, 1> cov_w{{1.0}};
    Eigen::Matrix<double, 1, 1> vec_v{0.0};
    Eigen::Matrix<double, 1, 1> cov_v{{2.0}};

    NormalRandomVector x = NormalRandomVector(vec_x, cov_x);
    NormalRandomVector w = NormalRandomVector(vec_w, cov_w);
    NormalRandomVector v = NormalRandomVector(vec_v, cov_v);

    int y_dim = 1;

    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> state_equation = state_equation_;
    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> output_equation = output_equation_;
    SigmaPointKalmanFilter solver = SigmaPointKalmanFilter(x, w, v, y_dim, state_equation, output_equation);

    Eigen::VectorXd u(1);
    u(0) = 0.0;
    Eigen::MatrixXd result_step1 = solver.calc_and_set_state_prediction(u);
    Eigen::MatrixXd result_step2 = solver.calc_and_set_state_covariance(result_step1);

    EXPECT_NEAR(solver.get_x().get_cov()(0, 0), 1.0741551248, 1e-6);
    EXPECT_NEAR(solver.get_x().get_cov()(0, 1), 1.0741551248, 1e-6);
    EXPECT_NEAR(solver.get_x().get_cov()(1, 0), 1.0741551248, 1e-6);
    EXPECT_NEAR(solver.get_x().get_cov()(1, 1), 1.0741551248, 1e-6);

    EXPECT_NEAR(result_step2(0, 0), 0.0140513139, 1e-6);
    EXPECT_NEAR(result_step2(0, 1), 0.0140513139, 1e-6);
    EXPECT_NEAR(result_step2(0, 2), 0.4423022381, 1e-6);
    EXPECT_NEAR(result_step2(0, 3), 1.7461021214, 1e-6);
    EXPECT_NEAR(result_step2(0, 4), 0.0140513139, 1e-6);
    EXPECT_NEAR(result_step2(0, 5), 0.0140513139, 1e-6);
    EXPECT_NEAR(result_step2(0, 6), -0.4985074936, 1e-6);
    EXPECT_NEAR(result_step2(0, 7), -1.7179994937, 1e-6);
    EXPECT_NEAR(result_step2(0, 8), 0.0140513139, 1e-6);

    EXPECT_NEAR(result_step2(1, 0), 0.0140513139, 1e-6);
    EXPECT_NEAR(result_step2(1, 1), 0.0140513139, 1e-6);
    EXPECT_NEAR(result_step2(1, 2), 0.4423022381, 1e-6);
    EXPECT_NEAR(result_step2(1, 3), 1.7461021214, 1e-6);
    EXPECT_NEAR(result_step2(1, 4), 0.0140513139, 1e-6);
    EXPECT_NEAR(result_step2(1, 5), 0.0140513139, 1e-6);
    EXPECT_NEAR(result_step2(1, 6), -0.4985074936, 1e-6);
    EXPECT_NEAR(result_step2(1, 7), -1.7179994937, 1e-6);
    EXPECT_NEAR(result_step2(1, 8), 0.0140513139, 1e-6);
}

TEST(SigmaPointKalmanFilterTest, TestStep3)
{
    Eigen::Matrix<double, 2, 1> vec_x{2, 2};
    Eigen::Matrix<double, 2, 2> cov_x{{2.0, 0.0}, {0.0, 2.0}};
    Eigen::Matrix<double, 1, 1> vec_w{0.0};
    Eigen::Matrix<double, 1, 1> cov_w{{1.0}};
    Eigen::Matrix<double, 1, 1> vec_v{0.0};
    Eigen::Matrix<double, 1, 1> cov_v{{2.0}};

    NormalRandomVector x = NormalRandomVector(vec_x, cov_x);
    NormalRandomVector w = NormalRandomVector(vec_w, cov_w);
    NormalRandomVector v = NormalRandomVector(vec_v, cov_v);

    int y_dim = 1;

    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> state_equation = state_equation_;
    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> output_equation = output_equation_;
    SigmaPointKalmanFilter solver = SigmaPointKalmanFilter(x, w, v, y_dim, state_equation, output_equation);

    Eigen::VectorXd u(1);
    u(0) = 0.0;
    Eigen::MatrixXd result_step1 = solver.calc_and_set_state_prediction(u);
    Eigen::MatrixXd result_step2 = solver.calc_and_set_state_covariance(result_step1);
    std::pair<Eigen::MatrixXd, Eigen::VectorXd> y_predictions = solver.predict_system_output(result_step2, u);

    EXPECT_NEAR(y_predictions.second(0), 0.0359298229, 1e-8);

    EXPECT_NEAR(y_predictions.first(0, 0), 0.0000027743, 1e-6);
    EXPECT_NEAR(y_predictions.first(0, 1), 0.0000027743, 1e-6);
    EXPECT_NEAR(y_predictions.first(0, 2), 0.0865281485, 1e-6);
    EXPECT_NEAR(y_predictions.first(0, 3), 5.3236429472, 1e-6);
    EXPECT_NEAR(y_predictions.first(0, 4), 3.4641043894, 1e-6);
    EXPECT_NEAR(y_predictions.first(0, 5), 0.0000027743, 1e-6);
    EXPECT_NEAR(y_predictions.first(0, 6), -0.1238839583, 1e-6);
    EXPECT_NEAR(y_predictions.first(0, 7), -5.0707137489, 1e-6);
    EXPECT_NEAR(y_predictions.first(0, 8), -3.4640988409, 1e-6);
}

TEST(SigmaPointKalmanFilterTest, TestStep4)
{
    Eigen::Matrix<double, 2, 1> vec_x{2, 2};
    Eigen::Matrix<double, 2, 2> cov_x{{2.0, 0.0}, {0.0, 2.0}};
    Eigen::Matrix<double, 1, 1> vec_w{0.0};
    Eigen::Matrix<double, 1, 1> cov_w{{1.0}};
    Eigen::Matrix<double, 1, 1> vec_v{0.0};
    Eigen::Matrix<double, 1, 1> cov_v{{2.0}};

    NormalRandomVector x = NormalRandomVector(vec_x, cov_x);
    NormalRandomVector w = NormalRandomVector(vec_w, cov_w);
    NormalRandomVector v = NormalRandomVector(vec_v, cov_v);

    int y_dim = 1;

    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> state_equation = state_equation_;
    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> output_equation = output_equation_;
    SigmaPointKalmanFilter solver = SigmaPointKalmanFilter(x, w, v, y_dim, state_equation, output_equation);

    Eigen::VectorXd u(1);
    u(0) = 0.0;
    Eigen::MatrixXd result_step1 = solver.calc_and_set_state_prediction(u);
    Eigen::MatrixXd result_step2 = solver.calc_and_set_state_covariance(result_step1);
    std::pair<Eigen::MatrixXd, Eigen::VectorXd> y_predictions = solver.predict_system_output(result_step2, u);
    std::pair<Eigen::MatrixXd, Eigen::MatrixXd> estimator_gain = solver.estimator_gain_matrix(y_predictions.first, y_predictions.second, result_step2);

    EXPECT_NEAR(estimator_gain.first(0, 0), 13.0114001325, 1e-6);
    EXPECT_NEAR(estimator_gain.second(0, 0), 0.2319393822, 1e-6);
    EXPECT_NEAR(estimator_gain.second(1, 0), 0.2319393822, 1e-6);
}

TEST(SigmaPointKalmanFilterTest, TestStep5)
{
    Eigen::Matrix<double, 2, 1> vec_x{2, 2};
    Eigen::Matrix<double, 2, 2> cov_x{{2.0, 0.0}, {0.0, 2.0}};
    Eigen::Matrix<double, 1, 1> vec_w{0.0};
    Eigen::Matrix<double, 1, 1> cov_w{{1.0}};
    Eigen::Matrix<double, 1, 1> vec_v{0.0};
    Eigen::Matrix<double, 1, 1> cov_v{{2.0}};

    NormalRandomVector x = NormalRandomVector(vec_x, cov_x);
    NormalRandomVector w = NormalRandomVector(vec_w, cov_w);
    NormalRandomVector v = NormalRandomVector(vec_v, cov_v);

    int y_dim = 1;

    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> state_equation = state_equation_;
    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> output_equation = output_equation_;
    SigmaPointKalmanFilter solver = SigmaPointKalmanFilter(x, w, v, y_dim, state_equation, output_equation);

    Eigen::VectorXd u(1);
    u(0) = 0.0;
    Eigen::MatrixXd result_step1 = solver.calc_and_set_state_prediction(u);
    Eigen::MatrixXd result_step2 = solver.calc_and_set_state_covariance(result_step1);
    std::pair<Eigen::MatrixXd, Eigen::VectorXd> y_predictions = solver.predict_system_output(result_step2, u);
    std::pair<Eigen::MatrixXd, Eigen::MatrixXd> estimator_gain = solver.estimator_gain_matrix(y_predictions.first, y_predictions.second, result_step2);

    Eigen::VectorXd y_true(1);
    y_true(0) = 0.04;
    solver.set_final_state_estimate(estimator_gain.second, y_true, y_predictions.second);

    EXPECT_NEAR(solver.get_x().get_vec()(0), 2.6326440316, 1e-6);
    EXPECT_NEAR(solver.get_x().get_vec()(1), 2.6326440316, 1e-6);
}

TEST(SigmaPointKalmanFilterTest, TestStep6)
{
    Eigen::Matrix<double, 2, 1> vec_x{2, 2};
    Eigen::Matrix<double, 2, 2> cov_x{{2.0, 0.0}, {0.0, 2.0}};
    Eigen::Matrix<double, 1, 1> vec_w{0.0};
    Eigen::Matrix<double, 1, 1> cov_w{{1.0}};
    Eigen::Matrix<double, 1, 1> vec_v{0.0};
    Eigen::Matrix<double, 1, 1> cov_v{{2.0}};

    NormalRandomVector x = NormalRandomVector(vec_x, cov_x);
    NormalRandomVector w = NormalRandomVector(vec_w, cov_w);
    NormalRandomVector v = NormalRandomVector(vec_v, cov_v);

    int y_dim = 1;

    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> state_equation = state_equation_;
    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> output_equation = output_equation_;
    SigmaPointKalmanFilter solver = SigmaPointKalmanFilter(x, w, v, y_dim, state_equation, output_equation);

    Eigen::VectorXd u(1);
    u(0) = 0.0;
    Eigen::MatrixXd result_step1 = solver.calc_and_set_state_prediction(u);
    Eigen::MatrixXd result_step2 = solver.calc_and_set_state_covariance(result_step1);
    std::pair<Eigen::MatrixXd, Eigen::VectorXd> y_predictions = solver.predict_system_output(result_step2, u);
    std::pair<Eigen::MatrixXd, Eigen::MatrixXd> estimator_gain = solver.estimator_gain_matrix(y_predictions.first, y_predictions.second, result_step2);

    Eigen::VectorXd y_true(1);
    y_true(0) = 0.04;
    solver.set_final_state_estimate(estimator_gain.second, y_true, y_predictions.second);
    solver.set_final_cov_estimate(estimator_gain.second, estimator_gain.first);

    EXPECT_NEAR(solver.get_x().get_cov()(0, 0), 0.3741954434, 1e-6);
    EXPECT_NEAR(solver.get_x().get_cov()(0, 1), 0.3741954434, 1e-6);
    EXPECT_NEAR(solver.get_x().get_cov()(1, 0), 0.3741954434, 1e-6);
    EXPECT_NEAR(solver.get_x().get_cov()(1, 1), 0.3741954434, 1e-6);
}

TEST(LowerCholeskyDecompositionTest, LowerCholeskydecompositon)
{
    Eigen::Matrix3d mat;
    mat << 4, 12, -16, 12, 37, -43, -16, -43, 98;

    Eigen::MatrixXd sqrt_mat = lower_Cholesky_decomposition(mat);

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
