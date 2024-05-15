#include <iostream>
#include <vector>

#include "coords.h"
#include "solvers.h"

static double L_n = 8e-5;
static double L_sep = 2.5e-5;
double L_p = 8.8e-5;

static double epsilon_e_n = 0.385;
static double epsilon_e_sep = 0.785;
static double epsilon_e_p = 0.485;

static double D_e = 3.5e-10; // [m2/s]
static double brugg = 4;
static double t_c = 0.354;
double c_e_init = 1000; // [mol/m3]

static double a_s_n = 5.78e3;
static double a_s_p = 7.28e3;

// Simulation parameters
static double dt = 0.1; // [s]
static double max_iter = 1000;

int main()
{
    ElectrolyteFVMCoordinates coords = ElectrolyteFVMCoordinates(L_n, L_sep, L_p,
                                                                 10, 10, 10);
    ElectrolyteFVMSolver solver = ElectrolyteFVMSolver(coords, c_e_init, t_c,
                                                       epsilon_e_n, epsilon_e_sep, epsilon_e_p,
                                                       a_s_n, a_s_p,
                                                       D_e, brugg);

    OWL::ArrayXD j_n = 2.19362652e-05 * OWL::Ones(10);
    OWL::ArrayXD j_sep = OWL::Zeros(10);
    OWL::ArrayXD j_p = -2.19362652e-05 * OWL::Ones(10);
    OWL::ArrayXD j_sep_p = OWL::append(j_sep, j_p);
    std::vector<double> j = OWL::append(j_n, j_sep_p).getArray();

    solver.solve(j, dt);
    std::cout << solver.get_vector_c_e()[0] << std::endl;

    return 0;
}
