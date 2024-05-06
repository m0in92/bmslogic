set(PYBIND11_SOURCES bindings_cpp_py.cpp 
                    cyclers.h cyclers.cpp
                    ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.h ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.cpp
                    solvers.h solvers.cpp
                    models.h models.cpp
                    solution.h solution.cpp 
                    battery_components.h battery_components.cpp)

pybind11_add_module(cell SHARED ${PYBIND11_SOURCES})
target_include_directories(cell PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic)


