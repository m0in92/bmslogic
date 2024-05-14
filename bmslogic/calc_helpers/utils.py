"""
Contains the functionalities for general use utilities.
"""
__all__ = ["timer"]
__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2024 by BMSLogic. All Rights Reserved."

import time


def timer(solver_func):
    """
    Timer function is intended to be a decorator function that takes in any solver function and calculates the solver
    solution time. It then displays the solution time.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        sol = solver_func(*args, **kwargs)
        print(f"Solver execution time: {time.time() - start_time}s")
        return sol
    return wrapper




