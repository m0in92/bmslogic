#pragma once

#include <vector>
#include <string>
#include <cmath>
#include <functional>

#include "Eigen/Core"

// these changes are for the version of Eigen used here
#define all placeholders::all
#define last placeholders::last

class InvalidSize : public std::exception
{
public:
    const char *what()
    {
        const char *error_msg = "invalid dimensions of input vector and covariance matrix.";
        return error_msg;
    }
};

class InvalidKFMethodType : public std::exception
{
public:
    const char *what()
    {
        const char *error_msg = "Invalid Kalman Filter Type.";
        return error_msg;
    }
};

class NormalRandomVector
{
public:
    NormalRandomVector() = default;
    NormalRandomVector(Eigen::VectorXd vector_init, Eigen::MatrixXd cov_init);
    // getters
    Eigen::VectorXd get_vec() const { return m_vec; }
    Eigen::MatrixXd get_cov() const { return m_cov; }
    // size_t get_dim() { return m_vec.size(); }
    // setters
    void set_vec(Eigen::VectorXd i_vec) { m_vec = i_vec; }
    void set_cov(Eigen::MatrixXd &i_cov) { m_cov = i_cov; }

private:
    Eigen::VectorXd m_vec;
    Eigen::MatrixXd m_cov;

    void check_for_square_matrix(Eigen::MatrixXd i_matrix);
    void check_for_vector_size_with_matrix(Eigen::VectorXd i_vec, Eigen::MatrixXd i_matrix);
};

struct SimulationResults
{
    Eigen::MatrixXd states_estimation;
};

class SigmaPointKalmanFilter
{
public:
    SigmaPointKalmanFilter() = default;
    SigmaPointKalmanFilter(NormalRandomVector i_x, NormalRandomVector i_w, NormalRandomVector i_v,
                           int y_dim,
                           std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> &state_equaton,
                           std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> &output_equation,
                           std::string method_type = "CDKF");
    SigmaPointKalmanFilter(NormalRandomVector i_x, NormalRandomVector i_w, NormalRandomVector i_v,
                           int y_dim);

    // getters
    int get_Nx() const { return m_Nx; }
    int get_Nw() const { return m_Nw; }
    int get_Nv() const { return m_Nv; }
    int get_L() const { return m_L; }
    int get_p() const { return m_p; }

    NormalRandomVector get_x() const { return m_x; }

    Eigen::VectorXd get_aug_vec() { return generate_aug_vec(); }
    Eigen::MatrixXd get_aug_cov() { return generate_aug_cov(); }
    Eigen::MatrixXd get_mat_sigma_pts() { return generate_mat_sigma_pts(); }
    Eigen::MatrixXd get_mat_sigma_pts_x() { return generate_mat_sigma_pts()(Eigen::seq(0, m_Nx - 1), Eigen::all); }
    Eigen::MatrixXd get_mat_sigma_pts_w() { return generate_mat_sigma_pts()(Eigen::seq(m_Nx, m_Nx + m_Nw - 1), Eigen::all); }
    Eigen::MatrixXd get_mat_sigma_pts_v() { return generate_mat_sigma_pts()(Eigen::seq(m_Nx + m_Nw, Eigen::last), Eigen::all); }

    double get_gamma() const { return m_gamma; }
    double get_h() const { return m_h; }
    double get_alpha_m0() const { return m_alpha_m0; }
    double get_alpha_m() const { return m_alpha_m; }
    double get_alpha_c0() const { return m_alpha_c0; }
    double get_alpha_c() const { return m_alpha_c; }
    Eigen::VectorXd get_vector_alpha_m() const { return m_vec_alpha_m; }
    Eigen::VectorXd get_vector_alpha_c() const { return m_vec_alpha_c; }

    // setters
    void set_state_equation(std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> i_state_equation) { m_state_equation = i_state_equation; }
    void set_output_equation(std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> i_output_equation) { m_output_equation = i_output_equation; }

