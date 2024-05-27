"""
Contains the example implementation of SPPy using custom cycler under isothermal conditions.
"""

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2024 by SPPy. All rights reserved.'
__status__ = 'development'

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
V_min: float = 3
V_max: float = 4
num_cycles: float = 10
charge_current: float = 1.656
discharge_current: float = 1.656
rest_time: float = 30

# Modelling parameters
# conditions in the literature source. Guo et al
SOC_init_p, SOC_init_n = 0.4956, 0.7568

# Setup battery components
cell = cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='test',
                                                      soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                      temp_init=T)

# set-up cycler and solver. Also plot the cycler time [s] and current [A]. For this example the data is extracted from
# a csv file.
# df = pd.read_csv(os.path.join(pathlib.Path(__file__).parent.__str__(), 'example_data.csv'))
cycler = cell_sim.PyHPPCCycler(t1=50, t2=100, i_app=1.5,
                               charge_or_discharge='discharge',
                               V_min=2.5, V_max=4.2, soc_lib_min=0.0,
                               soc_lib_max=1.0, soc_lib=1.0, hppc_steps=100)
# cycler.plot()
solver: cell_sim.PyEnhancedSPSolver = cell_sim.PyEnhancedSPSolver(b_cell=cell, electrode_soc_solver="poly",
                                                                  isothermal=True, degradation=False)

# simulate and plot
sol = solver.solve(cycler=cycler, verbose=False)

# Save Results
DIR_TO_SAVE: str = os.path.join(pathlib.Path(__file__).parent.__str__(), "saved_results")

with open(os.path.join(DIR_TO_SAVE, "hppc_espm_isothermal_time.pkl"), "wb") as pkl_file:
    pickle.dump(sol.t.tolist(), pkl_file)

with open(os.path.join(DIR_TO_SAVE, "hppc_espm_isothermal_V.pkl"), "wb") as pkl_file:
    pickle.dump(sol.V.tolist(), pkl_file)

# Plot
sol.comprehensive_isothermal_plot()
