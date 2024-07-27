#include <iostream>

#include "Eigen/Dense"

#include "battery_components.h"
#include "cyclers.h"
#include "solvers.h"
#include "kalman_solvers.h"
#include "solution.h"
#include "example_parameters.h"

int main()
{
    double temp = 298.15;
    double soc_n = 0.7522;
    double soc_p = 0.4952;

    double discharge_current = 1.65;
    double V_min = 2.5;
    double SOC_lib_min = 0.0;
    double SOC_lib = 0.0;

    std::function<double(double)> OCP_ref_n_ = OCP_ref_n;
    std::function<double(double)> dOCPdT_n_ = dOCPdT_n;
    std::function<double(double)> OCP_ref_p_ = OCP_ref_p;
    std::function<double(double)> dOCPdT_p_ = dOCPdT_p;

    NElectrode elec_n = NElectrode(L_n, A_n, kappa_n, epsilon_n, max_conc_n, R_n, S_n,
                                   T_ref_n, D_ref_n, k_ref_n, Ea_D_n, Ea_R_n, alpha_n,
                                   brugg_n, soc_n, temp, OCP_ref_n_, dOCPdT_n_);
    PElectrode elec_p = PElectrode(L_p, A_p, kappa_p, epsilon_p, max_conc_p, R_p, S_p,
                                   T_ref_p, D_ref_p, k_ref_p, Ea_D_p, Ea_R_p, alpha_p,
                                   brugg_p, soc_p, temp, OCP_ref_p_, dOCPdT_p_);
    Electrolyte electrolyte = Electrolyte(c_init_e, L_e, kappa_e, epsilon_e, brugg_e);
    BatteryCell b_cell = BatteryCell(elec_p, elec_n, electrolyte, rho, Vol, C_p, h, A, cap, V_max, V_min, R_cell);

    // Discharge cycler = Discharge(discharge_current, V_min, SOC_lib_min, SOC_lib);

    Eigen::VectorXd t(4);
    t << 0.0, 0.1, 0.2, 0.3;
    Eigen::VectorXd I(4);
    I << -1.656, -1.656, -1.656, -1.656;
    Eigen::VectorXd V(4);
    V << 4.2, 4.2, 4.2, 4.2;

    SPKFSolver solver = SPKFSolver(b_cell, true, true, soc_p, soc_n, 1e-3, 1e-3, 1e-3, 1e-3);
    Solution sol = solver.solve(t, I, V);

    // print results
    std::cout << sol.get_x_n()[0] << std::endl;
    std::cout << sol.get_x_n()[1] << std::endl;
}