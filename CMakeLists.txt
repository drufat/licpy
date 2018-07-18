cmake_minimum_required(VERSION 3.6)
project(licpy)

add_compile_options(
        -std=c++14
        -Wall
)

include_directories(~/.local/include/python3.6m)

find_package(PyBindCpp REQUIRED PATHS ../pybindcpp/cmake)
include_directories(${PYTHON_INCLUDE_DIR})
include_directories(${NUMPY_INCLUDE_DIR})

function(pymodule target name)
    py_module(${target} ${name} ${ARGN})
endfunction(pymodule)

pymodule(resample resample
    licpy/resample.cpp
)
