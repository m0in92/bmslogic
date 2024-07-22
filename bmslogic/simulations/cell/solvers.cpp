#include <iostream>
#include <stdexcept>
#include <cmath>
#include <ctime>
#include <stdexcept>
#include <chrono>
#include <iomanip>
#include <thread>

#include "calc_helpers/constants.h"
#include "extern/owl.h"
#include "solvers.h"
#include "models.h"
#include "coords.h"

// ECM Solvers below
ECMSolution ESCDTSolver::solve(BaseCycler cycler, double dt)
{
    ECMSolution sol;

    // Initial simulation variables values
    double i_R1 = 0.0;
    double h = 0.0;
    double s = 0.0;

    ESC model = ESC();

    for (int cycle_iter = 0; cycle_iter < cycler.num_cycles; cycle_iter++)
    {
        for (int step_iter = 0; step_iter < cycler.cycle_steps.size(); step_iter++)
        {
            double t_prev = 0.0;
            double t_curr;
            bool step_completed = false;
            double i_app;
            double i_R1_prev, h_prev, s_prev, V;
            int step_index = 0;

            while (!step_completed)
            {
                t_curr = t_prev + dt;
                i_app = cycler.get_current(cycler.cycle_steps[step_iter], step_index);

                // Calculation of the cell terminal potential below
                m_b_cell.set_soc(model.soc_next(dt, i_app, m_b_cell.get_soc(), m_b_cell.get_cap(), m_b_cell.get_eta()));
                i_R1_prev = m_b_cell.get_R1();
                i_R1 = model.i_R1_next(dt, i_app, i_R1, m_b_cell.get_R1(), m_b_cell.get_C1());
                h_prev = h;
                s_prev = s;
                s = model.s(i_app, s_prev);
                V = model.v(i_app, m_b_cell.get_ocv(), m_b_cell.get_R0(), m_b_cell.get_R1(), i_R1_prev, m_b_cell.get_M0(), m_b_cell.get_M(), h_prev, s_prev);

                // loop termination conditions
                if ((cycler.cycle_steps[step_iter] == "charge") & (V > cycler.V_max))
                    step_completed = true;
                if ((cycler.cycle_steps[step_iter] == "discharge") & (V < cycler.V_min))
                    step_completed = true;
                if ((cycler.cycle_steps[step_iter] == "rest") & (t_curr > cycler.rest_time))
                    step_completed = true;

                t_prev = t_curr; // update times
                step_index++;

                // Solution object update below
                sol.update_t(t_curr);
                sol.update_I(i_app);
                sol.update_V(V);
                sol.update_temp(m_b_cell.get_temp());
                sol.update_soc(m_b_cell.get_soc());
                sol.update_i_R1(i_R1);
            }
        }
    }
    return sol;
}

// degradation solvers definations below
ROMSEISolver::ROMSEISolver(double i_k, double i_c_e, double i_S, double i_c_s_max, double i_U_s, double i_j_0_s, double i_A,
                           double i_MW_SEI, double i_rho, double i_kappa) : m_k(i_k), m_c_e(i_c_e), m_S(i_S),
                                                                            m_c_s_max(i_c_s_max), m_U_s(i_U_s),
                                                                            m_j_0_s(i_j_0_s), m_A(i_A),
                                                                            m_MW_SEI(i_MW_SEI), m_rho(i_rho), m_kappa(i_kappa)
{
}

double ROMSEISolver::solve_current(double soc_n, double ocp_n, double temp, double i_app, double relative_tolerance, int max_iter)
{
    ROMSEI sei_model = ROMSEI();

    char electrode_type = 'n';
    m_j_s = 0.0;
    double j_s_prev = 0.0, j_s = 0.0;
    double j_tot = SPModel::molar_flux_electrode(i_app, m_S, electrode_type); // assuming the negative electrode
    double j_i = sei_model.calc_j_i(j_tot, j_s);

    double eta_n, eta_s, I_i{0.0}, I_s{0.0};

    if (i_app > 0)
    {
        double j_0_i = general_equations::calc_i_0(m_k, m_c_s_max, soc_n, m_c_e);
        double relative_error = 1.0;
        int iter = 0;

        while (relative_error > relative_tolerance)
        {
            j_i = sei_model.calc_j_i(j_tot, j_s);
            eta_n = sei_model.calc_eta_n(temp, j_i, j_0_i);
            eta_s = sei_model.calc_eta_s(eta_n, ocp_n, m_U_s);
            j_s_prev = j_s;
            j_s = sei_model.calc_j_s(temp, m_j_0_s, eta_s);

            relative_error = std::abs((j_s - j_s_prev) / j_s);
            iter += 1;
            if (iter >= max_iter)
                break;
        }
        I_s = general_equations::molar_flux_to_current(j_s, m_S, electrode_type);
    }
    else
        I_s = 0.0;
    m_j_s = j_s;
    return I_s;
}

double ROMSEISolver::solve_delta_L(double j_s, double dt)
{
    return -(m_MW_SEI * j_s / m_rho) * dt;
}

// thermal solver definations below
LumpedThermalSolver::LumpedThermalSolver(double i_h, double i_A, double i_rho, double i_vol, double i_C_p, double i_temp_init)
{
    m_h = i_h;
    m_A = i_A;
    m_rho = i_rho;
    m_vol = i_vol;
    m_C_p = i_C_p;
    m_temp_init = i_temp_init;
    m_temp = i_temp_init;      // initial condition
    m_temp_prev = i_temp_init; // initial condition
}

double
LumpedThermalSolver::reversible_heat(double dOCPdT_p, double dOCPdT_n, double I, double T)
{
    return I * T * (dOCPdT_p - dOCPdT_n);
}

