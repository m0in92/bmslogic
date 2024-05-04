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
#include "calc_helpers/constants.h"

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
