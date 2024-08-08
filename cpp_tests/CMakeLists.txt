enable_testing()

set(BMSLOGIC_SOURCES ${CALC_HELPERS_DIR}/owl.h ${CALC_HELPERS_DIR}/owl.cpp
                    ${CELL_SIM_DIR}/battery_components.h ${CELL_SIM_DIR}/battery_components.cpp
                    ${CELL_SIM_DIR}/cyclers.h ${CELL_SIM_DIR}/cyclers.cpp
                    ${CELL_SIM_DIR}/models.cpp
                    ${CALC_HELPERS_DIR}/kalman_filter.h ${CALC_HELPERS_DIR}/kalman_filter.cpp
                    ${CELL_SIM_DIR}/coords.h ${CELL_SIM_DIR}/coords.cpp
                    ${CELL_SIM_DIR}/solvers.h ${CELL_SIM_DIR}/solvers.cpp
                    ${CELL_SIM_DIR}/kalman_solvers.h ${CELL_SIM_DIR}/kalman_solvers.cpp)

add_executable(bmslogic_tests test_owl.cpp test_battery_components.cpp test_cyclers.cpp  test_models.cpp test_solvers.cpp
                                test_kalman_filter.cpp test_kalman_solvers.cpp ${BMSLOGIC_SOURCES})
target_link_libraries(bmslogic_tests gtest gtest_main)
target_include_directories(bmslogic_tests PUBLIC ${CELL_SIM_DIR} 
                                                    ${PROJECT_SOURCE_DIR}/extern/eigen
                                                    ${CALC_HELPERS_DIR})
include_directories(${PROJECT_SOURCE_DIR}/extern/google_tests/googletest/googletest/include 
                    ${PROJECT_SOURCE_DIR}/extern/google_tests/googletest)
set_target_properties(bmslogic_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/cpp_tests)
set_target_properties(bmslogic_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/cpp_tests)
set_target_properties(bmslogic_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/cpp_tests)

include(GoogleTest)
gtest_discover_tests(bmslogic_tests)
