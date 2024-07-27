#include <iostream>

#include "kalman_filter.h"

NormalRandomVector::NormalRandomVector(Eigen::VectorXd i_vec, Eigen::MatrixXd i_cov) : m_vec(i_vec), m_cov(i_cov)
{
    try
    {
        check_for_square_matrix(i_cov);
        check_for_vector_size_with_matrix(i_vec, m_cov);
    }
    catch (InvalidSize &e)
    {
        std::cout << e.what() << std::endl;
    }
}

void NormalRandomVector::check_for_square_matrix(Eigen::MatrixXd i_matrix)
{
    if (i_matrix.rows() != i_matrix.cols())
        throw InvalidSize();
}

void NormalRandomVector::check_for_vector_size_with_matrix(Eigen::VectorXd i_vec, Eigen::MatrixXd i_matrix)
{
    if (i_vec.size() != i_matrix.rows())
        throw InvalidSize();
}

SigmaPointKalmanFilter::SigmaPointKalmanFilter(NormalRandomVector i_x, NormalRandomVector i_w, NormalRandomVector i_v,
                                               int i_y_dim,
                                               std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> &i_state_equation,
                                               std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> &i_output_equation,
                                               std::string i_method_type) : m_x(i_x), m_w(i_w), m_v(i_v), m_y_dim(i_y_dim),
                                                                            m_state_equation(i_state_equation), m_output_equation(i_output_equation),
                                                                            m_method_type(i_method_type)
{
    if (i_method_type.compare("CDKF") != 0)
        throw InvalidKFMethodType();

    m_Nx = static_cast<int>(m_x.get_vec().rows());
    m_Nw = static_cast<int>(m_w.get_vec().rows());
    m_Nv = static_cast<int>(m_v.get_vec().rows());
    m_L = m_Nx + m_Nw + m_Nv;
    m_p = 2 * m_L;

    calc_and_set_gamma();
    calc_and_set_h();
    calc_and_set_alpha_m0();
    calc_and_set_alpha_m();
    calc_and_set_alpha_c0();
    calc_and_set_alpha_c();

    m_vec_alpha_m = m_alpha_m * Eigen::VectorXd::Constant(m_p + 1, 1);
    m_vec_alpha_m(0) = m_alpha_m0;

    m_vec_alpha_c = m_alpha_c * Eigen::VectorXd::Constant(m_p + 1, 1);
    m_vec_alpha_c(0) = m_alpha_c0;
}

SigmaPointKalmanFilter::SigmaPointKalmanFilter(NormalRandomVector i_x, NormalRandomVector i_w, NormalRandomVector i_v,
                                               int i_y_dim) : m_x(i_x), m_w(i_w), m_v(i_v), m_y_dim(i_y_dim)
{
    if (m_method_type.compare("CDKF") != 0)
        throw InvalidKFMethodType();

    m_Nx = static_cast<int>(m_x.get_vec().rows());
    m_Nw = static_cast<int>(m_w.get_vec().rows());
    m_Nv = static_cast<int>(m_v.get_vec().rows());
    m_L = m_Nx + m_Nw + m_Nv;
    m_p = 2 * m_L;

    calc_and_set_gamma();
    calc_and_set_h();
    calc_and_set_alpha_m0();
    calc_and_set_alpha_m();
    calc_and_set_alpha_c0();
    calc_and_set_alpha_c();

    m_vec_alpha_m = m_alpha_m * Eigen::VectorXd::Constant(m_p + 1, 1);
    m_vec_alpha_m(0) = m_alpha_m0;

    m_vec_alpha_c = m_alpha_c * Eigen::VectorXd::Constant(m_p + 1, 1);
    m_vec_alpha_c(0) = m_alpha_c0;
}

Eigen::VectorXd SigmaPointKalmanFilter::generate_aug_vec()
{
    auto size_aug_vec = m_x.get_vec().size() + m_w.get_vec().size() + m_v.get_vec().size();

    Eigen::VectorXd vec_aug_cov(size_aug_vec);
    vec_aug_cov << m_x.get_vec(), m_w.get_vec(), m_v.get_vec();
    return vec_aug_cov;
}

