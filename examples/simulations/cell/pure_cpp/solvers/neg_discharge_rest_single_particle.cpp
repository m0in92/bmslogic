#include <iostream>
#include <chrono>
#include <iomanip>

#include "cyclers.h"
#include "solvers.h"

// Electrode parameters below
static double R = 1.25e-5;               // electrode particle radius in [m]
static double c_max = 31833;             // max. electrode concentration [mol/m3]
static double D = 3.9e-14;               // electrode diffusivity [m2/s]
static double S = 0.7824;                // electrode electrochemical active area [m2]
static double SOC_init = 0.7568;         // initial electrode SOC
static double c_init = c_max * SOC_init; // initial electrode concentration [mol/m3]
static char electrode_type = 'n';

// Simulation parameters below
double V_min = 2.0;  // [V]
double i_app = 1.65; // Applied current [A]
double dt = 0.1;

int main()
{
    PolynomialApprox poly_solver = PolynomialApprox(electrode_type, c_init, "higher");
    EigenSolver eigen_solver = EigenSolver(electrode_type, SOC_init, 10);

    DischargeRest cycler = DischargeRest(i_app, V_min, 0.0, 1.0, 3600.0);

    // poly solver
    clock_t start, end;

    start = clock();

    double t_prev = 0.0;
    double soc_poly = SOC_init;
    double i_app_;
    while (soc_poly > 0)
    {
        i_app_ = cycler.get_current("discharge", 0);
        poly_solver.solve(dt, t_prev, i_app_, R, S, D);
        t_prev += dt;
        soc_poly = poly_solver.get_x_surf(c_max);
        // std::cout << poly_solver.get_x_surf(c_max) << std::endl;
    }
    // std::cout << R << std::endl;

    end = clock();
    std::cout << std::fixed << std::setprecision(10) << "Polynomial Solution time in seconds: " << double(end - start) / double(CLOCKS_PER_SEC) << std::endl;

    // Eigen solver
    clock_t eigen_start, eigen_end;

    eigen_start = clock();

    t_prev = 0.0;
    double soc_eigen = SOC_init;
    while (soc_eigen > 0)
    {
        i_app_ = cycler.get_current("discharge", 0);
        soc_eigen = eigen_solver.solve(dt, t_prev, i_app_, R, S, D, c_max);
        t_prev += dt;
        // soc_eigen = poly_solver.get_x_surf(c_max);
        // std::cout << poly_solver.get_x_surf(c_max) << std::endl;
    }
    // std::cout << R << std::endl;

    eigen_end = clock();
    std::cout << std::fixed << std::setprecision(10) << "Eigen Solution time in seconds: " << double(eigen_end - eigen_start) / double(CLOCKS_PER_SEC) << std::endl;

    return 0;
}