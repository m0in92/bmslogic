"""
This module is an example implementation of SPCPPy using the NElectrode, PElectrode, Electrolyte, and BatteryCell class using the custom cycler.
"""

__author__ = "Moin Ahmed"
__copyright__ = 'Copyright 2024 by BMSLogic. All rights reserved.'
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

from example_parameter import *


if __name__ == "__main__":
    SOC_init_p: float = 0.4952
    SOC_init_n: float = 0.7522
    soc_lib_min: float = 0.0
    soc_lib_max: float = 1.0
    V_min: float = 2.5
    V_max: float = 4.2
    soc_lib: float = 0.0

    battery_cell: cell_sim.BatteryCell = ParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=SOC_init_n,
                                                                                                  soc_p_init=SOC_init_p,
                                                                                                  T_amb=T,
                                                                                                  R_cell=R_cell)

    t: np.ndarray = np.linspace(0, 5000, 100 * 3601)
    I: np.ndarray = -1.656 * np.ones(len(t))
    cycler: cell_sim.CustomCycler = cell_sim.CustomCycler(t_array=t, current_array=I,
                                                          V_min=V_min, V_max=V_max,
                                                          soc_lib_min=soc_lib_min, soc_lib_max=soc_lib_max,
                                                          soc_lib=soc_lib)
    solver: cell_sim.BatterySolver = cell_sim.BatterySolver(battery_cell=battery_cell,
                                                            is_isothermal=True,
                                                            enable_degradation=False)
    sol: cell_sim.Solution = solver.solve(cycler=cycler)

    # plots
    Plot(sol=sol).plot_comprehensive()