double LumpedThermalSolver::irreversible_heat(double OCP_p, double OCP_n, double I, double V)
{
    return I * (V - (OCP_p - OCP_n));
}

double LumpedThermalSolver::heat_transfer(double T, double T_amb)
{
    return m_h * m_A * (T - T_amb);
}

double LumpedThermalSolver::solve_temp(double dt, double t_prev, double I, double V,
                                       double temp_amb,
                                       double OCP_p, double OCP_n, double dOCPdT_p, double dOCPdT_n)
{
    auto ode_func = [this, I, V, temp_amb, OCP_p, OCP_n, dOCPdT_p, dOCPdT_n](double t, double temp)
    {
        double main_coeff = 1 / (m_rho * m_vol * m_C_p);
        return main_coeff * (reversible_heat(dOCPdT_p, dOCPdT_n, I, V) +
                             irreversible_heat(OCP_p, OCP_n, I, V) -
                             heat_transfer(temp, temp_amb));
    };
    double temp_calculated = Newton::ODESolver::rk4(t_prev, m_temp_prev, dt, ode_func);
    m_temp_prev = m_temp;
    m_temp = temp_calculated;
    return temp_calculated;
}

BaseConcSolver::BaseConcSolver(char i_electrode_type)
{
    if ((i_electrode_type == 'p') | (i_electrode_type == 'n'))
        m_electrode_type = i_electrode_type;
    else
        throw std::invalid_argument("electrode_type must be p or n");
}

PolynomialApprox::PolynomialApprox(char electrodeType, double i_c_init, std::string type)
    : BaseConcSolver(electrodeType)
{
    m_type = type;
    m_c_s_avg_prev = i_c_init;
    m_c_surf = i_c_init;
    m_q = 0.0;
}

double PolynomialApprox::solve_c_s_avg(double dt, double t_prev, double j, double R, double D)
{
    auto ode_func = [j, R, D](double t, double x)
    { return -3 * j / R; };
    return Newton::ODESolver::rk4(t_prev, m_c_s_avg_prev, dt, ode_func);
}

double PolynomialApprox::solve_q(double dt, double t_prev, double j, double R, double D)
{
    auto ode_func_q = [j, R, D](double t, double x)
    { return -30 * (D / std::pow(R, 2)) * x - 45 * j / (2 * std::pow(R, 2)); };
    return Newton::ODESolver::rk4(t_prev, m_q, dt, ode_func_q);
}

void PolynomialApprox::solve(double dt, double t_prev, double i_app, double R, double S, double D)
{
    double j = SPModel().molar_flux_electrode(i_app, S, m_electrode_type);
    m_c_s_avg_prev = solve_c_s_avg(dt, t_prev, j, R, D);
    if (m_type == "two")
        m_c_surf = -(R / D) * (j / 5) + m_c_s_avg_prev;
    else if (m_type == "higher")
    {
        m_q = solve_q(dt, t_prev, j, R, D);
        m_c_surf = -(j * R) / (35 * D) + 8 * R * m_q / 35 + m_c_s_avg_prev;
    }
    else
        throw std::invalid_argument("Invalid solver type.");
}

// below are the method definations for the EigenSolver

EigenSolver::EigenSolver(char i_electrode_type, double i_soc_init, int i_num_roots)
    : BaseConcSolver(i_electrode_type), m_num_roots(i_num_roots)
{
    // check if the number of roots are greater than 0
    if (m_num_roots < 0)
        throw std::invalid_argument("number of roots have to greater than 0.");
    // get array bounds and vec_u_k
    m_lambda_bounds = OWL::Zeros(2, m_num_roots);
    for (int i = 0; i < m_num_roots; i++)
    {
        m_vec_u_k.push_back(0.0); // initialize the eigen values to zeros
        m_lambda_bounds[0][i] = Constants.pi + Constants.pi * i;
        m_lambda_bounds[1][i] = 2 * Constants.pi + Constants.pi * i;
    }

    // roots
    for (int i = 0; i < i_num_roots; i++)
    {
        m_roots.push_back(Newton::roots::Brent(lambda_function, m_lambda_bounds[0][i], m_lambda_bounds[1][i], 1e-5, 90));
    }

    // assign electrode type
    m_electrode_type = i_electrode_type;
    m_integ_term = 0.0;
    m_soc_init = i_soc_init;
}

/**
 * @brief Algebraic equation from which the eigenvalues can be calculated.
 *
 * @param lambda_k (double) eigen value ot the kth term.
 * @return double (float) the value of the elgebraic equation.
 */
double lambda_function(double lambda_k)
{
    return std::sin(lambda_k) - lambda_k * std::cos(lambda_k);
}

double EigenSolver::j_scaled(double i_app, double R, double S, double D_s, double c_s_max)
{
    double j_scaled_ = i_app * R / (Constants.F * S * D_s * c_s_max);
    if (m_electrode_type == 'p')
        return -j_scaled_;
    else if (m_electrode_type == 'n')
        return j_scaled_;
    else
        throw std::invalid_argument(" electrode type needs to be 'p' or 'n' ");
}

/**
 * @brief Updates the integration term. Integration is performed using simple algebraic integration.
 *
 * @param dt
 * @param i_app
 * @param R
 * @param S
 * @param D_s
 * @param c_s_max
 * @return
 */
void EigenSolver::update_integ_term(double dt, double i_app, double R, double S, double D_s, double c_s_max)
{
    m_integ_term += 3 * (D_s * j_scaled(i_app, R, S, D_s, c_s_max) / std::pow(R, 2)) * dt;
}

double EigenSolver::du_kdt(double root, double D, double R, double scaled_flux, double t, double u)
{
    return -std::pow(root, 2) * D * u / std::pow(R, 2) + 2 * D * scaled_flux / std::pow(R, 2);
}

