def chirp_tran(t, Tp, K, Fc, a=1.):
    ...

def chirp_recv(t, Tp, K, Fc, a=1., g=1., r=1e3):
    ...

class Chirp(th.nn.Module):
    ...

    def __init__(self, Tp, K, Fc=0., a=1.):
        ...

    def tran(self, t):
        ...

    def recv(self, t, g, r):

