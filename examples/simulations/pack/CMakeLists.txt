set(EXAMPLE_SOURCE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/battery_components.h 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/battery_components.cpp
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/cyclers.h
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/cyclers.cpp
                    ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.h ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.cpp 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/models.h ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/models.cpp 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/coords.h ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/coords.cpp
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/solvers.h
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/solvers.cpp)

add_executable(timed_sim ${PROJECT_SOURCE_DIR}/examples/simulations/pack/timed_simulation.cpp
                ${PROJECT_SOURCE_DIR}/bmslogic/simulations/pack/real_time_sims.cpp
                ${EXAMPLE_SOURCE})
target_include_directories(timed_sim PRIVATE 
                            ${PROJECT_SOURCE_DIR}/bmslogic
                            ${PROJECT_SOURCE_DIR}/bmslogic/simulations/pack/ 
                            ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/)
set_target_properties(timed_sim PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/pack)
set_target_properties(timed_sim PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/pack)
set_target_properties(timed_sim PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/pack)

add_executable(multiple_timed_sim ${PROJECT_SOURCE_DIR}/examples/simulations/pack/multiple_timed_simulations.cpp
                ${PROJECT_SOURCE_DIR}/bmslogic/simulations/pack/real_time_sims.cpp
                ${EXAMPLE_SOURCE})
target_include_directories(multiple_timed_sim PRIVATE 
                            ${PROJECT_SOURCE_DIR}/bmslogic
                            ${PROJECT_SOURCE_DIR}/bmslogic/simulations/pack/ 
                            ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/)
set_target_properties(multiple_timed_sim PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/pack)
set_target_properties(multiple_timed_sim PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/pack)
set_target_properties(multiple_timed_sim PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/pack)