double EigenSolver::solve_u_k(double root, double t_prev, double dt,
                              double u_k_prev, double i_app, double R, double S, double D_s, double c_s_max)
{
    double scaled_j_value = j_scaled(i_app, R, S, D_s, c_s_max);
    std::function<double(double, double)> func = [this, root, D_s, R, scaled_j_value](double t, double u)
    { return du_kdt(root, D_s, R, scaled_j_value, t, u); };
    return Newton::ODESolver::rk4(t_prev, u_k_prev, dt, func);
}

void EigenSolver::update_vec_u_k(double dt, double t_prev, double i_app, double R, double S, double D_s, double c_s_max)
{
    double current_root;
    double u_k_prev_value;
    for (int i = 0; i < get_roots().size(); i++)
    {
        current_root = get_roots()[i];
        u_k_prev_value = get_vec_u_k()[i];
        get_vec_u_k()[i] = solve_u_k(current_root, t_prev, dt, u_k_prev_value, i_app, R, S, D_s, c_s_max);
    }
}

double EigenSolver::get_summation_term(double dt, double t_prev, double i_app, double R, double S, double D_s, double c_s_max)
{
    double sum_term = 0.0;
    double j_scaled_value = j_scaled(i_app, R, S, D_s, c_s_max);
    double current_root;
    double u_k_prev_value;
    for (int i = 0; i < get_roots().size(); i++)
    {
        current_root = get_roots()[i];
        u_k_prev_value = get_vec_u_k()[i];
        m_vec_u_k[i] = solve_u_k(current_root, t_prev, dt, u_k_prev_value, i_app, R, S, D_s, c_s_max);
        sum_term += m_vec_u_k[i] - (2 * j_scaled_value / std::pow(current_root, 2));
    }
    return sum_term;
}

double EigenSolver::solve(double dt, double t_prev, double i_app, double R, double S, double D_s, double c_s_max)
{
    double j_scaled_value = j_scaled(i_app, R, S, D_s, c_s_max);
    double sum_term = get_summation_term(t_prev, dt, i_app, R, S, D_s, c_s_max);
    update_integ_term(dt, i_app, R, S, D_s, c_s_max);
    return m_soc_init + j_scaled_value / 5 + m_integ_term + sum_term;
}

CNSolver::CNSolver(double i_c_init, char i_electrode_type, int i_spatial_grid_points) : BaseConcSolver(i_electrode_type), m_K(i_spatial_grid_points)
{
    OWL::ArrayXD c_prev_ = i_c_init * OWL::Ones(m_K);
    m_c_prev = c_prev_.getArray();
    m_c_surf = m_c_prev[m_c_prev.size() - 1];
}

std::vector<double> CNSolver::array_R(double R)
{
    OWL::ArrayXD array_ = OWL::LinSpaced(0, R, m_K);
    return array_.getArray();
}

std::vector<double> CNSolver::LHS_diag_elements(double dt, double R, double D)
{
    double A_ = A(dt, R, D);
    OWL::ArrayXD array_ = (1 + A_) * OWL::Ones(m_K);
    std::vector<double> result_vector = array_.getArray();
    result_vector[0] = 1 + 3 * A_; // for symmetry boundary condition at r=0
    result_vector[result_vector.size() - 1] = 1 + A_;
    return result_vector;
}

std::vector<double> CNSolver::LHS_lower_diag_elements(double dt, double R, double D)
{
    double A_ = A(dt, R, D);
    double B_ = B(dt, R, D);
    std::vector<double> vector_R = array_R(R);

    std::vector<double> result_vector;
    for (int i = 0; i < m_K - 2; i++)
    {
        result_vector.push_back(-(A_ / 2 - B_ / vector_R[i + 1]));
    }
    result_vector.push_back(-A_);
    return result_vector;
}

std::vector<double> CNSolver::LHS_upper_diag_elements(double dt, double R, double D)
{
    double A_ = A(dt, R, D);
    double B_ = B(dt, R, D);
    std::vector<double> vector_R = array_R(R);

    std::vector<double> result_vector;
    result_vector.push_back(-3 * A_);
    for (int i = 1; i < m_K - 1; i++)
    {
        result_vector.push_back(-(A_ / 2 + B_ / vector_R[i]));
    }
    return result_vector;
}

std::vector<double> CNSolver::RHS_vector(double j, double dt, double R, double D)
{
    double A_ = A(dt, R, D);
    double B_ = B(dt, R, D);
    std::vector<double> vector_R = array_R(R);

    std::vector<double> result_vector;
    result_vector.push_back((1 - 3 * A_) * m_c_prev[0] + 3 * A_ * m_c_prev[1]); // for the symmetry boundary condition at r=0

    for (int i = 1; i < m_K - 1; i++)
    {
        result_vector.push_back((1 - A_) * m_c_prev[i] +
                                (A_ / 2 + B_ / vector_R[i]) * m_c_prev[i + 1] +
                                (A_ / 2 - B_ / vector_R[i]) * m_c_prev[i - 1]);
    }
    result_vector.push_back((1 - A_) * m_c_prev[m_c_prev.size() - 1] - (A_ + B_ / R) * (2 * dr(R = R) * j / D) +
                            A_ * m_c_prev[m_c_prev.size() - 2]); // for the boundary condition at r=R
    return result_vector;
}

void CNSolver::solve(double dt, double i_app, double R, double S, double D)
{
    SPModel model_ = SPModel();
    double j = model_.molar_flux_electrode(i_app, S, m_electrode_type);

    std::vector<double> diag = LHS_diag_elements(dt, R, D);
    std::vector<double> lower_diag = LHS_lower_diag_elements(dt, R, D);
    std::vector<double> upper_diag = LHS_upper_diag_elements(dt, R, D);
    std::vector<double> b = RHS_vector(j, dt, R, D);

    m_c_prev = Newton::MatrixSolvers::TDMASolver(lower_diag, diag, upper_diag, b);
    m_c_surf = m_c_prev[m_c_prev.size() - 1];
}

