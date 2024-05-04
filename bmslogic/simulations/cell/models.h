/**
 * @file models.h
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief Contains the class declarations for the relevant models. These classes are generally intended to contain
 * simulation equations in their methods. These equations are used by the relevant solvers during the simulation runs.
 * @version 0.1
 * @date 2024-05-04
 * 
 * @copyright Copyright (c) 2024
 * 
 */

#ifndef BMSLOGIC_PROJECT_MODELS_H
#define BMSLOGIC_PROJECT_MODELS_H

#include <string>
#include <cmath>

/// @brief contains the general battery-related equations
namespace general_equations
{
    double delta_cap(double Q, double I, double dt);
    double calc_cap(double cap_prev, double Q, double I, double dt);
    double calc_i_0(double k, double c_s_max, double soc, double c_e);
    double molar_flux_to_current(double &molar_flux, double &S, char electrode_type);
}

class SPModel
{
public:
    static double molar_flux_electrode(double &I, double &S, char &electrode_type);
    double m(double I, double k, double S, double c_max, double SOC, double c_e);
    double calc_terminal_V(double OCP_p, double OCP_n, double m_p, double m_n, double R_cell, double T, double I);
};

namespace ESPModel
{
    double molar_flux_electrode(double &i_app, double S, char electrode_type);
    double a_s(double epsilon, double R);
    double i_0(double k, double c_s_max, double c_e, double soc_surf);
    double m(double i_app, double k, double S, double c_s_max, double c_e, double soc_surf);
    double calc_terminal_voltage(double ocp_p, double ocp_n, double m_p, double m_n,
                                 double L_n, double L_sep, double L_p,
                                 double kappa_eff_avg, double k_f_avg, double t_c, double R_cell,
                                 double c_e_n, double c_e_p,
                                 double temp, double i_app);
};

/**
 * This class contains the equations for the reduced order SEI growth model as mentioned in ref [1], with slight
 * modifications.
 *
 * Literature Reference:
 * 1. Randell et al. "Controls oriented reduced order modeling of solid-electrolyte interphase layer growth". 2012.
 * Journal of Power Sources. Vol: 209. pgs: 282-288.
 */
class ROMSEI
{
public:
    ROMSEI() = default;
    double calc_j_i(double j_tot, double j_s);
    double calc_eta_n(double temp, double j_i, double i_0);
    double calc_eta_s(double eta_n, double OCP_n, double OCP_s);
    double calc_j_s(double temp, double i_0_s, double eta_s);
};

#endif // BMSLOGIC_PROJECT_MODELS_H
