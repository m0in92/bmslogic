#include <functional>

#include "Eigen/Dense"

#include "solvers.h"
#include "kalman_filter.h"

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

    TwoStatesOneInputOneOutput m_spkf_solver;

    // functions for calculations
    Eigen::VectorXd m_state_equation(Eigen::VectorXd x_k, Eigen::VectorXd u_k, Eigen::VectorXd w_k);
    Eigen::VectorXd m_output_equation(Eigen::VectorXd x_k, Eigen::VectorXd u_k, Eigen::VectorXd v_k);
    // std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> m_state_equation;
    // std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> m_output_equation;
};
