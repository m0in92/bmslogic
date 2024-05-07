"""
Contains the path definations for modules inside tests directory
"""

import os
import pathlib


PROJ_DIR: str = pathlib.Path(__file__).parent.parent.__str__()
TEST_ELECTROLYTE_ERROR_DIR: str = os.path.join(PROJ_DIR, 'bmslogic', 'parameters_sets', 'test', 'param_electrolyte_with_errors.csv')

print(PROJ_DIR)