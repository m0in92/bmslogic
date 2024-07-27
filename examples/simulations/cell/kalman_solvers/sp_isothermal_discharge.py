import os
import pathlib
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

discharge_current: float = 1.5
V_min: float = 2.5
V_max: float = 4.2
soc_lib_min: float = 0.0
soc_lib_max: float = 1.0
soc_lib: float = 1.0

T_END: float = 4000   # [s]
TIME_INCREMENT: float = 0.2  # [s]
CURRENT_NOISE_STD: float = 0.001  # [A]
VOLTAGE_SENSOR_NOISE_STD: float = 0.01  # [V]

# t: np.ndarray = np.arange(0, T_END, TIME_INCREMENT)
# I_true: np.ndarray = -1.656 * np.ones(len(t))
# I_noise: np.ndarray = I_true + \
#     np.random.normal(loc=0.0, scale=CURRENT_NOISE_STD, size=len(I_true))

battery_cell: cell_sim.BatteryCell = ParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=SOC_init_n,
                                                                                              soc_p_init=SOC_init_p,
                                                                                              T_amb=T,
                                                                                              R_cell=R_cell)
battery_cell_spkf: cell_sim.BatteryCell = ParameterSets(name='test').generate_BatteryCell_instance(soc_n_init=SOC_init_n,
                                                                                                   soc_p_init=SOC_init_p,
                                                                                                   T_amb=T,
                                                                                                   R_cell=R_cell)
# dc: cell_sim.Discharge = cell_sim.Discharge(
#     current=discharge_current, V_min=V_min, soc_lib_min=soc_lib_min, soc_lib=soc_lib)
# dc_true: cell_sim.CustomCycler = cell_sim.CustomCycler(
#     t_array=t, current_array=I_true, V_min=V_min, V_max=V_max, soc_lib_min=0.0, soc_lib_max=1.0, soc_lib=1.0)
# dc: cell_sim.CustomCycler = cell_sim.CustomCycler(
#     t_array=t, current_array=I_noise, V_min=V_min, V_max=V_max, soc_lib_min=0.0, soc_lib_max=1.0, soc_lib=1.0)
t: np.ndarray = np.linspace(0, 5000, 100 * 3601)
I: np.ndarray = -1.656 * np.ones(len(t)) + np.random.normal(loc=0.0, scale=CURRENT_NOISE_STD, size=len(t))
cycler: cell_sim.CustomCycler = cell_sim.CustomCycler(t_array=t, current_array=I,
                                                      V_min=V_min, V_max=V_max,
                                                      soc_lib_min=soc_lib_min, soc_lib_max=soc_lib_max,
                                                      soc_lib=soc_lib)
solver: cell_sim.BatterySolver = cell_sim.BatterySolver(battery_cell=battery_cell,
                                                        is_isothermal=True,
                                                        enable_degradation=False, electrode_soc_solver="poly")
sol: cell_sim.Solution = solver.solve(cycler=cycler, store_solution_iter=1)

t_exp: np.ndarray = sol.t
# I_exp: np.ndarray = -discharge_current * \
#     np.ones(len(t_exp)) + np.random.normal(0, 0.05, len(t_exp))
V_obs: np.ndarray = sol.V + np.random.normal(0, 0.05, len(t_exp))

spkf: cell_sim.SPKFSolver = cell_sim.SPKFSolver(battery_cell_spkf, False, False,
                                                SOC_init_p, SOC_init_n, 1e-3, 1e-3,
                                                1e-3, 1e-2)
sol_spkf: cell_sim.Solution = spkf.solve(t_exp, 0.12 * I, V_obs)

# plots
fig = plt.figure()

ax1 = fig.add_subplot(221)
ax1.plot(t_exp, V_obs)
ax1.plot(sol_spkf.t, sol_spkf.V)

ax2 = fig.add_subplot(222)
ax2.plot(sol.t, sol.soc_p)
ax2.plot(sol_spkf.t, sol_spkf.soc_p)

ax3 = fig.add_subplot(223)
ax3.plot(sol.t, sol.soc_p)
ax3.plot(sol_spkf.t, sol_spkf.soc_p)

plt.show()
# # Plot(sol=sol_spkf).plot_comprehensive()
