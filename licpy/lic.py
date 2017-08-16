import numpy as np
import tensorflow as tf

from licpy.pixelize import pixelize

INF = 1e10


def get_t1(u, f):
    if u == 0.0:
        return INF
    if u > 0:
        return (1 - f) / u
    else:
        return - f / u


def advance1(ux, uy, fx, fy):
    '''
    >>> advance1(1.0, 0.0, 0.6, 0.3)
    (0.4, 1, 0, 0.0, 0.3)
    >>> advance1(0.0, 1.0, 0.6, 0.3)
    (0.7, 0, 1, 0.6, 0.0)
    '''
    tx = get_t1(ux, fx)
    ty = get_t1(uy, fy)

    if tx < ty:
        t = tx
    else:
        t = ty

    dx, dy = 0, 0
    if tx < ty:
        if ux > 0:
            dx = +1
            fx = 0.0
        else:
            dx = -1
            fx = 1.0
        fy += t * uy
    else:
        if uy > 0:
            dy = +1
            fy = 0.0
        else:
            dy = -1
            fy = 1.0
        fx += t * ux

    return t, dx, dy, fx, fy


def get_t(u, f):
    return tf.where(
        tf.equal(u, 0.0),
        INF * tf.ones_like(u),
        tf.where(
            tf.greater(u, 0),
            (1 - f) / u,
            -f / u
        ))


def advance(ux, uy, fx, fy):
    '''
    >>> ux_ = tf.placeholder(tf.float64, [None])
    >>> uy_ = tf.placeholder(tf.float64, [None])
    >>> fx_ = tf.placeholder(tf.float64, [None])
    >>> fy_ = tf.placeholder(tf.float64, [None])
    >>> g = advance(ux_, uy_, fx_, fy_)
    >>> ux = [1.0, 0.0]
    >>> uy = [0.0, 1.0]
    >>> fx = [0.6, 0.6]
    >>> fy = [0.3, 0.3]
    >>> with tf.Session() as sess:
    ...     sess.run(g, feed_dict={ux_:ux, uy_:uy, fx_:fx, fy_:fy})
    (array([ 0.4,  0.7]), array([1, 0]), array([0, 1]), array([ 0. ,  0.6]), array([ 0.3,  0. ]))
    '''
    tx = get_t(ux, fx)
    ty = get_t(uy, fy)

    cond = tx < ty
    t = tf.where(
        cond,
        tx,
        ty,
    )

    fx += t * ux
    fy += t * uy

    one = tf.ones_like(fx)
    zero = tf.zeros_like(fy)

    fx = tf.where(
        cond,
        tf.where(
            ux > 0,
            zero,
            one,
        ),
        fx,
    )

    fy = tf.where(
        cond,
        fy,
        tf.where(
            uy > 0,
            zero,
            one,
        ),
    )

    one = tf.cast(one, dtype=tf.int64)
    zero = tf.cast(zero, dtype=tf.int64)

    dx = tf.where(
        cond,
        tf.where(
            ux > 0,
            one,
            -one,
        ),
        zero,
    )

    dy = tf.where(
        cond,
        zero,
        tf.where(
            uy > 0,
            one,
            -one,
        ),
    )

    return t, dx, dy, fx, fy


def advance_tmax(ux, uy, fx, fy, tmax):
    t_, dx_, dy_, fx_, fy_ = advance(ux, uy, fx, fy)

    cond = (t_ < tmax)

    zero = tf.zeros_like(fy)

    t = tf.where(cond, t_, zero + tmax)
    fx = tf.where(cond, fx_, fx + t * ux)
    fy = tf.where(cond, fy_, fy + t * uy)

    zero = tf.cast(zero, dtype=tf.int64)

    dx = tf.where(cond, dx_, zero)
    dy = tf.where(cond, dy_, zero)

    return t, dx, dy, fx, fy


def advance_smax(ux, uy, fx, fy, smax):
    u = tf.sqrt(ux ** 2 + uy ** 2)
    tmax = smax / u

    t_, dx_, dy_, fx_, fy_ = advance(ux, uy, fx, fy)

    cond = (t_ * u < smax)

    zero = tf.zeros_like(fy)

    t = tf.where(cond, t_, zero + tmax)
    fx = tf.where(cond, fx_, fx + t * ux)
    fy = tf.where(cond, fy_, fy + t * uy)

    zero = tf.cast(zero, dtype=tf.int64)

    dx = tf.where(cond, dx_, zero)
    dy = tf.where(cond, dy_, zero)

    return t, dx, dy, fx, fy


def bc(x, y, fx, fy, N, M):
    z = tf.zeros_like(x)
    fz = tf.zeros_like(fx)

    # Boundary conditions
    cond = (x < 0)
    x = tf.where(cond, z, x)
    fx = tf.where(cond, fz, fx)
    cond = (x >= N)
    x = tf.where(cond, z + N - 1, x)
    fx = tf.where(cond, fz + 1, fx)

    cond = (y < 0)
    y = tf.where(cond, z, y)
    fy = tf.where(cond, fz, fy)
    cond = (y >= M)
    y = tf.where(cond, z + M - 1, y)
    fy = tf.where(cond, fz + 1, fy)

    return x, y, fx, fy


