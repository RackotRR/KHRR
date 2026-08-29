cmake_minimum_required(VERSION 3.20)
project(rrgsim CXX CUDA)

add_executable(${PROJECT_NAME}
    src/rrgsim.cu
    src/rrgsim_log.cpp
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)


target_link_libraries(${PROJECT_NAME}
    PUBLIC
        rrgsim_common
        rrgsim_io
        rrgsim_nbody
)