Eigen::MatrixXd SigmaPointKalmanFilter::generate_aug_cov()
{
    int num_rows_x = static_cast<int>(m_x.get_cov().rows());
    int num_cols_x = static_cast<int>(m_x.get_cov().cols());
    int num_rows_w = static_cast<int>(m_w.get_cov().rows());
    int num_cols_w = static_cast<int>(m_w.get_cov().cols());
    int num_rows_v = static_cast<int>(m_v.get_cov().rows());
    int num_cols_v = static_cast<int>(m_v.get_cov().cols());

    auto num_rows = num_rows_x + num_rows_w + num_rows_v;
    auto num_cols = num_cols_x + num_rows_w + num_rows_v;

    Eigen::MatrixXd result_matrix = Eigen::MatrixXd::Zero(num_rows, num_cols);
    result_matrix.block(0, 0, num_rows_x, num_cols_x) = m_x.get_cov();
    result_matrix.block(num_rows_x, num_cols_x, num_rows_w, num_cols_w) = m_w.get_cov();
    result_matrix.block(num_rows_x + num_rows_w, num_cols_x + num_cols_w, num_rows_v, num_cols_v) = m_v.get_cov();

    return result_matrix;
}

Eigen::MatrixXd SigmaPointKalmanFilter::calc_sqrt_matrix(Eigen::MatrixXd i_matrix)
{
    Eigen::LLT<Eigen::MatrixXd> sqrt_matrix(i_matrix);
    return sqrt_matrix.matrixL();
}

void SigmaPointKalmanFilter::calc_and_set_gamma()
{
    if (m_method_type == "CDKF")
        m_gamma = std::sqrt(3.0);
    else
        throw InvalidKFMethodType();
}

void SigmaPointKalmanFilter::calc_and_set_h()
{
    if (m_method_type == "CDKF")
        m_h = std::sqrt(3.0);
    else
        throw InvalidKFMethodType();
}

void SigmaPointKalmanFilter::calc_and_set_alpha_m0()
{
    if (m_method_type == "CDKF")
        m_alpha_m0 = (std::pow(m_h, 2) - m_L) / (std::pow(m_h, 2));
    else
        throw InvalidKFMethodType();
}

void SigmaPointKalmanFilter::calc_and_set_alpha_m()
{
    if (m_method_type == "CDKF")
        m_alpha_m = 1 / (2 * std::pow(m_h, 2));
    else
        throw InvalidKFMethodType();
}

void SigmaPointKalmanFilter::calc_and_set_alpha_c0()
{
    if (m_method_type.compare("CDKF") == 0)
        m_alpha_c0 = (std::pow(m_h, 2) - m_L) / (std::pow(m_h, 2));
    else
        throw InvalidKFMethodType();
}

void SigmaPointKalmanFilter::calc_and_set_alpha_c()
{
    if (m_method_type.compare("CDKF") == 0)
        m_alpha_c = 1 / (2 * std::pow(m_h, 2));
    else
        throw InvalidKFMethodType();
}

Eigen::MatrixXd SigmaPointKalmanFilter::generate_mat_sigma_pts()
{
    Eigen::VectorXd aug_vec = get_aug_vec();
    Eigen::MatrixXd aug_std = calc_sqrt_matrix(get_aug_cov());
    Eigen::MatrixXd result_matrix = Eigen::MatrixXd::Zero(aug_std.rows(), m_p + 1);

    result_matrix.col(0) = aug_vec;
    result_matrix.col(1) = aug_vec + aug_std.col(0);
    for (int i = 0; i < m_L; i++)
    {
        result_matrix.col(i + 1) = aug_vec + m_gamma * aug_std.col(i);
        result_matrix.col(i + 1 + m_L) = aug_vec - m_gamma * aug_std.col(i);
    }
    return result_matrix;
}

/**
 * @brief  This is the step 1a (first step) of the process. The state estimate is performed in this step.
 *
 * @param u  The process input.
 * @return Eigen::MatrixXd
 */
Eigen::MatrixXd SigmaPointKalmanFilter::calc_and_set_state_prediction(Eigen::VectorXd u)
{
    Eigen::MatrixXd mat_sigma_pts = generate_mat_sigma_pts();

    Eigen::MatrixXd x_sp = mat_sigma_pts(Eigen::seq(0, m_Nx - 1), Eigen::all);
    Eigen::MatrixXd w_sp = mat_sigma_pts(Eigen::seq(m_Nx, m_Nx + m_Nw - 1), Eigen::all);

    // the obtained sigma points needs to be passed through the states equation
    Eigen::MatrixXd function_results(m_Nx, mat_sigma_pts.cols());
    for (int i = 0; i < static_cast<int>(mat_sigma_pts.cols()); i++)
    {
        Eigen::VectorXd x_sp_(m_Nx);
        x_sp_ = x_sp.col(i);
        Eigen::VectorXd w_sp_(m_Nw);
        w_sp_ = w_sp.col(i);

        function_results.col(i) = m_state_equation(x_sp_, u, w_sp_);
    }

    // Calculation and setting of the state estimate
    m_x.set_vec((function_results * m_vec_alpha_m).col(0));

    return function_results;
}

