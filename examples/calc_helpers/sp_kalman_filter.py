import os
import sys
import pathlib
import random

import numpy as np
import matplotlib.pyplot as plt



try:
    from bmslogic.calc_helpers.calc_helpers import TwoStatesOneInputOneOutput
except ModuleNotFoundError:
    sys.path.append(pathlib.Path(__file__).parent.parent.parent.__str__())
    from bmslogic.calc_helpers.calc_helpers import TwoStatesOneInputOneOutput

def state_equation(x_k: np.ndarray, u_k: np.ndarray, w_k: np.ndarray) -> np.ndarray:
    return np.array([np.sqrt(5 + x_k[0]) + w_k[0], np.sqrt(5 + x_k[0]) + w_k[0]])


def output_equation(x_k: np.ndarray, u_k: np.ndarray, v_k: np.ndarray) -> np.ndarray:
    return np.array([x_k[0]**3 + v_k[0]])


spkf_instance: TwoStatesOneInputOneOutput = TwoStatesOneInputOneOutput(
    2, 2, 2, 2, 1, 2, state_equation=state_equation, output_equation=output_equation)

print(spkf_instance.state)
print(spkf_instance.cov)

N_RUNS: int = 100
lst_input = [0.0 for i in range(N_RUNS)]
lst_y_true = [26 + 0.025*random.uniform(-1, 1) for i in range(N_RUNS)]

input: np.ndarray = np.array([lst_input, lst_input])
ytrue: np.ndarray = np.array([lst_y_true])
spkf_instance.solve(input, ytrue)  # the input and y_true dimensions have to be such that [[input1_run1,..,input1_run100], [input2_run1,..,input2_run100]]
print(spkf_instance.state)
print(spkf_instance.cov)
