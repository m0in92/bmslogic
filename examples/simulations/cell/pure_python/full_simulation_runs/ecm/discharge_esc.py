import pathlib
import sys
from typing import Callable

import numpy as np

PROJECT_PATH: str = pathlib.Path(
    __file__).parent.parent.parent.parent.parent.parent.parent.__str__()
print(PROJECT_PATH)
sys.path.append(PROJECT_PATH)
from bmslogic.simulations.cell.solution import PyECMSolution
from bmslogic.simulations.cell.solvers.ecm import PyESCDTSolver
from bmslogic.simulations.cell.battery_components import PyECMBatteryCell
from bmslogic import cell_sim


# with open("../saved_results/SOC", "rb") as f_SOC:
#     SOC = pickle.load(f_SOC)

# with open("../saved_results/OCV", "rb") as f_OCV:
#     OCV = pickle.load(f_OCV)

# with open("../saved_results/SOC_dOCVdT", "rb") as f_SOC:
#     SOC_dOCVdT = pickle.load(f_SOC)

# with open("../saved_results/dOCVdT", "rb") as f_OCV:
#     dOCVdT = pickle.load(f_OCV)


def func_eta(SOC: float, temp: float) -> float:
    return 1.0


# func_OCV: Callable = scipy.interpolate.interp1d(SOC, OCV, fill_value='extrapolate')
# func_dOCVdT: Callable = scipy.interpolate.interp1d(SOC_dOCVdT, dOCVdT, fill_value='extrapolate')

func_OCV: Callable = np.poly1d(np.array([7.83002260e+03, -4.72721395e+04, 1.25237092e+05, -1.91403553e+05,
                                         1.86656077e+05, -1.21342077e+05, 5.33553293e+04, -1.57665852e+04,
                                         3.04748964e+03, -3.65636105e+02, 2.50281588e+01, 2.93438431e+00]))
func_dOCVdT = np.poly1d(np.array([-1.62911207e+01, 9.66871309e+01, -2.50145828e+02, 3.70280039e+02,
                                  -3.46021781e+02, 2.12461660e+02, -8.64646004e+01, 2.29561374e+01,
                                  -3.80515739e+00, 3.58298325e-01, -1.40044753e-02, -6.86713653e-04]))

# Simulation Parameters
I: float = 1.65
v_min: float = 2.5
SOC_min: float = 0
SOC_LIB: float = 1

# setup the battery cell
cell: PyECMBatteryCell = PyECMBatteryCell(R0_ref=0.005, R1_ref=0.001, C1=0.03, temp_ref=298.15, Ea_R0=4000,
                                          Ea_R1=4000,
                                          rho=1626, vol=3.38e-5, c_p=750, h=1, area=0.085, cap=1.65, v_max=4.2,
                                          v_min=2.5,
                                          soc_init=0.98, temp_init=298.15, func_eta=func_eta, func_ocv=func_OCV,
                                          func_docvdtemp=func_dOCVdT, M_0=4.4782e-4, M=0.0012, gamma=523.8311)

# set-up cycler and solver
dc: cell_sim.PyDischarge = cell_sim.PyDischarge(
    discharge_current=I, v_min=v_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
solver: PyESCDTSolver = PyESCDTSolver(
    battery_cell_instance=cell, isothermal=True)

# solve
sol: PyECMSolution = solver.solve_standard_cycling_step(dt=0.1, cycler=dc)

# Plots
sol.comprehensive_plot(plot_line_color="0.25")
