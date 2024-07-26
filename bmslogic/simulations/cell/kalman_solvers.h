#include <functional>

#include "Eigen/Dense"

#include "solvers.h"
#include "calc_helpers/kalman_filter.h"

class BaseKFBatterySolver
{
public:
    BaseKFBatterySolver() = default;
    BaseKFBatterySolver(int i_Nx, int i_Nw, int i_Nv, int i_y_dim);
    BaseKFBatterySolver(NormalRandomVector i_x, NormalRandomVector i_w, NormalRandomVector i_v, int i_y_dim);

    // getters
    int get_y_dim() const { return m_y_dim; }
    int get_Nx() const { return m_Nx; }
    int get_Nw() const { return m_Nw; }
    int get_Nv() const { return m_Nv; }
    int get_L() const { return m_L; }
    int get_p() const { return m_p; }
    double get_gamma() const { return m_gamma; }
    double get_h() const { return m_h; }
    double get_alpha_m0() const { return m_alpha_m0; }
    double get_alpha_m() const { return m_alpha_m; }
    double get_alpha_c0() const { return m_alpha_c0; }
    double get_alpha_c() const { return m_alpha_c; }
    const Eigen::VectorXd &get_vec_alpha_m() const { return m_vec_alpha_m; }
    const Eigen::VectorXd &get_vec_alpha_c() const { return m_vec_alpha_c; }

    // setters
    void set_x(NormalRandomVector &i_x) { m_x = i_x; }
    void set_w(NormalRandomVector &i_w) { m_x = i_w; }
    void set_v(NormalRandomVector &i_v) { m_x = i_v; }

protected:
    NormalRandomVector m_x;
    NormalRandomVector m_w;
    NormalRandomVector m_v;

    int m_y_dim;
    int m_Nx;
    int m_Nw;
    int m_Nv;
    int m_L; // dimension of augmented matrix
    int m_p; // number of sigma points - 1

    // Sigma Point Kalman Filter Specific Variables
    double m_gamma;
    double m_h;
    double m_alpha_m0;
    double m_alpha_m;
    double m_alpha_c0;
    double m_alpha_c;
    Eigen::VectorXd m_vec_alpha_m;
    Eigen::VectorXd m_vec_alpha_c;

    // setters specific to Kalman Filters
    void calc_and_set_gamma();
    void calc_and_set_h();
    void calc_and_set_alpha_m0();
    void calc_and_set_alpha_m();
    void calc_and_set_alpha_c0();
    void calc_and_set_alpha_c();
};

class SPKFSolver : public BaseBatterySolver, public BaseKFBatterySolver
{
public:
    SPKFSolver(BatteryCell i_b_cell, bool i_isothermal, bool i_degradation,
               double i_state1_init, double i_state2_init, double i_cov_state1, double i_cov_state2,
               double i_cov_w, double i_cov_v);

    // functions for calculations
    Solution solve(Eigen::VectorXd i_t, Eigen::VectorXd i_I, Eigen::VectorXd i_V_obs);

private:
    double m_t_prev;
    double m_dt;

    // electrode soc solvers
    PolynomialApprox m_SOC_solver_p;
    PolynomialApprox m_SOC_solver_n;

    // variables specific to sigma point Kalman filter
    // // dimension related
    // NormalRandomVector m_x;
    // NormalRandomVector m_w;
    // NormalRandomVector m_v;

    // functions specific to sigma point Kalman filter
    Eigen::VectorXd m_state_equation(Eigen::VectorXd x_k, Eigen::VectorXd u_k, Eigen::VectorXd w_k);
    Eigen::VectorXd m_output_equation(Eigen::VectorXd x_k, Eigen::VectorXd u_k, Eigen::VectorXd v_k);

    // functions for conduting sigma point Kalman filter during a time step
    Eigen::MatrixXd calc_sqrt_matrix(Eigen::MatrixXd i_matrix);
    Eigen::VectorXd SPKFSolver::generate_aug_vec();
    Eigen::MatrixXd SPKFSolver::generate_aug_cov();
    Eigen::MatrixXd generate_sigma_pts();
    Eigen::MatrixXd calc_and_set_state_prediction(Eigen::VectorXd u);
    Eigen::MatrixXd calc_and_set_state_covariance(Eigen::MatrixXd state_equation_results);
    std::pair<Eigen::MatrixXd, Eigen::VectorXd> predict_system_output(Eigen::MatrixXd state_equation_output, Eigen::VectorXd u);
    std::pair<Eigen::MatrixXd, Eigen::MatrixXd> estimator_gain_matrix(Eigen::MatrixXd big_y, Eigen::VectorXd y_prediction, Eigen::MatrixXd covariance_estimates);
    void set_final_state_estimate(Eigen::MatrixXd L_k, Eigen::VectorXd y_true, Eigen::VectorXd y_estimate);
    void set_final_cov_estimate(Eigen::MatrixXd L_k, Eigen::MatrixXd sigma_y);
    Eigen::VectorXd spkf_solve_one_iteration(double u, double y_true);

    OverPotentials calc_overpotentials(double i_I_app);
};