def f(x):
    return tf.cast(x, tf.float64)


def loop(vx, vy, h, s, t, x, y, fx, fy, L, N, M, tex, tmax=None, smax=None):
    def cond(i, *args):
        return i < L

    def step(i, h, s, t, x, y, fx, fy, pix):
        xy = tf.stack([x, y], axis=-1)
        ux = tf.gather_nd(vx, xy)
        uy = tf.gather_nd(vy, xy)
        p = tf.gather_nd(tex, xy)
        if tmax is not None:
            dt, dx, dy, fx, fy = advance_tmax(ux, uy, fx, fy, tmax - t)
        elif smax is not None:
            dt, dx, dy, fx, fy = advance_smax(ux, uy, fx, fy, smax - s)
        else:
            dt, dx, dy, fx, fy = advance(ux, uy, fx, fy)
        v = tf.sqrt(ux ** 2 + uy ** 2)
        ds = dt * v
        dh = ds  # add weight function here
        pix += p * dh
        h += dh
        s += ds
        t += dt
        x += dx
        y += dy
        x, y, fx, fy = bc(x, y, fx, fy, N, M)
        i += 1
        return i, h, s, t, x, y, fx, fy, pix

    pix = tf.zeros_like(tex)
    return tf.while_loop(
        cond,
        step,
        [0, h, s, t, x, y, fx, fy, pix],
    )


def lic_points(vx, vy, px, py, L, N, M, tmax=None, smax=None):
    """
    >>> index_ = tf.placeholder(tf.int64, [None, 2])
    >>> params_ = tf.placeholder(tf.string, [None, None])
    >>> g = tf.gather_nd(params_, index_)
    >>> index = [[0, 3], [0, 2], [1, 0]]
    >>> params = [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h']]
    >>> with tf.Session() as sess:
    ...    sess.run(g, feed_dict={index_:index, params_:params})
    array([b'd', b'c', b'e'], dtype=object)
    """
    tex = tf.zeros_like(vx)

    x, y = [tf.cast(tf.floor(_), tf.int64) for _ in [px, py]]
    fx, fy = px - f(x), py - f(y)

    h = tf.zeros_like(px)
    s = tf.zeros_like(px)
    t = tf.zeros_like(px)

    P = [[f(x) + fx, f(y) + fy]]
    S = [s]
    T = [t]
    for _ in range(L):
        _, h, s, t, x, y, fx, fy, _ = loop(vx, vy, h, s, t, x, y, fx, fy, 1, N, M, tex, tmax, smax)
        P.append([f(x) + fx, f(y) + fy])
        S.append(s)
        T.append(t)

    return P, S, T


def line_integral_convolution(tex, vx, vy, L, N, M, tmax=None, smax=None):
    shape = tf.shape(tex)
    x = tf.range(shape[0])
    y = tf.range(shape[1])
    x = tf.cast(x, tf.int64)
    y = tf.cast(y, tf.int64)
    x, y = tf.meshgrid(x, y, indexing='ij')
    fx = tf.zeros_like(vx) + 0.5
    fy = tf.zeros_like(vy) + 0.5
    h = tf.zeros_like(tex)
    s = tf.zeros_like(tex)
    t = tf.zeros_like(tex)
    _, h1, _, _, _, _, _, _, pix1 = loop(vx, vy, h, s, t, x, y, fx, fy, L, N, M, tex, tmax, smax)
    _, h2, _, _, _, _, _, _, pix2 = loop(-vx, -vy, h, s, t, x, y, fx, fy, L, N, M, tex, tmax, smax)
    return (pix1 + pix2) / (h1 + h2)


def runlic_resample(N, M, x, y, vx, vy, L, magnitude=True):
    vx = pixelize(N, M, x, y, vx)
    vy = pixelize(N, M, x, y, vy)
    return runlic(vx, vy, L, magnitude)


def runlic(vx, vy, L, magnitude=True):
    assert vx.shape == vy.shape
    N, M = vx.shape
    np.random.seed(13)
    tex = np.random.rand(N, M)

    tex_ = tf.placeholder(tf.float64, [N, M])
    vx_ = tf.placeholder(tf.float64, [N, M])
    vy_ = tf.placeholder(tf.float64, [N, M])

    tex_out_ = line_integral_convolution(tex_, vx_, vy_, L, N, M, smax=0.8 * L)
    if magnitude:
        tex_out_ *= tf.erf(tf.sqrt(vx_ ** 2 + vy_ ** 2))
    # tex_out_ = 1 - tex_out_

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    with tf.Session(config=config):
        tex_out = tex_out_.eval(feed_dict={tex_: tex, vx_: vx, vy_: vy})

    return tex_out
