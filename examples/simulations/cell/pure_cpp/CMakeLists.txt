add_subdirectory(solvers)

set(EXAMPLE_SOURCE ${CELL_SIM_DIR}/battery_components.cpp
                    ${CELL_SIM_DIR}/cyclers.cpp
                    ${CALC_HELPERS_DIR}/owl.h ${CALC_HELPERS_DIR}/owl.cpp 
                    ${CELL_SIM_DIR}/models.cpp 
                    ${CELL_SIM_DIR}/coords.cpp
                    ${CELL_SIM_DIR}/solvers.cpp)

add_executable(discharge_spm discharge_spm.cpp ${EXAMPLE_SOURCE})
target_include_directories(discharge_spm PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/
                                                ${CALC_HELPERS_DIR}
                                                ${PROJECT_SOURCE_DIR}/extern/cpp_plotting)
target_link_libraries(discharge_spm matplotlib_cpp)
set_target_properties(discharge_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
set_target_properties(discharge_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
set_target_properties(discharge_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# add_executable(discharge_spm discharge_spm.cpp)
# target_link_libraries(discharge_spm PRIVATE cell_sim)
# target_include_directories(discharge_spm PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/)
# set_target_properties(discharge_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# set_target_properties(discharge_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# set_target_properties(discharge_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)

add_executable(discharge_espm discharge_espm.cpp ${EXAMPLE_SOURCE})
target_include_directories(discharge_espm PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/ ${CALC_HELPERS_DIR}
                                                ${PROJECT_SOURCE_DIR}/extern/cpp_plotting)
target_link_libraries(discharge_espm matplotlib_cpp)
set_target_properties(discharge_espm PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
set_target_properties(discharge_espm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
set_target_properties(discharge_espm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)

add_executable(discharge_spm_cn_solver discharge_spm_cn_solver.cpp ${EXAMPLE_SOURCE})
target_include_directories(discharge_spm_cn_solver PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${CALC_HELPERS_DIR})
set_target_properties(discharge_spm_cn_solver PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
set_target_properties(discharge_spm_cn_solver PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# set_target_properties(discharge_spm_cn_solver PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# add_executable(discharge_spm_cn_solver discharge_spm_cn_solver.cpp)
# target_link_libraries(discharge_spm_cn_solver PRIVATE cell_sim)
# target_include_directories(discharge_spm_cn_solver PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/)
# set_target_properties(discharge_spm_cn_solver PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# set_target_properties(discharge_spm_cn_solver PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# set_target_properties(discharge_spm_cn_solver PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)

add_executable(charge_spm charge_spm.cpp ${EXAMPLE_SOURCE})
target_include_directories(charge_spm PRIVATE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/ ${CALC_HELPERS_DIR})
set_target_properties(charge_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
set_target_properties(charge_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
set_target_properties(charge_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# add_executable(charge_spm charge_spm.cpp)
# target_link_libraries(charge_spm PRIVATE cell_sim)
# target_include_directories(charge_spm PRIVATE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/)
# set_target_properties(charge_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# set_target_properties(charge_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# set_target_properties(charge_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)

add_executable(discharge_rest_spm discharge_rest_spm.cpp ${EXAMPLE_SOURCE})
target_include_directories(discharge_rest_spm PRIVATE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/ ${CALC_HELPERS_DIR})
set_target_properties(discharge_rest_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
set_target_properties(discharge_rest_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
set_target_properties(discharge_rest_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# add_executable(discharge_rest_spm discharge_rest_spm.cpp)
# target_link_libraries(discharge_rest_spm cell_sim)
# target_include_directories(discharge_rest_spm PRIVATE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/)
# set_target_properties(discharge_rest_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# set_target_properties(discharge_rest_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# set_target_properties(discharge_rest_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)


add_executable(charge_rest_spm charge_rest_spm.cpp ${EXAMPLE_SOURCE})
target_include_directories(charge_rest_spm PRIVATE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/ ${CALC_HELPERS_DIR})
set_target_properties(charge_rest_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
set_target_properties(charge_rest_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
set_target_properties(charge_rest_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# add_executable(charge_rest_spm charge_rest_spm.cpp)
# target_link_libraries(charge_rest_spm PRIVATE cell_sim)
# target_include_directories(charge_rest_spm PRIVATE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/)
# set_target_properties(charge_rest_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# set_target_properties(charge_rest_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)
# set_target_properties(charge_rest_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp)

if(NOT EMBEDDED)
    add_executable(discharge_spkf_spm kalman_filter/sp_isothermal_discharge.cpp
                    ${EXAMPLE_SOURCE}
                    ${CALC_HELPERS_DIR}/kalman_filter.cpp 
                    ${CELL_SIM_DIR}/kalman_solvers.cpp)
    target_include_directories(discharge_spkf_spm PRIVATE ${CELL_SIM_DIR} ${CALC_HELPERS_DIR}
                                                            ${PROJECT_SOURCE_DIR}/bmslogic/
                                                            ${PROJECT_SOURCE_DIR}/extern/eigen)
    set_target_properties(discharge_spkf_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/kalman_filter)
    set_target_properties(discharge_spkf_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/kalman_filter)
    set_target_properties(discharge_spkf_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/kalman_filter)
endif()