/*
 *  Lithium-Ion Concentration Solver in the Electrolyte
 */

ElectrolyteFVMSolver::ElectrolyteFVMSolver(ElectrolyteFVMCoordinates i_coords, double i_c_e_init, double i_t_c,
                                           double i_epsilon_e_n, double i_epsilon_e_sep, double i_epsilon_e_p,
                                           double i_a_s_n, double i_a_s_p,
                                           double i_D_e, double i_brugg) : m_coords(i_coords), m_c_e_init(i_c_e_init), m_t_c(i_t_c),
                                                                           m_epsilon_e_n(i_epsilon_e_n), m_epsilon_e_sep(i_epsilon_e_sep), m_epsilon_e_p(i_epsilon_e_p),
                                                                           m_a_s_n(i_a_s_n), m_a_s_p(i_a_s_p),
                                                                           m_D_e(i_D_e), m_brugg(i_brugg)
{
    // below sets the vector_c_e
    OWL::ArrayXD m_vector_c_e_ = m_c_e_init * OWL::Ones(static_cast<int>(m_coords.get_vector_x().size()));
    m_vector_c_e = m_vector_c_e_.getArray();

    // below creates the vector_epsilon_e
    OWL::ArrayXD vector_epsilon_e_n_ = m_epsilon_e_n * OWL::Ones(static_cast<int>(m_coords.get_vector_x_n().size()));
    OWL::ArrayXD vector_epsilon_e_sep_ = m_epsilon_e_sep * OWL::Ones(static_cast<int>(m_coords.get_vector_x_sep().size()));
    OWL::ArrayXD vector_epsilon_e_p_ = m_epsilon_e_p * OWL::Ones(static_cast<int>(m_coords.get_vector_x_p().size()));
    OWL::ArrayXD vector_epsilon_e_ = OWL::append(vector_epsilon_e_n_, vector_epsilon_e_sep_);
    m_vector_epsilon_e = OWL::append(vector_epsilon_e_, vector_epsilon_e_p_).getArray();

    // below creates vector_D_e
    OWL::ArrayXD vector_D_e_n_ = m_D_e * std::pow(m_epsilon_e_n, m_brugg) * OWL::Ones(static_cast<int>(m_coords.get_vector_x_n().size()));
    OWL::ArrayXD vector_D_e_sep_ = m_D_e * std::pow(m_epsilon_e_sep, m_brugg) * OWL::Ones(static_cast<int>(m_coords.get_vector_x_sep().size()));
    OWL::ArrayXD vector_D_e_p_ = m_D_e * std::pow(m_epsilon_e_p, m_brugg) * OWL::Ones(static_cast<int>(m_coords.get_vector_x_p().size()));
    OWL::ArrayXD vector_D_e_ = OWL::append(vector_D_e_n_, vector_D_e_sep_);
    m_vector_D_eff = OWL::append(vector_D_e_, vector_D_e_p_).getArray();

    // below sets the vector_a_s
    OWL::ArrayXD vector_a_n_ = m_a_s_n * OWL::Ones(static_cast<int>(m_coords.get_vector_x_n().size()));
    OWL::ArrayXD vector_a_sep_ = OWL::Zeros(static_cast<int>(m_coords.get_vector_x_sep().size()));
    OWL::ArrayXD vector_a_p_ = m_a_s_p * OWL::Ones(static_cast<int>(m_coords.get_vector_x_p().size()));
    OWL::ArrayXD vector_a_s_ = OWL::append(vector_a_n_, vector_a_sep_);
    m_vector_a_s = OWL::append(vector_a_s_, vector_a_p_).getArray();
}

/**
 * @brief returns a vector representing the main diagonal the FVM left-hand side matrix
 *
 * @param dt time difference between the current and previous time steps
 * @return std::vector<double> vector representing the main diagonal
 */
std::vector<double> ElectrolyteFVMSolver::calc_diag(double &dt)
{
    std::vector<double> result_vector;
    double dx, dx1, dx2, D1, D2, D3, A;
    dx = m_coords.get_vector_x()[1] - m_coords.get_vector_x()[0];
    D1 = m_vector_D_eff[0];
    D2 = m_vector_D_eff[1];
    A = dt / (2 * m_coords.get_vector_dx()[0]);
    result_vector.push_back(m_vector_epsilon_e[0] + A * (D2 + D1) / dx);

    for (int i = 1; i < m_coords.get_vector_x().size() - 1; i++)
    {
        dx1 = m_coords.get_vector_x()[i] - m_coords.get_vector_x()[i - 1];
        dx2 = m_coords.get_vector_x()[i + 1] - m_coords.get_vector_x()[i];
        D1 = m_vector_D_eff[i - 1];
        D2 = m_vector_D_eff[i];
        D3 = m_vector_D_eff[i + 1];
        A = dt / (2 * m_coords.get_vector_dx()[i]);
        result_vector.push_back(m_vector_epsilon_e[i] + A * ((D1 + D2) / dx1 + (D2 + D3) / dx2));
    }

    dx = m_coords.get_vector_x().back() - m_coords.get_vector_x()[m_coords.get_vector_x().size() - 2];
    D1 = m_vector_D_eff.back();
    D2 = m_vector_D_eff.back();
    A = dt / (2 * m_coords.get_vector_dx().back());
    result_vector.push_back(m_vector_epsilon_e.back() + A * (D2 + D1) / dx);

    return result_vector;
}

/**
 * @brief returns a vector representing the lower diagonal of the FVM left-hand side matrix
 *
 * @param dt time difference between the current and the previous time step.
 * @return std::vector<double> vector representing the lower diagonal
 */
