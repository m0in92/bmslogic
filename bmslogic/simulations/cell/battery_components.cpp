/**
 * @file battery_components.cpp
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief Contains the classes and functionalities pertaining to the storage of battery parameters.
 * @version 0.1
 * @date 2024-05-03
 *
 * @copyright Copyright (c) 2024
 *
 */

#include <cmath>

#include "battery_components.h"
#include "common_includes.h"

Electrode::Electrode(double L_i, double A_i, double kappa_i, double epsilon_i, double max_conc_i, double R_i, double S_i,
                     double T_ref_i, double D_ref_i, double k_ref_i, double Ea_D_i, double Ea_R_i, double alpha_i,
                     double brugg_i, double SOC_i, double T_i,
                     std::function<double(double)> func_OCP_i, std::function<double(double)> func_dOCPdT_i)
{
    L = L_i;
    A = A_i;
    kappa = kappa_i;
    epsilon = epsilon_i;
    max_conc = max_conc_i;
    R = R_i;
    S = S_i,
    T_ref = T_ref_i;
    D_ref = D_ref_i;
    k_ref = k_ref_i;
    Ea_D = Ea_D_i;
    Ea_R = Ea_R_i;
    alpha = alpha_i;
    brugg = brugg_i;
    SOC_init = SOC_i;
    SOC = SOC_i; // initial condition
    T = T_i;     // initial condition

    func_OCP = func_OCP_i;
    func_dOCPdT = func_dOCPdT_i;
}

/**
 * calc_OCP
 *
 * Calculates the electrode's open-circuit potential [V]
 *
 * Parameters:
 *     None
 *
 * Return:
 *     (double) electrode open-circuit potential [V]
 * */
double Electrode::calc_OCP()
{
    return func_OCP(SOC) + func_dOCPdT(SOC) * (T - T_ref);
}

/**
 * calc_D
 *
 * calculates and returns the electrode diffusivity [m2/s]
 *
 * Parameters:
 *     None
 *
 * Return:
 *     (double) electrode diffusivity [m2/s]
 * */
double Electrode::calc_D()
{
    return D_ref * std::exp(-1 * Ea_D / Constants.R * (1 / T - 1 / T_ref));
}

/**
 * calc_k
 *
 * calculates and returns the reaction rate [m2.5 / (mol0.5 s)
 *
 * Parameters:
 *     None
 *
 * Return:
 *     (double) electrode reaction rate [m2.5/mol0.5/s]
 *
 * */
double Electrode::calc_k()
{
    return k_ref * std::exp(Ea_R / Constants.R * (1 / T_ref - 1 / T));
}

PElectrode::PElectrode(double L_i, double A_i, double kappa_i, double epsilon_i, double max_conc_i, double R_i, double S_i,
                       double T_ref_i, double D_ref_i, double k_ref_i, double Ea_D_i, double Ea_R_i, double alpha_i,
                       double brugg_i, double SOC_i, double T_i,
                       std::function<double(double)> func_OCP_i, std::function<double(double)> func_dOCPdT_i) : Electrode(L_i, A_i, kappa_i, epsilon_i, max_conc_i, R_i, S_i, T_ref_i, D_ref_i, k_ref_i,
                                                                                                                          Ea_D_i, Ea_R_i, alpha_i, brugg_i, SOC_i, T_i, func_OCP_i, func_dOCPdT_i)
{
}

/**
 * NElectrode
 *
 * Constructor class for the negative electrode class.
 *
 * Parameters:
 *     parameters pertaining to the negative electrode.
 *
 * Returns:
 *     None
 *
 * */
NElectrode::NElectrode(double L_i, double A_i, double kappa_i, double epsilon_i, double max_conc_i, double R_i,
                       double S_i, double T_ref_i, double D_ref_i, double k_ref_i, double Ea_D_i, double Ea_R_i,
                       double alpha_i, double brugg_i, double SOC_i, double T_i,
                       std::function<double(double)> func_OCP_i, std::function<double(double)> func_dOCPdT_i) : Electrode(L_i, A_i, kappa_i, epsilon_i, max_conc_i, R_i, S_i, T_ref_i, D_ref_i, k_ref_i,
                                                                                                                          Ea_D_i, Ea_R_i, alpha_i, brugg_i, SOC_i, T_i, func_OCP_i, func_dOCPdT_i)
{
}

Electrolyte::Electrolyte(double conc_i, double L_i, double kappa_i, double epsilon_i, double brugg_i)
{
    conc = conc_i;
    L = L_i;
    kappa = kappa_i;
    epsilon = epsilon_i;
    brugg = brugg_i;
}

Electrolyte::Electrolyte(double conc_i, double L_i, double kappa_i, double i_epsilon_n, double epsilon_i, double i_epsilon_p,
                         double i_D_e, double i_t_c, double brugg_i)
{
    conc = conc_i;
    L = L_i;
    kappa = kappa_i;
    epsilon = epsilon_i;
    epsilon_n = i_epsilon_n;
    epsilon_p = i_epsilon_p;
    D_e = i_D_e;
    t_c = i_t_c;
    brugg = brugg_i;
}

