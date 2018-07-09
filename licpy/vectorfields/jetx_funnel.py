# Copyright (C) 2010-2016 Dzhelil S. Rufat. All Rights Reserved.
from sympy import exp, sqrt


def V(x, y):
    dx = x + 1
    dy = y
    ds = sqrt(dx ** 2 + dy ** 2)
    c = exp(-2 * y ** 2 / dx ** 2)
    return c * dx / ds, c * dy / ds
