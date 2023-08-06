def rcmc_interp(Sr, tr, D):
    r"""range migration correction with linear interpolation

    Range migration correction with linear interpolation.

    Parameters
    ----------
    Sr : tensor
        SAR raw data :math:`N_a×N_r` in range dopplor domain
    tr : 1d-tensor
        time array :math:`N_r×1` in range
    D : 1d-tensor
        :math:`N_a×1` migration factor vector

    Returns
    -------
    Srrcmc
        data after range migration correction :math:`N_a×N_r`
    """


