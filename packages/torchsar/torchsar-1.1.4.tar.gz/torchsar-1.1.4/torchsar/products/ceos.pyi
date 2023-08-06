def decfmtfceos(F, n, x, b, e='<'):
    r"""decode format descriptor of CEOS

    decode format descriptor of CEOS.

    ``'nFx'`` --> decode :attr:`b` x Bytes-by-x Bytes as format :attr:`F` specified,
    and do :attr:`n` times.

    Parameters
    ----------
    F : str
        formation string, ``C`` --> Complex(real, imag), ``F`` --> float, ``B`` --> Bytes, ``A`` --> String, ``I`` --> asicc
    n : int
        amount of elements with formation :attr:`F`
    x : int
        number of Bytes
    b : bytes
        bytes to be decoded
    e : str, optional
        endian, ``'<'`` --> little, ``'>'`` -- > big (the default is '<', which means little endian)

    Returns
    -------
    list
        decoded result list.
    """

def _getdtype_component(fmtrcd, fmtuser):
    ...

def read_ceos_sar_raw(filepath, sl=1, el=-1, rmbp=False):
    r"""read CEOS SAR raw data

    read CEOS SAR raw data pulse from line :attr:`sl` to line :attr:`el`.

    Parameters
    ----------
    filepath : str
        SAR raw data file path string, for ERS1/2 --> ``*.raw`` for RADARSAT --> ``DAT_01.001``
    sl : int, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : int, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : bool, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    S : 2d-array


    """

def read_ceos_sar_slc(filepath, sl=1, el=-1, rmbp=False):
    r"""read CEOS SAR slc data

    read CEOS SAR slc data from line :attr:`sl` to line :attr:`el`.

    Parameters
    ----------
    filepath : str
        SAR slc data file path string, for ERS1/2 --> ``*.D`` for RADARSAT --> ``DAT_01.001``
    sl : int, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : int, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : bool, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    S : 2d-array
       Processed SLC SAR data matrix.

    """


