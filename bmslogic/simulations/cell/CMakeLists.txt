set(PYBIND11_SOURCES bindings_cpp_py.cpp battery_components.h battery_components.cpp)

pybind11_add_module(cell SHARED ${PYBIND11_SOURCES})
target_include_directories(cell PUBLIC ${PROJECT_SOURCE_DIR}/bmslogic)

if (MSVC)
    set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY bmslogic/)
    set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY_DEBUG bmslogic/)
    set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE bmslogic/)
endif(MSVC)
