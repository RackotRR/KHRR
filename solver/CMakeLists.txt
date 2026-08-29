cmake_minimum_required(VERSION 3.20)
project(RRGalaxSim CXX)


add_subdirectory(extern)
add_subdirectory(lib/rrgsim_common)
add_subdirectory(lib/rrgsim_io)
add_subdirectory(lib/rrgsim_nbody)
add_subdirectory(app)