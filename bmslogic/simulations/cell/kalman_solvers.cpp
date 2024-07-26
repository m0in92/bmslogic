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
    Eigen::MatrixXd cov_x = Eigen::MatrixXd::Zero(2, 2);
    cov_x(0, 0) = i_cov_state1;
    cov_x(1, 1) = i_cov_state2;
    NormalRandomVector x = NormalRandomVector(vec_x, cov_x);
    m_x = x;

    // // // normal vector for the system noise
    Eigen::VectorXd vec_w(1);
    vec_w(0) = 0.0;
    Eigen::MatrixXd cov_w(1, 1);
    cov_w(0, 0) = i_cov_w;
    NormalRandomVector w = NormalRandomVector(vec_w, cov_w);
    m_w = w;

    // // // normal vector for the sensor noise
    Eigen::VectorXd vec_v(1);
    vec_v(0) = 0.0;
    Eigen::MatrixXd cov_v(1, 1);
    cov_v(0, 0) = i_cov_v;
    NormalRandomVector v = NormalRandomVector(vec_v, cov_v);
    m_v = v;

    m_y_dim = 1;
    m_Nx = 2;
    m_Nw = 1;
    m_Nv = 1;
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

void SPKFSolver::calc_and_set_gamma()
{
    m_gamma = std::sqrt(3.0);
}

void SPKFSolver::calc_and_set_h()
{
    m_h = std::sqrt(3.0);
}

void SPKFSolver::calc_and_set_alpha_m0()
{
    m_alpha_m0 = (std::pow(m_h, 2) - m_L) / (std::pow(m_h, 2));
}

void SPKFSolver::calc_and_set_alpha_m()
{
    m_alpha_m = 1 / (2 * std::pow(m_h, 2));
}

void SPKFSolver::calc_and_set_alpha_c0()
{
    m_alpha_c0 = (std::pow(m_h, 2) - m_L) / (std::pow(m_h, 2));
}

