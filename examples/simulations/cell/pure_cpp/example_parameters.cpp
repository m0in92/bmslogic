/**
 * @file example_parameters.cpp
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief contains the example parameters for the battery cell
 * @version 0.1
 * @date 2024-05-06
 * 
 * @copyright Copyright (c) 2024 by BMSLogic
 * 
 */

#include <cmath>
#include <functional>

/*
* Negative Electrode
*/
static double A_n = 0.0596;
static double L_n = 7.35e-5;
static double kappa_n = 100;
static double epsilon_n = 0.59;
static double S_n = 0.7824;
static double max_conc_n = 31833;
static double R_n = 12.5e-6;
static double k_ref_n = 1.76e-11;
static double D_ref_n = 3.9e-14;
static double Ea_R_n = 2e4;
static double Ea_D_n = 3.5e4;
static double T_ref_n = 298.15;
static double brugg_n = 1.5;
static double soc_min_n = 0.01890232;
static double soc_max_n = 0.7568;
static double alpha_n = 0.5;

// OCP functions
static double OCP_ref_n(double SOC)
{
    return 0.13966 + 0.68920 * std::exp(-49.20361 * SOC) + 0.41903 * std::exp(-254.40067 * SOC) - std::exp(49.97886 * SOC - 43.37888) - 0.028221 * std::atan(22.52300 * SOC - 3.65328) - 0.01308 * std::atan(28.34801 * SOC - 13.43960);
}

static double dOCPdT_n(double SOC)
{
    double num = 0.00527 + 3.29927 * SOC - 91.79326 * std::pow(SOC, 2) + 1004.91101 * std::pow(SOC, 3) -
                 5812.27813 * std::pow(SOC, 4) + 19329.75490 * std::pow(SOC, 5) - 37147.89470 * std::pow(SOC, 6) +
                 38379.18127 * std::pow(SOC, 7) - 16515.05308 * std::pow(SOC, 8);
    double dem = 1 - 48.09287 * SOC + 1017.23480 * std::pow(SOC, 2) - 10481.80419 * std::pow(SOC, 3) +
                 59431.30001 * std::pow(SOC, 4) - 195881.64880 * std::pow(SOC, 5) + 374577.31520 * std::pow(SOC, 6) -
                 385821.16070 * std::pow(SOC, 7) + 165705.85970 * std::pow(SOC, 8);
    return (num / dem) * 1e-3; // since the original unit are of mV/K
}

/*
* Positive Electrode
*/
static double L_p = 7.000000e-05;
static double A_p = 5.960000e-02;
static double max_conc_p = 51410;
static double epsilon_p = 0.49;
static double kappa_p = 3.8;
static double S_p = 1.1167;
static double R_p = 8.5e-6;
static double T_ref_p = 298.15;
static double D_ref_p = 1e-14;
static double k_ref_p = 6.67e-11;
static double Ea_D_p = 29000;
static double Ea_R_p = 58000;
static double brugg_p = 1.5;
// SOC_init_p = 0.59;
// SOC_p = SOC_init_p
static double soc_min_p = 0.4956 ;
static double soc_max_p = 0.989011;
static double alpha_p = 0.5;

// functions
double OCP_ref_p(double SOC)
{
    return 4.04596 + std::exp(-42.30027 * SOC + 16.56714) - 0.04880 * std::atan(50.01833 * SOC - 26.48897) \
              - 0.05447 * std::atan(18.99678 * SOC - 12.32362) - std::exp(78.24095 * SOC - 78.68074);
}


double dOCPdT_p(double SOC)
{
    double num = -0.19952 + 0.92837*SOC - 1.36455 * std::pow(SOC, 2) + 0.61154 * std::pow(SOC, 3);
    double dem = 1 - 5.66148 * SOC + 11.47636 * std::pow(SOC, 2) - 9.82431 * std::pow(SOC, 3) + 3.04876 * std::pow(SOC, 4);
    return (num/dem) * 1e-3 ; // since the original unit are of mV/K
}

/*
* Electrolyte
*/
static double L_e = 2e-5;
static double c_init_e = 1000.0;
static double kappa_e = 0.2875;
static double epsilon_e = 0.724;
static double brugg_e = 1.5;
static double D_e = 3.5e-10;
static double t_c = 0.354;
static double epsilon_en = 0.385;
static double epsilon_ep = 0.485;

/*
* Battery Cell
*/
static double T = 298.15;
static double rho = 1626;
static double Vol = 3.38e-5;
static double C_p = 750;
static double h = 1.0;
static double A = 0.085;
static double cap = 1.65;
static double V_max = 4.2;
static double V_min = 2.5;
static double R_cell = 0.0028230038442483246;