# Copyright (C) 2010-2016 Dzhelil S. Rufat. All Rights Reserved.
from licpy.vectorfields.transform import radial


@radial
def V(r, θ):
    return 0, 1 / r
