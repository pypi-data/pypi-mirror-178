def spotlight_width(H, BWa, Lsar):
    ...

def phase_correction(x, phi, nsub=None, axis=-2, ftshift=True):
    ...

def pgaf_sm_1iter(x, windb=None, est='ML', deg=4, axis=-2, isrmlpe=False, iscrct=False, isplot=False):
    r"""perform phase gradient autofocus 1 iter

    Perform phase gradient autofocus 1 iter as described in [1].

    revised for stripmap SAR

    - [1] C.V. Jakowatz, D.E. Wahl, P.H. Eichel, D.C. Ghiglia, P.A. Thompson,
    {\em Spotlight-mode Synthetic Aperture Radar: A Signal Processing
    Approach.} Springer, 1996.

    - [2] D.E. Wahl, P.H. Eichel, D.C. Ghiglia, C.V. Jakowatz, "Phase
    gradient autofocus-a robust tool for high resolution SAR phase
    correction," IEEE Trans. Aero. & Elec. Sys., vol. 30, no. 3, 1994.

    Args:
        x (Tensor): Complex SAR image :math:`{\bm X}\in {\mathbb C}^{N×N_a×N_r}`, where :math:`N` is the batchsize.
        windb (None or float, optional): Cutoff for window (the default is None, which use the mean as the cutoff.)
        est (str, optional): Estimator, ``'ML'`` for Maximum Likelihood estimation, ``'LUMV'`` for Linear Unbiased Minimum Variance estimation (the default is 'ML')
        deg (int): The degree of polynominal
        axis (int, optional): Autofocus axis.
        isrmlpe (bool, optional): Is remove linear phase error? (the default is False)
        iscrct (bool, optional): Is corrected image? (the default is False)
        isplot (bool, optional): Is plot estimated phase error? (the default is False)

    Returns:
        xc (Tensor): Corrected SAR image :math:`{\bm Y}\in {\mathbb C}^{N×N_a×N_r}`, only if :attr:`iscrct` is ``True``, xc is returned.
        phi (Tensor): Estimated phase error :math:`\phi\in {\mathbb R}^{N×N_a}`.

    Raises:
        TypeError: :attr:`x` is complex and should be in complex or real represent formation!
        ValueError: Not supported estimator! Supported are ``'ML'`` and ``'LUMV'``.

    """

def pgaf_sm(SI, nsar, nsub=None, windb=None, est='ML', deg=4, niter=None, tol=1.e-6, isplot=False, islog=False):
    r"""Phase gradient autofocus for stripmap SAR.

    Phase gradient autofocus for stripmap SAR.

    Args:
        SI (Tensor): Complex SAR image :math:`N_a×N_r`.
        nsar (int): Number of synthetic aperture pixels.
        nsub (int, optional): Number of sub-aperture pixels. (the default is :math:`{\rm min}{N_{sar}, N_a}`)
        windb (None or float, optional): cutoff for window (the default is None, which use the mean as the cutoff.)
        est (str, optional): estimator, ``'ML'`` for Maximum Likelihood estimation, ``'LUMV'`` for Linear Unbiased Minimum Variance estimation (the default is 'ML')
        deg (int): Polynomial degrees (default 4) to fit the error, once fitted, the term of deg=[0,1] will be removed.
            If :attr:`deg` is None or lower than 2, then we do not fit the error with polynominal and not remove the linear trend.
        niter (int, optional): Maximum iters (the default is None, which means using :attr:`tol` for stopping)
        tol (float, optional): Phase error tolerance. (the default is 1.e-6)
        isplot (bool, optional): Plot estimated phase error or corrected image. (the default is False)
        islog (bool, optional): Print log information? (the default is False)

    Returns:
        SI (Tensor): Corrected SAR image :math:`{\bm X}\in {\mathbb C}^{N_a×N_r}`.
        phi (Tensor): Estimated phase error :math:`{\phi}\in {\mathbb R}^{N_a×1}`.

    Raises:
        TypeError: The input is complex and should be in complex or real represent formation!
        ValueError: For stripmap SAR, processing sub aperture should be smaller than synthetic aperture!
    """


