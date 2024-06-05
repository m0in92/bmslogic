"""
This example Python script demonstrates the fitting of lithium-ion battery's OCV from the electrode OCP.
"""
__author__ = "Moin Ahmed"


import pathlib
import sys
from typing import Callable

import numpy as np
import matplotlib.pyplot as plt

PROJECT_PATH: str = pathlib.Path(
    __file__).parent.parent.parent.parent.parent.parent.parent.__str__()
print(PROJECT_PATH)
sys.path.append(PROJECT_PATH)
from bmslogic.simulations.cell.solution import PyECMSolution
from bmslogic.simulations.cell.solvers.ecm import PyESCDTSolver
from bmslogic.simulations.cell.battery_components import PyECMBatteryCell
from bmslogic import cell_sim
from bmslogic.parameter_sets.test import funcs


soc_p: np.array = np.linspace(0.4956, 1)
soc_n: np.array = np.linspace(0.0189023, 0.7568)
soc_lib: np.array = np.linspace(0,1)

ocp_p: np.array = funcs.OCP_ref_p(soc_p)
ocp_n: np.array = funcs.OCP_ref_n(soc_n)

ocv_lib: np.array = np.flip(ocp_p) - ocp_n

# polynomial fit
poly_coeff: np.array = np.polyfit(soc_lib, ocv_lib, deg=11)
ocv_lib_fit: np.array = np.polyval(poly_coeff, soc_lib)

# print results
print(poly_coeff)

# plots
plt.plot(soc_lib, np.flip(ocp_p), "--")
plt.plot(soc_lib, ocp_n, "--")
plt.plot(soc_lib, ocv_lib, label="OCV-actual")
plt.plot(soc_lib, ocv_lib_fit, label="OCV-fit")

plt.xlabel("Time [$s$]", fontsize=15, weight="normal")
plt.ylabel("Voltage [$V$]", fontsize=15,weight="normal")
plt.legend(fontsize=12)
plt.tight_layout()
plt.ticklabel_format(style='sci', axis='x', scilimits=(-3,5), useMathText=True)
plt.show()

