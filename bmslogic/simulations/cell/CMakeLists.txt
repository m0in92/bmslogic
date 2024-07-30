set(PYBIND11_SOURCES bindings_cpp_py.cpp 
                    ${PROJECT_SOURCE_DIR}/bmslogic/calc_helpers/kalman_filter.h ${PROJECT_SOURCE_DIR}/bmslogic/calc_helpers/kalman_filter.cpp 
                    cyclers.h cyclers.cpp
                    ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.h ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.cpp
                    coords.h coords.cpp 
                    solvers.h solvers.cpp
                    models.h models.cpp
                    solution.h solution.cpp 
                    battery_components.h battery_components.cpp
                    kalman_solvers.h kalman_solvers.cpp)

pybind11_add_module(cell MODULE ${PYBIND11_SOURCES})
target_include_directories(cell PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic)
target_include_directories(cell PUBLIC ${PROJECT_SOURCE_DIR}/extern/eigen)
target_include_directories(cell PUBLIC ${PROJECT_SOURCE_DIR}/calc_helpers/)

set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell)

if (MSVC)
    set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell)
    set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell)
    set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell)
endif(MSVC)

set(CELL_SIM_LIB_DIR ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell)
set(CELL_SIM_LIB_SOURCES    ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.cpp
                            ${PROJECT_SOURCE_DIR}/bmslogic/calc_helpers/kalman_filter.cpp 
                            cyclers.cpp battery_components.cpp solvers.cpp coords.cpp models.cpp solution.cpp kalman_solvers.cpp)
add_library(cell_sim ${CELL_SIM_LIB_SOURCES})
target_include_directories(cell_sim PUBLIC  ${PROJECT_SOURCE_DIR}/bmslogic/ 
                                            ${PROJECT_SOURCE_DIR}/extern/eigen)
if (MSVC)
    set_target_properties(cell_sim PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell)
    set_target_properties(cell_sim PROPERTIES LIBRARY_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell)
    set_target_properties(cell_sim PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell)
endif(MSVC)
