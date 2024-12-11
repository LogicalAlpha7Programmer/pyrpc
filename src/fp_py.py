# Define generic type variables
from typing import Callable


# Pipe function with up to 20 transformations
def pipe[
    A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U
](
    a: A,
    fb: Callable[[A], B],
    fc: Callable[[B], C] = lambda x: x,
    fd: Callable[[C], D] = lambda x: x,
    fe: Callable[[D], E] = lambda x: x,
    ff: Callable[[E], F] = lambda x: x,
    fg: Callable[[F], G] = lambda x: x,
    fh: Callable[[G], H] = lambda x: x,
    fi: Callable[[H], I] = lambda x: x,
    fj: Callable[[I], J] = lambda x: x,
    fk: Callable[[J], K] = lambda x: x,
    fl: Callable[[K], L] = lambda x: x,
    fm: Callable[[L], M] = lambda x: x,
    fn: Callable[[M], N] = lambda x: x,
    fo: Callable[[N], O] = lambda x: x,
    fp: Callable[[O], P] = lambda x: x,
    fq: Callable[[P], Q] = lambda x: x,
    fr: Callable[[Q], R] = lambda x: x,
    fs: Callable[[R], S] = lambda x: x,
    ft: Callable[[S], T] = lambda x: x,
    fu: Callable[[T], U] = lambda x: x,
) -> U:
    b = fb(a)
    c = fc(b)
    d = fd(c)
    e = fe(d)
    f = ff(e)
    g = fg(f)
    h = fh(g)
    i = fi(h)
    j = fj(i)
    k = fk(j)
    l = fl(k)
    m = fm(l)
    n = fn(m)
    o = fo(n)
    p = fp(o)
    q = fq(p)
    r = fr(q)
    s = fs(r)
    t = ft(s)
    u = fu(t)
    return u


def flow[
    A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U
](
    fb: Callable[[A], B],
    fc: Callable[[B], C] = lambda x: x,
    fd: Callable[[C], D] = lambda x: x,
    fe: Callable[[D], E] = lambda x: x,
    ff: Callable[[E], F] = lambda x: x,
    fg: Callable[[F], G] = lambda x: x,
    fh: Callable[[G], H] = lambda x: x,
    fi: Callable[[H], I] = lambda x: x,
    fj: Callable[[I], J] = lambda x: x,
    fk: Callable[[J], K] = lambda x: x,
    fl: Callable[[K], L] = lambda x: x,
    fm: Callable[[L], M] = lambda x: x,
    fn: Callable[[M], N] = lambda x: x,
    fo: Callable[[N], O] = lambda x: x,
    fp: Callable[[O], P] = lambda x: x,
    fq: Callable[[P], Q] = lambda x: x,
    fr: Callable[[Q], R] = lambda x: x,
    fs: Callable[[R], S] = lambda x: x,
    ft: Callable[[S], T] = lambda x: x,
    fu: Callable[[T], U] = lambda x: x,
):
    def compose(a: A):
        return pipe(
            a,
            fb,
            fc,
            fd,
            fe,
            ff,
            fg,
            fh,
            fi,
            fj,
            fk,
            fl,
            fm,
            fn,
            fo,
            fp,
            fq,
            fr,
            fs,
            ft,
            fu,
        )

    return compose
