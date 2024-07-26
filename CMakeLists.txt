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
add_subdirectory(extern/eigen)
add_subdirectory(extern/google_tests)
if(CPP_ONLY)
    message("C++ ONLY")
elseif(NOT CPP_ONLY)
    add_subdirectory(bmslogic)
endif()   
add_subdirectory(examples)
add_subdirectory(cpp_tests)

if (WIN32)
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
endif(WIN32)


