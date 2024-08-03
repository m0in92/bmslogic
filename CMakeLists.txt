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
option(EMBEDDED "Only compiles the executables for the linux embedded system" OFF)

add_subdirectory(extern/pybind11)
add_subdirectory(extern/eigen)

# if (NO_CPP_TESTS)
#     message("NO_CPP_TESTS")
# else()
#     add_subdirectory(extern/google_tests)
#     if (WIN32)
#         set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
#     endif(WIN32)
#     add_subdirectory(cpp_tests)
# endif(NO_CPP_TESTS)

if(EMBEDDED)
    message("EMBEDDED")
elseif(NOT EMBEDDED)
    add_subdirectory(bmslogic)
    add_subdirectory(extern/google_tests)
    if (WIN32)
        set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
    endif(WIN32)
    add_subdirectory(cpp_tests)
endif()   
add_subdirectory(examples)
# add_subdirectory(cpp_tests)



