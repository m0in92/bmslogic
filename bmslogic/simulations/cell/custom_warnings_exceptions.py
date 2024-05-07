"""
Contains custom Python warning and exceptions for this repository.
"""

__author__ = 'Moin Ahmed'
__copyright__ = 'Copyright 2024 by BMSLogic. All Rights Reserved.'
__status__ = 'deployed'

import warnings


class InvalidSOCException(Exception):
    "Raised when SOC is smaller than 0 or greater than 1."
    def __init__(self, electrode_type):
        self.msg = f"{electrode_type} SOC is beyond 0-1"
        super().__init__(self.msg)


class InsufficientInputOperatingConditions(Exception):
    "Raised when time and current arrays are not present in the input argument."
    pass


class InvalidElectrodeType(Exception):
    "Raised when invalid electrode type is inputted"
    pass


class MaxConcReached(Exception):
    "Raised when maximum concentration is reached"
    pass


class PotientialThesholdReached(Exception):
    "Raised with the threshold potential is reached."
    pass


class InsufficientParameters(Exception):
    """
    Raised in case of Insufficient parameters. For instance, this is raised when an attempt is made to initiate
    EnhancedSingleParticle solver in case of missing electrolyte parameters.
    """
    pass


class ThresholdPotentialWarning(Warning):
    def __init__(self, V: float):
        self.message = f"Threshold battery cell potential reached {V} V."
        warnings.warn(self.message)


def threshold_SOC_warning():
    warnings.warn("Threshold battery cell SOC reached.")