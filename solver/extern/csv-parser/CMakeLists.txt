cmake_minimum_required(VERSION 3.20)

add_subdirectory(csv-parser)

include(../../cmake/cuda_safe_wrapper.cmake)

make_cuda_safe_wrapper(
    csv_wrapped
    csv
)