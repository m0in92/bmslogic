#include <chrono>

#include "kalman_solvers.h"

SPKFPolynomialApprox::SPKFPolynomialApprox(char i_electrode_type, double i_c_init,
                                           double i_R, double i_S, double i_D, double i_cov_x, double i_cov_w, double i_cov_v) : conc_solver(i_electrode_type,
                                                                                                                                             i_c_init,
                                                                                                                                             "higher"),
                                                                                                                                 m_R(i_R), m_S(i_S), m_D(i_D)
{
    Eigen::Matrix<double, 1, 1> vec_x;
    vec_x(0) = i_c_init;
    Eigen::Matrix<double, 1, 1> cov_x;
    cov_x(0, 0) = i_cov_x;
    NormalRandomVector x = NormalRandomVector(vec_x, cov_x);

    Eigen::Matrix<double, 1, 1> vec_w;
    vec_w(0) = 0.0;
    Eigen::Matrix<double, 1, 1> cov_w;
    cov_w(0, 0) = i_cov_w;
    NormalRandomVector w = NormalRandomVector(vec_w, cov_w);

    Eigen::Matrix<double, 1, 1> vec_v;
    vec_v(0) = 0.0;
    Eigen::Matrix<double, 1, 1> cov_v;
    cov_v(0, 0) = i_cov_v;
    NormalRandomVector v = NormalRandomVector(vec_v, cov_v);

    int y_dim = 1;

    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> state_equation = [this](Eigen::VectorXd x_k,
                                                                                                              Eigen::VectorXd u_k,
                                                                                                              Eigen::VectorXd w_k)
    {
        double I = u_k(0) + w_k(0);
        double j = SPModel().molar_flux_electrode(I, m_S, conc_solver.get_electrodeType());

        Eigen::Matrix<double, 1, 1> result_matrix;
        result_matrix(0) = conc_solver.get_solve_c_s_avg(m_dt, m_t_prev, m_j, m_R, m_D);
        return result_matrix;
    };

    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> output_equation = [this](Eigen::VectorXd x_k,
                                                                                                               Eigen::VectorXd u_k,
                                                                                                               Eigen::VectorXd v_k)
    {
        double j = SPModel().molar_flux_electrode(u_k(0), m_S, conc_solver.get_electrodeType());
        double q = conc_solver.get_solve_q(m_dt, m_t_prev, j, m_R, m_D);
        double c_surf = (-(j * m_R) / (35 * m_D) + 8 * m_R * q / 35) + x_k(0);

        Eigen::Matrix<double, 1, 1> result_matrix;
        result_matrix(0) = c_surf;
        return result_matrix;
    };

    m_spkf_solver = SigmaPointKalmanFilter(x, w, v, y_dim, state_equation, output_equation, "CDKF");
}

