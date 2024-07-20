/**
 * @file solution.cpp
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief Contains the funcitionalities to store and display the simulations results.
 * @version 0.1
 * @date 2024-05-04
 *
 * @copyright Copyright (c) 2024
 *
 */

#include "solution.h"

ECMSolution::ECMSolution(std::vector<double> i_t,
                         std::vector<double> i_I,
                         std::vector<double> i_V,
                         std::vector<double> i_temp,
                         std::vector<double> i_soc,
                         std::vector<double> i_i_R1)
{
    m_t = i_t;
    m_I = i_I;
    m_V = i_V;
    m_temp = i_temp;
    m_soc = i_soc;
    m_i_R1 = i_i_R1;
}

Solution::Solution(std::vector<double> i_t,
                   std::vector<std::string> i_cycling_step,
                   std::vector<double> i_V,
                   std::vector<double> i_temp,
                   std::vector<double> i_cap,
                   std::vector<double> i_x_p,
                   std::vector<double> i_x_n)
{
    m_t = i_t;
    m_cycling_step = i_cycling_step;
    m_V = i_V;
    m_temp = i_temp;
    m_cap = i_cap;
    m_x_p = i_x_p;
    m_x_n = i_x_n;
}

Solution::Solution(std::vector<double> i_t,
                   std::vector<std::string> i_cycling_step,
                   std::vector<double> i_V,
                   std::vector<double> i_temp,
                   std::vector<double> i_cap,
                   std::vector<double> i_x_p,
                   std::vector<double> i_x_n,
                   std::vector<double> i_OCV)
{
    m_t = i_t;
    m_cycling_step = i_cycling_step;
    m_V = i_V;
    m_temp = i_temp;
    m_cap = i_cap;
    m_x_p = i_x_p;
    m_x_n = i_x_n;
    m_OCV = i_OCV;
}