Eigen::MatrixXd SigmaPointKalmanFilter::calc_and_set_state_covariance(Eigen::MatrixXd state_equation_results)
{
    Eigen::MatrixXd Xs(state_equation_results.rows(), state_equation_results.cols());
    Eigen::MatrixXd state_prediction(m_Nx, 1);
    state_prediction.col(0) = m_x.get_vec();
    for (int i = 0; i < static_cast<int>(state_equation_results.cols()); i++)
    {
        Xs.col(i) = state_equation_results.col(i) - state_prediction.col(0);
    }

    // create diagonal matrix containing the array
    const int diagonal_size = static_cast<int>(m_vec_alpha_c.size());
    Eigen::MatrixXd alpha_c_ = m_vec_alpha_c.asDiagonal();

    // calculates and sets the covariance estimates
    Eigen::MatrixXd cov_estimate = Xs * alpha_c_ * Xs.transpose();
    m_x.set_cov(cov_estimate);
    return Xs;
}

std::pair<Eigen::MatrixXd, Eigen::VectorXd> SigmaPointKalmanFilter::predict_system_output(Eigen::MatrixXd state_equation_output, Eigen::VectorXd u)
{
    Eigen::MatrixXd mat_sigma_pts = generate_mat_sigma_pts();
    Eigen::MatrixXd v_sp = mat_sigma_pts(Eigen::seq(m_Nx + m_Nw, Eigen::last), Eigen::all);

    // pass the state estimates through the output function
    Eigen::MatrixXd big_y(m_y_dim, mat_sigma_pts.cols());
    Eigen::VectorXd x_(m_Nx);
    Eigen::VectorXd v_sp_(m_Nv);
    for (int i = 0; i < static_cast<int>(mat_sigma_pts.cols()); i++)
    {
        x_ = state_equation_output.col(i);
        v_sp_ = v_sp.col(i);
        big_y.col(i) = m_output_equation(x_, u, v_sp_);
    }

    // y_prediction
    Eigen::VectorXd y_prediction = big_y * m_vec_alpha_m;

    return {big_y, y_prediction};
}

std::pair<Eigen::MatrixXd, Eigen::MatrixXd> SigmaPointKalmanFilter::estimator_gain_matrix(Eigen::MatrixXd big_y, Eigen::VectorXd y_prediction, Eigen::MatrixXd Xs)
{
    // SigmaY calculation
    Eigen::MatrixXd Ys(m_y_dim, big_y.cols());
    for (int i = 0; i < static_cast<int>(big_y.cols()); i++)
    {
        Ys.col(i) = big_y.col(i) - y_prediction;
    }
    Eigen::MatrixXd sigma_y = Ys * m_vec_alpha_c.asDiagonal() * Ys.transpose();

    // SigmaXY calculation
    Eigen::MatrixXd sigma_xy = Xs * m_vec_alpha_c.asDiagonal() * Ys.transpose();

    // Calculation of the gain matrix L
    Eigen::MatrixXd L_k = sigma_xy * sigma_y.inverse();

    return {sigma_y, L_k};
}

void SigmaPointKalmanFilter::set_final_state_estimate(Eigen::MatrixXd L_k, Eigen::VectorXd y_true, Eigen::VectorXd y_estimate)
{
    Eigen::VectorXd final_state_estimate = m_x.get_vec() + (L_k * (y_true - y_estimate));

    m_x.set_vec(final_state_estimate);
}

void SigmaPointKalmanFilter::set_final_cov_estimate(Eigen::MatrixXd L_k, Eigen::MatrixXd sigma_y)
{
    Eigen::MatrixXd final_cov_estimate = m_x.get_cov() - (L_k * sigma_y * L_k.transpose());
    m_x.set_cov(final_cov_estimate);
}

