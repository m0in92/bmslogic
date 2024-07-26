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

    // getters
    const SigmaPointKalmanFilter get_spkf_solver_instance() { return m_spkf_solver; }

private:
    double m_t_prev;
    double m_dt;

    // electrode soc solvers
    PolynomialApprox m_SOC_solver_p;
    PolynomialApprox m_SOC_solver_n;

    // kalman filter specific
    SigmaPointKalmanFilter m_spkf_solver;
    Eigen::VectorXd m_state_equation_(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd);
    Eigen::VectorXd m_output_equation_(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd);
    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> m_state_equation;
    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> m_output_equation;
};

