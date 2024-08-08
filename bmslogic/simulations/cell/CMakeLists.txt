set(PYBIND11_SOURCES bindings_cpp_py.cpp 
                    ${PROJECT_SOURCE_DIR}/bmslogic/calc_helpers/kalman_filter.h ${PROJECT_SOURCE_DIR}/bmslogic/calc_helpers/kalman_filter.cpp 
                    cyclers.h cyclers.cpp
                    ${CALC_HELPERS_DIR}/owl.h ${CALC_HELPERS_DIR}/owl.cpp
                    coords.h coords.cpp 
                    solvers.h solvers.cpp
                    models.h models.cpp
                    solution.h solution.cpp 
                    battery_components.h battery_components.cpp
                    kalman_solvers.h kalman_solvers.cpp)

pybind11_add_module(cell MODULE ${PYBIND11_SOURCES})
target_include_directories(cell PUBLIC ${PROJECT_SOURCE_DIR}/extern/eigen)
target_include_directories(cell PUBLIC ${CALC_HELPERS_DIR})

set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CELL_SIM_DIR})

if (MSVC)
    set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CELL_SIM_DIR})
    set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY_DEBUG ${CELL_SIM_DIR})
    set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CELL_SIM_DIR})
endif(MSVC)

# LIBRARY
set(CELL_SIM_LIB_SOURCES    ${CALC_HELPERS_DIR}/owl.cpp
                            ${CALC_HELPERS_DIR}/kalman_filter.cpp 
                            ${CELL_SIM_DIR}/cyclers.cpp 
                            ${CELL_SIM_DIR}/battery_components.cpp 
                            ${CELL_SIM_DIR}/solvers.cpp 
                            ${CELL_SIM_DIR}/coords.cpp 
                            ${CELL_SIM_DIR}/models.cpp 
                            ${CELL_SIM_DIR}/solution.cpp 
                            ${CELL_SIM_DIR}/kalman_solvers.cpp)
add_library(cell_sim STATIC ${CELL_SIM_LIB_SOURCES})
target_include_directories(cell_sim PUBLIC  ${CALC_HELPERS_DIR}
                                            ${PROJECT_SOURCE_DIR}/extern/eigen
                                            ${CELL_SIM_DIR})
set_target_properties(cell_sim PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CELL_SIM_DIR})
set_target_properties(cell_sim PROPERTIES LIBRARY_OUTPUT_DIRECTORY_DEBUG ${CELL_SIM_DIR})
set_target_properties(cell_sim PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CELL_SIM_DIR})
set_target_properties(cell_sim PROPERTIES ARCHIVE_OUTPUT_DIRECTORY ${CELL_SIM_DIR})
set_target_properties(cell_sim PROPERTIES ARCHIVE_OUTPUT_DIRECTORY_DEBUG ${CELL_SIM_DIR})
set_target_properties(cell_sim PROPERTIES ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${CELL_SIM_DIR})