double SPKFPolynomialApprox::solve_spkf(double dt, double t_prev, double I_app, double c_surf_true)
{
    m_dt = dt;
    m_t_prev = t_prev;
    double j = SPModel().molar_flux_electrode(I_app, m_S, conc_solver.get_electrodeType());

    // spkf solve
    Eigen::Matrix<double, 1, 1> u_k;
    Eigen::Matrix<double, 1, 1> y_true;
    u_k(0) = I_app;
    y_true(0) = c_surf_true;

    m_spkf_solver.solve(u_k, y_true);

    // solve and update the PolyApprox members
    conc_solver.set_c_s_avg(m_spkf_solver.get_x().get_vec()(0)); // c_s_avg
    double q = conc_solver.get_solve_q(m_dt, m_t_prev, j, m_R, m_D);
    conc_solver.set_q(q); // set q
    double c_surf = -(j * m_R) / (35 * m_D) + 8 * m_R * q / 35 + conc_solver.get_c_s_avg();
    conc_solver.just_set_c_surf(c_surf); // set c_surf

    return conc_solver.get_c_surf();
}

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

    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> state_equation = [this](Eigen::VectorXd x_k, Eigen::VectorXd u_k, Eigen::VectorXd w_k) -> Eigen::VectorXd
    {
        double soc_p, soc_n;
        soc_p = m_SOC_solver_p.solve_without_update(m_dt, m_t_prev, u_k(0) + w_k(0), m_b_cell.elec_p.get_R(), m_b_cell.elec_p.get_S(), m_b_cell.elec_p.get_D());
        soc_n = m_SOC_solver_n.solve_without_update(m_dt, m_t_prev, u_k(0) + w_k(0), m_b_cell.elec_n.get_R(), m_b_cell.elec_n.get_S(), m_b_cell.elec_n.get_D());

        Eigen::VectorXd results(2);
        results(0) = (soc_p / m_b_cell.elec_p.get_c_max());
        results(1) = (soc_n / m_b_cell.elec_n.get_c_max());

        return results;
    };

    std::function<Eigen::VectorXd(Eigen::VectorXd, Eigen::VectorXd, Eigen::VectorXd)> output_equation = [this](Eigen::VectorXd x_k, Eigen::VectorXd u_k, Eigen::VectorXd v_k) -> Eigen::VectorXd
    {
        double m_p = SPModel().m(u_k(0), m_b_cell.elec_p.get_k(), m_b_cell.elec_p.get_S(), m_b_cell.elec_p.get_c_max(),
                                 x_k(0), m_b_cell.electrolyte.get_conc());
        double m_n = SPModel().m(u_k(0), m_b_cell.elec_n.get_k(), m_b_cell.elec_n.get_S(), m_b_cell.elec_n.get_c_max(),
                                 x_k(1), m_b_cell.electrolyte.get_conc());
        OverPotentials overpotentials_ = SPModel().calc_overpotentials(m_b_cell.elec_p.get_OCP(), m_b_cell.elec_n.get_OCP(), m_p, m_n,
                                                                       m_b_cell.get_R_cell(), m_b_cell.get_T(), u_k(0));
        Eigen::VectorXd results(1);
        results(0) = overpotentials_.V + v_k(0);
        return results;
    };

    m_spkf_solver = SigmaPointKalmanFilter(x, w, v, 1, state_equation, output_equation);
}

OverPotentials SPKFSolver::calc_overpotentials(double I)
{
    double m_p = SPModel().m(I, m_b_cell.elec_p.get_k(), m_b_cell.elec_p.get_S(), m_b_cell.elec_p.get_c_max(),
                             m_b_cell.elec_p.get_SOC(), m_b_cell.electrolyte.get_conc());
    double m_n = SPModel().m(I, m_b_cell.elec_n.get_k(), m_b_cell.elec_n.get_S(), m_b_cell.elec_n.get_c_max(),
                             m_b_cell.elec_n.get_SOC(), m_b_cell.electrolyte.get_conc());
    return SPModel().calc_overpotentials(m_b_cell.elec_p.get_OCP(), m_b_cell.elec_n.get_OCP(), m_p, m_n,
                                         m_b_cell.get_R_cell(), m_b_cell.get_T(), I);
}

Solution SPKFSolver::solve(Eigen::VectorXd i_t, Eigen::VectorXd i_I, Eigen::VectorXd i_V_obs)
{
    Solution sol = Solution();

    auto t1 = std::chrono::high_resolution_clock::now();

    // simulation loop
    // int sim_index = 0;
    double cap = 0;
    for (int i = 1; i < static_cast<int>(i_t.size()); i++)
    {
        // Gather all the simulation parameters in the right data type

        double I_app = i_I(i);
        Eigen::VectorXd I_app_(1);
        I_app_(0) = I_app;
        double V_obs = i_V_obs(i);
        Eigen::VectorXd V_obs_(1);
        V_obs_(0) = V_obs;

        m_dt = i_t(i) - i_t(i - 1);
        m_t_prev = i_t(i - 1);

        // perform the simulation calculations
        // // SPKF
        Eigen::VectorXd result_state_estimations = m_spkf_solver.solve_one_iteration(I_app_, V_obs_);

        // // update the electrode SOC
        try
        {
            m_b_cell.elec_p.update_SOC(result_state_estimations(0));
            m_b_cell.elec_n.update_SOC(result_state_estimations(1));
        }
        catch (InvalidSOCException &e)
        {
            std::cout << e.what() << std::endl;
            break;
        }

        // // calculate the cell terminal voltage
        OverPotentials step_overpotentials = calc_overpotentials(I_app);
        double V = step_overpotentials.V;

        cap = general_equations::calc_cap(cap, m_b_cell.get_cap(), I_app, m_dt);

        // update the Solution's instance variables
        sol.update_t(i_t(i));
        sol.update_cycling_step("custom");
        sol.update_V(V);
        sol.update_temp(m_b_cell.get_T());
        sol.update_cap(cap);
        sol.update_x_p(m_b_cell.elec_p.get_SOC());
        sol.update_x_n(m_b_cell.elec_n.get_SOC());
        sol.update_OCV_LIB(step_overpotentials.OCV_LIB);
        sol.update_overpotential_elec_p(step_overpotentials.elec_p);
        sol.update_overpotential_elec_n(step_overpotentials.elec_n);
        sol.update_overpotential_R_cell(step_overpotentials.R_cell);
        sol.update_overpotential_electrolyte(step_overpotentials.electrolyte);
    }

    auto t2 = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1);
    std::cout << "Simulation time: " << duration.count() << " ms" << std::endl;

    return sol;
}

