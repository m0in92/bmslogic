/**
 * @file coords.h
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief contains classes that enable functionality to define coordinate systems.
 * @version 0.1
 * @date 2024-05-12
 *
 * @copyright Copyright (c) 2024 by BMSLogoc. All Rights Reserved.
 *
 */

#ifndef BMSLOGIC_SIMULATIONS_COORDS
#define BMSLOGIC_SIMULATIONS_COORDS

#include <vector>

/**
 * @class ElectrolyteFVMCoordinates
 * @brief Contains the functionality to define and store co-ordinate points for 1D finite volume coordinates
 * across the battery cell thickness.
 *
 */
class ElectrolyteFVMCoordinates
{
public:
    ElectrolyteFVMCoordinates(double i_L_n, double i_L_sep, double i_L_p,
                              int i_num_grid_n, int i_num_grid_sep, int i_num_grid_p);
    ~ElectrolyteFVMCoordinates() = default;
    // Getter functions
    double get_L_n() const { return m_L_n; }
    double get_L_sep() const { return m_L_sep; }
    double get_L_p() const { return m_L_p; }
    double get_num_grid_n() const { return m_num_grid_n; }
    double get_num_grid_sep() const { return m_num_grid_sep; }
    double get_num_grid_p() const { return m_num_grid_p; }
    double get_dx_n() const { return m_dx_n; }
    double get_dx_sep() const { return m_dx_sep; }
    double get_dx_p() const { return m_dx_p; }
    std::vector<double> get_vector_x_n() const { return m_vector_x_n; }
    std::vector<double> get_vector_x_sep() const { return m_vector_x_sep; }
    std::vector<double> get_vector_x_p() const { return m_vector_x_p; }
    std::vector<double> get_vector_x() const { return m_vector_x; }
    std::vector<double> get_vector_dx() const { return m_vector_dx; }

private:
    double m_L_n;
    double m_L_sep;
    double m_L_p;

    int m_num_grid_n;
    int m_num_grid_sep;
    int m_num_grid_p;

    double m_dx_n;
    double m_dx_sep;
    double m_dx_p;

    std::vector<double> m_vector_x_n;
    std::vector<double> m_vector_x_sep;
    std::vector<double> m_vector_x_p;
    std::vector<double> m_vector_x;
    std::vector<double> m_vector_dx;
};

#endif // BMSLOGIC_SIMULATIONS_COORDS
