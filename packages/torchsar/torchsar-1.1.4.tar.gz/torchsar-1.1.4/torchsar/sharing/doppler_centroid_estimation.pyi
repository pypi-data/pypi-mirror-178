def bdce_sf(Sr, Fsa, Fsr, rdflag=False, Nroff=0, isplot=False):
    r"""Baseband doppler centroid estimation by spectrum fitting

    Baseband doppler centroid estimation by spectrum fitting.

    Parameters
    ----------
    Sr : numpy array
        SAR signal :math:`N_a×N_r` in range-doppler domain (range frequency domain).
    Fsa : float
        Sampling rate in azimuth
    rdflag : bool
        Specifies whether the input SAR signal is in range-doppler domain. If not, :func:`dce_sf` excutes FFT in range direction.
    isplot : bool
        Whether to plot the estimated results.(Default: False)
    """

def bdce_api(Sr, Fsa, isplot=False):
    r"""Baseband doppler centroid estimation by average phase increment

    Baseband doppler centroid estimation by average phase increment.

    Parameters
    ----------
    Sr : numpy array
        SAR raw data or range compressed data
    Fsa : float
        Sampling rate in azimuth
    isplot : bool
        Whether to plot the estimated results.(Default: False)
    """

def bdce_madsen(Sr, Fsa, isplot=False):
    r"""Baseband doppler centroid estimation by madsen

    Baseband doppler centroid estimation bymadsen.

    Parameters
    ----------
    Sr : numpy array
        SAR raw data or range compressed data
    Fsa : float
        Sampling rate in azimuth
    isplot : bool
        Whether to plot the estimated results.(Default: False)
    """

def abdce_wda_ori(Sr, Fsa, Fsr, Fc, rate=0.9, isplot=False, islog=False):
    r"""Absolute and baseband doppler centroid estimation by wavelength diversity algorithm

    Absolute and baseband doppler centroid estimation by Wavelength Diversity Algorithm (WDA).

    <<合成孔径雷达成像_算法与实现>> p350.

    Parameters
    ----------
    Sr : numpy array
        SAR signal :math:`N_a×N_r` in range frequency domain.
    Fsa : float
        Sampling rate in azimuth.
    Fsr : float
        Sampling rate in range.
    """

def abdce_wda_opt(Sr, Fsr, Fsa, Fc, ncpb=None, tr=None, isfftr=False, isplot=False, islog=False):
    """Absolute and baseband doppler centroid estimation by wavelength diversity algorithm

    Absolute and baseband doppler centroid estimation by Wavelength Diversity Algorithm (WDA).

    <<合成孔径雷达成像_算法与实现>> p350.

    Parameters
    ----------
    Sr : 2d-tensor
        SAR signal :math:`N_a×N_r` in range frequency domain.
    Fsr : float
        Sampling rate in range, unit Hz.
    Fsa : float
        Sampling rate in azimuth, unit Hz.
    Fc : float
        Carrier frequency, unit Hz.
    ncpb : tuple or list, optional
        Number of cells per block, so we have blocks (int(Na/ncpb[0])) × (int(Nr/ncpb[1]))
        (the default is [Na, Nr], which means all).
    tr : 1d-tensor, optional
        Time in range (the default is None, which linspace(0, Nr, Nr)).
    isplot : bool, optional
        Whether to plot the estimation results (the default is False).
    isfftr : bool, optional
        Whether to do FFT in range (the default is False).

    Returns
    -------
    fadc : 2d-tensor
        Absolute doppler centroid frequency, which has the size specified by :attr:`ncpb`.
    fbdc : 2d-tensor
        Baseband doppler centroid frequency, which has the size specified by :attr:`ncpb`.
    Ma : 2d-tensor
        Doppler ambiguity number, which has the size specified by :attr:`ncpb`.
    """

def fullfadc(fdc, shape):

