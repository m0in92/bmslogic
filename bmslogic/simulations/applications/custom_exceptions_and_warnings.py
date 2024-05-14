"""
Contains custom exceptions relevant for EV_sim.
"""

__all__ = ["UndefinedEVError", "UndefinedDriveCycleError", "UndefinedRhoError", "RoadAngleCalcError", "UndefinedRoadForce"]

__author__ = "Moin Ahmed"
__copyright__ = "Copyright (c) 2024 by BMSLogic. All Rights Reserved."
__Status__ = "Deployed"


class UndefinedEVError(Exception):
    def __init__(self):
        super().__init__("Undefined EV.")


class UndefinedDriveCycleError(Exception):
    def __init__(self):
        super().__init__("Undefined Drive Cycle.")


class UndefinedRhoError(Exception):
    def __init__(self):
        super().__init__("Undefined rho.")


class RoadAngleCalcError(Exception):
    """
    Cannot calculate road grade angle since road grade is not the correct type.
    """
    def __init__(self):
        super().__init__("Cannot calculate road grade angle since road grade is not the correct type.")


class UndefinedRoadForce(Exception):
    def __init__(self):
        super().__init__("Undefined road force.")