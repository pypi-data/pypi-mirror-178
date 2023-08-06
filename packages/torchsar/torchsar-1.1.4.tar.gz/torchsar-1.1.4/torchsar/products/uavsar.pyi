def read_uavsar_csm(filepath, sl=1, el=-1, rmbp=False):
    r"""read UAVSAR raw data

    read UAVSAR SAR raw data pulse from line :attr:`sl` to line :attr:`el`. This function call
    function :func:`read_ceos_sar_raw` firstly and do some post-process.


    Parameters
    ----------
    filepath : str
        UAVSAR raw data file path string, for UAVSAR --> ``*.raw``
    sl : int, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : int, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : bool, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    S : 2d-array
       SAR raw signal data matrix.

    """

def read_uavsar_mlc(filepath, dshape=None, dtype='complex'):
    r"""read UAVSAR MLC data

    read UAVSAR SAR MLC data.


    Parameters
    ----------
    filepath : str
        UAVSAR MLC data file path string, for UAVSAR --> ``*.mlc``
    dshape : tuple, optional
        MLC data shape (:math:`N_a\times N_r`), where, :math:`N_a, N_r` equal
        to ``mlc_mag.set_rows``, ``mlc_mag.set_cols`` which can be obtained
        from the ``.ann`` file (the default is 1, which means the first line)
    dshape : str
        MLC data type: ``'complex'`` for complex-valued floating point data,
        ``'real'`` for real-valued floating point data.

    Returns
    -------
    S : 2d-array
       SAR MLC data matrix.

    """


