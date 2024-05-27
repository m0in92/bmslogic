"""
Contains an example of using electrolyte solver in a simulation. The solver uses numerical finite volume
method (FVM).
"""
__author__ = "Moin Ahmed"
__copyright__ = "Copyright SPPy 2024. All rights reserved."
__status__ = "Deployed"

import os
import pathlib
import pickle
import time
import sys

import numpy as np
import matplotlib.pyplot as plt
from memory_profiler import profile

sys.path.append(pathlib.Path(
    __file__).parent.parent.parent.parent.parent.parent.parent.__str__())
from bmslogic.simulations.cell.solvers.electrolyte_conc import PyElectrolyteFVMCoordinates
from bmslogic.simulations.cell.solvers.electrolyte_conc import PyElectrolyteConcFVMSolver
from bmslogic.simulations.cell.models import PySPMe


# Simulation parameters
dt: float = 0.1
max_iter: int = int(4000 / dt)

# Create solver instances
co_ords: PyElectrolyteFVMCoordinates = PyElectrolyteFVMCoordinates(
    L_n=8e-5, L_s=2.5e-5, L_p=8.8e-5)
conc_solver_inverse: PyElectrolyteConcFVMSolver = PyElectrolyteConcFVMSolver(fvm_co_ords=co_ords, transference=0.354,
                                                                             epsilon_en=0.385, epsilon_esep=0.785, epsilon_ep=0.485,
                                                                             a_sn=5.78e3, a_sp=7.28e3,
                                                                             D_e=3.5e-10,
                                                                             brugg=4,
                                                                             c_e_init=1000)
conc_solver_TDMA: PyElectrolyteConcFVMSolver = PyElectrolyteConcFVMSolver(fvm_co_ords=co_ords, transference=0.354,
                                                                             epsilon_en=0.385, epsilon_esep=0.785, epsilon_ep=0.485,
                                                                             a_sn=5.78e3, a_sp=7.28e3,
                                                                             D_e=3.5e-10,
                                                                             brugg=4,
                                                                             c_e_init=1000)

# print(conc_solver_inverse.M_ce(dt=dt))

# specify the flux
j_p = PySPMe.molar_flux_electrode(
    I=-1.656, S=1.1167, electrode_type='p') * np.ones(len(co_ords.array_x_p))  # [mol/m2/s]
j_sep = np.zeros(len(co_ords.array_x_s))  # [mol/m2/s]
j_n = PySPMe.molar_flux_electrode(
    I=-1.656, S=0.7824, electrode_type='n') * np.ones(len(co_ords.array_x_n))  # [mol/m2/s]
j = np.append(np.append(j_n, j_sep), j_p)  # [mol/m2/s]


@profile
def perform_inverse() -> tuple[np.ndarray, np.ndarray]:
    time_start: int = time.time()
    for i in range(max_iter):
        conc_solver_inverse.solve_ce(j=j, dt=dt, solver_method='inverse')
    time_end: int = time.time()

    print("Simulation loop solution time [s] for the inverse matrix", time_end - time_start, " s.")


@profile
def perform_TDMA() -> tuple[np.ndarray, np.ndarray]:
    time_start: int = time.time()
    for i in range(max_iter):
        conc_solver_TDMA.solve_ce(j=j, dt=dt, solver_method='TDMA')
    time_end: int = time.time()

    print("Simulation loop solution time [s] for the TDMA", time_end - time_start, " s.")
    return co_ords.array_x, conc_solver_inverse.array_c_e

# -----------------------------------------------Perform profiler ---------------------------------------------------
perform_inverse()
perform_TDMA()

