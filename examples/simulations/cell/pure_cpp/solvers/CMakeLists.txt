set(SOLVER_SOURCE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/battery_components.h 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/battery_components.cpp
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/cyclers.h
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/cyclers.cpp
                    ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.h ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.cpp 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/models.h ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/models.cpp 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/coords.h ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/coords.cpp 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/solvers.h
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/solvers.cpp)

set(COMMON_INCLUDE_DIRECTORIES ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic)
set(COMMON_TARGET_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)

add_executable(neg_electrode_conc_solvers neg_electrode_conc_solvers.cpp ${SOLVER_SOURCE})
target_include_directories(neg_electrode_conc_solvers PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/)
set_target_properties(neg_electrode_conc_solvers PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)
set_target_properties(neg_electrode_conc_solvers PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)
set_target_properties(neg_electrode_conc_solvers PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)

add_executable(pos_electrode_conc_solvers pos_electrode_conc_solvers.cpp ${SOLVER_SOURCE})
target_include_directories(pos_electrode_conc_solvers PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/)
set_target_properties(pos_electrode_conc_solvers PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)
set_target_properties(pos_electrode_conc_solvers PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)
set_target_properties(pos_electrode_conc_solvers PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)

add_executable(electrolyte_conc_fvm electrolyte_conc_fvm.cpp ${SOLVER_SOURCE})
target_include_directories(electrolyte_conc_fvm PUBLIC ${COMMON_INCLUDE_DIRECTORIES})
set_target_properties(electrolyte_conc_fvm PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${COMMON_TARGET_OUTPUT_DIRECTORY})
set_target_properties(electrolyte_conc_fvm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${COMMON_TARGET_OUTPUT_DIRECTORY})
set_target_properties(electrolyte_conc_fvm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${COMMON_TARGET_OUTPUT_DIRECTORY})