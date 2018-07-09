# Copyright (C) 2010-2016 Dzhelil S. Rufat. All Rights Reserved.
from sympy import sin, pi

from licpy.vectorfields import ring


def V(x, y):
    return ring.V(sin(pi * x / 2), sin(pi * y / 2))
