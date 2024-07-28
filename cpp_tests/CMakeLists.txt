enable_testing()

set(CELL_DIR ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell)
set(CALC_HELPERS_DIR ${PROJECT_SOURCE_DIR}/bmslogic/calc_helpers)

set(BMSLOGIC_SOURCES ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.h ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.cpp
                    ${CELL_DIR}/battery_components.h ${CELL_DIR}/battery_components.cpp
                    ${CELL_DIR}/cyclers.h ${CELL_DIR}/cyclers.cpp
                    ${CALC_HELPERS_DIR}/kalman_filter.h ${CALC_HELPERS_DIR}/kalman_filter.cpp)
set(BMSLOGIC_INCLUDE_DIRS ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic)

add_executable(bmslogic_tests test_battery_components.cpp test_cyclers.cpp test_kalman_filter.cpp ${BMSLOGIC_SOURCES})
target_link_libraries(bmslogic_tests gtest gtest_main)
target_include_directories(bmslogic_tests PUBLIC ${BMSLOGIC_INCLUDE_DIRS} 
                                                    ${PROJECT_SOURCE_DIR}/extern/eigen
                                                    ${CALC_HELPERS_DIR})
include_directories(${PROJECT_SOURCE_DIR}/extern/google_tests/googletest/googletest/include 
                    ${PROJECT_SOURCE_DIR}/extern/google_tests/googletest)
set_target_properties(bmslogic_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/cpp_tests)

