"""
This script contains the example usage of the single particle model in the charge operation.
"""

__all__ = []

__author__ = 'Moin Ahmed'
__copywrite__ = 'Copyright 2024 by BMSLogic. All rights reserved.'
__status__ = 'Deployed'

# try/except block are used since the user of this script can call this Python module from any file path.
# If the user calls this module from a path other than the project directory, then the except block appends the
# absolute path to the project directory to the system path.
import os
import pathlib
import pickle
import sys

try:
    from bmslogic import cell_sim
except ModuleNotFoundError as e:
    PROJECT_DIR: str = pathlib.Path(
        __file__).parent.parent.parent.parent.parent.parent.parent.__str__()
    sys.path.append(PROJECT_DIR)

    from bmslogic import cell_sim


# Operating parameters
I: float = 1.656
T: float = 298.15
V_max: float = 4.2
SOC_max: float = 0.9
SOC_LIB: float = 0.9

# Modelling parameters
SOC_init_p: float = 0.989011
SOC_init_n: float = 0.01890232

# Setup battery components
cell:cell_sim.PyBatteryCell =cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='Gao-Randall-Han',
                                                                  soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                                  temp_init=T)

# set-up cycler and solver
dc:cell_sim.PyCharge =cell_sim.PyCharge(charge_current=I, V_max=V_max, SOC_LIB_max=SOC_max, SOC_LIB=SOC_LIB)
solver:cell_sim.PySPSolver =cell_sim.PySPSolver(b_cell=cell, isothermal=False, degradation=False,
                                          electrode_SOC_solver='poly')

# simulate
sol: cell_sim.PySolution = solver.solve(cycler_instance=dc)

# Save Results

DIR_TO_SAVE: str = os.path.join(pathlib.Path(__file__).parent.__str__(), "saved_results")

with open(os.path.join(DIR_TO_SAVE, "charge_spm_non_isothermal_time.pkl"), "wb") as pkl_file:
    pickle.dump(sol.t.tolist(), pkl_file)

with open(os.path.join(DIR_TO_SAVE, "charge_spm_non_isothermal_V.pkl"), "wb") as pkl_file:
    pickle.dump(sol.V.tolist(), pkl_file)

# Plot
sol.comprehensive_isothermal_plot()
