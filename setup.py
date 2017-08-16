# Copyright (C) 2010-2016 Dzhelil S. Rufat. All Rights Reserved.
import glob, os

import numpy
from setuptools import setup, Extension

include_dirs = [
    'src',
    '../pybindcpp/include',
    numpy.get_include(),
]

depends = [
              'setup.py',
          ]

extra_compile_args = [
    '-std=c++14',
]

libraries = []

if ('CC' in os.environ) and ('gcc' in os.environ['CC'] or 'g++' in os.environ['CC']):
    extra_compile_args += ['-fopenmp']
    libraries += ['gomp']

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
        libraries=libraries,
    ),
]

setup(
    name='licpy',
    packages=['licpy'],
    package_dir={'licpy': 'licpy'},
    ext_modules=ext_modules,
    version='0.1',
    description='Line Integral Convolution',
    author='Dzhelil Rufat',
    author_email='drufat@caltech.edu',
    license='GNU GPLv3',
    url='http://github.com/drufat/licpy.git',
    requires=[
        'numpy',
        'tensorflow',
        'pybindcpp',
    ],
)
