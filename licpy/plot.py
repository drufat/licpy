# Copyright (C) 2010-2018 Dzhelil S. Rufat. All Rights Reserved.
import matplotlib.pyplot as plt
import numpy as np


def grey_save(name, tex):
    tex = tex[:, ::-1]
    tex = tex.T

    M, N = tex.shape
    texture = np.empty((M, N, 4), np.float32)
    texture[:, :, 0] = tex
    texture[:, :, 1] = tex
    texture[:, :, 2] = tex
    texture[:, :, 3] = 1

    plt.imsave(name, texture)
