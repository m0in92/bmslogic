"""
Contains the example implementation of SPPy using custom cycler under isothermal conditions.
"""

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2024 by SPPy. All rights reserved.'
__status__ = 'development'


import pathlib
import os  # os and pathlib is used to define the module path.

import pandas as pd

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
cell = cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='Gao-Randall-Han',
                                                      soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                      temp_init=T)

# set-up cycler and solver. Also plot the cycler time [s] and current [A]. For this example the data is extracted from
# a csv file.
df = pd.read_csv(os.path.join(pathlib.Path(__file__).parent.__str__(), 'example_data.csv'))
cycler = cell_sim.PyHPPCCycler(t1=500, t2=100, i_app=1.5,
                               charge_or_discharge='discharge',
                               V_min=2.5, V_max=4.2, soc_lib_min=0.0,
                               soc_lib_max=1.0, soc_lib=1.0, hppc_steps=10)
cycler.plot()
solver = cell_sim.PySPSolver(b_cell=cell, isothermal=True, degradation=False,
                             electrode_SOC_solver="poly")

# simulate and plot
sol = solver.solve(cycler_instance=cycler, verbose=False)

sol.comprehensive_isothermal_plot()
