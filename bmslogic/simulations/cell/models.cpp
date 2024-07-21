/**
 * @file models.cpp
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief Contains the class declarations for the relevant models. These classes are generally intended to contain
 * simulation equations in their methods. These equations are used by the relevant solvers during the simulation runs.
 * @version 0.1
 * @date 2024-05-04
 *
 * @copyright Copyright (c) 2024
 *
 */

#include <cmath>

#include "models.h"
#include "common_includes.h"
#include "extern/owl.h"

/**
 * @brief the capacity increment
 *
 * @param Q Nomainl battery capacity [A hr]
 * @param I Battery current [A]
 * @param dt Time increment [s]
 * @return double
 */
double general_equations::delta_cap(double Q, double I, double dt)
{
    return (1.0 / 3600.0) * std::abs(I) * dt / Q;
}

/**
 * @brief calculates the battery capacity [A hr]
 *
 * @param cap_prev Battery capacity at the previous time step
 * @param Q Nominal battery capacity [Ahr]
 * @param I current [A]
 * @param dt time increment [s]
 * @return double
 */
double general_equations::calc_cap(double cap_prev, double Q, double I, double dt)
{
    return cap_prev + general_equations::delta_cap(Q, I, dt);
}

/**
 * @brief Calculates the exchange current density [mol/m2/s] for charge-transfer reactions at the
 * electrode-electrolyte interface.
 *
 * @param k rate constant m^2.5/mol^0.5/s
 * @param c_s_max max. lithium-ion concentration at the electrode [mol/m3]
 * @param soc state of charge of the electrode
 * @param c_e lithium-ion concentration in the electrolyte [mol/m3]
 * @return double exchange current density [mol/m2/s]
 */
double general_equations::calc_i_0(double k, double c_s_max, double soc, double c_e)
{
    return k * c_s_max * std::pow(c_e, 0.5) * std::pow((1 - soc), 0.5) * std::pow(soc, 0.5);
}

double general_equations::molar_flux_to_current(double &molar_flux, double &S, char electrode_type)
{
    char positive_electrode_char = 'p';
    if (electrode_type == positive_electrode_char)
        return molar_flux * Constants.F * S;
    else if (electrode_type == 'n')
        return -molar_flux * Constants.F * S;
    else
        throw std::invalid_argument("invalid electrode_type argument");
}

int ESC::sign(int &number)
{
    if (number < 0)
        return -1;
    else if (number == 0)
        return 0;
    else
        return 1;
}

int ESC::sign(double &number)
{
    if (number < 0.0)
        return -1;
    else if (number == 0.0)
        return 0;
    else
        return 1;
}

double ESC::s(double &i_app, double &s_prev)
{
    if (std::abs(i_app) > 0)
        return ESC::sign(i_app);
    else
        return s_prev;
}

double ESC::h_next(double dt, double i_app, double eta, double gamma, double cap, double h_prev)
{
    double exp_term = std::exp(-std::abs((eta * i_app * gamma * dt) / (3600 * cap)));
    return exp_term * h_prev - (1 - exp_term) * sign(i_app);
}

double ESC::v(double i_app, double ocv, double R0, double R1, double i_R1, double m_0, double m, double h, double s_prev)
{
    return ocv - R1 * i_R1 - R0 * i_app + m * h + m_0 * s(i_app, s_prev);
}

/**
 * molar_flux_electrode
 *
 * Calculates the molar flux into the electrode [mol/m2/s].
 *
 * Parameters:
 *     I: (double) applied current [A]
 *     S: (double) electro-active electrode area [m2]
 *     electrode_type: (char) electrode type
 *
 * Returns:
 *     (double) molar area flux [mol/m2/s]
 * */
double SPModel::molar_flux_electrode(double &I, double &S, char &electrode_type)
{
    if (electrode_type == 'p')
        return I / (Constants.F * S); // molar flux [mol/m2/s]
    else if (electrode_type == 'n')
        return -I / (Constants.F * S); // molar flux [mol/m2/s]
    else
        throw std::invalid_argument("Electrode type values must be 'p' or 'n'.");
}

/**
 * m
 *
 * Calculates the intermediary variable in the single particle model.
 *
 * Parameters:
 *     (double) I: applied current [A]
 *     (double) k: reaction rate [m2.5/mol0.5/s]
 *     (double) c_max: max. conc [mol/m3]
 *     (double) SOC: electrode SOC
 *     (double) c_e: electrolyte conc. [mol/m3]
 *
 * Return:
 *     (double) m
 * */
