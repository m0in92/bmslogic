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
df = pd.read_csv(os.path.join(pathlib.Path(__file__).parent.__str__(), 'example_data.csv'))
cycler = cell_sim.PyCustomCycler(array_t=df['t [s]'].to_numpy(), array_I=df['I [A]'].to_numpy(), SOC_LIB=1.0,
                                 V_min=V_min, V_max=V_max)
solver = cell_sim.PySPSolver(b_cell=cell, isothermal=True, degradation=False)

# simulate and plot
sol = solver.solve(cycler_instance=cycler, verbose=False, termination_criteria='V_min')

sol.plot_tV()
