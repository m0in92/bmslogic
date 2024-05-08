# Project Directory Structure

This directory contains the source code for the project. The subdirectories and their brief content description as outlined below.

  - *calc_helpers*: contains source code that aids in the simulation calculations.
  - *extern*: external libraries or dependencies for the simulations.
  - *parameter_sets*: contains the datasets for the simulations.
  - *simulations*: Configuration files for build tools.
    - *application*: source code for the battery pack applications, including electric vehicles (EVs)
    - *cell*: source code for the battery cell simulations
    - *pack*: source code for the battery pack simulations

More details on the contents of the subdirectories are described in the following sections and will be updated throughout the course of this project.


## *simulations/cell*

This subdirectory contains the source code for performing battery cell simulations in the continuum-scale and cell-level length-scales. The source code is written in Python and C++ programming language. Furthermore, the C++ to Python bindings are coded in the ```bindings_cpp_py.cpp``` file using pybind11 (https://pybind11.readthedocs.io/en/stable/index.html).

### *Python Source Code*
All the Python modules (files ending with ```.py``` extensions) are source code written in Python programming language. Most (if not all) the names of the classes in these modules are prefixed with the ```Py``` prefix.

### *C++ Source Code*
The source code written in C++ are used for Python bindings as well as creating executables (stored in the examples directory are ```cmake``` built).

### *C++ Python bindings* 
When this project is compiled using ```cmake``` (refer to the installation section of the ```README.md```), the bindings (as well as the executable, refer to the examples/ directory) can be build from the ```CMakeLists.txt``` found in this directory. The resulting pybind11 module is compiled in this directory. This module can be imported in any Python module.

