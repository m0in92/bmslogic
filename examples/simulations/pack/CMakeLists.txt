set(EXAMPLE_SOURCE ${CELL_SIM_DIR}/battery_components.cpp
                    ${CELL_SIM_DIR}/cyclers.cpp
                    ${CALC_HELPERS_DIR}/owl.h ${CALC_HELPERS_DIR}/owl.cpp 
                    ${CELL_SIM_DIR}/models.cpp 
                    ${CELL_SIM_DIR}/coords.cpp
                    ${CELL_SIM_DIR}/solvers.cpp)

add_executable(timed_sim ${PROJECT_SOURCE_DIR}/examples/simulations/pack/timed_simulation.cpp
                ${PROJECT_SOURCE_DIR}/bmslogic/simulations/pack/real_time_sims.cpp
                ${EXAMPLE_SOURCE})
target_include_directories(timed_sim PRIVATE ${CALC_HELPERS_DIR}
                            ${PROJECT_SOURCE_DIR}/bmslogic/simulations/pack/ 
                            ${CELL_SIM_DIR})
set_target_properties(timed_sim PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/pack)
set_target_properties(timed_sim PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/pack)
set_target_properties(timed_sim PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/pack)

add_executable(multiple_timed_sim ${PROJECT_SOURCE_DIR}/examples/simulations/pack/multiple_timed_simulations.cpp
                ${PROJECT_SOURCE_DIR}/bmslogic/simulations/pack/real_time_sims.cpp
                ${EXAMPLE_SOURCE})
target_include_directories(multiple_timed_sim PRIVATE ${CALC_HELPERS_DIR}
                            ${PROJECT_SOURCE_DIR}/bmslogic/simulations/pack/ 
                            ${CELL_SIM_DIR})
set_target_properties(multiple_timed_sim PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/pack)
set_target_properties(multiple_timed_sim PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/pack)
set_target_properties(multiple_timed_sim PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/pack)