std::vector<double> ElectrolyteFVMSolver::calc_lower_diag(double &dt)
{
    std::vector<double> result_vector;
    double dx, dx1, D1, D2, A;

    for (int i = 1; i < m_coords.get_vector_x().size() - 1; i++)
    {
        dx1 = m_coords.get_vector_x()[i] - m_coords.get_vector_x()[i - 1];
        D1 = m_vector_D_eff[i - 1];
        D2 = m_vector_D_eff[i];
        A = dt / (2 * m_coords.get_vector_dx()[i]);
        result_vector.push_back(-A * (D1 + D2) / dx1);
    }

    dx = m_coords.get_vector_x().back() - m_coords.get_vector_x()[m_coords.get_vector_x().size() - 2];
    D1 = m_vector_D_eff.back();
    D2 = m_vector_D_eff.back();
    A = dt / (2 * m_coords.get_vector_dx().back());
    result_vector.push_back(-A * (D2 + D1) / dx);

    return result_vector;
}

/**
 * @brief Returns the upper diagonal of the FVM left-hand side matrix.
 *
 * @param dt time difference between the previous time step and the current time step
 * @return std::vector<double> vector representing the upper diagonal
 */
std::vector<double> ElectrolyteFVMSolver::calc_upper_diag(double &dt)
{
    std::vector<double> result_vector;
    double dx, dx1, dx2, D1, D2, D3, A;

    dx = m_coords.get_vector_x()[1] - m_coords.get_vector_x()[0];
    D1 = m_vector_D_eff[0];
    D2 = m_vector_D_eff[1];
    A = dt / (2 * m_coords.get_vector_dx()[0]);
    result_vector.push_back(-A * (D2 + D1) / dx);

    for (int i = 1; i < m_coords.get_vector_x().size() - 1; i++)
    {
        dx1 = m_coords.get_vector_x()[i] - m_coords.get_vector_x()[i - 1];
        dx2 = m_coords.get_vector_x()[i + 1] - m_coords.get_vector_x()[i];
        D1 = m_vector_D_eff[i - 1];
        D2 = m_vector_D_eff[i];
        D3 = m_vector_D_eff[i + 1];
        A = dt / (2 * m_coords.get_vector_dx()[i]);
        result_vector.push_back(-A * (D3 + D2) / dx2);
    }

    return result_vector;
}

std::vector<double> ElectrolyteFVMSolver::calc_vector_ce_j(std::vector<double> &c_prev, std::vector<double> &j, double &dt)
{
    std::vector<double> result_vector;

    for (int i = 0; i < m_coords.get_vector_x().size(); i++)
    {
        result_vector.push_back(c_prev[i] * m_vector_epsilon_e[i] + (1 - m_t_c) * m_vector_a_s[i] * j[i] * dt);
    }

    return result_vector;
}

void ElectrolyteFVMSolver::solve(std::vector<double> j, double dt)
{
    std::vector<double> b = calc_vector_ce_j(m_vector_c_e, j, dt);
    m_vector_c_e = Newton::MatrixSolvers::TDMASolver(calc_lower_diag(dt), calc_diag(dt), calc_upper_diag(dt), b);
}

/*
 *  Battery Solvers Below
 */

BaseBatterySolver::BaseBatterySolver(BatteryCell i_b_cell, bool i_isothermal, bool i_degradation,
                                     std::string i_electrode_SOC_solver) : m_b_cell(i_b_cell)
{
    m_isothermal = i_isothermal;
    m_degradation = i_degradation;
    m_electrode_SOC_solver = i_electrode_SOC_solver;
}

BatterySolver::BatterySolver(BatteryCell i_b_cell, bool i_isothermal, bool i_degradation,
                             std::string i_electrode_SOC_solver) : BaseBatterySolver(i_b_cell, i_isothermal, i_degradation, i_electrode_SOC_solver),
                                                                   SOC_solver_p('p', i_b_cell.elec_p.get_c_max() * i_b_cell.elec_p.get_SOC(), "higher"),
                                                                   SOC_solver_n('n', i_b_cell.elec_n.get_c_max() * i_b_cell.elec_n.get_SOC(), "higher"),
                                                                   m_CN_SOC_solver_p(i_b_cell.elec_p.get_c_max() * i_b_cell.elec_p.get_SOC(), 'p', 100),
                                                                   m_CN_SOC_solver_n(i_b_cell.elec_n.get_c_max() * i_b_cell.elec_n.get_SOC(), 'n', 100),
                                                                   thermal_solver(i_b_cell.get_h(), i_b_cell.get_A(), i_b_cell.get_rho(),
                                                                                  i_b_cell.get_Vol(), i_b_cell.get_C_p(), i_b_cell.get_T()),
                                                                   m_electrode_SOC_solver(i_electrode_SOC_solver)
{
}

double BatterySolver::calc_V(double I)
{
    double m_p = SPModel().m(I, m_b_cell.elec_p.get_k(), m_b_cell.elec_p.get_S(), m_b_cell.elec_p.get_c_max(),
                             m_b_cell.elec_p.get_SOC(), m_b_cell.electrolyte.get_conc());
    double m_n = SPModel().m(I, m_b_cell.elec_n.get_k(), m_b_cell.elec_n.get_S(), m_b_cell.elec_n.get_c_max(),
                             m_b_cell.elec_n.get_SOC(), m_b_cell.electrolyte.get_conc());
    double V = SPModel().calc_terminal_V(m_b_cell.elec_p.get_OCP(), m_b_cell.elec_n.get_OCP(), m_p, m_n,
                                         m_b_cell.get_R_cell(), m_b_cell.get_T(), I);
    return V;
}

