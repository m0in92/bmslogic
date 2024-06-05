
import pathlib
import sys
from typing import Callable

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

try:
    from bmslogic.simulations.cell.solution import PyECMSolution
    from bmslogic.simulations.cell.solvers.ecm import PyESCDTSolver
    from bmslogic.simulations.cell.battery_components import PyECMBatteryCell
    from bmslogic import cell_sim
    # from bmslogic.simulations.cell.parameter_set_manager import ParameterSets
    # import bmslogic.simulations.cell.cell as cell_sim
except ModuleNotFoundError as e:
    PROJECT_PATH: str = pathlib.Path(
        __file__).parent.parent.parent.parent.parent.parent.parent.__str__()
    print(PROJECT_PATH)
    sys.path.append(PROJECT_PATH)
    from bmslogic.simulations.cell.solution import PyECMSolution
    from bmslogic.simulations.cell.solvers.ecm import PyESCDTSolver
    from bmslogic.simulations.cell.battery_components import PyECMBatteryCell
    from bmslogic import cell_sim
    # from bmslogic.simulations.cell.parameter_set_manager import ParameterSets
    # import bmslogic.simulations.cell.cell as cell_sim
    # from bmslogic.simulations.cell.cyclers import PyDischarge, PyDischargeRest


def func_eta(SOC: float, temp: float) -> float:
    return 1.0


func_OCV: Callable = np.poly1d(np.array([1.40397547e+04, -8.44474191e+04, 2.21786698e+05, -3.34299193e+05,
                                         3.19797964e+05, -2.02770371e+05, 8.64154424e+04, -2.45738381e+04,
                                         4.53370220e+03, -5.14215292e+02, 3.27943338e+01, 2.78301303e+00]))


func_dOCVdT = np.poly1d(np.array([-1.62911207e+01, 9.66871309e+01, -2.50145828e+02, 3.70280039e+02,
                                  -3.46021781e+02, 2.12461660e+02, -8.64646004e+01, 2.29561374e+01,
                                  -3.80515739e+00, 3.58298325e-01, -1.40044753e-02, -6.86713653e-04]))


# Simulation Parameters
I: float = 1.65
v_min: float = 2.5
SOC_min: float = 0
SOC_LIB: float = 1
R_cell: float = 0.0028230038442483246

SOC_init_p: float = 0.4956  # from Guo et. al.
SOC_init_n: float = 0.7568  # from Guo et. al.
temp: float = 298.15


# setup the battery cell
cell: PyECMBatteryCell = PyECMBatteryCell(R0_ref=0.035, R1_ref=0.1, C1=3000, temp_ref=298.15, Ea_R0=4000,
                                          Ea_R1=4000,
                                          rho=1626, vol=3.38e-5, c_p=750, h=1, area=0.085, cap=1.96, v_max=4.2,
                                          v_min=2.5,
                                          soc_init=1.0, temp_init=298.15, func_eta=func_eta, func_ocv=func_OCV,
                                          func_docvdtemp=func_dOCVdT, M_0=4.4782e-4, M=0.0012, gamma=523.8311)
# cell_spm: cell_sim.BatteryCell = cell_sim.ParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=SOC_init_n,
#                                                                                                    soc_p_init=SOC_init_p,
#                                                                                                    T_amb=temp,
#                                                                                                    R_cell=R_cell)
cell_spm: cell_sim.PyBatteryCell = cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='Gao-Randall-Han',
                                                                              soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                                              temp_init=temp)

# set-up cycler and solver
dc: cell_sim.PyDischarge = cell_sim.PyDischarge(
    discharge_current=I, v_min=v_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
# dc_spm: cell_sim.Discharge = cell_sim.Discharge(
#     current=I, V_min=v_min, soc_lib_min=SOC_min, soc_lib=SOC_LIB)
solver: PyESCDTSolver = PyESCDTSolver(
    battery_cell_instance=cell, isothermal=True)
solver_spm: cell_sim.PySPSolver = cell_sim.PySPSolver(b_cell=cell_spm,
                                                      isothermal=True, degradation=False,
                                                      electrode_SOC_solver='poly')

# solver_spm: cell_sim.BatterySolver = cell_sim.BatterySolver(battery_cell=cell_spm,
#                                                             is_isothermal=True,
#                                                             enable_degradation=False)

# ECM solve
sol: PyECMSolution = solver.solve_standard_cycling_step(dt=0.1, cycler=dc)

# SPM solve
dc.reset()
sol_spm: cell_sim.PySolution = solver_spm.solve(cycler_instance=dc)
# sol_spm: cell_sim.Solution = solver_spm.solve(cycler=dc_spm)

# Plots
matplotlib.rc('xtick', labelsize=12) 
matplotlib.rc('ytick', labelsize=12) 

plt.plot(sol.array_t, sol.array_V, label="ECM")
plt.plot(sol_spm.t, sol_spm.V, label="SPM")

plt.xlabel("Time [$s$]", fontsize=15, weight="normal")
plt.ylabel("Terminal Voltage [$V$]", fontsize=15,weight="normal")
plt.legend(fontsize=12)
plt.tight_layout()
plt.ticklabel_format(style='sci', axis='x', scilimits=(-3,5), useMathText=True)
plt.show()
