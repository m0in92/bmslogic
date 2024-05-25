"""
Script for extracting and plotting the results of the error obtained from the optimization eigen solver of the negative electrode during discharge.
"""
__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."
__status__ = "Deployed"

import os
import pathlib
import pickle
import sys

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(pathlib.Path(
    __file__).parent.parent.parent.parent.parent.parent.parent.__str__())
from bmslogic.calc_helpers.errors import calc_mse, absolute_error


# ----------------------------------------OPEN FILES------------------------------------------------------------------------
FILE_DIR: str = pathlib.Path(__file__).parent.__str__()

# N=2
with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_time_2.pkl"), "rb") as pkl_cn_file:
    lst_eigen_time_2: list = pickle.load(pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_soc_2.pkl"), "rb") as pkl_cn_file:
    lst_eigen_soc_2: list = pickle.load(pkl_cn_file)

# N=5
with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_time_5.pkl"), "rb") as pkl_cn_file:
    lst_eigen_time_5: list = pickle.load(pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_soc_5.pkl"), "rb") as pkl_cn_file:
    lst_eigen_soc_5: list = pickle.load(pkl_cn_file)

# N=10
with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_time_10.pkl"), "rb") as pkl_cn_file:
    lst_eigen_time_10: list = pickle.load(pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_soc_10.pkl"), "rb") as pkl_cn_file:
    lst_eigen_soc_10: list = pickle.load(pkl_cn_file)

# N=20
with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_time_20.pkl"), "rb") as pkl_cn_file:
    lst_eigen_time_20: list = pickle.load(pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_soc_20.pkl"), "rb") as pkl_cn_file:
    lst_eigen_soc_20: list = pickle.load(pkl_cn_file)

# N=50
with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_time_50.pkl"), "rb") as pkl_cn_file:
    lst_eigen_time_50: list = pickle.load(pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_soc_50.pkl"), "rb") as pkl_cn_file:
    lst_eigen_soc_50: list = pickle.load(pkl_cn_file)

# N=100
with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_time_100.pkl"), "rb") as pkl_cn_file:
    lst_eigen_time_100: list = pickle.load(pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_electrode_discharge_eigen_soc_100.pkl"), "rb") as pkl_cn_file:
    lst_eigen_soc_100: list = pickle.load(pkl_cn_file)

# ----------------------------------------PLOTS------------------------------------------------------------------------
matplotlib.rc('xtick', labelsize=12)
matplotlib.rc('ytick', labelsize=12)

plt.plot(lst_eigen_time_2, absolute_error(np.array(lst_eigen_soc_100),
         np.array(lst_eigen_soc_2)) * 1000, label="N=2")
plt.plot(lst_eigen_time_5, absolute_error(np.array(lst_eigen_soc_100),
         np.array(lst_eigen_soc_5)) * 1000, label="N=5")
plt.plot(lst_eigen_time_10, absolute_error(np.array(lst_eigen_soc_100),
         np.array(lst_eigen_soc_10)) * 1000, label="N=10")
plt.plot(lst_eigen_time_20, absolute_error(np.array(lst_eigen_soc_100),
         np.array(lst_eigen_soc_20)) * 1000, label="N=20")
plt.plot(lst_eigen_time_50, absolute_error(np.array(lst_eigen_soc_100),
         np.array(lst_eigen_soc_50)) * 1000, label="N=50")
# plt.plot(lst_eigen_time_100, absolute_error(lst_eigen_soc_100, label="N=100")

plt.xlabel("Time [s]", fontsize=15)
plt.ylabel("Absolute Error [mV]", fontsize=15)

plt.legend()
plt.tight_layout()
plt.show()
