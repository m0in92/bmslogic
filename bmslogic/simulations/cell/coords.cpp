/**
 * @file coords.cpp
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief contains classes that enable functionality to define coordinate systems.
 * @version 0.1
 * @date 2024-05-12
 *
 * @copyright Copyright (c) 2024 by BMSLogoc. All Rights Reserved.
 *
 */

#include "constants.h"
#include "owl.h"
#include "coords.h"

ElectrolyteFVMCoordinates::ElectrolyteFVMCoordinates(double i_L_n, double i_L_sep, double i_L_p,
                                                     int i_num_grid_n, int i_num_grid_sep, int i_num_grid_p) : m_L_n(i_L_n),
                                                                                                               m_L_sep(i_L_sep), m_L_p(i_L_p),
                                                                                                               m_num_grid_n(i_num_grid_n), m_num_grid_sep(i_num_grid_sep), m_num_grid_p(i_num_grid_p)
{
    m_dx_n = m_L_n / m_num_grid_n;
    m_dx_sep = m_L_sep / m_num_grid_sep;
    m_dx_p = m_L_p / m_num_grid_p;

    OWL::ArrayXD vector_x_n_ = OWL::aRange(m_dx_n / 2, m_L_n, m_dx_n);
    OWL::ArrayXD vector_x_sep_ = OWL::aRange(m_L_n + m_dx_sep / 2, m_L_n + m_L_sep, m_dx_sep);
    OWL::ArrayXD vector_x_p_ = OWL::aRange(m_L_n + +m_L_sep + m_dx_p / 2, m_L_n + m_L_sep + m_L_p, m_dx_p);
    OWL::ArrayXD vector_x_ = OWL::append(vector_x_n_, vector_x_sep_);
    vector_x_ = OWL::append(vector_x_, vector_x_p_);
    m_vector_x_n = vector_x_n_.getArray();
    m_vector_x_sep = vector_x_sep_.getArray();
    m_vector_x_p = vector_x_p_.getArray();
    m_vector_x = vector_x_.getArray();

    OWL::ArrayXD vector_dx_n_ = m_dx_n * OWL::Ones(m_num_grid_n);
    OWL::ArrayXD vector_dx_sep_ = m_dx_sep * OWL::Ones(m_num_grid_sep);
    OWL::ArrayXD vector_dx_p_ = m_dx_p * OWL::Ones(m_num_grid_p);
    OWL::ArrayXD vector_dx_ = OWL::append(vector_dx_n_, vector_dx_sep_);
    vector_dx_ = OWL::append(vector_dx_, vector_dx_p_);
    m_vector_dx = vector_dx_.getArray();
}
