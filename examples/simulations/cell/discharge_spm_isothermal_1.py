"""
This module is an example simulation run using single particle model under CC discharge.
"""

__author__ = "Moin Ahmed"
__copyright__ = 'Copyright 2024 by SPCPPy. All rights reserved.'
__status__ = 'deployed'

import pathlib
import sys

import numpy as np
import matplotlib.pyplot as plt


try:
    import bmslogic.simulations.cell.cell as cell_sim
    from bmslogic.simulations.cell.parameter_set_manager import ParameterSets
    from bmslogic.simulations.cell.plot import Plot

    from examples.simulations.cell.example_parameter import *

except ModuleNotFoundError as e:
    PROJECT_DIR: str = pathlib.Path(
        __file__).parent.parent.parent.parent.__str__()
    print(PROJECT_DIR)
    sys.path.append(PROJECT_DIR)

    from bmslogic import cell_sim
    import bmslogic.simulations.cell.cell as cell_sim
    from bmslogic.simulations.cell.parameter_set_manager import ParameterSets
    from bmslogic.simulations.cell.plot import Plot

    from examples.simulations.cell.example_parameter import *


if __name__ == "__main__":
    SOC_init_p: float = 0.4952
    SOC_init_n: float = 0.7522

    battery_cell: cell_sim.BatteryCell = ParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=SOC_init_n,
                                                                                                  soc_p_init=SOC_init_p,
                                                                                                  T_amb=T,
                                                                                                  R_cell=R_cell)
    dc: cell_sim.Discharge = cell_sim.Discharge(
        current=discharge_current, V_min=V_min, soc_lib_min=soc_lib_min, soc_lib=soc_lib)

    solver: cell_sim.BatterySolver = cell_sim.BatterySolver(battery_cell=battery_cell,
                                                            is_isothermal=True,
                                                            enable_degradation=False)
    sol: cell_sim.Solution = solver.solve(cycler=dc, store_solution_iter=10)

    # plots
    Plot(sol=sol).plot_comprehensive()
