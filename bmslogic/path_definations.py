"""
Defines the important absolute file paths used by any source code within the BMSLogic directory.
"""

import pathlib
import os


ROOT_DIR: str = pathlib.Path(__file__).parent.parent.__str__()
BMSLOGIC_DIR: str = pathlib.Path(__file__).parent.__str__()

# File paths pertaining to the databases
EV_DATABASE_DIR: str = os.path.join(BMSLOGIC_DIR, "parameter_sets", "application", "EV")
EV_DRIVECYCLE_DIR: str = os.path.join(EV_DATABASE_DIR, "drivecycles")

PARAMETER_SET_DIR: str = os.path.join(BMSLOGIC_DIR, 'parameter_sets')
ECM_PARAMETER_SET_DIR: str = os.path.join(PARAMETER_SET_DIR, 'parameter_sets_ecm')