double SPModel::m(double I, double k, double S, double c_max, double SOC, double c_e)
{
    return I / (Constants.F * k * S * c_max * std::pow(c_e, 0.5) * std::pow((1 - SOC), 0.5) * std::pow(SOC, 0.5));
}

/**
 * calc_terminal_V
 *
 * Calculates the cell terminal potential [V]
 *
 * Parameters:
 *     OCP_p: (double) positive eletrode's OCP
 *     OCP_n: (double) negative electrode's OCP
 *     m_n: (double) negative electrode's m
 *     m_p: (double) positive electrode's m
 *     R_cell (double): battery cell's internal resistance [ohm]
 *     T: (double) battery cell's internal resistance
 *     I: (double) applied current [A]
 *
 * Returns:
 *     (double) battery cell's terminal voltage
 * */
double SPModel::calc_terminal_V(double OCP_p, double OCP_n, double m_p, double m_n, double R_cell, double T, double I)
{
    double V = OCP_p - OCP_n;
    V += (2 * Constants.R * T / Constants.F) * std::log((std::sqrt(std::pow(m_p, 2) + 4) + m_p) / 2);
    V += (2 * Constants.R * T / Constants.F) * std::log((std::sqrt(std::pow(m_n, 2) + 4) + m_n) / 2);
    V += I * R_cell;
    return V;
}

std::tuple<double, double, double, double, double> SPModel::calc_overpotentials(double OCP_p, double OCP_n, double m_p, double m_n, double R_cell, double T, double I)
{
    std::tuple<double, double, double, double, double> overpotentials;
    double OCV = OCP_p - OCP_n;
    double overpotential_elec_p = (2 * Constants.R * T / Constants.F) * std::log((std::sqrt(std::pow(m_p, 2) + 4) + m_p) / 2);
    double overpotential_elec_n = (2 * Constants.R * T / Constants.F) * std::log((std::sqrt(std::pow(m_n, 2) + 4) + m_n) / 2);
    double overpotential_R_cell = I * R_cell;
    double terminal_V = OCV + overpotential_elec_p + overpotential_elec_n + overpotential_R_cell;

    return std::tuple<double, double, double, double, double>{terminal_V, OCV, overpotential_elec_p, overpotential_elec_n, overpotential_R_cell};
}

namespace ESPModel
{
    double molar_flux_electrode(double &I, double S, char electrode_type)
    {
        if (electrode_type == 'p')
            return I / (Constants.F * S); // molar flux [mol/m2/s]
        else if (electrode_type == 'n')
            return -I / (Constants.F * S); // molar flux [mol/m2/s]
        else
            throw std::invalid_argument("electrode_type must be p or n");
    }

    double a_s(double epsilon, double R)
    {
        return 3 * epsilon / R;
    }

    /**
     * @brief Calculates the exchange current density for an electrode [mol/m2/s].
     *
     * @param k         rate constant [m2.5 / mol0.5 / s]
     * @param c_s_max   max. lithium-ion electrode conc. [mol/m3]
     * @param c_e       lithium-ion conc in the electrolyte [mol/m3]
     * @param soc_surf  state-of-charge of the electrode particle surface
     * @return double   exchange current density [mol/m2/s]
     */
    double i_0(double k, double c_s_max, double c_e, double soc_surf)
    {
        return k * c_s_max * std::pow(c_e, 0.5) * std::pow(1 - soc_surf, 0.5) * std::pow(soc_surf, 0.5);
    }

    double m(double i_app, double k, double S, double c_s_max, double c_e, double soc_surf)
    {
        return i_app / (Constants.F * S * i_0(k, c_s_max, c_e, soc_surf));
    }

