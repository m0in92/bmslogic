#include <functional>

#include "Eigen/Dense"

#include "solvers.h"
#include "calc_helpers/kalman_filter.h"

class SPKFSolver : public BaseBatterySolver
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
    NormalRandomVector m_x;
    NormalRandomVector m_w;
    NormalRandomVector m_v;

    int m_y_dim;
    int m_Nx;
    int m_Nw;
    int m_Nv;
    int m_L; // dimension of augmented matrix
    int m_p; // number of sigma points - 1

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
