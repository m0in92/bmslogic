"""
This module is an example implementation of SPCPPy using the parameter_sets under dst discharge steps.
"""

__author__ = "Moin Ahmed"
__copyright__ = 'Copyright 2024 by BMSLogic. All rights reserved.'
__status__ = 'deployed'

import time

import numpy as np
import matplotlib.pyplot as plt

try:
    import bmslogic.simulations.cell.cell as cell_sim
    from bmslogic.simulations.cell.parameter_set_manager import ParameterSets
    from bmslogic.simulations.cell import pycyclers
    from bmslogic.simulations.cell.plot import Plot
except ModuleNotFoundError as e:
    import sys
    import pathlib

    sys.path.append(pathlib.Path(
        __file__).parent.parent.parent.parent.__str__())
    import bmslogic.simulations.cell.cell as cell_sim
    from bmslogic.simulations.cell.parameter_set_manager import ParameterSets
    from bmslogic.simulations.cell import pycyclers
    from bmslogic.simulations.cell.plot import Plot


from example_parameter import *


if __name__ == "__main__":
    SOC_init_p: float = 0.4952
    SOC_init_n: float = 0.7522
    battery_cell: cell_sim.BatteryCell = ParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=SOC_init_n,
                                                                                                  soc_p_init=SOC_init_p,
                                                                                                  T_amb=T,
                                                                                                  R_cell=R_cell)
    cycler: pycyclers.DSTCycler = pycyclers.DSTCycler(cap_nom=2.9,
                                                      V_min=2.5, V_max=4.2,
                                                      soc_min=0.0, soc_max=1.0, soc=1.0, dst_step=10)

    solver: cell_sim.BatterySolver = cell_sim.BatterySolver(battery_cell=battery_cell,
                                              is_isothermal=False,
                                              enable_degradation=False)
    sol: cell_sim.Solution = solver.solve(cycler=cycler)

    # plots
    Plot(sol=sol).plot_comprehensive()
