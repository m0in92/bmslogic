#pragma once

#include <functional>
#include <vector>

#include "Eigen/Core"

#include "solvers.h"
#include "calc_helpers/kalman_filter.h"

/**
 * @brief Sigma-Point Kalman filter solver for the electrode lithium-ion concentration inside the electrode
 * particle using the polynomial approximation on the volume-averaged quantities.
 *
 * state: c_s_avg
 * output: c_s_surf
 *
 */
class SPKFPolynomialApprox
{
public:
    SPKFPolynomialApprox(char electrode_type, double c_init, double R, double S, double D, double cov_x, double cov_w, double cov_v);
    ~SPKFPolynomialApprox() = default;
    // getter functions
    SigmaPointKalmanFilter get_spkf_solver() const { return m_spkf_solver; }
    // helper functions
    double solve_spkf(double dt, double t_prev, double I_app, double c_surf_true);

private:
    double m_dt;     // [s]
    double m_t_prev; // [D]
    double m_R;      // Electrode Particle Size [m]
    double m_S;      // Electrode Electrochemically Active Area [m2];
    double m_D;      // Electrode Lithium-Ion Diffusivity [m2/2]
    double m_j;      // Electrode Lithoim-ion Flux [mol/m2/s]

    PolynomialApprox conc_solver;
    // SPKF specific variables and methods
    SigmaPointKalmanFilter m_spkf_solver;
};

class SPKFSolver : public BaseBatterySolver
{
public:
    SPKFSolver(BatteryCell i_b_cell, bool i_isothermal, bool i_degradation,
               double i_state1_init, double i_state2_init, double i_cov_state1, double i_cov_state2,
               double i_cov_w, double i_cov_v);
    ~SPKFSolver() = default;

    // functions for calculations
    Solution solve(Eigen::VectorXd i_t, Eigen::VectorXd i_I, Eigen::VectorXd i_V_ob);
    Solution solve(std::vector<double> i_t, std::vector<double> i_I, std::vector<double> i_V_ob);

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

    // helper functions
    OverPotentials calc_overpotentials(double i_I);
};
