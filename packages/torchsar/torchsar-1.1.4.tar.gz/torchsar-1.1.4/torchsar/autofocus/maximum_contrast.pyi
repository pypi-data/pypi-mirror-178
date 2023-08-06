def mcaf_sm(x, phi=None, niter=10, tol=1e-4, eta=0.1, method='N-MCA', selscat=False, axis=-2, ftshift=True, islog=False):
    r"""Contrast based autofocus

    Maximum-Contrast based Autofocus (MCA)

    Parameters
    ----------
    x : Tensor
        complex image with shape :math:`N×N_a×N_r` or :math:`N×N_a×N_r×2`
    phi : float, optional
        initial value of :math:`\phi` (the default is None, which means zeros)
    niter : int, optional
        number of iterations (the default is 10)
    method : str, optional
        method used to update the phase error
        - ``'FP-MCA'`` --> Fix Point
        - ``'CD-MCA'`` --> Coordinate Descent
        - ``'SU-MCA'`` --> Simultaneous Update
        - ``'N-MCA'`` --> Newton, see [2], [1] has problem when used to small image
        - ``'SN-MCA'`` --> Simplified Newton
        - ``'MN-MCA'`` --> Modified Newton
    selscat : bool, optional
        Select brighter scatters.
    axis : int, optional
        Compensation axis.
    ftshift :  bool, optional
        Does shift zero frequency to center?
    islog :  bool, optional
        Does print log info.


    see [1] Zhang S , Liu Y , Li X . Fast Entropy Minimization Based Autofocusing Technique for ISAR Imaging[J]. IEEE Transactions on Signal Processing, 2015, 63(13):3425-3434.
        [2] Zeng T , Wang R , Li F . SAR Image Autofocus Utilizing Minimum-Entropy Criterion[J]. IEEE Geoence & Remote Sensing Letters, 2013, 10(6):1552-1556.
    """


