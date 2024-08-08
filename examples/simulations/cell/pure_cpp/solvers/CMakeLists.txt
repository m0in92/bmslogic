set(SOLVER_SOURCE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/battery_components.h 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/battery_components.cpp
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/cyclers.h
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/cyclers.cpp
                    ${CALC_HELPERS_DIR}/owl.h ${CALC_HELPERS_DIR}/owl.cpp 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/models.h ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/models.cpp 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/coords.h ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/coords.cpp 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/solvers.h
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/solvers.cpp)

set(COMMON_INCLUDE_DIRECTORIES ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${CALC_HELPERS_DIR})
set(COMMON_TARGET_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)

add_executable(neg_discharge_single_particle neg_discharge_single_particle.cpp ${SOLVER_SOURCE})
target_include_directories(neg_discharge_single_particle PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${CALC_HELPERS_DIR})
set_target_properties(neg_discharge_single_particle PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)
set_target_properties(neg_discharge_single_particle PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)
set_target_properties(neg_discharge_single_particle PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)

add_executable(neg_charge_single_particle neg_charge_single_particle.cpp ${SOLVER_SOURCE})
target_include_directories(neg_charge_single_particle PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${CALC_HELPERS_DIR})
set_target_properties(neg_charge_single_particle PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)
set_target_properties(neg_charge_single_particle PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)
set_target_properties(neg_charge_single_particle PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)

add_executable(neg_discharge_rest_single_particle neg_discharge_rest_single_particle.cpp ${SOLVER_SOURCE})
target_include_directories(neg_discharge_rest_single_particle PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${CALC_HELPERS_DIR})
set_target_properties(neg_discharge_rest_single_particle PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)
set_target_properties(neg_discharge_rest_single_particle PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)
set_target_properties(neg_discharge_rest_single_particle PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)

add_executable(pos_discharge_single_particle pos_discharge_single_particle.cpp ${SOLVER_SOURCE})
target_include_directories(pos_discharge_single_particle PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${CALC_HELPERS_DIR})
set_target_properties(pos_discharge_single_particle PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)
set_target_properties(pos_discharge_single_particle PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)
set_target_properties(pos_discharge_single_particle PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)

add_executable(pos_charge_single_particle pos_charge_single_particle.cpp ${SOLVER_SOURCE})
target_include_directories(pos_charge_single_particle PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${CALC_HELPERS_DIR})
set_target_properties(pos_charge_single_particle PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)
set_target_properties(pos_charge_single_particle PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)
set_target_properties(pos_charge_single_particle PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/solvers)

add_executable(electrolyte_conc_fvm electrolyte_conc_fvm.cpp ${SOLVER_SOURCE})
target_include_directories(electrolyte_conc_fvm PUBLIC ${COMMON_INCLUDE_DIRECTORIES})
set_target_properties(electrolyte_conc_fvm PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${COMMON_TARGET_OUTPUT_DIRECTORY})
set_target_properties(electrolyte_conc_fvm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${COMMON_TARGET_OUTPUT_DIRECTORY})
set_target_properties(electrolyte_conc_fvm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${COMMON_TARGET_OUTPUT_DIRECTORY})