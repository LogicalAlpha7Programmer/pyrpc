# Define generic type variables
from typing import Callable


# Pipe function with up to 20 transformations
def pipe[
    A, B, C, D, E, F, G, H, I, J, K, U
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
) -> K:
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
    return k


def flow[
    A, B, C, D, E, F, G, H, I, J, K
](
    fb: Callable[[A | None], B],
    fc: Callable[[B], C] = lambda x: x,
    fd: Callable[[C], D] = lambda x: x,
    fe: Callable[[D], E] = lambda x: x,
    ff: Callable[[E], F] = lambda x: x,
    fg: Callable[[F], G] = lambda x: x,
    fh: Callable[[G], H] = lambda x: x,
    fi: Callable[[H], I] = lambda x: x,
    fj: Callable[[I], J] = lambda x: x,
    fk: Callable[[J], K] = lambda x: x,
) -> Callable[[A],K]:
    def compose(a: A | None = None):
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
        )

    return compose

