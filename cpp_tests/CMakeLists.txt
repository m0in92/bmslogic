enable_testing()

set(BMSLOGIC_SOURCES ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/battery_components.cpp ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell/battery_components.cpp)
set(BMSLOGIC_INCLUDE_DIRS ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell ${PROJECT_SOURCE_DIR}/bmslogic)

add_executable(bmslogic_tests test_battery_components.cpp ${BMSLOGIC_SOURCES})
target_link_libraries(bmslogic_tests gtest gtest_main)
target_include_directories(bmslogic_tests PUBLIC ${BMSLOGIC_INCLUDE_DIRS})
include_directories(${PROJECT_SOURCE_DIR}/extern/google_tests/googletest/googletest/include ${PROJECT_SOURCE_DIR}/extern/google_tests/googletest)
set_target_properties(bmslogic_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/cpp_tests)