Eigen::VectorXd SigmaPointKalmanFilter::solve_one_iteration(Eigen::VectorXd u, Eigen::VectorXd y_true)
{
    Eigen::MatrixXd big_X = calc_and_set_state_prediction(u);
    Eigen::MatrixXd covariance_estimate = calc_and_set_state_covariance(big_X);
    std::pair<Eigen::MatrixXd, Eigen::VectorXd> y_predictions = predict_system_output(big_X, u);

    std::pair<Eigen::MatrixXd, Eigen::MatrixXd> gain_estimator_results = estimator_gain_matrix(y_predictions.first, y_predictions.second, covariance_estimate);
    set_final_state_estimate(gain_estimator_results.second, y_true, y_predictions.second);
    set_final_cov_estimate(gain_estimator_results.second, gain_estimator_results.first);

    return m_x.get_vec();
}

SimulationResults SigmaPointKalmanFilter::solve(Eigen::MatrixXd u, Eigen::MatrixXd y_true)
{
    Eigen::VectorXd u_;
    Eigen::VectorXd y_true_;

    SimulationResults sim_results;
    sim_results.states_estimation = Eigen::MatrixXd::Zero(m_Nx, u.cols());

    Eigen::VectorXd one_iteration_results;
    for (int i = 0; i < static_cast<int>(u.cols()); i++)
    {
        u_ = u.col(i);
        y_true_ = y_true.col(i);
        one_iteration_results = solve_one_iteration(u_, y_true_);

        sim_results.states_estimation.col(i) = one_iteration_results;
    }
    return sim_results;
}

TwoStatesOneInputOneOutput::TwoStatesOneInputOneOutput()
{
    Eigen::VectorXd vec_x(2);
    vec_x(0) = 0.0;
    vec_x(1) = 0.0;
    Eigen::MatrixXd cov_x = Eigen::MatrixXd::Zero(2, 2);
    cov_x(0, 0) = 0.0;
    cov_x(1, 1) = 0.0;
    NormalRandomVector x = NormalRandomVector(vec_x, cov_x);

    Eigen::VectorXd vec_w(1);
    vec_w(0) = 0.0;
    Eigen::MatrixXd cov_w(1, 1);
    cov_w(0, 0) = 0.0;
    NormalRandomVector w = NormalRandomVector(vec_w, cov_w);

    Eigen::VectorXd vec_v(1);
    vec_v(0) = 0.0;
    Eigen::MatrixXd cov_v(1, 1);
    cov_v(0, 0) = 0.0;
    NormalRandomVector v = NormalRandomVector(vec_v, cov_v);

    int y_dim = 1;

    m_spkf = SigmaPointKalmanFilter(x, w, v, y_dim, default_state_equation, default_output_equation);
}

TwoStatesOneInputOneOutput::TwoStatesOneInputOneOutput(double i_state1_init, double i_state2_init, double i_cov_state1, double i_cov_state2,
                                                       double i_cov_w, double i_cov_v,
                                                       std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> i_state_equation,
                                                       std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> i_output_equation)
{
    Eigen::VectorXd vec_x(2);
    vec_x(0) = i_state1_init;
    vec_x(1) = i_state2_init;
    Eigen::MatrixXd cov_x = Eigen::MatrixXd::Zero(2, 2);
    cov_x(0, 0) = i_cov_state1;
    cov_x(1, 1) = i_cov_state2;
    NormalRandomVector x = NormalRandomVector(vec_x, cov_x);

    Eigen::VectorXd vec_w(1);
    vec_w(0) = 0.0;
    Eigen::MatrixXd cov_w(1, 1);
    cov_w(0, 0) = i_cov_w;
    NormalRandomVector w = NormalRandomVector(vec_w, cov_w);

    Eigen::VectorXd vec_v(1);
    vec_v(0) = 0.0;
    Eigen::MatrixXd cov_v(1, 1);
    cov_v(0, 0) = i_cov_v;
    NormalRandomVector v = NormalRandomVector(vec_v, cov_v);

    int y_dim = 1;

    m_spkf = SigmaPointKalmanFilter(x, w, v, y_dim, i_state_equation, i_output_equation);
}

Eigen::VectorXd TwoStatesOneInputOneOutput::solve_one_iteration(Eigen::VectorXd u, Eigen::VectorXd y_true)
{
    Eigen::VectorXd state_estimation = m_spkf.solve_one_iteration(u, y_true);
    return state_estimation;
}

Eigen::MatrixXd TwoStatesOneInputOneOutput::solve(Eigen::MatrixXd u, Eigen::MatrixXd y_true)
{
    SimulationResults sim_results;
    sim_results = m_spkf.solve(u, y_true);
    return sim_results.states_estimation;
}
