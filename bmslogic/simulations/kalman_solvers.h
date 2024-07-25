#include "solvers.h"
#include "kalman_filter.h"

class SPKFSolver : public BaseBatterySolver
{
public:
    SPKFSolver(BatteryCell i_b_cell, bool i_isothermal, bool i_degradation, std::string i_electrode_SOC_solver);

private:
    TwoStatesOneInputOneOutput m_spkf_solver;
};
