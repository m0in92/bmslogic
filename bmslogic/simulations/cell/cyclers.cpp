/**
 * @file cyclers.cpp
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief functionalities for defining the battery cyclers
 * @version 0.1
 * @date 2024-05-04
 * 
 * @copyright Copyright (c) 2024
 * 
 */

#include <stdexcept>

#include "cyclers.h"


/// @brief constructor for the BaseCycler. Essentially the typical LIB parameters are initialized.
BaseCycler::BaseCycler() : SOC_LIB(1.0),
                           SOC_LIB_min(0.0), SOC_LIB_max(1.0),
                           V_min(2.5), V_max(4.2), discharge_current(0.0),
                           charge_current(0.0), rest_time(0.0), num_cycles(1),
                           cycle_steps({}) {}

/// @brief method to get the current during the battery cycling steps.
/// @param step_name "charge", "discharge" or "rest".
/// @param t time value [in s] of the present time step in question.
/// @return current [in A] value of the present time step.
double BaseCycler::get_current(std::string step_name, int t_step)
{
    if (step_name == "rest")
        return 0.0;
    else if (step_name == "discharge")
        return discharge_current;
    else if (step_name == "charge")
        return charge_current;
    else if (step_name == "custom")
        return m_current_vector[t_step];
    else
    {
        std::invalid_argument("Invalid cycling step name.");
    }
}

/// @brief resets the time_elapsed to zero. Useful when subjecting an already cycled BaseCycler instance.
void BaseCycler::reset_time_elapsed()
{
    time_elapsed = 0.0;
}

Discharge::Discharge(double i_discharge_current, double i_V_min, double i_SOC_LIB_min, double i_SOC_LIB) : BaseCycler()
{
    discharge_current = -i_discharge_current;
    V_min = i_V_min;
    SOC_LIB_min = i_SOC_LIB_min;
    SOC_LIB = i_SOC_LIB;
    num_cycles = 1;
    cycle_steps = {"discharge"};
}

DischargeRest::DischargeRest(double i_discharge_current, double i_V_min,
                             double i_soc_lib_min, double i_soc_lib,
                             double i_rest_time) : BaseCycler()
{
    discharge_current = -i_discharge_current;
    V_min = i_V_min;
    SOC_LIB_min = i_soc_lib_min;
    SOC_LIB = i_soc_lib;
    num_cycles = 1;
    rest_time = i_rest_time;
    cycle_steps = {"discharge", "rest"};
}

Charge::Charge(double i_charge_current, double i_V_max, double i_soc_lib_max, double i_soc)
{
    charge_current = i_charge_current;
    V_max = V_max;
    SOC_LIB_max = i_soc_lib_max;
    SOC_LIB = i_soc;
    cycle_steps = {"charge"};
}

ChargeDischarge::ChargeDischarge(double i_charge_current, double i_discharge_current, double i_V_min, double i_V_max,
                                 double i_soc_min, double i_soc_max, double i_soc, double i_rest_time) : BaseCycler()
{
    charge_current = i_charge_current;
    discharge_current = -i_discharge_current;
    V_min = i_V_min;
    V_max = i_V_max;
    SOC_LIB_min = i_soc_min;
    SOC_LIB_max = i_soc_max;
    SOC_LIB = i_soc;
    rest_time = i_rest_time;
    cycle_steps = {"charge", "rest", "discharge", "rest"};
}

CustomCycler::CustomCycler(std::vector<double> i_t, std::vector<double> i_current,
                           double i_V_min, double i_V_max, double i_soc_min, double i_soc_max, double i_soc) : BaseCycler()
{
    m_t_vector = i_t;
    m_current_vector = i_current;
    V_min = i_V_min;
    V_max = i_V_max;
    SOC_LIB_min = i_soc_min;
    SOC_LIB_max = i_soc_max;
    SOC_LIB = i_soc;
    rest_time = i_t.back();
    cycle_steps = {"custom"};
}

// double CustomCycler::get_current(std::string cycling_step, double t) 
// {
//     return -1.656;
// }