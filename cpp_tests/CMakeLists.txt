enable_testing()

set(CELL_DIR ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell)
set(CALC_HELPERS_DIR ${PROJECT_SOURCE_DIR}/bmslogic/calc_helpers)

set(BMSLOGIC_SOURCES ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.h ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.cpp
                    ${CELL_DIR}/battery_components.h ${CELL_DIR}/battery_components.cpp
                    ${CELL_DIR}/cyclers.h ${CELL_DIR}/cyclers.cpp
                    ${CELL_DIR}/models.cpp
                    ${CALC_HELPERS_DIR}/kalman_filter.h ${CALC_HELPERS_DIR}/kalman_filter.cpp
                    ${CELL_DIR}/coords.h ${CELL_DIR}/coords.cpp
                    ${CELL_DIR}/solvers.h ${CELL_DIR}/solvers.cpp
                    ${CELL_DIR}/kalman_solvers.h ${CELL_DIR}/kalman_solvers.cpp)
set(BMSLOGIC_INCLUDE_DIRS ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic)

add_executable(bmslogic_tests test_owl.cpp test_battery_components.cpp test_cyclers.cpp  test_models.cpp test_solvers.cpp
                                test_kalman_filter.cpp test_kalman_solvers.cpp ${BMSLOGIC_SOURCES})
target_link_libraries(bmslogic_tests gtest gtest_main)
target_include_directories(bmslogic_tests PUBLIC ${BMSLOGIC_INCLUDE_DIRS} 
                                                    ${PROJECT_SOURCE_DIR}/extern/eigen
                                                    ${CALC_HELPERS_DIR})
include_directories(${PROJECT_SOURCE_DIR}/extern/google_tests/googletest/googletest/include 
                    ${PROJECT_SOURCE_DIR}/extern/google_tests/googletest)
set_target_properties(bmslogic_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/cpp_tests)
set_target_properties(bmslogic_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/cpp_tests)
set_target_properties(bmslogic_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/cpp_tests)

include(GoogleTest)
gtest_discover_tests(bmslogic_tests)
