/**
 * @file cyclers.h
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief functionalities for defining the battery cyclers
 * @version 0.1
 * @date 2024-05-04
 *
 * @copyright Copyright (c) 2024
 *
 */

#ifndef BMSLOGIC_PROJECT_CYCLERS_H
#define BMSLOGIC_PROJECT_CYCLERS_H

#include <string>
#include <vector>

#include "extern/owl.h"

/**
 * @brief This class is intended to store the relevant cycling variables for the battery cell simulations.
 */
class BaseCycler
{
public:
    BaseCycler();
    virtual ~BaseCycler() = default;
    // public variables
    double time_elapsed = 0.0;
    double SOC_LIB;
    double SOC_LIB_min;
    double SOC_LIB_max;
    double V_min;
    double V_max;
    double discharge_current;
    double charge_current;
    double rest_time;
    int num_cycles;
    std::vector<double> m_t_vector;
    std::vector<double> m_current_vector;
    std::vector<std::string> cycle_steps;
    // getters
    double get_time_elapsed() { return time_elapsed; }
    double get_V_min() { return V_min; }
    double get_V_max() { return V_max; }
    double get_rest_time() { return rest_time; }
    int get_num_cycles() { return num_cycles; }
    // setters
    void set_time_elapsed(double time_elapsed_new) { time_elapsed = time_elapsed_new; }
    void set_V_min(double V_min_new) { V_min = V_min_new; }
    void set_V_max(double &V_max_new) { V_max = V_max_new; }
    void set_rest_time(double &rest_time_new) { rest_time = rest_time_new; }
    void set_num_cycles(int &num_cycles_new) { num_cycles = num_cycles_new; }
    // Helper/calculation methods
    virtual double get_current(std::string cycling_step, int time_step);
    void reset_time_elapsed();
};

/**
 * @brief Contains cycling parameters relevant for the discharge cycling step.
 *
 */
class Discharge : public BaseCycler
{
public:
    Discharge(double discharge_current, double V_min, double SOC_LIB_min, double SOC_LIB);
    ~Discharge() = default;
};

/**
 * @brief Contains cycling parameters relevant for the discharge-rest cycling step.
 *
 */
class DischargeRest : public BaseCycler
{
public:
    DischargeRest(double i_discharge_current, double i_V_min, double i_soc_lib_min, double i_soc_lib, double i_rest_time);
    ~DischargeRest() = default;
};

/**
 * @brief Contains cycling parameters relevant for the charge cycling step.
 *
 */
class Charge : public BaseCycler
{
public:
    Charge(double i_charge_current, double i_V_max, double i_soc_lib_max, double i_soc);
    ~Charge() = default;
};

/**
 * @brief Contains cycling parameters relevant for the charge-rest cycling steps.
 *
 */
class ChargeRest : public BaseCycler
{
public:
    ChargeRest(double i_charge_current, double i_V_min, double i_soc_lib_max, double i_soc, double i_rest_time);
    ~ChargeRest() = default;
};

/**
 * @brief Contains cycling parameters relevant for the charge-discharge cycle. The first charge step is followed by the rest period.
 * The subsequent discharge cycling step is again followed by the rest period.
 *
 */
class ChargeDischarge : public BaseCycler
{
public:
    ChargeDischarge(double i_charge_current, double i_discharge_current, double i_V_max, double i_V_min,
                    double i_soc_min, double i_soc_max, double i_soc, double i_rest_time);
    ~ChargeDischarge() = default;
};

/**
 * @brief Contains cycling parameters for the Custom Cycling step. The use inputs the time and current arrays where the elements in the
 * current array corresponds to the applied battery cell current at the time step.
 *
 */
class CustomCycler : public BaseCycler
{
public:
    CustomCycler(std::vector<double> t, std::vector<double> current, double V_min, double V_max, double soc_min, double soc_max, double soc);
    ~CustomCycler() = default;
    // getters
    std::vector<double> get_t_vector() { return m_t_vector; }
    std::vector<double> get_current_vector() { return m_current_vector; }
    // setters
    void set_t_vector(std::vector<double> &t_vector_new) { m_t_vector = t_vector_new; }
    void set_current_vector(std::vector<double> &current_vector_new) { m_current_vector = current_vector_new; }
};

/**
 * @brief Creates a cycler class whose time and current array values have been filled through interpolation.
 *        THIS CLASS HAS VERY HIGH COMPUTATIONAL TIMES AND IT IS RECOMMENDED TO NOT USE IT! USE THE CYCLER IN PYCYCLER
 *        INSTEAD.
 *
 */
class InterpolatedCustomCycler : public BaseCycler
{
public:
    InterpolatedCustomCycler(std::vector<double> i_t_exp, std::vector<double> i_I_exp, double dt,
                             double V_min, double V_max, double soc_min, double soc_max, double soc);
    ~InterpolatedCustomCycler() = default;
    // getters
    std::vector<double> get_t_vector() { return m_t_vector; }
    std::vector<double> get_current_vector() { return m_current_vector; }
    // setters
    void set_t_vector(std::vector<double> &t_vector_new) { m_t_vector = t_vector_new; }
    void set_current_vector(std::vector<double> &current_vector_new) { m_current_vector = current_vector_new; }
};

/**
 * @brief This cycler is intended to provide the applied current during the HPPC discharge step.
 *
 */
class HPPCCycler : public BaseCycler
{
public:
    HPPCCycler(double i_t1, double i_t2, double i_i_app, int i_num_hppc_pulses,
               double i_V_min, double i_SOC_LIB_min, double i_SOC_LIB);
    ~HPPCCycler() = default;
    // helpers functions
    double get_current(std::string cycling_step, double t);

private:
    double m_t1;
    double m_t2;
    double m_num_hppc_pulses;
};

#endif // BMSLOGIC_PROJECT_CYCLERS_H
