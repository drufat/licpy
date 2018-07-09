# Copyright (C) 2010-2016 Dzhelil S. Rufat. All Rights Reserved.
def V(x, y):
    f = (1 - x ** 2) * (1 - y ** 2)
    return -3 * y * f, 3 * x * f
