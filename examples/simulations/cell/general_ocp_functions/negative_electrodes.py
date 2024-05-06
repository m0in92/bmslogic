import numpy as np
import matplotlib.pyplot as plt

from cpp_modules.solvers import graphite


SOC_graphite: np.ndarray = np.linspace(0, 0.8)
OCP_graphite: np.ndarray = graphite(soc=SOC_graphite)


plt.plot(SOC_graphite, OCP_graphite)

plt.xlabel("SOC")
plt.ylabel("OCP [V]")

plt.title("OCP of Negative Electrodes at 298.15 K")
plt.show()
