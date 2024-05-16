add_subdirectory(calc_helpers)
add_subdirectory(simulations/cell)
add_subdirectory(extern)

# if (MSVC)
#     set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${SOURCE_DIR})
#     set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY_DEBUG ${SOURCE_DIR})
#     set_target_properties(cell PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE ${SOURCE_DIR})
# endif(MSVC)