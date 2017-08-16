from licpy.resample import resample_s, resample_endpoints_s


def interpol(v, i, j, sx, sy):
    v00 = v[i, j]
    v01 = v[i, j + 1]
    v10 = v[i + 1, j]
    v11 = v[i + 1, j + 1]
    v = (
        v00 * (1 - sx) * (1 - sy) +
        v01 * (1 - sx) * sy +
        v10 * sx * (1 - sy) +
        v11 * sx * sy
    )
    return v


def pixelize(N, M, x, y, v):
    i, sx = resample_s(x, N)
    j, sy = resample_s(y, M)
    i, sx = i[:, None], sx[:, None]
    j, sy = j[None, :], sy[None, :]

    return interpol(v, i, j, sx, sy)

def pixelize_endpoints(N, M, x, y, v):
    i, sx = resample_endpoints_s(x, N)
    j, sy = resample_endpoints_s(y, M)
    i, sx = i[:, None], sx[:, None]
    j, sy = j[None, :], sy[None, :]

    return interpol(v, i, j, sx, sy)