void SPKFSolver::calc_and_set_alpha_c()
{
    m_alpha_c = 1 / (2 * std::pow(m_h, 2));
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

Eigen::MatrixXd SPKFSolver::calc_sqrt_matrix(Eigen::MatrixXd i_matrix)
{
    Eigen::LLT<Eigen::MatrixXd> sqrt_matrix(i_matrix);
    return sqrt_matrix.matrixL();
}

Eigen::VectorXd SPKFSolver::generate_aug_vec()
{
    auto size_aug_vec = m_x.get_vec().size() + m_w.get_vec().size() + m_v.get_vec().size();

    Eigen::VectorXd vec_aug_cov(size_aug_vec);
    vec_aug_cov << m_x.get_vec(), m_w.get_vec(), m_v.get_vec();
    return vec_aug_cov;
}

Eigen::MatrixXd SPKFSolver::generate_aug_cov()
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

Eigen::MatrixXd SPKFSolver::generate_sigma_pts()
{
    Eigen::VectorXd aug_vec = generate_aug_vec();
    Eigen::MatrixXd aug_std = calc_sqrt_matrix(generate_aug_cov());
    Eigen::MatrixXd result_matrix = Eigen::MatrixXd::Zero(aug_std.rows(), m_p + 1);

    result_matrix.col(0) = aug_vec;
    for (int i = 0; i < m_L; i++)
    {
        result_matrix.col(i + 1) = aug_vec + m_gamma * aug_std.col(i);
        result_matrix.col(i + 1 + m_L) = aug_vec - m_gamma * aug_std.col(i);
    }
    return result_matrix;
}

Eigen::MatrixXd SPKFSolver::calc_and_set_state_prediction(Eigen::VectorXd u)
{
    Eigen::MatrixXd mat_sigma_pts = generate_sigma_pts();

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

Eigen::MatrixXd SPKFSolver::calc_and_set_state_covariance(Eigen::MatrixXd state_equation_results)
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

std::pair<Eigen::MatrixXd, Eigen::VectorXd> SPKFSolver::predict_system_output(Eigen::MatrixXd state_equation_output, Eigen::VectorXd u)
{
    Eigen::MatrixXd mat_sigma_pts = generate_sigma_pts();
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

std::pair<Eigen::MatrixXd, Eigen::MatrixXd> SPKFSolver::estimator_gain_matrix(Eigen::MatrixXd big_y, Eigen::VectorXd y_prediction, Eigen::MatrixXd Xs)
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

void SPKFSolver::set_final_state_estimate(Eigen::MatrixXd L_k, Eigen::VectorXd y_true, Eigen::VectorXd y_estimate)
{
    Eigen::VectorXd final_state_estimate = m_x.get_vec() + (L_k * (y_true - y_estimate));

    m_x.set_vec(final_state_estimate);
}

void SPKFSolver::set_final_cov_estimate(Eigen::MatrixXd L_k, Eigen::MatrixXd sigma_y)
{
    Eigen::MatrixXd final_cov_estimate = m_x.get_cov() - (L_k * sigma_y * L_k.transpose());
    m_x.set_cov(final_cov_estimate);
}

Eigen::VectorXd SPKFSolver::spkf_solve_one_iteration(double i_I_app, double i_V_obs)
{
    Eigen::VectorXd u(1);
    u(0) = i_I_app;
    Eigen::VectorXd y_true(1);
    y_true(0) = i_V_obs;

    Eigen::MatrixXd big_X = calc_and_set_state_prediction(u);
    Eigen::MatrixXd covariance_estimate = calc_and_set_state_covariance(big_X);
    std::pair<Eigen::MatrixXd, Eigen::VectorXd> y_predictions = predict_system_output(big_X, u);

    std::pair<Eigen::MatrixXd, Eigen::MatrixXd> gain_estimator_results = estimator_gain_matrix(y_predictions.first, y_predictions.second, covariance_estimate);
    set_final_state_estimate(gain_estimator_results.second, y_true, y_predictions.second);
    set_final_cov_estimate(gain_estimator_results.second, gain_estimator_results.first);

    return m_x.get_vec();
}

OverPotentials SPKFSolver::calc_overpotentials(double i_I_app)
{
    double m_p = SPModel().m(i_I_app, m_b_cell.elec_p.get_k(), m_b_cell.elec_p.get_S(), m_b_cell.elec_p.get_c_max(),
                             m_b_cell.elec_p.get_SOC(), m_b_cell.electrolyte.get_conc());
    double m_n = SPModel().m(i_I_app, m_b_cell.elec_n.get_k(), m_b_cell.elec_n.get_S(), m_b_cell.elec_n.get_c_max(),
                             m_b_cell.elec_n.get_SOC(), m_b_cell.electrolyte.get_conc());
    return SPModel().calc_overpotentials(m_b_cell.elec_p.get_OCP(), m_b_cell.elec_n.get_OCP(), m_p, m_n,
                                         m_b_cell.get_R_cell(), m_b_cell.get_T(), i_I_app);
}

Solution SPKFSolver::solve(Eigen::VectorXd i_t, Eigen::VectorXd i_I, Eigen::VectorXd i_V_obs)
{
    Solution sol = Solution();

    // simulation loop
    int sim_index = 0;
    double cap;
    for (auto current_time : i_t.tail(i_t.size() - 1))
    {
        // Gather all the simulation parameters in the right data type
        double I_app = i_I(sim_index);
        double V_obs = i_V_obs(sim_index);

        m_dt = i_t(sim_index) - i_t(sim_index - 1);
        m_t_prev = i_t(sim_index - 1);

        // perform the simulation calculations
        Eigen::VectorXd result_state_estimations = spkf_solve_one_iteration(I_app, V_obs);

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

        OverPotentials step_overpotentials = calc_overpotentials(I_app);
        double V = step_overpotentials.V;

        cap = general_equations::calc_cap(cap, m_b_cell.get_cap(), I_app, m_dt);

        // update the Solution's instance variables
        sol.update_t(current_time);
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

        // update the relevant simulations variables
        sim_index++;
    }

    return sol;
}
