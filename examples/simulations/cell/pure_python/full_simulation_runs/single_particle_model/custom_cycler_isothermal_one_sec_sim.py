"""
Contains the example implementation of SPPy using custom cycler under isothermal conditions.
"""

__all__ = []

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2023 by BMSLogic. All rights reserved.'
__status__ = 'deployed'


import os
import pathlib  # os and pathlib are imported to define the absolute file path of the extracted csv
import sys

import pandas as pd
import matplotlib.pyplot as plt

try:
    from bmslogic import cell_sim
except ModuleNotFoundError as e:
    PROJECT_DIR: str = pathlib.Path(
        __file__).parent.parent.parent.parent.parent.parent.parent.__str__()
    sys.path.append(PROJECT_DIR)

    from bmslogic import cell_sim


# Operating parameters
I = 1.656
T = 298.15
V_min = 4.08
V_max = 4
num_cycles = 10
charge_current = 1.656
discharge_current = 1.656
rest_time = 30

# Modelling parameters
# conditions in the literature source. Guo et al
SOC_init_p, SOC_init_n = 0.4956, 0.7568

# Setup battery components
cell = cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='Gao-Randall-Han',
                                                      soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                      temp_init=T)

# set-up cycler and solver. Also plot the cycler time [s] and current [A]. For this example the data is extracted from
# a csv file.
df = pd.read_csv(os.path.join(pathlib.Path(
    __file__).parent.__str__(), 'example_data.csv'))
cycler = cell_sim.PyCustomCycler(array_t=df['t [s]'].to_numpy(), array_I=df['I [A]'].to_numpy(), SOC_LIB=1.0,
                                 V_min=V_min, V_max=V_max)
# cycler.t_max = 1.0
solver = cell_sim.PySPSolver(
    b_cell=cell, isothermal=True, degradation=False, electrode_SOC_solver="poly")

# simulate and collect results at every set interval
t_curr: float = 0.0
lst_t_end: list = []
lst_V: list = []
dt: float = 50
t_end: float = 600
for i in range(int(t_end/dt)):
    t_cycle_end = t_curr + dt
    sol = solver.solve(cycler_instance=cycler, verbose=False,
                       termination_criteria='time', t_sim_max=t_cycle_end)
    t_curr += dt
    print("Anticpated End Time [s]: ", t_curr, "Actual End Time [s]",
          sol.t[-1], "Calcuated V [V]: ", sol.V[-1])
    lst_t_end.append(sol.t[-1])
    lst_V.append(sol.V[-1])

# plots
plt.plot(sol.t, sol.V)
plt.scatter(lst_t_end, lst_V, color='red')

plt.show()
