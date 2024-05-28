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
    dc: cell_sim_.Discharge = cell_sim_.Discharge(
        current=discharge_current, V_min=V_min, soc_lib_min=soc_lib_min, soc_lib=soc_lib)

    solver: cell_sim_.BatterySolver = cell_sim_.BatterySolver(battery_cell=battery_cell,
                                                            is_isothermal=True,
                                                            enable_degradation=False)
    cpp_sol: cell_sim_.Solution = solver.solve(cycler=dc)

    # plots
    # Plot(sol=sol).plot_comprehensive()

    # ------------------------------------------------ Pure Python ----------------------------------------------------------
    # Setup battery components
    cell: cell_sim.PyBatteryCell = cell_sim.PyBatteryCell.read_from_parametersets(parameter_set_name='test',
                                                                                  soc_init_p=SOC_init_p, soc_init_n=SOC_init_n,
                                                                                  temp_init=T)

    # set-up cycler and solver
    dc: cell_sim.PyDischarge = cell_sim.PyDischarge(discharge_current=discharge_current, v_min=V_min,
                                                    SOC_LIB_min=soc_lib_min, SOC_LIB=soc_lib)
    solver: cell_sim.PySPSolver = cell_sim.PySPSolver(b_cell=cell,
                                                      isothermal=True, degradation=False,
                                                      electrode_SOC_solver='poly')

    # simulate
    py_sol: cell_sim.PySolution = solver.solve(cycler_instance=dc)

    print(py_sol.t[0], py_sol.V[0])
    print(cpp_sol.t[1], cpp_sol.V[1])

    # Plots
    plt.plot(cpp_sol.t, cpp_sol.V)
    plt.plot(py_sol.t, py_sol.V)

    plt.show()
