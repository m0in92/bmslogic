__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."

import pathlib
import pickle  # pickle is used for storing the results of this script
import os
import sys
import time

import matplotlib
import matplotlib.pyplot as plt


# Open files

FILE_DIR: str = pathlib.Path(__file__).parent.__str__()

with open(os.path.join(FILE_DIR, "neg_discharge_rest_cn_time.pkl"), "rb") as pkl_cn_file:
    lst_cn_time: list = pickle.load(pkl_cn_file)

with open(os.path.join(FILE_DIR, "neg_discharge_rest_cn_soc.pkl"), "rb") as pkl_cn_file:
    lst_cn_soc: list = pickle.load(pkl_cn_file)

with open(os.path.join(FILE_DIR, "neg_discharge_rest_eigen_time.pkl"), "rb") as pkl_eigen_file:
    lst_eigen_time: list = pickle.load(pkl_eigen_file)

with open(os.path.join(FILE_DIR, "neg_discharge_rest_eigen_soc.pkl"), "rb") as pkl_eigen_file:
    lst_eigen_soc: list = pickle.load(pkl_eigen_file)

with open(os.path.join(FILE_DIR, "neg_discharge_rest_poly_time.pkl"), "rb") as pkl_poly_file:
    lst_poly_time: list = pickle.load(pkl_poly_file)

with open(os.path.join(FILE_DIR, "neg_discharge_rest_poly_soc.pkl"), "rb") as pkl_poly_file:
    lst_poly_soc: list = pickle.load(pkl_poly_file)

# Plots
# Plots
matplotlib.rc('xtick', labelsize=12) 
matplotlib.rc('ytick', labelsize=12) 

plt.plot(lst_cn_time, lst_cn_soc, label="Crank-Nicolson Scheme")
plt.plot(lst_eigen_time, lst_eigen_soc, label="Eigen Expansion Method")
plt.plot(lst_poly_time, lst_poly_soc, label="Polynomial Approximation")
# plt.plot(lst_poly_time_two, lst_poly_soc_two, label="Polynomial Approximation - Two Order")

plt.xlabel("Time [s]", fontsize=15)
plt.ylabel("Negative Electrode SOC", fontsize=15)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()


