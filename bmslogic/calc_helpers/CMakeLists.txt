set(CALC_HELPER_SRC kalman_filter.h kalman_filter.cpp)

# pybind11_add_module(calc_helpers MODULE binding_cpp_py.cpp ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.h ${PROJECT_SOURCE_DIR}/bmslogic/extern/owl.cpp kalman_filter.h kalman_filter.cpp)
pybind11_add_module(calc_helpers MODULE ${CALC_HELPER_SRC})
target_include_directories(calc_helpers PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic)
target_include_directories(calc_helpers PUBLIC ${PROJECT_SOURCE_DIR}/extern/eigen)
set_target_properties(calc_helpers PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bmslogic/calc_helpers)
set_target_properties(calc_helpers PROPERTIES LIBRARY_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/bmslogic/calc_helpers)
set_target_properties(calc_helpers PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/bmslogic/calc_helpers)