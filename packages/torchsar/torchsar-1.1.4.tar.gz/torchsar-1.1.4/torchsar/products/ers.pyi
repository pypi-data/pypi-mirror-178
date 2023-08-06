def _getdtype_component(fmtrcd, fmtuser):
    ...

def get_ers_sar_plat_position(D):
    """get platform position data

    return a numpy array
        1st: X Y Z Vx Vy Vz
        2st: X Y Z Vx Vy Vz
           :
        nst: X Y Z Vx Vy Vz

    Parameters
    ----------
    D : dict
        LeaderFileImportantImagingParametersRecordALOS dict
    """

def read_ers_sar_ldr_iip(filepath, verbose=False):
    r"""Read important imaging parameters from leader file

    Read important imaging parameters from leader file.

    Parameters
    ----------
    filepath : str
        Leader file path string.
    """

def read_ers_sar_raw(rawfile, ledfile, sl=1, el=-1, rmbp=False):
    r"""read ERS SAR raw data

    read ERS1/2 SAR raw data pulse from line :attr:`sl` to line :attr:`el`.


    Parameters
    ----------
    rawfile : str
        ERS SAR raw data file path string, for ERS1/2 --> ``*.raw``
        e.g. ``E2_81988_STD_L0_F327.000.raw``
    ledfile : str
        ERS SAR leader file path string, ---> ``*.ldr``, e.g. ``E2_81988_STD_L0_F327.000.ldr``
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

    Pd : dict
       Parameter dictionary.

    """

def read_ers_sar_slc(filepath, sl=1, el=-1, rmbp=False):
    r"""read ERS SAR SLC data

    read ERS1/2 SAR SLC data pulse from line :attr:`sl` to line :attr:`el`.


    Parameters
    ----------
    filepath : str
        ERS SAR raw data file path string, for ERS1/2 --> ``*.raw``
    sl : int, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : int, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : bool, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    S : 2d-array
       SAR SLC data matrix.

    """


