"""
This module is an example implementation of SPCPPy using the parameter_sets for a cycling step involving charge, rest, discharge, and rest steps.
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
    charge_current: float = 1.5
    discharge_current: float = 1.5
    soc_lib_min: float = 0.0
    soc_lib_max: float = 1.0
    V_min: float = 2.5
    V_max: float = 4.2
    rest_time: float = 3600  # in seconds
    soc_p_init: float = 0.9464153612484812
    soc_n_init: float = 0.04495402282492643

    battery_cell: cell_sim_.BatteryCell = ParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=soc_n_init,
                                                                                                   soc_p_init=soc_p_init,
                                                                                                   T_amb=T,
                                                                                                   R_cell=R_cell)
    cycler: cell_sim_.ChargeDischarge = cell_sim_.ChargeDischarge(charge_current=charge_current, discharge_current=discharge_current,
                                                                  V_min=V_min, V_max=V_max,
                                                                  soc_min=soc_lib_min, soc_max=soc_lib_max, soc=0.0,
                                                                  rest_time=rest_time)

    solver: cell_sim_.BatterySolver = cell_sim_.BatterySolver(battery_cell=battery_cell,
                                                              is_isothermal=True,
                                                              enable_degradation=False)
    sol: cell_sim_.Solution = solver.solve(cycler=cycler)

    # plots
    Plot(sol=sol).plot_comprehensive()
