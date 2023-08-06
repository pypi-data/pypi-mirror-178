def slantr2groundr(R, H, Ar, Xc):
    """slant range to ground range

    Convert slant range :math:`R` to ground range :math:`X`.

    Parameters
    ----------
    R : 1d-tensor
        slant range array
    H : float
        sarplat height
    Ar : float
        squint angle (unit, rad) in line geometry

    Returns
    -------
    X : 1d-tensor
        ground range

    """

def slantt2groundr(tr, H, Ar):
    """slant time to ground range

    Convert slant range time :math:`t_r` to ground range :math:`X`.

    Parameters
    ----------
    tr : 1d-tensor
        range time array
    H : float
        sarplat height
    Ar : float
        squint angle (unit, rad) in line geometry

    Returns
    -------
    X : 1d-tensor
        ground range

    """

def groundr2slantr(X, H, Ar, Xc):
    """ground range to slant range

    Convert ground range :math:`R` to slant range :math:`X`.

    Parameters
    ----------
    X : 1d-tensor
        ground range array
    H : float
        sarplat height
    Ar : float
        squint angle (unit, rad) in line geometry

    Returns
    -------
    R : 1d-tensor
        slant range

    """

def groundr2slantt(X, H, Ar):
    """ground range to slant time

    Convert ground range :math:`X` to slant time :math:`t_r`.

    Parameters
    ----------
    X : 1d-tensor
        ground range
    H : float
        sarplat height
    Ar : float
        squint angle (unit, rad) in line geometry

    Returns
    -------
    tr : 1d-tensor
        range time array

    """

def min_slant_range(Rnear, Fsr, Noff):
    """minimum slant range from radar to target

    Compute the minimum slant range from radar to target.

    Parameters
    ----------
    Rnear : float
        The nearest range (start sampling) from radar to the target.
    Fsr : float
        Sampling rate in range direction
    Noff : 1d-tensor
        Offset from the start distance (start sampling) cell.

    Returns
    -------
    r : 1d-tensor
        Minimum slant range of each range cell.
    """

def min_slant_range_with_migration(Rnear, Fsr, Noff, Wl, Vr, fdc):

