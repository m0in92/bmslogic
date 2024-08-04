add_subdirectory(solvers)

set(EXAMPLE_SOURCE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/battery_components.h 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/battery_components.cpp
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/cyclers.h
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/cyclers.cpp
                    ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.h ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.cpp 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/models.h ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/models.cpp 
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/coords.h ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/coords.cpp
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/solvers.h
                    ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/solvers.cpp)

add_executable(discharge_spm discharge_spm.cpp ${EXAMPLE_SOURCE})
target_include_directories(discharge_spm PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/
                                                ${PROJECT_SOURCE_DIR}/extern/cpp-matplotlib)
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

add_executable(discharge_spm_cn_solver discharge_spm_cn_solver.cpp ${EXAMPLE_SOURCE})
target_include_directories(discharge_spm_cn_solver PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/)
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
target_include_directories(charge_spm PRIVATE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/)
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
target_include_directories(discharge_rest_spm PRIVATE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/)
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
target_include_directories(charge_rest_spm PRIVATE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/)
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
    add_executable(discharge_spkf_spm kalman_filter/sp_isothermal_discharge.cpp)
    target_link_libraries(discharge_spkf_spm cell_sim)
    target_include_directories(discharge_spkf_spm PRIVATE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic/
                                                            ${PROJECT_SOURCE_DIR}/extern/eigen)
    set_target_properties(discharge_spkf_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/kalman_filter)
    set_target_properties(discharge_spkf_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/kalman_filter)
    set_target_properties(discharge_spkf_spm PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/examples/simulations/cell/pure_cpp/kalman_filter)
endif()
