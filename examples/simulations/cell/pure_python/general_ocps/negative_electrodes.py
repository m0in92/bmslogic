"""
Example of the usage of open-circuit potentials (OCP) of the negative electrodes
"""

__all__ = []

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by Moin Ahmed. All Rights Reserved."
__status__ = "Deployed"


import numpy as np
import matplotlib.pyplot as plt

from bmslogic import cell_sim


electrode_temp = 298.15
SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al


SOC_PC: np.ndarray = np.linspace(1e-12, 0.69)
OCP_PC: np.ndarray = cell_sim.general_ocps.PetroleumCoke(soc=SOC_PC)

SOC_graphite: np.ndarray = np.linspace(0, 0.815)
OCP_graphite: np.ndarray = cell_sim.general_ocps.graphite(soc=SOC_graphite)

SOC_MCMC: np.ndarray = np.linspace(0.32, 0.85)
OCP_MCMB: np.ndarray = cell_sim.general_ocps.MCMB(soc=SOC_MCMC)

SOC_HardCarbon: np.ndarray = np.linspace(0.2, 0.65)
OCP_HardCarbon: np.ndarray =cell_sim.general_ocps.HardCarbon(soc=SOC_HardCarbon)

SOC_LTO: np.ndarray = np.linspace(0, 1)
OCP_LTO: np.ndarray = cell_sim.general_ocps.LTO(soc=SOC_HardCarbon)

# Plots
plt.plot(SOC_PC, OCP_PC, label="Petroleum Coke")
plt.plot(SOC_graphite, OCP_graphite, label="graphite")
plt.plot(SOC_MCMC, OCP_MCMB, label="MCMB")
plt.plot(SOC_HardCarbon, OCP_HardCarbon, label="Hard Carbon")
plt.plot(SOC_LTO, OCP_LTO, label="LTO")

plt.grid()
plt.legend()
plt.show()


