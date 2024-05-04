/**
 * @file constants.h
 * @author Moin Ahmed (moinahmed100@gmail.com)
 * @brief Contains the class that contains the physical constants.
 * @version 0.1
 * @date 2024-05-03
 * 
 * @copyright Copyright (c) 2024
 * 
 */

#ifndef BMSLOGIC_PROJECT_CONSTANTS_H
#define BMSLOGIC_PROJECT_CONSTANTS_H

#include <cmath>


static struct
{
public:
    double F = 96487;  // Faraday's constant [C/mol]
    double R = 8.3145;   // Gas constant [J/(mol K)]
    double T_abs = 273.15;  // absolute temp [K]
    double pi = std::atan(1.0) * 4.0; // value of pi
} Constants;

#endif //BMSLOGIC_PROJECT_CONSTANTS_H
