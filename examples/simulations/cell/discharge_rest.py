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
    SOC_init_p: float = 0.4952
    SOC_init_n: float = 0.7522

    battery_cell: cell_sim_.BatteryCell = ParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=SOC_init_n,
                                                                                                  soc_p_init=SOC_init_p,
                                                                                                  T_amb=T,
                                                                                                  R_cell=R_cell)
    dc: cell_sim_.DischargeRest = cell_sim_.DischargeRest(current=discharge_current, V_min=V_min, soc_lib_min=soc_lib_min, soc_lib=soc_lib,
                                            rest_time=3600)

    solver: cell_sim_.BatterySolver = cell_sim_.BatterySolver(battery_cell=battery_cell,
                                                is_isothermal=True,
                                                enable_degradation=False)
    sol: cell_sim_.Solution = solver.solve(cycler=dc)

    # examples of simulation results
    print("soc_p the end of the simulation: ", sol.soc_p[-1],
          "soc_n the end of the simulation: ", sol.soc_n[-1])

    # plots
    Plot(sol=sol).plot_comprehensive()
