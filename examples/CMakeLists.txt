add_subdirectory(simulations/cell)

add_executable(timed_sim ${PROJECT_SOURCE_DIR}/examples/simulations/pack/timed_simulation.cpp)
target_include_directories(timed_sim PRIVATE ${PROJECT_SOURCE_DIR}/bmslogic/simulations/pack/)