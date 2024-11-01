import os
import pathlib
import pickle
import sys

import matplotlib
import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------OPEN FILES------------------------------------------------------------------------
FILE_DIR_TO_OPEN: str = os.path.join(pathlib.Path(__file__).parent.__str__(), "saved_results")

with open(os.path.join(FILE_DIR_TO_OPEN, "discharge_spm_isothermal_time.pkl"), "rb") as pkl_file:
    sol_time: list = pickle.load(pkl_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "discharge_spm_isothermal_V.pkl"), "rb") as pkl_file:
    sol_V: list = pickle.load(pkl_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "discharge_spm_non_isothermal_time.pkl"), "rb") as pkl_file:
    sol_spm_non_isothermal_time: list = pickle.load(pkl_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "discharge_spm_non_isothermal_V.pkl"), "rb") as pkl_file:
    sol_spm_non_isothermal_V: list = pickle.load(pkl_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "discharge_espm_isothermal_time.pkl"), "rb") as pkl_file:
    sol_espm_time: list = pickle.load(pkl_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "discharge_espm_isothermal_V.pkl"), "rb") as pkl_file:
    sol_espm_V: list = pickle.load(pkl_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "discharge_espm_non_isothermal_time.pkl"), "rb") as pkl_file:
    sol_espm_non_isothermal_time: list = pickle.load(pkl_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "discharge_espm_non_isothermal_V.pkl"), "rb") as pkl_file:
    sol_espm_non_isothermal_V: list = pickle.load(pkl_file)

# ----------------------------------------PLOTS------------------------------------------------------------------------
# Plots
matplotlib.rc('xtick', labelsize=25) 
matplotlib.rc('ytick', labelsize=25) 

plt.plot(sol_time, sol_V, label="SPM", linewidth=3)
plt.plot(sol_spm_non_isothermal_time, sol_spm_non_isothermal_V, label="SPM-non_isothermal", linewidth=3)
plt.plot(sol_espm_time, sol_espm_V, label="Enhanced SPM", linewidth=3)
plt.plot(sol_espm_non_isothermal_time, sol_espm_non_isothermal_V, label="Enhanced SPM-non_isothermal", linewidth=3)

plt.xlim(3250, 4300)
# plt.ylim(3.5, 4.2)
plt.tight_layout()
plt.show()

