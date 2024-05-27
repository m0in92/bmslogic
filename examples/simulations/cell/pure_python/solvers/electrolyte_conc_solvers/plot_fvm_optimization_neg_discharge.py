import pathlib
import pickle
import os

import matplotlib
import matplotlib.pyplot as plt


# ----------------------------------------OPEN FILES---------------------------------------------
FILE_DIR_TO_OPEN: str = os.path.join(pathlib.Path(__file__).parent.__str__(), "saved_results")

# CN solvers below
with open(os.path.join(FILE_DIR_TO_OPEN, "fvm_inverse_neg_discharge_x.pkl"), "rb") as pkl_file:
    x: list = pickle.load(pkl_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "fvm_neg_discharge_t_0.pkl"), "rb") as pkl_file:
    lst_0: list = pickle.load(pkl_file)

# eigen solvers below
with open(os.path.join(FILE_DIR_TO_OPEN, "fvm_neg_discharge_t_1000.pkl"), "rb") as pkl_file:
    lst_1000: list = pickle.load(pkl_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "fvm_neg_discharge_t_2000.pkl"), "rb") as pkl_file:
    lst_2000: list = pickle.load(pkl_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "fvm_neg_discharge_t_3000.pkl"), "rb") as pkl_file:
    lst_3000: list = pickle.load(pkl_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "fvm_neg_discharge_t_4000.pkl"), "rb") as pkl_file:
    lst_4000: list = pickle.load(pkl_file)

# ----------------------PLOTS----------------------------------------------------------------------------

matplotlib.rc('xtick', labelsize=12) 
matplotlib.rc('ytick', labelsize=12) 

# plt.plot(inverse_co_ord_x, inverse_conc, label="Inverse")
# plt.plot(TDMA_co_ord_x, TDMA_conc, label="TDMA")
# plt.plot(lst_poly_time_two, lst_poly_soc_two, label="Polynomial Approximation - Two Order")
plt.plot(x, lst_0, label="t=0s")
plt.plot(x, lst_1000, label="t=1000s")
plt.plot(x, lst_2000, label="t=2000s")
plt.plot(x, lst_3000, label="t=3000s")
plt.plot(x, lst_4000, label="t=4000s")

plt.xlabel("x [$m$]", fontsize=15)
plt.ylabel("Electrolyte Conc. [$mol/m^3$]", fontsize=15)
plt.legend(fontsize=12)
plt.tight_layout()
plt.ticklabel_format(style='sci', axis='x', scilimits=(-3,5), useMathText=True)
plt.show()