BatteryCell::BatteryCell(PElectrode i_elec_p, NElectrode i_elec_n, Electrolyte i_electrolyte, double i_rho, double i_Vol,
                         double i_C_p, double i_h, double i_A, double i_cap, double i_V_max, double i_V_min,
                         double i_R_cell) : elec_p(i_elec_p), elec_n(i_elec_n), electrolyte(i_electrolyte)
{
    rho = i_rho;
    Vol = i_Vol;
    C_p = i_C_p;
    h = i_h;
    A = i_A;
    cap = i_cap;
    V_max = i_V_max;
    V_min = i_V_min;
    R_cell = i_R_cell;
    T = elec_n.get_T();
}

BatteryCell::BatteryCell(double L_p, double A_p, double kappa_p, double epsilon_p, double max_conc_p, double R_p, double S_p,
                         double T_ref_p, double D_ref_p, double k_ref_p, double Ea_D_p, double Ea_R_p, double alpha_p,
                         double brugg_p, double SOC_p, double T_p, std::function<double(double)> func_OCP_p, std::function<double(double)> func_dOCPdT_p,
                         double c_e, double L_s, double kappa_s, double epsilon_s, double brugg_s,
                         double L_n, double A_n, double kappa_n, double epsilon_n, double max_conc_n, double R_n, double S_n,
                         double T_ref_n, double D_ref_n, double k_ref_n, double Ea_D_n, double Ea_R_n, double alpha_n,
                         double brugg_n, double SOC_n, double T_n, std::function<double(double)> func_OCP_n, std::function<double(double)> func_dOCPdT_n,
                         double i_rho, double i_Vol,
                         double i_C_p, double i_h, double i_A, double i_cap, double i_V_max, double i_V_min, double i_R_cell) : elec_p(L_p, A_p, kappa_p, epsilon_p, max_conc_p, R_p, S_p, T_ref_p, D_ref_p,
                                                                                                                                       k_ref_p, Ea_D_p, Ea_R_p, alpha_p, brugg_p, SOC_p, T_p,
                                                                                                                                       func_OCP_p, func_dOCPdT_p),
                                                                                                                                electrolyte(c_e, L_s, kappa_s, epsilon_s, brugg_s),
                                                                                                                                elec_n(L_n, A_n, kappa_n, epsilon_n, max_conc_n, R_n, S_n, T_ref_n, D_ref_n,
                                                                                                                                       k_ref_n, Ea_D_n, Ea_R_n, alpha_n, brugg_n, SOC_n, T_n,
                                                                                                                                       func_OCP_n, func_dOCPdT_n)
{
    rho = i_rho;
    Vol = i_Vol;
    C_p = i_C_p;
    h = i_h;
    A = i_A;
    cap = i_cap;
    V_max = i_V_max;
    V_min = i_V_min;
    R_cell = i_R_cell;
    T = elec_n.get_T();
}

ECMBatteryCell::ECMBatteryCell(double i_R0_ref, double i_R1_ref, double i_C1, double i_temp_ref, double i_Ea_R0, double i_Ea_R1,
                               double i_rho, double i_vol, double i_c_p, double i_h, double i_area, double i_cap, double i_V_max, double i_V_min,
                               double i_soc_init, double i_temp_init,
                               std::function<double(double)> i_func_eta, std::function<double(double)> i_func_ocv, std::function<double(double)> i_func_docvdtemp,
                               double i_M_0, double i_M, double i_gamma) : m_R0_ref(i_R0_ref), m_R1_ref(i_R1_ref), m_C1(i_C1), m_temp_ref(i_temp_ref),
                                                                           m_Ea_R0(i_Ea_R0), m_Ea_R1(i_Ea_R1), m_rho(i_rho), m_vol(i_vol), m_c_p(i_c_p), m_h(i_h), m_area(i_area), m_cap(i_cap),
                                                                           m_v_max(i_V_max), m_v_min(i_V_min), m_soc_init(i_soc_init), m_temp_init(i_temp_init),
                                                                           m_func_eta(i_func_eta), m_func_ocv(i_func_ocv), m_func_docvdtemp(i_func_docvdtemp),
                                                                           m_M_0(i_M_0), m_M(i_M), m_gamma(i_gamma)
{
    m_soc = m_soc_init;
    m_temp = m_temp_init;
}

double ECMBatteryCell::calc_R0()
{
    return m_R0_ref * std::exp(-1 * m_Ea_R0 / Constants.R * (1 / m_temp - 1 / m_temp_ref));
}

double ECMBatteryCell::calc_R1()
{
    return m_R1_ref * std::exp(-1 * m_Ea_R1 / Constants.R * (1 / m_temp - 1 / m_temp_ref));
}