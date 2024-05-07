"""
Contains the relevant path variables for the battery cell simulations
"""

import pathlib
import os


CELL_SIM_DIR: str = pathlib.Path(__file__).parent.__str__()
ROOT_DIR: str = pathlib.Path(__file__).parent.parent.parent.parent.__str__()
BMSLOGIC_DIR: str = pathlib.Path(__file__).parent.parent.parent.__str__()

PARAMETER_SET_DIR: str = os.path.join(BMSLOGIC_DIR, 'parameter_sets')
ECM_PARAMETER_SET_DIR: str = os.path.join(PARAMETER_SET_DIR, 'parameter_sets_ecm')
