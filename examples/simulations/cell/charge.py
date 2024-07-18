"""
This module is an example implementation of SPCPPy using the parameter_sets for a cycling step involving discharge and rest steps.
"""

__author__ = "Moin Ahmed"
__copyright__ = 'Copyright 2024 by SPCPPy. All rights reserved.'
__status__ = 'deployed'

import time

import numpy as np
import matplotlib.pyplot as plt

try:
    import bmslogic.simulations.cell.cell as cell_sim
    from bmslogic.simulations.cell.parameter_set_manager import ParameterSets
    from bmslogic.simulations.cell.plot import Plot

    from examples.simulations.cell.example_parameter import *

except ModuleNotFoundError as e:
    import sys
    import pathlib

    PROJECT_DIR: str = pathlib.Path(
        __file__).parent.parent.parent.parent.__str__()
    print(PROJECT_DIR)
    sys.path.append(PROJECT_DIR)

    from bmslogic import cell_sim
    import bmslogic.simulations.cell.cell as cell_sim_
    from bmslogic.simulations.cell.parameter_set_manager import ParameterSets
    from bmslogic.simulations.cell.plot import Plot

    from examples.simulations.cell.example_parameter import *


if __name__ == "__main__":
    soc_p_init: float = 0.9464153612484812
    soc_n_init: float = 0.04495402282492643
    charge_current: float = 1.5

    battery_cell: cell_sim_.BatteryCell = ParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=soc_n_init,
                                                                                               soc_p_init=soc_p_init,
                                                                                               T_amb=T,
                                                                                               R_cell=R_cell)
    cc: cell_sim_.Charge = cell_sim_.Charge(
        current=charge_current, V_max=V_max, soc_lib_max=soc_lib_min, soc_lib=soc_lib)

    solver: cell_sim_.BatterySolver = cell_sim_.BatterySolver(battery_cell=battery_cell,
                                                is_isothermal=True,
                                                enable_degradation=False)
    sol: cell_sim_.Solution = solver.solve(cycler=cc)

    # plots
    Plot(sol=sol).plot_comprehensive()
