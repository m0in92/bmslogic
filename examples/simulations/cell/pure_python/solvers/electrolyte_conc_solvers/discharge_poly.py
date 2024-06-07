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

try:
    from bmslogic.simulations.cell.solvers.electrolyte_conc import PyElectrolyteConcVolAvgSolver
    from bmslogic.simulations.cell.models import PySPMe 
except ModuleNotFoundError:
    sys.path.append(pathlib.Path(
        __file__).parent.parent.parent.parent.parent.parent.parent.__str__())
    from bmslogic.simulations.cell.solvers.electrolyte_conc import PyElectrolyteConcVolAvgSolver
    from bmslogic.simulations.cell.models import PySPMe


# Battery cell parameters
epsilon_ep: float = 0.485
epsilon_sep: float = 0.785
epsilon_en: float = 0.385
a_s_p: float = 7.28e3
a_s_n: float = 5.78e3
brugg: float = 4
t_c: float = 0.354
kappa_e: float = 0.2875
temp: float = 298.15
D_e: float = 3.5e-10
D_e_eff_p: float = D_e * (epsilon_ep**1.5)
D_e_eff_s: float = D_e * (epsilon_sep**1.5)
D_e_eff_n: float = D_e * (epsilon_en**1.5)
L_n: float = 7.35e-5
L_s: float = 2e-5
L_p: float = 7e-5

# Simulation parameters
dt: float = 0.1
t_end: int = 3600  # [s]

conc_solver: PyElectrolyteConcVolAvgSolver = PyElectrolyteConcVolAvgSolver(L_n=L_n, L_s=L_s, L_p=L_p,
                                                                           epsilon_n=epsilon_en,
                                                                           epsilon_s=epsilon_sep,
                                                                           epsilon_p=epsilon_ep,
                                                                           D_n=D_e_eff_n, D_s=D_e_eff_s, D_p=D_e_eff_p,
                                                                           a_n=a_s_n, a_p=a_s_p, t_c=t_c, c_e_init=1000)

j_p = PySPMe.molar_flux_electrode(
    I=-1.656, S=1.1167, electrode_type='p')  # [mol/m2/s]
j_sep = 0.0  # [mol/m2/s]
j_n = PySPMe.molar_flux_electrode(I=-1.656, S=0.7824, electrode_type='n') # [mol/m2/s]

# --------------------------------SIMULATION-----------------------------------------------------------------

x_n: np.ndarray = np.linspace(0.0, L_n, 10)
x_s: np.ndarray = np.linspace(L_n, L_n + L_s, 10)
x_p: np.ndarray = np.linspace(L_n+L_s, L_n+L_s+L_p, 10)
x: np.ndarray = np.append(x_n, np.append(x_s, x_p))

array_c_e_n: np.ndarray = conc_solver.conc_profile_n(L_value=x_n)
array_c_e_sep: np.ndarray = conc_solver.conc_profile_s(L_value=x_s)
array_c_e_p: np.ndarray = conc_solver.conc_profile_p(L_value=x_p)
array_c_e: np.ndarray = np.append(array_c_e_n, np.append(array_c_e_sep, array_c_e_p))

lst_0: list = conc_solver.array_c_e
lst_1000: list = []
lst_2000: list = []
lst_3000: list = []
lst_4000: list = []

t_prev: float = 0.0
max_iter: int = int(4000 / dt)

time_start: float = time.time() 
for i in range(max_iter):
    conc_solver.solve(t_prev=t_prev, avg_j_p=j_p, avg_j_n=j_n, dt=dt)
    t_prev += dt

    array_c_e_n: np.ndarray = conc_solver.conc_profile_n(L_value=x_n)
    array_c_e_sep: np.ndarray = conc_solver.conc_profile_s(L_value=x_s)
    array_c_e_p: np.ndarray = conc_solver.conc_profile_p(L_value=x_p)
    array_c_e: np.ndarray = np.append(array_c_e_n, np.append(array_c_e_sep, array_c_e_p))

    if i == 1000:
        lst_1000 = array_c_e.tolist()

    if i == 2000:
        lst_2000 = array_c_e.tolist()

    if i == 3000:
        lst_3000 = array_c_e.tolist()

    if i == 4000:
        lst_4000 = array_c_e.tolist()
time_end: int = time.time()

print(f"Solution Time [s]: {time_end-time_start}")

# ----------------------------------SAVE RESULTS ---------------------------------------------------------

FILE_DIR_TO_SAVE = os.path.join(pathlib.Path(__file__).parent, "saved_results")

with open(os.path.join(FILE_DIR_TO_SAVE, "poly_neg_discharge_t_0.pkl"), "wb") as pkl_file:
    pickle.dump(lst_0, pkl_file)

with open(os.path.join(FILE_DIR_TO_SAVE, "poly_neg_discharge_t_1000.pkl"), "wb") as pkl_file:
    pickle.dump(lst_1000, pkl_file)

with open(os.path.join(FILE_DIR_TO_SAVE, "poly_neg_discharge_t_2000.pkl"), "wb") as pkl_file:
    pickle.dump(lst_2000, pkl_file)

with open(os.path.join(FILE_DIR_TO_SAVE, "poly_neg_discharge_t_3000.pkl"), "wb") as pkl_file:
    pickle.dump(lst_3000, pkl_file)

with open(os.path.join(FILE_DIR_TO_SAVE, "poly_neg_discharge_t_4000.pkl"), "wb") as pkl_file:
    pickle.dump(lst_4000, pkl_file)

# -----------------------------------PLOTS --------------------------------------------------------------
plt.xlabel("Battery Cell Thickness [m]")
plt.ylabel("Electrolyte Conc. [mol/m3]")
plt.title(f"Electrolyte Conc. [mol/m3] after {max_iter * dt} s of discharge")
plt.ticklabel_format(axis="x", scilimits=[-3, 1])
plt.plot(x, lst_0, label="t=0s")
plt.plot(x, lst_1000, label="t=1000s")
plt.plot(x, lst_2000, label="t=2000s")
plt.plot(x, lst_3000, label="t=3000s")
plt.plot(x, lst_4000, label="t=4000s")

plt.legend()
plt.show()
