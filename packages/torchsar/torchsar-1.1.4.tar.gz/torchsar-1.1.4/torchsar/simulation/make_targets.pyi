def gpoints(SceneArea, npoints, amin=0., amax=1., seed=None):
    """Generates point targets

    Parameters
    ----------
    SceneArea : tuple or list
        The area of scene.
    npoints : int
        The number of points.
    amin : float, optional
        The minimum amplitude. (default is 0)
    amax : float, optional
        The maximum amplitude. (default is 1)
    seed : int or None, optional
        The seed for random generator.

    Returns
    -------
    tensor
        A tensor contains coordinate and amplitude information.
    """


