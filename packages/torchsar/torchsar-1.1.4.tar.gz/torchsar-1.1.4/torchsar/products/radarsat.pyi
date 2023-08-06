def _getdtype_component(fmtrcd, fmtuser):
    ...

def read_radarsat_sar_raw(filepath, sl=1, el=-1, rmbp=False):
    r"""read RADARSAT SAR raw data

    read RADARSAT raw data pulse from line :attr:`sl` to line :attr:`el`. This function call
    function :func:`read_ceos_sar_raw` firstly and do some post-process.


    Parameters
    ----------
    filepath : str
        RADARSAT SAR raw data file path string with format ``.001``, such as ``DAT_01.001``.
    sl : int, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : int, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : bool, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    S : 2d-array
        SAR raw data.

    """