Solution SPKFSolver::solve(std::vector<double> i_t, std::vector<double> i_I, std::vector<double> i_V_obs)
{
    Solution sol = Solution();

    auto t1 = std::chrono::high_resolution_clock::now();

    // simulation loop
    double cap = 0;
    for (int i = 1; i < static_cast<int>(i_t.size()); i++)
    {
        // Gather all the simulation parameters in the right data type

        double I_app = i_I[i];
        Eigen::VectorXd I_app_(1);
        I_app_(0) = I_app;
        double V_obs = i_V_obs[i];
        Eigen::VectorXd V_obs_(1);
        V_obs_(0) = V_obs;

        m_dt = i_t[i] - i_t[i - 1];
        m_t_prev = i_t[i - 1];

        // perform the simulation calculations
        // // SPKF
        Eigen::VectorXd result_state_estimations = m_spkf_solver.solve_one_iteration(I_app_, V_obs_);

        // // update the electrode SOC
        m_SOC_solver_p.set_c_surf(result_state_estimations(0) * m_b_cell.elec_p.get_c_max(), m_dt, m_t_prev, I_app,
                                  m_b_cell.elec_p.get_R(), m_b_cell.elec_p.get_S(), m_b_cell.elec_p.get_D());
        m_SOC_solver_n.set_c_surf(result_state_estimations(1) * m_b_cell.elec_n.get_c_max(), m_dt, m_t_prev, I_app,
                                  m_b_cell.elec_n.get_R(), m_b_cell.elec_n.get_S(), m_b_cell.elec_n.get_D());
        try
        {
            m_b_cell.elec_p.update_SOC(result_state_estimations(0));
            m_b_cell.elec_n.update_SOC(result_state_estimations(1));
        }
        catch (InvalidSOCException &e)
        {
            std::cout << e.what() << std::endl;
            break;
        }

        // // calculate the cell terminal voltage
        OverPotentials step_overpotentials = calc_overpotentials(I_app);
        double V = step_overpotentials.V;

        cap = general_equations::calc_cap(cap, m_b_cell.get_cap(), I_app, m_dt);

        // update the Solution's instance variables
        sol.update_t(i_t[i]);
        sol.update_cycling_step("custom");
        sol.update_V(V);
        sol.update_temp(m_b_cell.get_T());
        sol.update_cap(cap);
        sol.update_x_p(m_b_cell.elec_p.get_SOC());
        sol.update_x_n(m_b_cell.elec_n.get_SOC());
        sol.update_OCV_LIB(step_overpotentials.OCV_LIB);
        sol.update_overpotential_elec_p(step_overpotentials.elec_p);
        sol.update_overpotential_elec_n(step_overpotentials.elec_n);
        sol.update_overpotential_R_cell(step_overpotentials.R_cell);
        sol.update_overpotential_electrolyte(step_overpotentials.electrolyte);
    }

    auto t2 = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1);
    std::cout << "Simulation time: " << duration.count() << " ms" << std::endl;

    return sol;

    return sol;
}
