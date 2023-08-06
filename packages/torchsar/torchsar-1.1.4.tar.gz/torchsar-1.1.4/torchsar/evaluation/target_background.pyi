def extract_targets(x, region=None, thresh=None, cdim=None, isshow=False):
    r"""Extracts the pixels of targetss

    Parameters
    ----------
    x : tensor or numpy array
        The input image, if it's complex-valued, it's amplitude is used.
    region : list or None, optional
        The region ([top-left, bottom-right]) that contains targets for computing TBR.
        If :obj:`None`, :attr:`region` equals to ``([0, 0], [H, W])``, where :math:`H,W` 
        are the height and width of the image.
    thresh : float or None, optional
        The threshold targets.
    cdim : int or None, optional
        Specifies the complex axis of :attr:`x`. ``None`` --> complex or real
    isshow : bool, optional
        Show pixels of the extracted targets?
    """

def tbr(x, targets, region=None, cdim=None, isshow=False):
    r"""Target-to-Background Ratio (TBR)

    .. math::
        \begin{align}
        {\rm TBR} = 20{\rm log}_{10}\left(\frac{{\rm max}_{i\in{\mathbb T}}(|{\bf X}_i|)}{{(1/N_{\mathbb B})}\Sigma_{j\in \mathbb B}|{\bf X}_j|)}\right)
        \label{equ:TBR}
        \end{align}

    Parameters
    ----------
    x : tensor
        The input image, if it's complex-valued, it's amplitude is used.
    targets : list or tuple
        The targets pixels. ([row1, row2, ...], [col1, col2, ...])
    region : list, tuple or None, optional
        The region ([top-left, bottom-right]) that contains targets for computing TBR.
        If :obj:`None`, :attr:`region` equals to ``([0, 0], [H, W])``, where :math:`H,W` 
        are the height and width of the image.
    cdim : int or None, optional
        Specifies the complex axis of :attr:`x`. ``None`` --> complex or real
    isshow : bool, optional
        Show target mask? (default: False)
    """

def tbr2(X, tgrs, subrs=None, isshow=False):
    r"""Target-to-Background Ratio (TBR)

    .. math::
        \begin{align}
        {\rm TBR} = 20{\rm log}_{10}\left(\frac{{\rm max}_{i\in{\mathbb T}}(|{\bf X}_i|)}{{(1/N_{\mathbb B})}\Sigma_{j\in \mathbb B}|{\bf X}_j|)}\right)
        \label{equ:TBR}
        \end{align}

    Parameters
    ----------
    X : tensor
        The input image, if it's complex-valued, it's amplitude is used.
    tgrs : list, optional
        target regions:[[TG1], [TG2], ..., [TGn]], [TGk] = [lefttop, rightbottom]]
    subrs : list, optional
        sub regions:[[SUB1], [SUB2], ..., [SUBn]], [SUBk] = [lefttop, rightbottom]]
    isshow : bool, optional
        show target mask given by :attr:`tgrs` (default: False)

    Returns
    -------
    TBR : float
        Target-to-Background Ratio (TBR)

    Raises
    ------
    TypeError
        tgrs mast be given
    """


