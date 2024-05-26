__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."

import pathlib
import pickle  # pickle is used for storing the results of this script
import os
import sys
import time

import matplotlib
import matplotlib.pyplot as plt

# Open files containing the saved results
FILE_DIR: str = pathlib.Path(__file__).parent.__str__()

with open(os.path.join(FILE_DIR, "saved_results", "poly_higher_pos_discharge_time.pkl"), "rb") as pkl_cn_file:
    lst_poly_higher_time: list = pickle.load(pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "poly_higher_pos_discharge_soc.pkl"), "rb") as pkl_cn_file:
    lst_poly_higher_soc: list = pickle.load(pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "poly_two_pos_discharge_time.pkl"), "rb") as pkl_cn_file:
    lst_poly_two_time: list = pickle.load(pkl_cn_file)

with open(os.path.join(FILE_DIR, "saved_results", "poly_two_pos_discharge_soc.pkl"), "rb") as pkl_cn_file:
    lst_poly_two_soc: list = pickle.load(pkl_cn_file)


# Plots
matplotlib.rc('xtick', labelsize=12)
matplotlib.rc('ytick', labelsize=12)

plt.plot(lst_poly_higher_time, lst_poly_higher_soc,
         label="Polynomial Approximation - Higher Order")
plt.plot(lst_poly_two_time, lst_poly_two_soc,
         label="Polynomial Approximation - Second Order")

plt.xlabel("Time [s]", fontsize=15)
plt.ylabel("Positive Electrode SOC", fontsize=15)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()
