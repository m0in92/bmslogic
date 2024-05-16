pybind11_add_module(extern MODULE binding_cpp_python.cpp hummingbird.h hummingbird.cpp)
set_target_properties(extern PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bmslogic/extern)
set_target_properties(extern PROPERTIES LIBRARY_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/bmslogic/extern)
set_target_properties(extern PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR}/bmslogic/extern)