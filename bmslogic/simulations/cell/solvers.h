#ifndef SPCPP_PROJECT_SOLVERS_H
#define SPCPP_PROJECT_SOLVERS_H

#include <string>
#include <vector>

#include "extern/owl.h"
#include "battery_components.h"
#include "cyclers.h"
#include "solution.h"
#include "coords.h"

/// ECM Models

/**
 * @brief Base solver for the equivalent circuit model (ECM)
 *
 */
class BaseECMSolver
{
public:
    BaseECMSolver(ECMBatteryCell i_b_cell, bool i_isothermal) : m_b_cell(i_b_cell), m_isothermal(i_isothermal) {}

protected:
    ECMBatteryCell m_b_cell;
    bool m_isothermal;
};

/**
 * @class ESCDTSolver
 * @brief Solver for discrete solver for enhanced self correcting equivalent circuit model
 */
class ESCDTSolver : public BaseECMSolver
{
public:
    ESCDTSolver(ECMBatteryCell i_b_cell, bool i_isothermal) : BaseECMSolver(i_b_cell, i_isothermal) {}
    ECMSolution solve(BaseCycler cycler, double dt);

    // private:
    //     ECMBatteryCell m_b_cell;
    //     bool m_isothermal;
};

/// @brief Degradation solvers
class ROMSEISolver
{
public:
    ROMSEISolver(double i_k, double i_c_e, double i_S, double i_c_s_max, double i_U_s, double i_j_0_s, double i_A,
                 double i_MW_SEI, double i_rho, double i_kappa);
    // getters
    double get_k() { return m_k; }
    double get_c_e() { return m_c_e; }
    double get_S() { return m_S; }
    double get_c_s_max() { return m_c_s_max; }
    double get_U_s() { return m_U_s; }
    double get_j_0_s() { return m_j_0_s; }
    double get_A() { return m_A; }
    double get_MW() { return m_MW_SEI; }
    double get_rho() { return m_rho; }
    double get_kappa() { return m_kappa; }
    double get_cumulative_j_s() { return m_cumulative_j_s; }
    double get_L_SEI() { return m_L_SEI; }

    // calculation methods
    double solve_current(double soc_n, double ocp_n, double temp, double i_app, double relative_tolerance, int max_iter);
    double solve_delta_L(double j_s, double dt);
    void update_L(double j_s, double dt) { m_L_SEI += solve_delta_L(j_s, dt); }

private:
    double m_k;       // rate of reaction at the negative electrode [m2.5/mol0.5/s]
    double m_c_e;     // electrolyte conc. [mol/m3]
    double m_S;       // electrode electrochemical area [mol/m2]
    double m_c_s_max; // max. electrode conc. [mol/m3]
    double m_U_s;     // side-reaction open-circuit potential [V]
    double m_j_0_s;   // exchange current density of the side reaction [mol/m2/s]
    double m_A;       // electrode Area [m2]
    double m_MW_SEI;  // molar weight of SEI [g/mol]
    double m_rho;     // SEI density [g/m3]
    double m_kappa;   // SEI conductivity [S/m]

    double m_j_s = 0.0;            // side-reaction molar flux [mol/m2/s]
    double m_cumulative_j_s = 0.0; // cumlative side reaction flux [mol/m2/s]
    double m_L_SEI = 0.0;          // represents the SEI thickness [m]
};

/// @brief Thermal Solvers
class LumpedThermalSolver
{
public:
    LumpedThermalSolver(double i_h, double i_A, double i_rho, double i_vol, double i_C_p, double i_temp_init);
    // Calculation methods below
    double reversible_heat(double dOCPdT_p, double dOCPdT_n, double I, double T);
    double irreversible_heat(double OCP_p, double OCP_n, double I, double V);
    double heat_transfer(double T, double T_amb);
    double solve_temp(double dt, double t_prev, double I, double V, double temp_amb,
                      double OCP_p, double OCP_n, double dOCPdT_p, double dOCPdT_n);
    // getters
    double get_temp_init() { return m_temp_init; }
    double get_temp() { return m_temp; }
    double get_temp_prev() { return m_temp_prev; }

private:
    double m_temp_init;
    double m_temp;
    double m_temp_prev;

    double m_h;
    double m_A;
    double m_rho;
    double m_vol;
    double m_C_p;
};

/**
 * @brief Lithium-ion concentration solver in the solid electrode region.
 *
 */

class BaseConcSolver
{
public:
    explicit BaseConcSolver(char electrode_type);
    // getter functions
    char &get_electrodeType() { return m_electrode_type; }

protected:
    char m_electrode_type;
};

