# Copyright (C) 2010-2016 Dzhelil S. Rufat. All Rights Reserved.
import numpy as np


def c(f):
    return np.ctypeslib.as_ctypes(f.ravel())


def resample_wrap(imp):
    """
    >>> from licpy.resample import resample, resample_s
    >>> xx = np.array([1.1, 2.0, 3.1])
    >>> idx, yy = resample(xx, 10)
    >>> idx
    array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1], dtype=int32)
    >>> yy
    array([ 1.2,  1.4,  1.6,  1.8,  2. ,  2.2,  2.4,  2.6,  2.8,  3. ])
    >>> idx, ss = resample_s(xx, 10)
    >>> idx
    array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1], dtype=int32)
    >>> ss
    array([ 0.111,  0.333,  0.556,  0.778,  1.   ,  0.182,  0.364,  0.545,
            0.727,  0.909])

    >>> from licpy.resample import resample_endpoints, resample_endpoints_s
    >>> idx, yy = resample_endpoints(xx, 11)
    >>> idx
    array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], dtype=int32)
    >>> yy
    array([ 1.1,  1.3,  1.5,  1.7,  1.9,  2.1,  2.3,  2.5,  2.7,  2.9,  3.1])
    >>> idx, ss = resample_endpoints_s(xx, 11)
    >>> idx
    array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], dtype=int32)
    >>> ss
    array([ 0.   ,  0.222,  0.444,  0.667,  0.889,  0.091,  0.273,  0.455,
            0.636,  0.818,  1.   ])
    """

    def _(f, N):
        f = np.ascontiguousarray(f, dtype='double')
        out = np.empty(N, dtype='int32')
        fout = np.empty(N, dtype='double')
        imp(c(f), f.shape[0], c(out), c(fout), N)
        return out, fout

    return _
