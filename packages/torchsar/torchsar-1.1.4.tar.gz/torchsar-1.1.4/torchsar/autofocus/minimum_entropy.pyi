def __entropy(X):
    ...

def meaf_ssa_sm(x, niter=10, delta=None, toli=1e-2, tolo=1e-2, ftshift=True, islog=False):
    r"""Stage-by-Stage minimum entropy

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

def meaf_sm(x, phi=None, niter=10, tol=1e-4, eta=0.1, method='N-MEA', selscat=False, isunwrap=True, deg=None, axis=-2, ftshift=True, islog=False):
    r"""Entropy based autofocus

    Minimum-Entropy based Autofocus (MEA)

    Args:
        x (Tensor): complex image with shape :math:`N×N_a×N_r` or :math:`N×N_a×N_r×2`
        phi (Tensor, optional): initial value of :math:`\phi` (the default is None, which means zeros)
        niter (int, optional): number of iterations (the default is 10)
        tol (float, optional): Error tolerance.
        eta (float, optional): Learning rate.
        method (str, optional): method used to update the phase error
            - ``'FP-MEA'`` --> Fix Point
            - ``'CD-MEA'`` --> Coordinate Descent
            - ``'SU-MEA'`` --> Simultaneous Update
            - ``'N-MEA'`` --> Newton, see [2], [1] has problem when used to small image
            - ``'SN-MEA'`` --> Simplified Newton
            - ``'MN-MEA'`` --> Modified Newton
        selscat (bool, optional): Select brighter scatters (default: False).
        isunwrap (bool, optional): Unwrap radian phase (default: True).
        deg (int or None, optional): The degree of polynominal, if None, no fitting.
        axis (int, optional): Compensation axis.
        ftshift (bool, optional): Does shift zero frequency to center?
        islog (bool, optional): Does print log info.


        see [1] Zhang S , Liu Y , Li X . Fast Entropy Minimization Based Autofocusing Technique for ISAR Imaging[J]. IEEE Transactions on Signal Processing, 2015, 63(13):3425-3434.
            [2] Zeng T , Wang R , Li F . SAR Image Autofocus Utilizing Minimum-Entropy Criterion[J]. IEEE Geoence & Remote Sensing Letters, 2013, 10(6):1552-1556.

    Returns:
        (Tensor): Description
    """


