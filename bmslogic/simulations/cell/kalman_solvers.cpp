#include "kalman_solvers.h"

SPKFSolver::SPKFSolver(BatteryCell i_b_cell, bool i_isothermal, bool i_degradation,
                       double i_state1_init, double i_state2_init, double i_cov_state1, double i_cov_state2,
                       double i_cov_w, double i_cov_v) : BaseBatterySolver(i_b_cell,
                                                                           i_isothermal,
                                                                           i_degradation,
                                                                           "poly"),
                                                         m_SOC_solver_p('p', i_b_cell.elec_p.get_c_max() * i_b_cell.elec_p.get_SOC(), "higher"),
                                                         m_SOC_solver_n('n', i_b_cell.elec_n.get_c_max() * i_b_cell.elec_n.get_SOC(), "higher")
{
    // below sets sigma point Kalman filter variables
    // // // normal vector for the system states
    Eigen::VectorXd vec_x(2);
    vec_x(0) = i_state1_init;
    vec_x(1) = i_state2_init;
    Eigen::MatrixXd cov_x(2, 2);
    cov_x(0, 0) = i_cov_state1;
    cov_x(1, 1) = i_cov_state2;
    NormalRandomVector x = NormalRandomVector(vec_x, cov_x);

    // // // normal vector for the system noise
    Eigen::VectorXd vec_w(1);
    vec_w(0) = 0.0;
    Eigen::MatrixXd cov_w(1, 1);
    cov_w(0, 0) = i_cov_w;
    NormalRandomVector w = NormalRandomVector(vec_w, cov_w);

    // // // normal vector for the sensor noise
    Eigen::VectorXd vec_v(1);
    vec_v(0) = 0.0;
    Eigen::MatrixXd cov_v(1, 1);
    cov_v(0, 0) = i_cov_v;
    NormalRandomVector v = NormalRandomVector(vec_v, cov_v);

    m_spkf_solver = SigmaPointKalmanFilter(x, w, v, 1);
}

Eigen::VectorXd SPKFSolver::m_state_equation_(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)
{
    Eigen::VectorXd result;
    result << m_b_cell.elec_p.get_c_max();
    return result;
}

Eigen::VectorXd SPKFSolver::m_output_equation_(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)
{
    Eigen::VectorXd result;
    result << m_b_cell.elec_p.get_c_max();
    return result;
}

// Solution SPKFSolver::solve(Eigen::VectorXd i_t, Eigen::VectorXd i_I, Eigen::VectorXd i_V_obs)
// {
//     Solution sol = Solution();

//     // simulation loop
//     int sim_index = 0;
//     double cap;
//     for (int i = 1; i < static_cast<int>(i_t.size()); i++)
//     {
//         // Gather all the simulation parameters in the right data type
//         double I_app = i_I(sim_index);
//         Eigen::VectorXd I_app_(1);
//         I_app_(0) = I_app;
//         double V_obs = i_V_obs(sim_index);
//         Eigen::VectorXd V_obs_(1);
//         V_obs_(0) = V_obs;

//         m_dt = i_t(sim_index) - i_t(sim_index - 1);
//         m_t_prev = i_t(sim_index - 1);

//         // perform the simulation calculations
//         Eigen::VectorXd result_state_estimations = m_spkf_solver.solve_one_iteration(I_app_, V_obs_);

//         try
//         {
//             m_b_cell.elec_p.update_SOC(result_state_estimations(0));
//             m_b_cell.elec_n.update_SOC(result_state_estimations(1));
//         }
//         catch (InvalidSOCException &e)
//         {
//             std::cout << e.what() << std::endl;
//             break;
//         }

//         OverPotentials step_overpotentials = calc_overpotentials(I_app);
//         double V = step_overpotentials.V;

//         cap = general_equations::calc_cap(cap, m_b_cell.get_cap(), I_app, m_dt);

//         // update the Solution's instance variables
//         sol.update_t(i_t(sim_index));
//         sol.update_cycling_step("custom");
//         sol.update_V(V);
//         sol.update_temp(m_b_cell.get_T());
//         sol.update_cap(cap);
//         sol.update_x_p(m_b_cell.elec_p.get_SOC());
//         sol.update_x_n(m_b_cell.elec_n.get_SOC());
//         sol.update_OCV_LIB(step_overpotentials.OCV_LIB);
//         sol.update_overpotential_elec_p(step_overpotentials.elec_p);
//         sol.update_overpotential_elec_n(step_overpotentials.elec_n);
//         sol.update_overpotential_R_cell(step_overpotentials.R_cell);
//         sol.update_overpotential_electrolyte(step_overpotentials.electrolyte);

//         // update the relevant simulations variables
//         sim_index++;
//     }

//     return sol;
// }