OverPotentials BatterySolver::calc_overpotentials(double I)
{
    double m_p = SPModel().m(I, m_b_cell.elec_p.get_k(), m_b_cell.elec_p.get_S(), m_b_cell.elec_p.get_c_max(),
                             m_b_cell.elec_p.get_SOC(), m_b_cell.electrolyte.get_conc());
    double m_n = SPModel().m(I, m_b_cell.elec_n.get_k(), m_b_cell.elec_n.get_S(), m_b_cell.elec_n.get_c_max(),
                             m_b_cell.elec_n.get_SOC(), m_b_cell.electrolyte.get_conc());
    return SPModel().calc_overpotentials(m_b_cell.elec_p.get_OCP(), m_b_cell.elec_n.get_OCP(), m_p, m_n,
                                         m_b_cell.get_R_cell(), m_b_cell.get_T(), I);
}

std::pair<OverPotentials, bool> BatterySolver::solve_one_iteration(double t_prev, double dt, double I)
{
    bool step_completed = false;

    if (m_electrode_SOC_solver.compare("poly") == 0)
    {
        SOC_solver_p.solve(dt, t_prev, I, m_b_cell.elec_p.get_R(), m_b_cell.elec_p.get_S(), m_b_cell.elec_p.get_D());
        SOC_solver_n.solve(dt, t_prev, I, m_b_cell.elec_n.get_R(), m_b_cell.elec_n.get_S(), m_b_cell.elec_n.get_D());

        try
        {
            m_b_cell.elec_p.update_SOC(SOC_solver_p.get_x_surf(m_b_cell.elec_p.get_c_max()));
            m_b_cell.elec_n.update_SOC(SOC_solver_n.get_x_surf(m_b_cell.elec_n.get_c_max()));
        }
        catch (InvalidSOCException &e)
        {
            step_completed = true;
            std::cout << e.what() << std::endl;
        }
    }
    else if (m_electrode_SOC_solver.compare("CN") == 0)
    {
        m_CN_SOC_solver_p.solve(dt, I, m_b_cell.elec_p.get_R(), m_b_cell.elec_p.get_S(), m_b_cell.elec_p.get_D());
        m_CN_SOC_solver_n.solve(dt, I, m_b_cell.elec_n.get_R(), m_b_cell.elec_n.get_S(), m_b_cell.elec_n.get_D());

        try
        {
            m_b_cell.elec_p.update_SOC(m_CN_SOC_solver_p.get_c_s_surf() / m_b_cell.elec_p.get_c_max());
            m_b_cell.elec_n.update_SOC(m_CN_SOC_solver_n.get_c_s_surf() / m_b_cell.elec_n.get_c_max());
        }
        catch (InvalidSOCException &e)
        {
            std::cout << e.what() << std::endl;
        }
    }
    else
    {
        throw std::exception();
    }

    OverPotentials overpotential_ = calc_overpotentials(I);
    double V_new = overpotential_.V;

    if (!m_isothermal)
    {
        double temp_new = thermal_solver.solve_temp(dt, t_prev, I, V_new,
                                                    thermal_solver.get_temp_init(),
                                                    m_b_cell.elec_p.get_OCP(), m_b_cell.elec_n.get_OCP(),
                                                    m_b_cell.elec_p.get_dOCPdT(),
                                                    m_b_cell.elec_n.get_dOCPdT()); // Note: It is assumed that the ambient temperature remains constant.
                                                                                   // FOr varying ambient temperature, enter the value of the ambient temperature at that time-step here.
        m_b_cell.elec_p.update_T(temp_new);
        m_b_cell.elec_n.update_T(temp_new);
        m_b_cell.set_temp(temp_new);
    }
    return {overpotential_, step_completed};
}

Solution BatterySolver::solve(BaseCycler i_cycler, int store_solution_iter)
{
    clock_t start, end;
    start = clock();
    // const std::clock_t c_start = std::clock();
    // auto t_start = std::chrono::high_resolution_clock::now();
    // std::time_t time_start = std::time(NULL);

    // initialization of the simulation results vectors
    Solution sol = Solution();

    // Simulation calculation at the initial time step
    double term_V = m_b_cell.elec_p.get_OCP() - m_b_cell.elec_n.get_OCP();
    double cap = 0.0;
    double sim_time = 0.0;

    // simultion loop
    for (int i = 0; i < i_cycler.cycle_steps.size(); i++)
    {
        cap = 0.0;
        int time_index = 0;
        double t_curr = 0.0; // This is the cycling step time.
        double t_prev;
        double dt = 0.1;
        double I;
        bool step_completed = false;
        std::string cycling_step = i_cycler.cycle_steps[i];
        OverPotentials step_overpontentials;
        std::pair<OverPotentials, bool> term_V_and_bool;

        while (!step_completed)
        {
            t_prev = t_curr;
            t_curr = t_curr + dt;
            sim_time += dt;
            I = i_cycler.get_current(i_cycler.cycle_steps[i], time_index);
            term_V_and_bool = solve_one_iteration(t_prev, dt, I);
            step_overpontentials = term_V_and_bool.first;
            term_V = step_overpontentials.V;
            if (term_V_and_bool.second)
            {
                step_completed = true;
            }
            cap = general_equations::calc_cap(cap, m_b_cell.get_cap(), I, dt);

            // break conditions
            if ((i_cycler.cycle_steps[i] == "rest") & (t_curr > i_cycler.rest_time))
                step_completed = true;
            if ((i_cycler.cycle_steps[i] == "discharge") & (term_V < i_cycler.V_min))
                step_completed = true;
            if ((i_cycler.cycle_steps[i] == "charge") & (term_V > i_cycler.V_max))
                step_completed = true;
            if ((i_cycler.cycle_steps[i] == "custom") & ((t_curr > i_cycler.rest_time) | (term_V < i_cycler.V_min)))
                step_completed = true;

            // The arrays are updated below
            if ((time_index == 0) || (time_index % store_solution_iter == 0))
            {
                sol.update_t(sim_time);
                sol.update_cycling_step(cycling_step);
                sol.update_V(term_V);
                sol.update_temp(m_b_cell.get_T());
                sol.update_cap(cap);
                sol.update_x_p(m_b_cell.elec_p.get_SOC());
                sol.update_x_n(m_b_cell.elec_n.get_SOC());

                // // calculation and updates of overpotentials
                // std::tuple<double, double, double, double, double> overpotential_values = calc_overpotentials(I);
                // sol.update_OCV_LIB(std::get<1>(overpotential_values));
                // sol.update_overpotential_elec_p(std::get<2>(overpotential_values));
                // sol.update_overpotential_elec_n(std::get<3>(overpotential_values));
                // sol.update_overpotential_R_cell(std::get<4>(overpotential_values));
                sol.update_OCV_LIB(step_overpontentials.OCV_LIB);
                sol.update_overpotential_elec_p(step_overpontentials.elec_p);
                sol.update_overpotential_elec_n(step_overpontentials.elec_n);
                sol.update_overpotential_R_cell(step_overpontentials.R_cell);
                sol.update_overpotential_electrolyte(step_overpontentials.electrolyte);
            }

            time_index += 1;
        }
    }

    end = clock();
    // const std::clock_t c_end = std::clock();
    // std::time_t time_end = std::time(NULL);
    // const auto t_end = std::chrono::high_resolution_clock::now();

    std::cout << std::fixed << std::setprecision(10) << "Solution time: " << double(end - start) / double(CLOCKS_PER_SEC) << "s" << std::endl;

    return sol;
}

