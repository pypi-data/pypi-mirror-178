def _getdtype_component(fmtrcd, fmtuser):
    ...

def get_alos_palsar_plat_position(D):
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

def get_alos_palsar_attitude(D):
    """get attitude data

    return a numpy array
        1st: Pitch Roll Yaw PitchRate RollRate YawRate
        2st: Pitch Roll Yaw PitchRate RollRate YawRate
           :
        nst: Pitch Roll Yaw PitchRate RollRate YawRate

    Parameters
    ----------
    D : dict
        LeaderFileImportantImagingParametersRecordALOS dict
    """

def read_alos_palsar_ldr_iip(ledfile, verbose=False):
    r"""Read important imaging parameters from leader file

    Read important imaging parameters from leader file.

    For example, ``LED-ALPSRP050500980-H1.0__A``

    Parameters
    ----------
    ledfile : str
        Leader file path string.
    """

def read_alos_palsar_raw(rawfile, ledfile, sl=1, el=-1, rmbp=False):
    r"""read ALOS PALSAR raw data

    read ALOS PALSAR raw data pulse from line :attr:`sl` to line :attr:`el`. This function call
    function :func:`read_ceos_sar_raw` firstly and do some post-process.


    Parameters
    ----------
    rawfile : str
        ALOS PALSAR raw data file path string, ---> ``IMG*.0__A``, e.g. ``IMG-HH-ALPSRP050500980-H1.0__A``
    ledfile : str
        ALOS PALSAR leader file path string, ---> ``LED*.0__A``, e.g. ``LED-ALPSRP050500980-H1.0__A``
    sl : int, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : int, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : bool, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    Sr : 2d-array
       SAR raw signal data matrix.

    Pd : dict
       Parameter dictionary.

    """

def read_alos_palsar_slc(filepath, sl=1, el=-1, rmbp=False):
    r"""read ALOS PALSAR SLC data

    read ALOS PALSAR SLC data pulse from line :attr:`sl` to line :attr:`el`. This function call
    function :func:`read_ceos_sar_slc` firstly.


    Parameters
    ----------
    filepath : str
        ALOS PALSAR raw data file path string, for ALOSPALSAR --> ``IMG*.1__A``
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


