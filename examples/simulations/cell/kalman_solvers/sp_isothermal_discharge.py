import os
import pathlib
import sys

import numpy as np
import pandas as pd

try:
    from bmslogic.simulations.cell.plot import Plot
    from bmslogic.simulations.cell.parameter_set_manager import ParameterSets
    import bmslogic.simulations.cell.cell as cell_sim
except:
    PROJ_DIR: str = pathlib.Path(
        __file__).parent.parent.parent.parent.parent.__str__()
    sys.path.append(PROJ_DIR)
    from bmslogic.simulations.cell.plot import Plot
    from bmslogic.simulations.cell.parameter_set_manager import ParameterSets
    import bmslogic.simulations.cell.cell as cell_sim


SOC_init_p: float = 0.4952
SOC_init_n: float = 0.7522
T: float = 298.15
R_cell: float = 0.0028230038442483246

battery_cell: cell_sim.BatteryCell = ParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=SOC_init_n,
                                                                                              soc_p_init=SOC_init_p,
                                                                                              T_amb=T,
                                                                                              R_cell=R_cell)
# dc: cell_sim.DischargeRest = cell_sim.DischargeRest(current=discharge_current, V_min=V_min, soc_lib_min=soc_lib_min, soc_lib=soc_lib,
#                                         rest_time=3600)
t_exp: np.ndarray = np.arange(0, 3000, 0.1)
I_exp: np.ndarray = -1.656 * np.ones(len(t_exp))
V_obs = 4.2 * np.ones(len(t_exp))

spkf: cell_sim.SPKFSolver = cell_sim.SPKFSolver(battery_cell, False, False,
                                                SOC_init_p, SOC_init_n, 1e-3, 1e-3,
                                                1e-3, 1e-3)
print(spkf.get_p)
# sol: cell_sim.Solution = spkf.solve(t_exp, I_exp, V_obs)

# plots
Plot(sol=sol).plot_comprehensive()
