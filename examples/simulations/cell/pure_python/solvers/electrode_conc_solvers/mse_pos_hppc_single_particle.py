"""
Script for calculating the error of the electrode solvers with the Crank Nicolson Scheme.
"""
__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."
__status__ = "Deployed"

import os
import pathlib
import pickle
import sys

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

try:
    from bmslogic.calc_helpers.errors import calc_mse, absolute_error
except ModuleNotFoundError as e:
    PROJECT_DIR = pathlib.Path(__file__).parent.parent.parent.parent.parent.parent.parent.__str__()
    sys.path.append(PROJECT_DIR)
    from bmslogic.calc_helpers.errors import calc_mse, absolute_error


FILE_DIR: str = pathlib.Path(__file__).parent.__str__()

# CN solvers below
with open(os.path.join(FILE_DIR, "saved_results", "pos_hppc_cn_time.pkl"), "rb") as pkl_cn_file:
    lst_cn_time: list = pickle.load(pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_hppc_cn_soc.pkl"), "rb") as pkl_cn_file:
    lst_cn_soc: list = pickle.load(pkl_cn_file)

# eigen solvers below
with open(os.path.join(FILE_DIR, "saved_results", "pos_hppc_eigen_time.pkl"), "rb") as pkl_eigen_file:
    lst_eigen_time: list = pickle.load(pkl_eigen_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_hppc_eigen_soc.pkl"), "rb") as pkl_eigen_file:
    lst_eigen_soc: list = pickle.load(pkl_eigen_file)

# # polynomial solvers below
with open(os.path.join(FILE_DIR, "saved_results", "pos_hppc_poly_time.pkl"), "rb") as pkl_poly_file:
    lst_poly_time: list = pickle.load(pkl_poly_file)

with open(os.path.join(FILE_DIR, "saved_results", "pos_hppc_poly_soc.pkl"), "rb") as pkl_poly_file:
    lst_poly_soc: list = pickle.load(pkl_poly_file)

diff_len_cn_poly: float = len(lst_cn_soc) - len(lst_poly_soc)  # since the solution array from different solvers are of different lenghts.
diff_len_cn_eigen: float = len(lst_cn_soc) - len(lst_eigen_soc)  # since the solution array from different solvers are of different lenghts.

#plots
matplotlib.rc('xtick', labelsize=12) 
matplotlib.rc('ytick', labelsize=12) 

plt.plot(lst_cn_time, absolute_error(np.array(lst_cn_soc), np.array(lst_poly_soc)[:len(lst_cn_soc)]), label="Polynomial Approximation")
plt.plot(lst_eigen_time, absolute_error(np.array(lst_cn_soc)[
         :len(lst_eigen_soc)], np.array(lst_eigen_soc)), label="Eigen Expansion Method")

plt.xlabel("Time [s]", fontsize=15)
plt.ylabel("Absolute Error", fontsize=15)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()
