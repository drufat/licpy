# Copyright (C) 2010-2016 Dzhelil S. Rufat. All Rights Reserved.
from sympy import exp, sqrt


def V(x, y):
    dx = x
    dy = y + 1
    ds = sqrt(dx ** 2 + dy ** 2)
    c = exp(-2 * x ** 2 / dy ** 2)
    return c * dx / ds, c * dy / ds
