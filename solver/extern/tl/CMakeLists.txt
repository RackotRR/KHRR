cmake_minimum_required(VERSION 3.20)

set(OPTIONAL_BUILD_TESTS OFF)
set(EXPECTED_BUILD_TESTS OFF)

add_subdirectory(optional)
add_subdirectory(expected)

add_library(rrgsim_tl INTERFACE)
target_link_libraries(rrgsim_tl
    INTERFACE
        tl::expected
        tl::optional
)
target_include_directories(rrgsim_tl
    INTERFACE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)