cmake_minimum_required(VERSION 3.12)
project(bmslogic)

set(CXX_STANDARD 20)
set(CXX_STANDARD_REQUIRED FALSE)

option(CPP_ONLY "Only compiles the executables" OFF)

add_subdirectory(extern/pybind11)
if(CPP_ONLY)
    message("C++ ONLY")
elseif(NOT CPP_ONLY)
    add_subdirectory(bmslogic)
endif()   
add_subdirectory(examples)


