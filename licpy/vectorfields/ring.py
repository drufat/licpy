# Copyright (C) 2010-2016 Dzhelil S. Rufat. All Rights Reserved.
from sympy import (exp, Rational)

from licpy.vectorfields.transform import radial


@radial
def V(r, θ, c=Rational(1, 6)):
    return (
        0,
        1 / r * exp(-(r - 1 / 2) ** 2 / 2 / c ** 2)
    )
