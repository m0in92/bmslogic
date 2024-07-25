#include "kalman_solvers.h"

SPKFSolver::SPKFSolver(BatteryCell i_b_cell, bool i_isothermal, bool i_degradation,
                       double i_state1_init, double i_state2_init, double i_cov_state1, double i_cov_state2,
                       double i_cov_w, double i_cov_v) : BaseBatterySolver(i_b_cell,
                                                                           i_isothermal,
                                                                           i_degradation,
                                                                           "poly"),
                                                         m_SOC_solver_p('p', i_b_cell.elec_p.get_c_max() * i_b_cell.elec_p.get_SOC(), "higher"),
                                                         m_SOC_solver_n('n', i_b_cell.elec_n.get_c_max() * i_b_cell.elec_n.get_SOC(), "higher"),
                                                         m_spkf_solver(i_state1_init, i_state2_init, i_cov_state1, i_cov_state2,
                                                                       i_cov_w, i_cov_v, (this->*m_state_equation), (this->*m_output_equation))

{
}

Eigen::VectorXd SPKFSolver::m_state_equation(Eigen::VectorXd x_k, Eigen::VectorXd u_k, Eigen::VectorXd w_k)
{
    m_SOC_solver_p.solve(m_dt, m_t_prev, u_k(0), m_b_cell.elec_p.get_R(), m_b_cell.elec_p.get_S(), m_b_cell.elec_p.get_D());
    m_SOC_solver_n.solve(m_dt, m_t_prev, u_k(0), m_b_cell.elec_n.get_R(), m_b_cell.elec_n.get_S(), m_b_cell.elec_n.get_D());

    Eigen::VectorXd results(2);
    results(0) = m_SOC_solver_p.get_x_surf(m_b_cell.elec_p.get_c_max()) + w_k(0);
    results(1) = m_SOC_solver_n.get_x_surf(m_b_cell.elec_n.get_c_max()) + w_k(0);
    return results;
}

Eigen::VectorXd SPKFSolver::m_output_equation(Eigen::VectorXd x_k, Eigen::VectorXd u_k, Eigen::VectorXd v_k)
{
    double OCP_p = m_b_cell.elec_p.calc_OCP(x_k(0));
    double OCP_n = m_b_cell.elec_n.calc_OCP(x_k(1));
    double m_p = SPModel().m(u_k(0), m_b_cell.elec_p.get_k(), m_b_cell.elec_p.get_S(), m_b_cell.elec_p.get_c_max(),
                             x_k(0), m_b_cell.electrolyte.get_conc());
    double m_n = SPModel().m(u_k(0), m_b_cell.elec_n.get_k(), m_b_cell.elec_n.get_S(), m_b_cell.elec_n.get_c_max(),
                             x_k(1), m_b_cell.electrolyte.get_conc());
    OverPotentials V_ = SPModel().calc_overpotentials(OCP_p, OCP_n, m_p, m_n,
                                                      m_b_cell.get_R_cell(), m_b_cell.get_T(), u_k(0));
    double V = V_.V;
    Eigen::VectorXd result(1);
    result(0) = V;
    return result;
}

Solution SPKFSolver::solve(Eigen::VectorXd i_t, Eigen::VectorXd i_I, Eigen::VectorXd i_V_obs)
{
    Solution sol = Solution();

    // simulation loop
    int sim_index = 0;
    double cap;
    for (auto current_time : i_t.tail(i_t.size()-1))
    {
        // Gather all the simulation parameters in the right data type
        double I_app = i_I(sim_index);
        Eigen::VectorXd vec_I_app(1);
        vec_I_app(0) = I_app;
        double V_obs = i_V_obs(sim_index);
        Eigen::VectorXd vec_V_obs(1);
        vec_V_obs(0) = V_obs;

        m_dt = i_t(sim_index) - i_t(sim_index-1);
        m_t_prev = i_t(sim_index-1);

        // perform the simulation calculations
        Eigen::VectorXd result_state_estimations = m_spkf_solver.solve_one_iteration(vec_I_app, vec_V_obs);
        m_b_cell.elec_p.update_SOC(result_state_estimations(0));
        m_b_cell.elec_n.update_SOC(result_state_estimations(1));

        OverPotentials overpotential_ = calc_overpotentials(I_app);
        double V_new = overpotential_.V;

        cap = general_equations::calc_cap(cap, m_b_cell.get_cap(), I_app, m_dt);

        // update the Solution's instance variables
        sol.update_t(current_time);
        sol.update_cycling_step("custom");
        sol.update_V(V);
        sol.update_temp(m_b_cell.get_T());
        sol.update_cap(cap);
        sol.update_x_p(m_b_cell.elec_p.get_SOC());
        sol.update_x_n(m_b_cell.elec_n.get_SOC());

        // update the relevant simulations variables
        sim_index++;
    }

    return sol;
}
