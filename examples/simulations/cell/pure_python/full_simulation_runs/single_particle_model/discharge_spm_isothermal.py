"""
This script contains the example usage of the single particle model for the discharge operation.
"""

__all__ = []

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2024 by BMSLogic. All rights reserved.'
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
temp: float = 298.15
V_min: float = 3
SOC_min: float = 0.1
soc_lib_init: float = 1.0

# Modelling parameters
SOC_init_p: float = 0.4956  # from Guo et. al.
SOC_init_n: float = 0.7568  # from Guo et. al.

# Setup battery components
cell: cell_sim.PyBatteryCell = cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='Gao-Randall-Han',
                                                                              soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                                              temp_init=temp)

# set-up cycler and solver
dc: cell_sim.PyDischarge = cell_sim.PyDischarge(discharge_current=I, v_min=V_min,
                                                SOC_LIB_min=SOC_min, SOC_LIB=soc_lib_init)
solver: cell_sim.PySPSolver = cell_sim.PySPSolver(b_cell=cell,
                                                  isothermal=True, degradation=False,
                                                  electrode_SOC_solver='poly')

# simulate
sol: cell_sim.PySolution = solver.solve(cycler_instance=dc)

# Save Results
DIR_TO_SAVE: str = os.path.join(pathlib.Path(__file__).parent.__str__(), "saved_results")

with open(os.path.join(DIR_TO_SAVE, "discharge_spm_isothermal_time.pkl"), "wb") as pkl_file:
    pickle.dump(sol.t.tolist(), pkl_file)

with open(os.path.join(DIR_TO_SAVE, "discharge_spm_isothermal_V.pkl"), "wb") as pkl_file:
    pickle.dump(sol.V.tolist(), pkl_file)


# Plot
sol.comprehensive_isothermal_plot()
