cmake_minimum_required(VERSION 3.12)
project(bmslogic)

# set variables for the relevant filepaths of the BMSLogic project.
set(CALC_HELPERS_DIR ${PROJECT_SOURCE_DIR}/bmslogic/calc_helpers)
set(CELL_SIM_DIR ${PROJECT_SOURCE_DIR}/bmslogic/simulations/cell)

if(${APPLE})
    set(CMAKE_CXX_STANDARD 20)
    set(CXX_STANDARD_REQUIRED OFF)
else()
    set(CXX_STANDARD 20)
    set(CXX_STANDARD_REQUIRED FALSE)
endif()

# option(CPP_ONLY "Only compiles the executables" OFF)
option(EMBEDDED "Only compiles the executables for the linux embedded system" OFF)

# add the subdirectory to the extern libraries
add_subdirectory(extern/pybind11)
add_subdirectory(extern/eigen)
add_subdirectory(extern/cpp_plotting)

# add subdirectories to this project directories
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



