def dsm2sar_fd(g, pdict, mode='StationaryTarget2D', ftshift=True, device='cpu'):
    """Frequency-domain simulation

    SAR raw data simulation by frequency-domain method.

    Parameters
    ----------
    g : tensor
        The digital scene matrix.
    pdict : dict
        The SAR platform parameters.
    mode : str, optional
        Simulation mode.
    ftshift : bool, optional
        Shift zero-frequency to center?
    device : str, optional
        Specifies which device to be used.

    Returns
    -------
    tensor
        Simulated SAR raw data.
    """


