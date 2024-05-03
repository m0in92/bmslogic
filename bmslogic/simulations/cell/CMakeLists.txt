pybind11_add_module(cell SHARED bindings_cpp_py.cpp battery_components.h battery_components.cpp)
target_include_directories(cell PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic)
