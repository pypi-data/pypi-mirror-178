def azimuth_beamwidth(Wl, La):
    ...

def azimuth_footprint(R, Wl, La):
    ...

def compute_range_beamwidth2(Nr, Fsr, H, Aon):
    r"""computes beam angle in range direction


    Parameters
    ----------
    Nr : int
        Number of samples in range direction.
    Fsr : float
        Sampling rate in range direction.
    H : float
        Height of the platform.
    Aon : float
        The off-nadir angle (unit: rad).

    Returns
    -------
    float
        The beam angle (unit, rad) in range direction.

    """

def cr_footprint(Wl, H, La, Ad):
    r"""cross range (azimuth) foot print

    .. math::
       R_{CR} \approx \frac{\lambda}{L_a}\frac{H}{{\rm cos}\theta_d}

    Parameters
    ----------
    Wl : float
        wave length
    H : float
        height of SAR platform
    La : float
        length of antenna aperture (azimuth)
    Ad : float
        depression angle

    Returns
    -------
    float
        foot print size in azimuth
    """


