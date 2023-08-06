def rectangle(SceneArea, x0, y0, h, w, a=None, dx=None, dy=None, verbose=False):
    r"""rectangle area

    generates rectangle area

    Parameters
    ----------
    SceneArea : list or tuple
        Scene Area, unit m, [xmin,xmax,ymin,ymax]
    x0 : float
        x center of rectangle, unit m (x: horizontal, y: vertical)
    y0 : float
        y center of rectangle, unit m (x: horizontal, y: vertical)
    h : float
        height of rectangle, unit m (the default is None, which generates randomly)
    w : float
        width of rectangle, unit m (the default is None, which generates randomly)
    a : float, optional
        amplitude (the default is None, which generates randomly)
    dx : float, optional
        resolution in range (default: {1 / (xmax-xmin)})
    dy : float, optional
        resolution in azimuth (default: {1 / (ymax-ymin)})
    verbose : bool, optional
        show more log info (the default is False, which means does not show)

    Returns
    -------
    rects : tensor
        rectangle area
    """

def disc(SceneArea, x0, y0, r, a=None, dx=None, dy=None, verbose=False):
    r"""disc area

    generates disc area


    Parameters
    ----------
    SceneArea : list or tuple
        Scene Area, [xmin,xmax,ymin,ymax]
    x0 : int
        x center of disc (x: horizontal, y: vertical)
    y0 : int
        y center of disc (x: horizontal, y: vertical)
    r : int
        radius of disc
    a : int, optional
        amplitude of disc (default: {None})
    dx : float, optional
        resolution in range (default: {1 / (xmax-xmin)})
    dy : float, optional
        resolution in azimuth (default: {1 / (ymax-ymin)})
    verbose : bool, optional
        show more log info (the default is False, which means does not show)

    Returns
    -------
    ccas : tensor
        disk area
    """


