/**
 * @file solution.h
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief Contains the funcitionalities to store and display the simulations results.
 * @version 0.1
 * @date 2024-05-04
 *
 * @copyright Copyright (c) 2024
 *
 */

#ifndef BMSLOGIC_PROJECT_SOLUTION_H
#define BMSLOGIC_PROJECT_SOLUTION_H

#include <vector>
#include <string>

#include "extern/owl.h"

class ECMSolution
{
public:
    ECMSolution(){};
    ECMSolution(std::vector<double> i_t,
                std::vector<double> i_I,
                std::vector<double> i_V,
                std::vector<double> i_temp,
                std::vector<double> i_soc,
                std::vector<double> i_i_R1);
    // getter methods
    std::vector<double> get_t() { return m_t; }
    std::vector<double> get_I() { return m_I; }
    std::vector<double> get_V() { return m_V; }
    std::vector<double> get_temp() { return m_temp; }
    std::vector<double> get_soc() { return m_soc; }
    std::vector<double> get_i_R1() { return m_i_R1; }
    // setters
    void set_t(std::vector<double> i_t) { m_t = i_t; }
    void set_I(std::vector<double> i_t) { m_I = i_t; }
    void set_V(std::vector<double> i_t) { m_V = i_t; }
    void set_temp(std::vector<double> i_temp) { m_temp = i_temp; }
    void set_soc(std::vector<double> i_soc) { m_soc = i_soc; }
    void set_i_R1(std::vector<double> i_i_R1) { m_i_R1 = i_i_R1; }
    // the methods below are intended for updating the member vectors
    void update_t(double t_new) { m_t.push_back(t_new); }
    void update_I(double I_new) { m_t.push_back(I_new); }
    void update_V(double V_new) { m_t.push_back(V_new); }
    void update_temp(double temp_new) { m_t.push_back(temp_new); }
    void update_soc(double soc_new) { m_t.push_back(soc_new); }
    void update_i_R1(double i_R1_new) { m_t.push_back(i_R1_new); }

private:
    std::vector<double> m_t;
    std::vector<double> m_I;
    std::vector<double> m_V;
    std::vector<double> m_temp;
    std::vector<double> m_soc;
    std::vector<double> m_i_R1;
};

class Solution
{
public:
    Solution(){};
    Solution(std::vector<double> i_t,
             std::vector<std::string> i_cycling_step,
             std::vector<double> i_V,
             std::vector<double> i_temp,
             std::vector<double> i_cap,
             std::vector<double> i_x_p,
             std::vector<double> i_x_n);
    // getter methods
    std::vector<double> get_t() { return m_t; }
    std::vector<std::string> get_cycling_step() { return m_cycling_step; }
    std::vector<double> get_V() { return m_V; }
    std::vector<double> get_temp() { return m_temp; }
    std::vector<double> get_cap() { return m_cap; }
    std::vector<double> get_x_p() { return m_x_p; }
    std::vector<double> get_x_n() { return m_x_n; }
    // setter methods
    void set_t(std::vector<double> t_new) { m_t = t_new; }
    void set_cycling_step(std::vector<std::string> cycling_step_new) { m_cycling_step = cycling_step_new; }
    void set_V(std::vector<double> V_new) { m_V = V_new; }
    void set_temp(std::vector<double> temp_new) { m_temp = temp_new; }
    void set_cap(std::vector<double> cap_new) { m_cap = cap_new; }
    void set_x_p(std::vector<double> x_p_new) { m_x_p = x_p_new; }
    void set_x_n(std::vector<double> x_n_new) { m_x_n = x_n_new; }
    // the methods below are intended for updating the member vectors
    void update_t(double t_new) { m_t.push_back(t_new); }
    void update_cycling_step(std::string cycling_step_new) { m_cycling_step.push_back(cycling_step_new); }
    void update_V(double V_new) { m_V.push_back(V_new); }
    void update_temp(double temp_new) { m_temp.push_back(temp_new); }
    void update_cap(double cap_new) { m_cap.push_back(cap_new); }
    void update_x_p(double x_p_new) { m_x_p.push_back(x_p_new); }
    void update_x_n(double x_n_new) { m_x_n.push_back(x_n_new); }

private:
    std::vector<double> m_t;
    std::vector<std::string> m_cycling_step;
    std::vector<double> m_V;
    std::vector<double> m_temp;
    std::vector<double> m_cap;
    std::vector<double> m_x_p;
    std::vector<double> m_x_n;
};

#endif // BMSLOGIC_PROJECT_SOLUTION_H
