"""
Contains an example of using electrolyte solver in a simulation. The solver uses numerical finite volume
method (FVM).
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright SPPy 2024. All rights reserved."
__status__ = "Deployed"

import pathlib
import pickle
import os
import time
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.append(pathlib.Path(
    __file__).parent.parent.parent.parent.parent.parent.parent.__str__())
from bmslogic.simulations.cell.models import PySPMe
from bmslogic.simulations.cell.solvers.electrolyte_conc import PyElectrolyteConcFVMSolver
from bmslogic.simulations.cell.solvers.electrolyte_conc import PyElectrolyteFVMCoordinates


# Simulation parameters
dt: float = 0.1
max_iter: int = int(4000 / dt)

co_ords: PyElectrolyteFVMCoordinates = PyElectrolyteFVMCoordinates(
    L_n=8e-5, L_s=2.5e-5, L_p=8.8e-5)
conc_solver: PyElectrolyteConcFVMSolver = PyElectrolyteConcFVMSolver(fvm_co_ords=co_ords, transference=0.354,
                                                                     epsilon_en=0.385, epsilon_esep=0.785, epsilon_ep=0.485,
                                                                     a_sn=5.78e3, a_sp=7.28e3,
                                                                     D_e=3.5e-10,
                                                                     brugg=4,
                                                                     c_e_init=1000)

j_p = PySPMe.molar_flux_electrode(
    I=-1.656, S=1.1167, electrode_type='p') * np.ones(len(co_ords.array_x_p))  # [mol/m2/s]
j_sep = np.zeros(len(co_ords.array_x_s))  # [mol/m2/s]
j_n = PySPMe.molar_flux_electrode(
    I=-1.656, S=0.7824, electrode_type='n') * np.ones(len(co_ords.array_x_n))  # [mol/m2/s]
j = np.append(np.append(j_n, j_sep), j_p)  # [mol/m2/s]

# --------------------------------SIMULATION-----------------------------------------------------------------

lst_0: list = conc_solver.array_c_e
lst_1000: list = []
lst_2000: list = []
lst_3000: list = []
lst_4000: list = []

time_start: int = time.time()
for i in range(max_iter):
    conc_solver.solve_ce(j=j, dt=dt, solver_method='TDMA')

    if i==1000:
        lst_1000 = conc_solver.array_c_e.tolist()

    if i==2000:
        lst_2000 = conc_solver.array_c_e.tolist()

    if i==3000:
        lst_3000 = conc_solver.array_c_e.tolist()

    if i==4000:
        lst_4000 = conc_solver.array_c_e.tolist()

time_end: int = time.time()

print(f"Solution Time [s]: {time_end-time_start}")

# ----------------------------------SAVE RESULTS ---------------------------------------------------------

FILE_DIR_TO_SAVE = os.path.join(pathlib.Path(__file__).parent, "saved_results")

with open(os.path.join(FILE_DIR_TO_SAVE, "fvm_inverse_neg_discharge_x.pkl"), "wb") as pkl_file:
    pickle.dump(co_ords.array_x.tolist(), pkl_file)

with open(os.path.join(FILE_DIR_TO_SAVE, "fvm_neg_discharge_t_0.pkl"), "wb") as pkl_file:
    pickle.dump(lst_0, pkl_file)

with open(os.path.join(FILE_DIR_TO_SAVE, "fvm_neg_discharge_t_1000.pkl"), "wb") as pkl_file:
    pickle.dump(lst_1000, pkl_file)

with open(os.path.join(FILE_DIR_TO_SAVE, "fvm_neg_discharge_t_2000.pkl"), "wb") as pkl_file:
    pickle.dump(lst_2000, pkl_file)

with open(os.path.join(FILE_DIR_TO_SAVE, "fvm_neg_discharge_t_3000.pkl"), "wb") as pkl_file:
    pickle.dump(lst_3000, pkl_file)

with open(os.path.join(FILE_DIR_TO_SAVE, "fvm_neg_discharge_t_4000.pkl"), "wb") as pkl_file:
    pickle.dump(lst_4000, pkl_file)

# -----------------------------------PLOTS --------------------------------------------------------------
plt.xlabel("Battery Cell Thickness [m]")
plt.ylabel("Electrolyte Conc. [mol/m3]")
plt.title(f"Electrolyte Conc. [mol/m3] after {max_iter * dt} s of discharge")
plt.ticklabel_format(axis="x", scilimits=[-3, 1])
plt.plot(co_ords.array_x, lst_0, label="t=0s")
plt.plot(co_ords.array_x, lst_1000, label="t=1000s")
plt.plot(co_ords.array_x, lst_2000, label="t=2000s")
plt.plot(co_ords.array_x, lst_3000, label="t=3000s")
plt.plot(co_ords.array_x, lst_4000, label="t=4000s")

plt.legend()
plt.show()
