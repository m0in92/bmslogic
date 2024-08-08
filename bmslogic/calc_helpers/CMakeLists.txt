set(CALC_HELPER_SRC hummingbird.h hummingbird.cpp kalman_filter.h kalman_filter.cpp)

pybind11_add_module(calc_helpers MODULE binding_cpp_py.cpp ${CALC_HELPER_SRC})
target_include_directories(calc_helpers PUBLIC ${PROJECT_SOURCE_DIR}/extern/eigen)
set_target_properties(calc_helpers PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CALC_HELPERS_DIR})
set_target_properties(calc_helpers PROPERTIES LIBRARY_OUTPUT_DIRECTORY_DEBUG ${CALC_HELPERS_DIR})
set_target_properties(calc_helpers PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CALC_HELPERS_DIR})
