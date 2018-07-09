# Copyright (C) 2010-2016 Dzhelil S. Rufat. All Rights Reserved.
from sympy import cos, sin, pi, S
from sympy.matrices import Matrix

vortex_spacing = S(7) / 8
a = Matrix([1, 0]) * vortex_spacing
b = Matrix([cos(pi / 3), sin(pi / 3)]) * vortex_spacing


def V(x, y):
    σ = - S(1) / 6
    vx, vy = 0, 0
    for (n, m, s) in [
        (0, 0, 1),
        (1, 0, σ),
        (0, 1, σ),
        (-1, 0, σ),
        (0, -1, σ),
        (-1, 1, σ),
        (1, -1, σ),
    ]:
        xv, yv = n * a + m * b
        rr = (x - xv) ** 2 + (y - yv) ** 2
        vx += -s * (y - yv) / rr
        vy += +s * (x - xv) / rr

    return vx, vy