    /**
     * @brief Returns the cell terminal voltage [V] according to Moura et al.
     *
     * @param ocp_p
     * @param ocp_n
     * @param m_p
     * @param m_n
     * @param L_n
     * @param L_sep
     * @param L_p
     * @param kappa_eff_avg
     * @param k_f_avg
     * @param t_c
     * @param R_cell
     * @param c_e_n
     * @param c_e_p
     * @param temp
     * @param i_app
     * @return double
     */
    double calc_terminal_voltage(double ocp_p, double ocp_n, double m_p, double m_n,
                                 double L_n, double L_sep, double L_p,
                                 double kappa_eff_avg, double k_f_avg, double t_c, double R_cell,
                                 double c_e_n, double c_e_p,
                                 double temp, double i_app)
    {
        double k_conc = (2 * Constants.R * temp / Constants.F) * (1 - t_c) * k_f_avg;
        double V = ocp_p - ocp_n;
        V += (2 * Constants.R * temp / Constants.F) * std::log((std::sqrt(std::pow(m_p, 2) + 4) + m_p) / 2);
        V += (2 * Constants.R * temp / Constants.F) * std::log((std::sqrt(std::pow(m_n, 2) + 4) + m_n) / 2);
        V += R_cell * i_app;
        V += (L_p + 2 * L_sep + L_n) * i_app / (2 * kappa_eff_avg);
        V += k_conc * (std::log(c_e_p) - std::log(c_e_n));

        return V;
    }

    OverPotentials calc_overpotentials(double ocp_p, double ocp_n, double m_p, double m_n,
                                       double L_n, double L_sep, double L_p,
                                       double kappa_eff_avg, double k_f_avg, double t_c, double R_cell,
                                       double c_e_n, double c_e_p,
                                       double temp, double i_app)
    {
        double k_conc = (2 * Constants.R * temp / Constants.F) * (1 - t_c) * k_f_avg;
        double OCV = ocp_p - ocp_n;
        double overpotential_elec_p = (2 * Constants.R * temp / Constants.F) * std::log((std::sqrt(std::pow(m_p, 2) + 4) + m_p) / 2);
        double overpotential_elec_n = (2 * Constants.R * temp / Constants.F) * std::log((std::sqrt(std::pow(m_n, 2) + 4) + m_n) / 2);
        double overpotential_R_cell = R_cell * i_app;
        double overpotential_electrolyte = (L_p + 2 * L_sep + L_n) * i_app / (2 * kappa_eff_avg);
        overpotential_electrolyte += k_conc * (std::log(c_e_p) - std::log(c_e_n));

        double V = OCV + overpotential_elec_p + overpotential_elec_n + overpotential_R_cell + overpotential_electrolyte;

        return {V, OCV, overpotential_elec_p, overpotential_elec_n, overpotential_R_cell, overpotential_electrolyte};
    }
}

/**
 * @brief Calculates the intercalation lithium molar flux density [mol/m2/s]
 *
 * @param j_tot total lithium molar flux density [mol/m2/s]
 * @param j_s lithium side-reaction flux density [mol/m2/s]
 * @return double intercalation lithium molar flux density [mol/m2/s]
 */
double ROMSEI::calc_j_i(double j_tot, double j_s)
{
    return j_tot - j_s;
}

/**
 * @brief Calculates the overpotential [V] at the electrode (most probably negative
 *  electrode) using the Butler Volmer equation
 *
 * @param temp electrode temperature [K]
 * @param j_i lithium molar flux density [mol/m2/s]
 * @param i_0 exchange current density of the intercalation charge-transfer reaction [mol/m2/s]
 * @return double overpotential at the electrode [V]
 */
double ROMSEI::calc_eta_n(double temp, double j_i, double i_0)
{
    return (2 * Constants.R * temp / Constants.F) * std::asinh(j_i / (2 * i_0));
}

/**
 * @brief Calculates the side reaction over-potential [V]
 *
 * @param eta_n Overpotential of the intercalation reaction [V]
 * @param OCP_n Open-circuit potential of the electrode [V]
 * @param OCP_s Open-circuit potential of the side-reaction [V]
 * @return double
 */
double ROMSEI::calc_eta_s(double eta_n, double OCP_n, double OCP_s)
{
    return eta_n + OCP_n - OCP_s;
}

/**
 * @brief Calculates the side reaction molar flux at the electrode-electrolyte interface.
 *
 * @param temp electrode temperature [K]
 * @param i_0_s exchange current density of the side reaction [mol/m2/s]
 * @param eta_s exhange current density of the side reaction [mol/m2/s]
 * @return double side reaction molar flux [mol/m2/s]
 */
double ROMSEI::calc_j_s(double temp, double i_0_s, double eta_s)
{
    return -i_0_s * std::exp(-Constants.F * eta_s / (2 * Constants.R * temp));
}