ESPBatterySolver::ESPBatterySolver(BatteryCell i_b_cell,
                                   bool i_isothermal,
                                   bool i_degradation,
                                   std::string i_electrode_SOC_solver) : BaseBatterySolver(i_b_cell, i_isothermal, i_degradation, i_electrode_SOC_solver),
                                                                         a_s_p(m_b_cell.elec_p.get_S() / m_b_cell.elec_p.get_L()),
                                                                         a_s_n(m_b_cell.elec_n.get_S() / m_b_cell.elec_n.get_L()),
                                                                         SOC_solver_p('p', i_b_cell.elec_p.get_c_max() * i_b_cell.elec_p.get_SOC(), "higher"),
                                                                         SOC_solver_n('n', i_b_cell.elec_n.get_c_max() * i_b_cell.elec_n.get_SOC(), "higher"),
                                                                         electrolyte_coords(i_b_cell.elec_n.get_L(), i_b_cell.electrolyte.get_L(), i_b_cell.elec_p.get_L(), 10, 10, 10),
                                                                         electrolyte_solver(electrolyte_coords, i_b_cell.electrolyte.get_conc(),
                                                                                            m_b_cell.electrolyte.get_t_c(),
                                                                                            m_b_cell.electrolyte.get_epsilon_n(), m_b_cell.electrolyte.get_epsilon(), m_b_cell.electrolyte.get_epsilon_p(),
                                                                                            a_s_n, a_s_p, m_b_cell.electrolyte.get_D_e(),
                                                                                            m_b_cell.electrolyte.get_brugg()),
                                                                         thermal_solver(i_b_cell.get_h(), i_b_cell.get_A(), i_b_cell.get_rho(),
                                                                                        i_b_cell.get_Vol(), i_b_cell.get_C_p(), i_b_cell.get_T())
{
}

std::pair<OverPotentials, bool> ESPBatterySolver::solve_one_iteration(double t_prev, double dt, double i_app, double temp)
{
    bool step_completed = false;

    // solve for the electrode surface conc
    SOC_solver_p.solve(dt, t_prev, i_app, m_b_cell.elec_p.get_R(), m_b_cell.elec_p.get_S(), m_b_cell.elec_p.get_D());
    SOC_solver_n.solve(dt, t_prev, i_app, m_b_cell.elec_n.get_R(), m_b_cell.elec_n.get_S(), m_b_cell.elec_n.get_D());

    try
    {
        m_b_cell.elec_p.update_SOC(SOC_solver_p.get_x_surf(m_b_cell.elec_p.get_c_max()));
        m_b_cell.elec_n.update_SOC(SOC_solver_n.get_x_surf(m_b_cell.elec_n.get_c_max()));
    }
    catch (InvalidSOCException &e)
    {
        std::cout << e.what() << std::endl;
        step_completed = true;
    }

    // solve for the electrolyte conc
    OWL::ArrayXD j_n_ = ESPModel::molar_flux_electrode(i_app, m_b_cell.elec_n.get_S(), 'n') * OWL::Ones(static_cast<int>(electrolyte_coords.get_vector_x_n().size()));
    OWL::ArrayXD j_sep_ = OWL::Zeros(static_cast<int>(electrolyte_coords.get_vector_x_sep().size()));
    OWL::ArrayXD j_p_ = ESPModel::molar_flux_electrode(i_app, m_b_cell.elec_p.get_S(), 'p') * OWL::Ones(static_cast<int>(electrolyte_coords.get_vector_x_p().size()));
    OWL::ArrayXD j_ = OWL::append(j_n_, j_sep_);
    j_ = OWL::append(j_, j_p_);
    std::vector<double> j = j_.getArray();

    electrolyte_solver.solve(j, dt);

    // calculation of the terminal voltage
    double c_e_n = electrolyte_solver.get_vector_c_e()[0];
    double c_e_p = electrolyte_solver.get_vector_c_e().back();

    double m_p = ESPModel::m(i_app, m_b_cell.elec_p.get_k(), m_b_cell.elec_p.get_S(), m_b_cell.elec_p.get_c_max(),
                             c_e_p, m_b_cell.elec_p.get_SOC());
    double m_n = ESPModel::m(i_app, m_b_cell.elec_n.get_k(), m_b_cell.elec_n.get_S(), m_b_cell.elec_n.get_c_max(),
                             c_e_n, m_b_cell.elec_n.get_SOC());

    OverPotentials overpotentials_ = ESPModel::calc_overpotentials(m_b_cell.elec_p.get_OCP(), m_b_cell.elec_n.get_OCP(), m_p, m_n,
                                                                   m_b_cell.elec_n.get_L(), m_b_cell.electrolyte.get_L(), m_b_cell.elec_p.get_L(),
                                                                   m_b_cell.electrolyte.get_kappa_eff(), 1.0,
                                                                   m_b_cell.electrolyte.get_t_c(), m_b_cell.get_R_cell(),
                                                                   c_e_n, c_e_p, temp, i_app);
    double V = overpotentials_.V;

    if (!m_isothermal)
    {
        double temp_new = thermal_solver.solve_temp(dt, t_prev, i_app, V,
                                                    thermal_solver.get_temp_init(),
                                                    m_b_cell.elec_p.get_OCP(), m_b_cell.elec_n.get_OCP(),
                                                    m_b_cell.elec_p.get_dOCPdT(),
                                                    m_b_cell.elec_n.get_dOCPdT()); // Note: It is assumed that the ambient temperature remains constant.
                                                                                   // FOr varying ambient temperature, enter the value of the ambient temperature at that time-step here.
        m_b_cell.elec_p.update_T(temp_new);
        m_b_cell.elec_n.update_T(temp_new);
        m_b_cell.set_temp(temp_new);
    }

    return {overpotentials_, step_completed};
}