class PolynomialApprox : public BaseConcSolver
{
public:
    PolynomialApprox(char electrodeType, double i_c_init, std::string type);
    // getter functions
    std::string get_solver_type() const { return m_type; }
    double &get_c_surf() { return m_c_surf; }
    double get_x_surf(double c_s_max) const { return m_c_surf / c_s_max; }
    // helper functions
    void solve(double dt, double t_prev, double i_app, double R, double S, double D);

private:
    std::string m_type;
    double m_c_s_avg_prev;
    double m_c_surf;
    double m_q; // used for higher order approximations
    // helper funcs
    double solve_c_s_avg(double dt, double t_prev, double j, double R, double D);
    double solve_q(double dt, double t_prev, double j, double R, double D);
};

/**
 * @brief
 *   This solver uses the Eigen Function Expansion method as detailed in ref 1 to calculate the electrode
 *   surface SOC. As such, it stores all the necessary variables required for the iterative calculations for all time
 *   steps. After initiating the class, the object instance can be called iteratively to solve for electrode surface SOC
 *   for all time steps.
 *
 *   The equation solved is
 *      x_j_surf = x_ini + (1/5)*j_scaled + 3 * integration{D_sj * j_scaled / R_j ** 2} * dt +
 *                  summation{u_jk - 2 * scaled_j / lambda_k ** 2}
 * In the above equation, the integration is performed from t=0 to the current time. Moreover, the summation is
 *  performed from k=1 to k=N. Here k represents the kth term of the solution series.
 *
 *  Reference:
 * 1. Guo, M., Sikha, G., & White, R. E. (2011). Single-Particle Model for a Lithium-Ion Cell: Thermal Behavior.
 * Journal of The Electrochemical Society, 158(2), A122. https://doi.org/10.1149/1.3521314/XML
 *  """
 *
 */
class EigenSolver : public BaseConcSolver
{
public:
    EigenSolver(char i_electrode_type, double i_soc_init, int i_num_roots);
    // getters
    std::vector<double> get_roots() const { return m_roots; }
    double get_integ_term() { return m_integ_term; }
    std::vector<double> get_vec_u_k() { return m_vec_u_k; }
    // calculations
    double j_scaled(double i_app, double R, double S, double D_s, double c_s_max);
    void update_integ_term(double dt, double i_app, double R, double S, double D_s, double c_s_max);
    double du_kdt(double root, double D, double R, double scaled_j, double t, double u);
    double solve_u_k(double roots, double t_prev, double dt, double u_k_prev, double i_app, double R, double S, double D_s, double c_s_max);
    void update_vec_u_k(double dt, double t_prev, double i_app, double R, double S, double D_s, double c_s_max);
    double get_summation_term(double dt, double t_prev, double i_app, double R, double S, double D_s, double c_s_max);
    double solve(double dt, double t_prev, double i_app, double R, double S, double D_s, double c_s_max);

private:
    char m_electrode_type;
    int m_num_roots;
    OWL::MatrixXD m_lambda_bounds;
    std::vector<double> m_roots;
    double m_soc_init;
    double m_integ_term;
    std::vector<double> m_vec_u_k;
};

double lambda_function(double lambda_k);

/**
 * @brief This class uses the Crank Nicolson method for numerically calculating the electrode Li-ion concentration during battery operations.
 *
 */
class CNSolver : public BaseConcSolver
{
public:
    CNSolver(double i_c_init, char i_electrode_type, int i_spatial_grid_points);

    // getter functions
    char get_electrode_type() { return m_electrode_type; }
    int get_spatial_pts() { return m_K; }
    double get_c_s_surf() { return m_c_prev[m_c_prev.size() - 1]; }
    std::vector<double> get_c_prev() { return m_c_prev; }
    double get_c_surf() { return m_c_surf; }

    // calculation functions
    double calc_A(double dt, double R, double D) { return A(dt, R, D); }
    double calc_B(double dt, double R, double D) { return B(dt, R, D); }
    void solve(double dt, double i_app, double R, double S, double D);

private:
    int m_K;
    std::vector<double> m_c_prev;
    double m_c_surf;

    double dr(double R) { return R / m_K; };
    double A(double dt, double R, double D) { return dt * D / std::pow(dr(R), 2); }
    double B(double dt, double R, double D) { return dt * D / (2 * dr(R)); };

    std::vector<double> array_R(double R);
    std::vector<double> LHS_diag_elements(double dt, double R, double D);
    std::vector<double> LHS_lower_diag_elements(double dt, double R, double D);
    std::vector<double> LHS_upper_diag_elements(double dt, double R, double D);
    std::vector<double> RHS_vector(double j, double dt, double R, double D);
};

