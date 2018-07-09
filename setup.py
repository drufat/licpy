# Copyright (C) 2010-2016 Dzhelil S. Rufat. All Rights Reserved.

import numpy
import pybind11
from setuptools import setup, Extension

include_dirs = [
    'src',
    numpy.get_include(),
    pybind11.get_include(True),
    pybind11.get_include(False),
]

depends = [
    'setup.py',
]

extra_compile_args = [
    '-std=c++11',
]

ext_modules = [

    Extension(
        'licpy.resample',
        sources=[
            'licpy/resample.cpp',
        ],
        depends=depends,
        include_dirs=include_dirs,
        extra_compile_args=extra_compile_args,
        language="c++",
    ),
]

setup(
    name='licpy',
    packages=['licpy'],
    package_dir={'licpy': 'licpy'},
    ext_modules=ext_modules,
    version='0.2',
    description='Line Integral Convolution',
    author='Dzhelil Rufat',
    author_email='drufat@fastmail.com',
    license='GNU GPLv3',
    url='http://github.com/drufat/licpy.git',
    requires=[
        'pybind11',
        'numpy',
        'sympy',
        'tensorflow',
    ],
)