    // helper functions
    static Eigen::MatrixXd calc_sqrt_matrix(Eigen::MatrixXd i_matrix);

    // SPKF calculation steps
    Eigen::MatrixXd calc_and_set_state_prediction(Eigen::VectorXd u);
    Eigen::MatrixXd calc_and_set_state_covariance(Eigen::MatrixXd state_equation_results);
    std::pair<Eigen::MatrixXd, Eigen::VectorXd> predict_system_output(Eigen::MatrixXd state_equation_output, Eigen::VectorXd u);
    std::pair<Eigen::MatrixXd, Eigen::MatrixXd> estimator_gain_matrix(Eigen::MatrixXd big_y, Eigen::VectorXd y_prediction, Eigen::MatrixXd covariance_estimates);
    void set_final_state_estimate(Eigen::MatrixXd L_k, Eigen::VectorXd y_true, Eigen::VectorXd y_estimate);
    void set_final_cov_estimate(Eigen::MatrixXd L_k, Eigen::MatrixXd sigma_y);
    Eigen::VectorXd solve_one_iteration(Eigen::VectorXd u, Eigen::VectorXd y_true);
    SimulationResults solve(Eigen::MatrixXd u, Eigen::MatrixXd y_true);

private:
    // // instance variables
    NormalRandomVector m_x;
    NormalRandomVector m_w;
    NormalRandomVector m_v;

    // dimension related
    int m_y_dim;
    int m_Nx;
    int m_Nw;
    int m_Nv;
    int m_L; // dimension of augmented matrix
    int m_p; // number of sigma points - 1

    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> m_state_equation;
    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> m_output_equation;

    std::string m_method_type;

    double m_gamma;
    double m_h;
    double m_alpha_m0;
    double m_alpha_m;
    double m_alpha_c0;
    double m_alpha_c;
    Eigen::VectorXd m_vec_alpha_m;
    Eigen::VectorXd m_vec_alpha_c;

    // // helper methods
    Eigen::VectorXd generate_aug_vec();
    Eigen::MatrixXd generate_aug_cov();

    Eigen::MatrixXd generate_mat_sigma_pts();

    // setters
    void calc_and_set_gamma();
    void calc_and_set_h();
    void calc_and_set_alpha_m0();
    void calc_and_set_alpha_m();
    void calc_and_set_alpha_c0();
    void calc_and_set_alpha_c();
};

/**
 * @brief Below are the equations for the default contructor of classes pertaining to Kalman_filters
 * that require functions parameters.
 *
 */
static Eigen::VectorXd default_state_equation_(Eigen::VectorXd x_k, Eigen::VectorXd u_k, Eigen::VectorXd w_k)
{
    return x_k;
}

static Eigen::VectorXd default_output_equation_(Eigen::VectorXd x_k, Eigen::VectorXd u_k, Eigen::VectorXd w_k)
{
    return x_k;
}

static std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> default_state_equation = default_state_equation_;
static std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> default_output_equation = default_state_equation_;

class TwoStatesOneInputOneOutput
{
public:
    TwoStatesOneInputOneOutput();
    TwoStatesOneInputOneOutput(double i_state1_init, double i_state2_init, double i_cov_state1, double i_cov_state2,
                               double i_cov_w, double i_cov_v,
                               std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> i_state_equation,
                               std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> i_output_equation);
    // getters
    Eigen::VectorXd get_state() { return m_spkf.get_x().get_vec(); }
    Eigen::MatrixXd get_cov() { return m_spkf.get_x().get_cov(); }
    // helper functions
    Eigen::VectorXd solve_one_iteration(Eigen::VectorXd u, Eigen::VectorXd y_true);
    Eigen::MatrixXd solve(Eigen::MatrixXd u, Eigen::MatrixXd y_true);

private:
    SigmaPointKalmanFilter m_spkf;
};
