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
#include <tuple>

/// @brief contains the general battery-related equations
namespace general_equations
{
    double delta_cap(double Q, double I, double dt);
    double calc_cap(double cap_prev, double Q, double I, double dt);
    double calc_i_0(double k, double c_s_max, double soc, double c_e);
    double molar_flux_to_current(double &molar_flux, double &S, char electrode_type);
}

/**
 * @brief     This class creates a first order Thevenin model object for a lithium-ion battery cell. It contains relevant model
 * parameters as class attributes and methods to calculate SOC and terminal voltage.
 *
 * Thevenin first order model is a phenomenological model that can be used to simulate the terminal voltage across a
 * lithium-ion battery cell. It has representative electrical components that represent the open-circuit voltage,
 * internal resistance, and diffusion voltages. The set of differential and algebraic equations are:

 * dz/dt = -eta(t) * i_app(t) / capacity
 * di_R1/dt = -i_R1/(R1*C1) + i_app(t)/(R1*C1)
 * v(t) = OCV(z(t)) - R1*i_R1(t) - R0*i_app(t)

 * Where the second equation is a non-homogenous linear first-order differential equation. Furthermore, the variables
 * are:
 * z: state of charge (SOC)
 * R0: resistance of the resistor that represents the battery cell's internal resistance
 * R1: resistance of the resistor in the RC pair.
 * C1: capacitance of the capacitor in the RC pair.
 * i_R1: current through R1
 * i_app: applied current
 * eta: Colombic efficiency

 * Note that the RC pair represents the diffusion voltage in the battery cell.


 * After time discretization, the set of algebraic equations are:

 * z[k+1] = z[k] - delta_t*eta[k]*i_app[k]/capacity
 * i_R1[k+1] = exp(-delta_t/(R1*C1))*i_R1[k] + (1-exp(-delta_t/(R1*C1))) * i_app[k]
 * v[k] = OCV(z[k]) - R1*i_R1[k] - R0*i_app[k]

 * Where k represents the time-point and delta_t represents the time-step between z[k+1] and z[k].

 * Code Notes:
 * 1. It is assumed for now that eta is a function of applied current only.
 * 2. Discharge currrent is positve and charge current is negative by convention.

 * Reference:
 * Hariharan, K. S. (2013). A coupled nonlinear equivalent circuit – Thermal model for lithium ion cells.
 * In Journal of Power Sources (Vol. 227, pp. 171–176). Elsevier BV.
 * https://doi.org/10.1016/j.jpowsour.2012.11.044
 *
 */
class Thevenin1RC
{
public:
    Thevenin1RC() = default;
    ~Thevenin1RC() = default;
    double soc_next(double dt, double i_app, double soc_prev, double Q, double eta) { return soc_prev - dt * eta * i_app / (3600 * Q); }
    double i_R1_next(double dt, double i_app, double i_R1_prev, double R1, double C1) { return std::exp(-dt / (R1 * C1)) * i_R1_prev + (1 - std::exp(-dt / (R1 * C1))) * i_app; }
    double V(double i_app, double ocv, double R0, double R1, double i_R1) { return ocv - R1 * i_R1 - R0 * i_app; }
};

/**
 * @brief     Class oject contains the relevant functions to perform the Enhanched-self-correcting ECM model.
 *
 * Notes:
 *      The discharge current is assumed to be positive values. Meanwhile, the charge current is negative by convention.
 *
 */
class ESC
{
public:
    ESC() = default;
    ~ESC() = default;

    // helper functions
    int sign(double &i_number);
    int sign(int &i_number);
    double s(double &i_app, double &s_prev);
    double soc_next(double dt, double i_app, double soc_prev, double Q, double eta) { return soc_prev - dt * eta * i_app / (3600 * Q); }
    double i_R1_next(double dt, double i_app, double i_R1_prev, double R1, double C1) { return std::exp(-dt / (R1 * C1)) * i_R1_prev + (1 - std::exp(-dt / (R1 * C1))) * i_app; }
    double h_next(double dt, double i_app, double eta, double gamma, double cap, double h_prev);
    double v(double i_app, double ocv, double R0, double R1, double i_R1, double m_0, double m, double h, double s_prev);
};

struct OverPotentials
{
    double V;
    double OCV_LIB;
    double elec_p;
    double elec_n;
    double R_cell;
    double electrolyte;
};

/**
 * @class SPModel
 * @brief Equations for the single particle model
 *
 */
class SPModel
{
public:
    static double molar_flux_electrode(double &I, double &S, char &electrode_type);
    double m(double I, double k, double S, double c_max, double SOC, double c_e);
    double calc_terminal_V(double OCP_p, double OCP_n, double m_p, double m_n, double R_cell, double T, double I);
    OverPotentials calc_overpotentials(double OCP_p, double OCP_n, double m_p, double m_n, double R_cell, double T, double I);
};

/**
 * @brief contains equations for the Enhanced single particle models.
 *
 */

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
    OverPotentials calc_overpotentials(double ocp_p, double ocp_n, double m_p, double m_n,
                                       double L_n, double L_sep, double L_p,
                                       double kappa_eff_avg, double k_f_avg, double t_c, double R_cell,
                                       double c_e_n, double c_e_p,
                                       double temp, double i_app);
};

/**
 * @class ROMSEI
 * @brief This class contains the equations for the reduced order SEI growth model as mentioned in ref [1], with slight
 * modifications.
 *
 *  * Literature Reference:
 *      1. Randell et al. "Controls oriented reduced order modeling of solid-electrolyte interphase layer growth". 2012.
 *          Journal of Power Sources. Vol: 209. pgs: 282-288.
 */
class ROMSEI
{
public:
    ROMSEI() = default;
    ~ROMSEI() = default;
    
    // calculation methods
    double calc_j_i(double j_tot, double j_s);
    double calc_eta_n(double temp, double j_i, double i_0);
    double calc_eta_s(double eta_n, double OCP_n, double OCP_s);
    double calc_j_s(double temp, double i_0_s, double eta_s);
};

#endif // BMSLOGIC_PROJECT_MODELS_H
