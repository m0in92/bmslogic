cmake_minimum_required(VERSION 3.12)
project(bmslogic)

if(${APPLE})
    set(CMAKE_CXX_STANDARD 20)
    set(CXX_STANDARD_REQUIRED OFF)
else()
    set(CXX_STANDARD 20)
    set(CXX_STANDARD_REQUIRED FALSE)
endif()

option(CPP_ONLY "Only compiles the executables" OFF)

add_subdirectory(extern/pybind11)
if(CPP_ONLY)
    message("C++ ONLY")
elseif(NOT CPP_ONLY)
    add_subdirectory(bmslogic)
endif()   
add_subdirectory(examples)


