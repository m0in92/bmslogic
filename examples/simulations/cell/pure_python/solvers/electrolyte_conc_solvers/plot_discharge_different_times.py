import pathlib
import pickle
import os

import matplotlib
import matplotlib.pyplot as plt


# ----------------------------------------OPEN FILES---------------------------------------------
FILE_DIR_TO_OPEN: str = os.path.join(pathlib.Path(__file__).parent.__str__(), "saved_results")

# CN solvers below
with open(os.path.join(FILE_DIR_TO_OPEN, "fvm_inverse_neg_discharge_x.pkl"), "rb") as pkl_file:
    inverse_co_ord_x: list = pickle.load(pkl_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "fvm_inverse_neg_discharge_conc.pkl"), "rb") as pkl_file:
    inverse_conc: list = pickle.load(pkl_file)

# eigen solvers below
with open(os.path.join(FILE_DIR_TO_OPEN, "fvm_TDMA_neg_discharge_x.pkl"), "rb") as pkl_file:
    TDMA_co_ord_x: list = pickle.load(pkl_file)

with open(os.path.join(FILE_DIR_TO_OPEN, "fvm_TDMA_neg_discharge_conc.pkl"), "rb") as pkl_file:
    TDMA_conc: list = pickle.load(pkl_file)