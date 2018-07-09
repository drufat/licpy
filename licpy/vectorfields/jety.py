# Copyright (C) 2010-2016 Dzhelil S. Rufat. All Rights Reserved.
from sympy import exp, Rational


def V(x, y, c=Rational(1, 6)):
    return (0, exp(-x ** 2 / 2 / c ** 2))
