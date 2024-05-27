import os
import pathlib
import pickle
import sys

import matplotlib
import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------OPEN FILES------------------------------------------------------------------------
FILE_DIR_TO_OPEN: str = os.path.join(pathlib.Path(__file__).parent.__str__(), "saved_results")

with open(os.path.join(FILE_DIR_TO_OPEN, "discharge_rest_spm_isothermal_time.pkl"), "rb") as pkl_cn_file:
    sol_time: list = pickle.load(pkl_cn_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "discharge_rest_spm_isothermal_V.pkl"), "rb") as pkl_cn_file:
    sol_V: list = pickle.load(pkl_cn_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "discharge_rest_espm_isothermal_time.pkl"), "rb") as pkl_cn_file:
    sol_espm_time: list = pickle.load(pkl_cn_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "discharge_rest_espm_isothermal_V.pkl"), "rb") as pkl_cn_file:
    sol_espm_V: list = pickle.load(pkl_cn_file)

# ----------------------------------------PLOTS------------------------------------------------------------------------
# Plots
matplotlib.rc('xtick', labelsize=12) 
matplotlib.rc('ytick', labelsize=12) 

plt.plot(sol_time, sol_V, label="SPM")
plt.plot(sol_espm_time, sol_espm_V, label="Enhanced SPM")

plt.xlabel("Time [$s$]", fontsize=15)
plt.ylabel("Terminal Voltage [$V$]", fontsize=15)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

