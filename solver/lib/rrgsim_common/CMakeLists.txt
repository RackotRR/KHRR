cmake_minimum_required(VERSION 3.18)
project(rrgsim_common LANGUAGES CXX CUDA)

find_package(CUDAToolkit REQUIRED)
find_package(CCCL REQUIRED COMPONENTS libcudacxx)

# цель для настройки общих параметров
add_library(rrgsim_common_properties INTERFACE)
target_compile_definitions(rrgsim_common_properties
    INTERFACE
        FMT_UNICODE=0
)
set_target_properties(rrgsim_common_properties PROPERTIES
    CUDA_SEPARABLE_COMPILATION  ON
    CUDA_RESOLVE_DEVICE_SYMBOLS ON
    CUDA_ARCHITECTURES          native
    CXX_STANDARD                20
    CUDA_STANDARD               20
)
target_link_libraries(rrgsim_common_properties
    INTERFACE
        CUDA::cudart
        CCCL::libcudacxx
        spdlog
)
target_link_options(rrgsim_common_properties
    INTERFACE
        /NODEFAULTLIB:LIBCMT
)

# библиотека с общим кодом
add_library(rrgsim_common STATIC
    src/co_particles.cu
)

target_include_directories(rrgsim_common
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)

target_link_libraries(rrgsim_common
    PUBLIC
        rrgsim_common_properties
)