Solution ESPBatterySolver::solve(BaseCycler i_cycler)
{
    // check for existence of relevant electrolyte parameters
    if ((m_b_cell.electrolyte.get_D_e() == 0.0) || (m_b_cell.electrolyte.get_t_c() == 0.0) || (m_b_cell.electrolyte.get_epsilon_n() == 0.0) || (m_b_cell.electrolyte.get_epsilon_p() == 0.0))
        throw InsufficientESPMParameters();

    clock_t start, end;
    start = clock();
    // const std::clock_t c_start = std::clock();
    // auto t_start = std::chrono::high_resolution_clock::now();
    // std::time_t time_start = std::time(NULL);

    // initialization of the simulation results vectors
    Solution sol = Solution();

    // Simulation calculation at the initial time step
    double term_V = m_b_cell.elec_p.get_OCP() - m_b_cell.elec_n.get_OCP();
    double cap = 0.0;
    double sim_time = 0.0;
    std::pair<OverPotentials, bool> term_V_and_bool;
    // sol.update_t(sim_time);
    // sol.update_cycling_step("rest");
    // sol.update_V(term_V);
    // sol.update_temp(m_b_cell.get_T());
    // sol.update_cap(cap);
    // sol.update_x_p(m_b_cell.elec_p.get_SOC());
    // sol.update_x_n(m_b_cell.elec_n.get_SOC());

    // simultion loop
    for (int i = 0; i < i_cycler.cycle_steps.size(); i++)
    {
        cap = 0.0;
        int time_index = 0;
        double t_curr = 0.0; // This is the cycling step time.
        double t_prev;
        double dt = 0.1;
        double I;
        bool step_completed = false;
        std::string cycling_step = i_cycler.cycle_steps[i];

        while (!step_completed)
        {
            t_prev = t_curr;
            t_curr = t_curr + dt;
            sim_time += dt;
            I = i_cycler.get_current(i_cycler.cycle_steps[i], time_index);
            term_V_and_bool = solve_one_iteration(t_prev, dt, I, m_b_cell.get_T());
            term_V = term_V_and_bool.first.V;
            if (term_V_and_bool.second)
            {
                step_completed = true;
            }
            cap = general_equations::calc_cap(cap, m_b_cell.get_cap(), I, dt);

            // break conditions
            if ((i_cycler.cycle_steps[i] == "rest") & (t_curr > i_cycler.rest_time))
                step_completed = true;
            if ((i_cycler.cycle_steps[i] == "discharge") & (term_V < i_cycler.V_min))
                step_completed = true;
            if ((i_cycler.cycle_steps[i] == "charge") & (term_V > i_cycler.V_max))
                step_completed = true;
            if ((i_cycler.cycle_steps[i] == "custom") & ((t_curr > i_cycler.rest_time) | (term_V < i_cycler.V_min)))
                step_completed = true;

            // The arrays are updated below
            sol.update_t(sim_time);
            sol.update_cycling_step(cycling_step);
            sol.update_V(term_V);
            sol.update_temp(m_b_cell.get_T());
            sol.update_cap(cap);
            sol.update_x_p(m_b_cell.elec_p.get_SOC());
            sol.update_x_n(m_b_cell.elec_n.get_SOC());

            sol.update_OCV_LIB(term_V_and_bool.first.OCV_LIB);
            sol.update_overpotential_elec_p(term_V_and_bool.first.elec_p);
            sol.update_overpotential_elec_n(term_V_and_bool.first.elec_n);
            sol.update_overpotential_R_cell(term_V_and_bool.first.R_cell);
            sol.update_overpotential_electrolyte(term_V_and_bool.first.electrolyte);

            time_index += 1;
        }
    }

    end = clock();
    // const std::clock_t c_end = std::clock();
    // std::time_t time_end = std::time(NULL);
    // const auto t_end = std::chrono::high_resolution_clock::now();

    std::cout << std::fixed << std::setprecision(10) << "Solution time: " << double(end - start) / double(CLOCKS_PER_SEC) << "s" << std::endl;

    return sol;
}