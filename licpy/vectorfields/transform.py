# Copyright (C) 2010-2016 Dzhelil S. Rufat. All Rights Reserved.
from sympy import (sqrt, atan2, sin, cos, pi)


def radial(Vrad):
    def V(x, y):
        r = sqrt(x ** 2 + y ** 2)
        θ = atan2(y, x)
        Vr, Vθ = Vrad(r, θ)
        Vx = cos(θ) * Vr - r * sin(θ) * Vθ
        Vy = sin(θ) * Vr + r * cos(θ) * Vθ
        return Vx, Vy

    return V


def periodicdomain(V):
    def Vperiodic(x, y):
        return V(x / pi - 1, y / pi - 1)

    return Vperiodic
