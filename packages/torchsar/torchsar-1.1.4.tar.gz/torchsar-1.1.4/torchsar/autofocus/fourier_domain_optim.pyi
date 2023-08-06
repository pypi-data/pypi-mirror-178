def __fdnorm(X, p):
    ...

def af_ffo_sm(x, p=2, niter=10, delta=None, toli=1e-2, tolo=1e-2, ftshift=True, islog=False):
    """Stage-by-Stage minimum entropy

    [1] Morrison Jr, Robert Lee; Autofocus, Entropy-based (2002): Entropy-based autofocus for synthetic aperture radar.

    Parameters
    ----------
    x : Tensor
       Corrupt complex SAR image. N-Na-Nr(complex) or N-Na-Nr-2(real)
    niter : int, optional
       The number of iteration (the default is 10)
    delta : {float or None}, optional
       The change step (the default is None (i.e. PI))
    toli : int, optional
       Tolerance error for inner loop (the default is 1e-2)
    tolo : int, optional
       Tolerance error for outer loop (the default is 1e-2)
    ftshift : bool, optional
       Shift the zero frequency to center? (the default is True)
    islog : bool, optional
       Print log information? (the default is False)
    """

def af_ffo(g, w=None, p=2, niter=10, eta=0.5, tol=1e-2, ftshift=False):

