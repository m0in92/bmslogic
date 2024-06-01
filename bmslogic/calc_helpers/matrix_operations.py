import math

import numpy as np
import numpy.typing as npt


def TDMAsolver(l_diag: npt.ArrayLike, diag: npt.ArrayLike, u_diag: npt.ArrayLike, col_vec: npt.ArrayLike) -> npt.ArrayLike:
    '''
    TDMA (a.k.a Thomas algorithm) solver for tridiagonal system of equations.
    Code Modified from:
    https://gist.github.com/cbellei/8ab3ab8551b8dfc8b081c518ccd9ada9?permalink_comment_id=3109807
    '''
    nf = len(col_vec)  # number of equations
    c_l_diag, c_diag, c_u_diag, c_col_vec = map(np.array, (l_diag, diag, u_diag, col_vec))  # copy arrays
    for it in range(1, nf):
        mc = c_l_diag[it - 1] / c_diag[it - 1]
        c_diag[it] = c_diag[it] - mc * c_u_diag[it - 1]
        c_col_vec[it] = c_col_vec[it] - mc * c_col_vec[it - 1]

    xc = c_diag
    xc[-1] = c_col_vec[-1] / c_diag[-1]

    for il in range(nf - 2, -1, -1):
        xc[il] = (c_col_vec[il] - c_u_diag[il] * xc[il + 1]) / c_diag[il]
    return xc


def find_the_element_with_closest_number(value: float, array: np.ndarray) -> float:
    """source code largely got from the following stackoverflow 
            https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array

        This function finds the value of the array element closest to the user specified value.

    Args:
        value (float): _description_
        array (np.ndarray): _description_

    Returns:
        float: _description_
    """
    index: float = np.searchsorted(array, value, side="left")

    if (index > 0) and (index==len(array) or math.fabs(value - array[index-1] < math.fabs(value - array[index]))):
        return index-1, array[index-1]
    else:
        return index, array[index]


def interp1d(array_1: np.ndarray, array_2: np.ndarray, value: float) -> float:
    """provides an interpolation based on the two arrays. Uses linear interpolation for the values that lie between two datapoints and
    provides extrapolation based on the value of the closest datapoint.

    Args:
        array_1 (np.ndarray): _description_
        array_2 (np.ndarray): _description_
        value (float): _description_

    Returns:
        _type_: _description_
    """
    # sort the arrays
    array_1_index: np.ndarray = np.argsort(array_1)
    array_1_sorted: np.ndarray = array_1[array_1_index]
    array_2_sorted: np.ndarray = array_2[array_1_index]

    # find the values closest to the user-specified value
    index: float = np.searchsorted(array_1_sorted, value, side="right")
    if value <= array_1_sorted[0]:
        return array_2_sorted[0]
    if (index + 1) <= (len(array_1)):
        x1: float = array_1_sorted[index-1]
        x2: float = array_1_sorted[index]
        y1: float = array_2_sorted[index-1]
        y2: float = array_2_sorted[index]

        # calculate the gradient and y-intercept
        m: float = (y2-y1) / (x2-x1)
        y_intercept: float = y2 - m * x2

        # calculate the interpolation
        return m * value + y_intercept
    else:
        return array_2_sorted[-1]



# array_1: np.ndarray = np.array([0,4,5,3,2])
# array_2: np.ndarray = np.array([10, 90, 67, 34, 98])
# print(inter1pd(array_1=array_1, array_2=array_2, value=4.5))