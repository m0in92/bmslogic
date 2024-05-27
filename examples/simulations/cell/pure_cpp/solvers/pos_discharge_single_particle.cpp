#include <iostream>
#include <chrono>
#include <iomanip>

#include "solvers.h"

// Electrode parameters below
static double R = 8.5e-6;       // electrode particle radius in [m]
static double c_max = 51410;     // max. electrode concentration [mol/m3]
static double D = 1e-14 ;       // electrode diffusivity [m2/s]
static double S = 1.1167;        // electrode electrochemical active area [m2]
static double SOC_init = 0.4956; // initial electrode SOC
static double c_init = c_max * SOC_init; // initial electrode concentration [mol/m3]
static char electrode_type = 'p';

// Simulation parameters below
double i_app = -1.65;  // Applied current [A]
double dt = 0.1;

int main()
{
    PolynomialApprox poly_solver = PolynomialApprox(electrode_type, c_init, "higher");

    clock_t start, end;
    start = clock();
    
    double t_prev = 0.0;
    double soc_poly = SOC_init;
    while(soc_poly < 1) {
        poly_solver.solve(dt, t_prev, i_app, R, S, D);
        t_prev += dt;
        soc_poly = poly_solver.get_x_surf(c_max);
        // std::cout << poly_solver.get_x_surf(c_max) << std::endl;
    }

    end = clock();
    std::cout << std::fixed << std::setprecision(10) << "Solution time in seconds: " << double(end - start) / double(CLOCKS_PER_SEC) << std::endl;

    return 0;
}