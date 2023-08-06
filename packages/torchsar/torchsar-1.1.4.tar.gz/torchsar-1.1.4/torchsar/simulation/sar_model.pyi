def sarmodel(pdict, mod='2D1', gdshape=None, device='cpu', islog=False):
    r"""model sar imaging process.

    SAR imaging model

    Parameters
    ----------
    pdict: dict
        SAR platform parameters
    mod: str, optional
        mod type(default: '2D1')

            if mod is '2D1':
                the model will be in vector mode:
                    s = A      g
                    MNx1      MNxHW  HWx1(M: Na, N: Nr, MN << HW)
            if mod is '2D2':
                the model will be in mat mode:
                    S = Aa     G     Be
                    MxN       MxH    HxW   WxN(M: Na, N: Nr, M << H, N << W)
            if mod is '1Da':
                    S = A      G
                    MxW       MxH    HxW(M: Na, N: Nr, M << H)
            if mod is '1Dr':
                    S'    =   A      G'
                    NxH       NxW    WxH(M: Na, N: Nr, N << W)

    gdshape: tuple, optional
        discrete scene size of G (default: None, sarplat.acquisition['SceneArea'], dx=dy=1)
    device: str
        device, default is 'cpu'
    islog : bool
        show log info (default: True)

    Returns
    -------
    A : torch tensor
        Imaging mapping matrix.
    """

def __computeRmn(ta, tr, H, V, Xc, Yc, SA, gH, gW):
    r"""compute range at g(i, j)

    compute range at g(i, j)

    Arguments
    ------------
    m int
        current y coordinate of H
    n int
        current x coordinate of W
    ta {time in azimuth}
        azimuth time
    tr numpy array
        range time
    H int
        height of SAR platform
    V float
        velocity of SAR platform
    Yc float
        center coordinate in Y axis
    Xc float
        center coordinate in X axis
    SA list
        scene area: [xmin, xmax, ymin, ymax]
    H int
        height of scene(Y)
    W int
        width of scene(X)
    """

def load_sarmodel(datafile, mod='AinvA'):
    r"""load sarmodel file

    load sarmodel file (``.pkl``)

    Parameters
    ----------
    datafile : str
        Model data file path.
    mod : str, optional
        Specify load which variable, ``A``, ``invA``, ``AinvA``
        (the default is 'AinvA', which :math:`\bm A`, :math:`{\bm A}^{-1}` )

    Returns
    -------
    A : numpy array
        Imaging mapping matrix.
    invA : numpy array
        Inverse of imaging mapping matrix.

    Raises
    ------
    ValueError
        wrong mod
    """

def save_sarmodel(A, invA=None, AH=None, datafile='./model.pkl'):
    r"""save model mapping matrix

    save model mapping matrix to a file.


    Parameters
    ----------
    A : numpy array
        Imaging mapping matrix
    invA : numpy array, optional
        Moore - Penorse inverse of A(default: {None})
    AH : numpy array, optional
        The Hermite :math:`{\bm A}^H` of the Imaging mapping matrix :math:`\bm A`
        (the default is None, which does not store)
    datafile : str, optional
        save file path(default: {'./model.pkl'})
    """


