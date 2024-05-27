"""
This module is an example implementation of SPCPPy using the parameter_sets under hppc discharge steps.
"""

__author__ = "Moin Ahmed"
__copyright__ = 'Copyright 2024 by SPCPPy. All rights reserved.'
__status__ = 'deployed'

import time
import os
import pathlib
import pickle
import sys

import numpy as np
import matplotlib.pyplot as plt

try:
    import bmslogic.simulations.cell.cell as cell_sim
    from bmslogic.simulations.cell import pycyclers
    from bmslogic.simulations.cell.plot import Plot

    from examples.simulations.cell.example_parameter import *

except ModuleNotFoundError as e:
    PROJECT_DIR: str = pathlib.Path(
        __file__).parent.parent.parent.parent.__str__()
    print(PROJECT_DIR)
    sys.path.append(PROJECT_DIR)

    import bmslogic.simulations.cell.cell as cell_sim
    from bmslogic.simulations.cell import pycyclers
    from bmslogic.simulations.cell.plot import Plot

    from examples.simulations.cell.example_parameter import *

# import SPCPPY as sp
# from SPCPPY import pycyclers

# from examples.example_parameter import *


if __name__ == "__main__":
    SOC_init_p: float = 0.4952
    SOC_init_n: float = 0.7522
    battery_cell: cell_sim.BatteryCell = cell_sim.PyParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=SOC_init_n,
                                                                                                             soc_p_init=SOC_init_p,
                                                                                                             T_amb=T,
                                                                                                             R_cell=R_cell)
    cycler: pycyclers.HPPCCycler = pycyclers.HPPCCycler(t1=500, t2=100, i_app=1.5,
                                                        charge_or_discharge='discharge',
                                                        V_min=2.5, V_max=4.2, soc_lib_min=0.0,
                                                        soc_lib_max=1.0, soc_lib=1.0, hppc_steps=100)

    solver: sp.BatterySolver = sp.BatterySolver(battery_cell=battery_cell,
                                                is_isothermal=True,
                                                enable_degradation=False)
    sol: sp.Solution = solver.solve(cycler=cycler)

    # plots
    sp.Plot(sol=sol).plot_comprehensive()
