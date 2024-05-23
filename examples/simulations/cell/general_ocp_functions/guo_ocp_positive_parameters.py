import pathlib 
import sys

import numpy as np
import matplotlib 
import matplotlib.pyplot as plt

sys.path.append(pathlib.Path(__file__).parent.parent.parent.parent.parent.__str__())
from bmslogic.parameter_sets.test.funcs import OCP_ref_n, OCP_ref_p


soc_p: np.ndarray = np.linspace(0.4, 1)
ocp_p: np.ndarray = OCP_ref_p(soc_p)

plt.plot(soc_p, ocp_p)
plt.vlines(0.4956, 3, 5, 'r', linestyles='dotted', label="$soc_p^{max}$")
plt.vlines(0.98901, 3, 5, 'r', linestyles='dotted', label="$soc_p^{max}$")

matplotlib.rc('xtick', labelsize=12) 
matplotlib.rc('ytick', labelsize=12) 

plt.ylabel("$U_p$", fontsize=15)
plt.xlabel('$soc_p$', fontsize=15)
plt.legend(loc="upper center")
plt.tight_layout()
plt.show()



