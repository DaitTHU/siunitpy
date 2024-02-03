from ..utilcollections.constclass import ConstClass

__all__ = ['prefix']


class prefix(ConstClass):
    # SI prefixes
    Q = quetta = 1e30
    R = ronna = 1e27
    Y = yotta = 1e24
    Z = zetta = 1e21
    E = exa = 1e18
    P = peta = 1e15
    T = tera = 1e12
    G = giga = 1e9
    M = mega = 1e6
    k = kilo = 1e3
    h = hecto = 1e2
    da = deca = 1e1
    d = deci = 1e-1
    c = centi = 1e-2
    m = milli = 1e-3
    u = micro = 1e-6
    n = nano = 1e-9
    p = pico = 1e-12
    f = femto = 1e-15
    a = atto = 1e-18
    z = zepto = 1e-21
    y = yocto = 1e-24
    r = ronto = 1e-27
    q = quecto = 1e-30
    # binary prefixes
    ki = kibi = int(2**10)
    Mi = mebi = int(2**20)
    Gi = gibi = int(2**30)
    Ti = tebi = int(2**40)
    Pi = pebi = int(2**50)
    Ei = exbi = int(2**60)
    Zi = zebi = int(2**70)
    Yi = yobi = int(2**80)
