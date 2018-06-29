#This is out of date. 

cmake_minimum_required(VERSION 3.6)
project(licpy)

add_compile_options(
        -std=c++14
        -Wall
)

include_directories(../pybindcpp/include)

find_package(PyBindCpp REQUIRED PATHS ../pybindcpp/cmake)
include_directories(${PYTHON_INCLUDE_DIR})
include_directories(${NUMPY_INCLUDE_DIR})

add_custom_target(
	    ${PROJECT_NAME}_pytest ALL
		COMMAND py.test -v --doctest-modules licpy
		WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

function(pymodule target name)
    py_module(${target} ${name} ${ARGN})
    add_dependencies(${PROJECT_NAME}_pytest ${target}_symlink)
endfunction(pymodule)

pymodule(resample resample
        licpy/resample.cpp
        )
