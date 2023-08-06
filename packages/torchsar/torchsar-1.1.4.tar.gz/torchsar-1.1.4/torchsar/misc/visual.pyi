def saraxis(pdict, axismod=None):
    r"""generate SAR image axes ticks and strings

    Parameters
    ----------
    pdict : dict
        SAR parameter dictionary.
    axismod : str, optional
        axis mode, supported are ``'Image'`` ``'SceneAbsoluteSlantRange'``, ``'SceneRelativeSlantRange'``,
        ``'SceneAbsoluteGroundRange'``, ``'SceneRelativeGroundRange'``, ``'BeamAreaSceneArea'``
         by default None (``'Image'``)

    Returns
    -------
    list and str
        extent, xlabel string, ylabel string, title string.
    """    

def tgshow(targets, scene, shape, extent=None, cmap=None, isflip=[False, False], labelstr=None, outfile=None, isshow=True):
    r"""show targets

    Show targets in an image.

    Arguments
    --------------
    targets : Tensor
        A tensor contains information of targets.
    scene : tuple or list
        Area of scene [xmin, xmax, ymin, ymax].
    shape : tuple or list
        The shape of the scene.

    Keyword Arguments
    --------------
    outfile : str
        The filename for writting figure (default: None, do not save).
    isshow : bool
        Whether to plot figure (default: True).

    Returns
    --------------
        Tensor -- The final image tensor for show.

    Raises
    --------------
        ValueError -- :attr:`targets` should not be None.
    """

def apshow(Srx, Title=None, cmap=None, extent=None, keepAspectRatio=True, outfile=None, isshow=True):
    r"""Show amplitude and phase.

    Show amplitude and phase.

    Parameters
    ----------
    Srx : Tensor
        Complex-valued tensor.
    Title : str, optional
        The figure title (the default is None, which means
        no title).
    cmap : str, optional
        The colormap (the default is None)
    extent : tuple or list, optional
        [description] (the default is None)
    keepAspectRatio : bool, optional
        [description] (the default is True)
    outfile : str, optional
        The filename for outputing (the default is None, which means not save)
    isshow : bool, optional
        Whether to show the figure (the default is True).
    """

def show_response(Srx, extent=None, title="Figure", keepAspectRatio=True, outfile=None, isshow=True):
    r"""show SAR response

    [description]

    Arguments
    ------------------
    Srx : Tensor
        [description]

    Keyword Arguments
    ------------------
    extent : tuple, list or None
        [description] (default: None)
    title : str
        [description] (default: "Figure")
    keepAspectRatio : bool
        [description] (default: True)
    outfile : str
        [description] (default: None)
    isshow : bool
        [description] (default: True)
    """

def showReImAmplitudePhase(Srx, extent=None, title=None, keepAspectRatio=True):
    r"""[summary]

    [description]

    Parameters
    ----------
    Srx : {[type]}
        [description]
    extent : {[type]}, optional
        [description] (the default is None, which [default_description])
    title : str, optional
        [description] (the default is None, which [default_description])
    keepAspectRatio : bool, optional
        [description] (the default is True, which [default_description])
    """

def show_image(img, Title=None, cmap=None, keepAspectRatio=True, outfile=None, isshow=True):
    ...

def sarshow(Xs, pdict, axismod=None, nrows=None, ncols=None, xlabels=None, ylabels=None, titles=None, figsize=None, outfile=None, **kwargs):
    """_summary_

    Parameters
    ----------
    Xs : tensor, array, list or tuple
        list/tuple of image arrays/tensors, if the type is not list or tuple, wrap it.
    pdict : dict
        SAR parameter dict
    axismod : _type_, optional
        _description_, by default None
    nrows : int, optional
        show in :attr:`nrows` rows, by default None (auto computed).
    ncols : int, optional
        show in :attr:`ncols` columns, by default None (auto computed).
    xlabels : str, optional
        labels of x-axis
    ylabels : str, optional
        labels of y-axis
    titles : str, optional
        titles
    figsize : tuple, optional
        figure size, by default None
    outfile : str, optional
        save image to file, by default None (do not save).
    kwargs : 
        see :func:`matplotlib.pyplot.imshow`
    """

def show_sarimage(SI, pdict, axismod=None, title=None, cmap=None, isimgadj=False, aspect=None, outfile=None, newfig=True, figsize=None):
    r"""[summary]

    [description]

    Arguments:
        SI {[type]} -- [description]
        pdict {[type]} -- [description]

    Keyword Arguments:
        axismod {[type]} -- [description] (default: {None})
        title {[type]} -- [description] (default: {None})
        cmap {[type]} -- [description] (default: {None})
        isimgadj bool -- [description] (default: {False})
        aspect {[type]} -- [description] (default: {None})
        outfile {[type]} -- [description] (default: {None})
        newfig bool -- [description] (default: {True})
        figsize {[type]} -- [description] (default: {None})
    """

def show_sarimage3d(SI, pdict, axismod=None, title=None, cmap=None, isimgadj=False, aspect=None, outfile=None, figsize=None):
    r"""[summary]

    [description]

    Arguments:
        SI {[type]} -- [description]
        sarplat {[type]} -- [description]

    Keyword Arguments:
        axismod {[type]} -- [description] (default: {None})
        title {[type]} -- [description] (default: {None})
        cmap {[type]} -- [description] (default: {None})
        isimgadj bool -- [description] (default: {False})
        aspect {[type]} -- [description] (default: {None})
        outfile {[type]} -- [description] (default: {None})
        figsize {[type]} -- [description] (default: {None})
    """

def imshow(Xs, nrows=None, ncols=None, xlabels=None, ylabels=None, titles=None, figsize=None, outfile=None, **kwargs):
    r"""show images

    This function create an figure and show images in :math:`a` rows and :math:`b` columns.

    Parameters
    ----------
    Xs : tensor, array, list or tuple
        list/tuple of image arrays/tensors, if the type is not list or tuple, wrap it.
    nrows : int, optional
        show in :attr:`nrows` rows, by default None (auto computed).
    ncols : int, optional
        show in :attr:`ncols` columns, by default None (auto computed).
    xlabels : str, optional
        labels of x-axis
    ylabels : str, optional
        labels of y-axis
    titles : str, optional
        titles
    figsize : tuple, optional
        figure size, by default None
    outfile : str, optional
        save image to file, by default None (do not save).
    kwargs : 
        see :func:`matplotlib.pyplot.imshow`

    Returns
    -------
    plt
        plot handle
    """


