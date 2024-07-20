set(PYBIND11_SOURCES bindings_cpp_py.cpp 
                    cyclers.h cyclers.cpp
                    ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.h ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.cpp
                    coords.h coords.cpp 
                    solvers.h solvers.cpp
                    models.h models.cpp
                    solution.h solution.cpp 
                    battery_components.h battery_components.cpp)

pybind11_add_module(cell MODULE ${PYBIND11_SOURCES})
target_include_directories(cell PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic)

set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell)

if (MSVC)
    set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell)
    set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell)
    set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell)
endif(MSVC)
