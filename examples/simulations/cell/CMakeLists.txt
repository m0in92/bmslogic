set(EXAMPLE_SOURCE discharge_1.cpp 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/battery_components.h 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/battery_components.cpp
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/cyclers.h
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/cyclers.cpp
                    ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.h ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.cpp 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/models.h ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/models.cpp 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/solvers.h
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/solvers.cpp)

add_executable(discharge_1 ${EXAMPLE_SOURCE})
target_include_directories(discharge_1 PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/)

set_target_properties(discharge_1 PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell)
set_target_properties(discharge_1 PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell)
set_target_properties(discharge_1 PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell)