/*
 * Lithium-Ion Concentration Solver in the Electrolyte
 */
class ElectrolyteFVMSolver
{
public:
    ElectrolyteFVMSolver(ElectrolyteFVMCoordinates i_coords, double i_c_e_init, double i_t_c,
                         double i_epsilon_e_n, double i_epsilon_e_sep, double i_epsilon_e_p,
                         double i_a_s_n, double i_a_s_p,
                         double i_D_e, double i_brugg);
    ElectrolyteFVMCoordinates get_coords() const { return m_coords; }

    // getter functions
    double get_t_c() const { return m_t_c; }
    double get_c_e_init() const { return m_c_e_init; }
    double get_epsilon_e_n() const { return m_epsilon_e_n; }
    double get_epsilon_e_sep() const { return m_epsilon_e_sep; }
    double get_epsilon_e_p() const { return m_epsilon_e_p; }
    double get_a_s_n() const { return m_a_s_n; }
    double get_a_s_p() const { return m_a_s_p; }
    double get_D_e() const { return m_D_e; }
    double get_brugg() const { return m_brugg; }
    std::vector<double> get_vector_c_e() const { return m_vector_c_e; }
    std::vector<double> get_vector_a_s() const { return m_vector_a_s; }
    std::vector<double> get_vector_D_eff() const { return m_vector_D_eff; }
    std::vector<double> get_vector_epsilon_e() const { return m_vector_epsilon_e; }
    const std::vector<double> get_calc_lower_diag(double &dt) { return calc_lower_diag(dt); }
    const std::vector<double> get_calc_diag(double &dt) { return calc_diag(dt); }
    const std::vector<double> get_calc_upper_diag(double &dt) { return calc_upper_diag(dt); }
    const std::vector<double> get_vec_ce_j(std::vector<double> &c_prev, std::vector<double> &j, double &dt) { return calc_vector_ce_j(c_prev, j, dt); }

    // setter functions
    void set_vector_c_e(std::vector<double> &i_vector_c_e) { m_vector_c_e = i_vector_c_e; }

    // functions for calculations
    std::vector<double> calc_lower_diag(double &dt);
    std::vector<double> calc_diag(double &dt);
    std::vector<double> calc_upper_diag(double &dt);

    std::vector<double> calc_vector_ce_j(std::vector<double> &c_prev, std::vector<double> &j, double &dt);

    void solve(std::vector<double> j, double dt);

private:
    ElectrolyteFVMCoordinates m_coords;
    double m_t_c;
    double m_c_e_init;
    double m_epsilon_e_n;
    double m_epsilon_e_sep;
    double m_epsilon_e_p;
    double m_a_s_n;
    double m_a_s_p;
    double m_D_e;
    double m_brugg;

    std::vector<double> m_vector_c_e;
    std::vector<double> m_vector_epsilon_e;
    std::vector<double> m_vector_D_eff;
    std::vector<double> m_vector_a_s;
};

/*
 * Battery Solvers below
 */

class BaseBatterySolver
{
public:
    BaseBatterySolver(BatteryCell i_b_cell, bool i_isothermal, bool i_degradation, std::string i_electrode_SOC_solver);
    BatteryCell m_b_cell;
    bool m_isothermal;
    bool m_degradation;
    std::string m_electrode_SOC_solver;
};

class BatterySolver : public BaseBatterySolver
{
public:
    explicit BatterySolver(BatteryCell i_b_cell, bool i_isothermal, bool i_degradation, std::string i_electrode_SOC_solver);
    // Solvers instances
    PolynomialApprox SOC_solver_p;
    PolynomialApprox SOC_solver_n;
    LumpedThermalSolver thermal_solver;
    // Calculation functions
    Solution solve(BaseCycler i_cycler);
    // Solution solve(DischargeRest i_cycler);

private:
    double calc_V(double I);
    double calc_T(double I, double V);
    double solve_one_iteration(double t_prev, double dt, double I);
};

// class ESPBatterySolver : public BaseBatterySolver
// {
// public:
//     explicit ESPBatterySolver(BatteryCell i_b_cell, bool i_isothermal, bool i_degradation, std::string i_electrode_SOC_solver);
//     // Solvers instances
//     PolynomialApprox SOC_solver_p;
//     PolynomialApprox SOC_solver_n;
//     LumpedThermalSolver thermal_solver;
//     ElectrolyteFVMCoordinates electrolyte_coords;
//     ElectrolyteFVMSolver electrolyte_solver;

// private:
//     double calc_V();
//     double solve_one_iteration(double t_prev, double dt, double i_app, double temp);
// };

#endif // SPCPP_PROJECT_SOLVERS_H