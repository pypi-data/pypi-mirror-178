def sls_fd(x, axis=0, wtype=None, dtype=None):
    """Sidelobe suppression in frequency domain

    Sidelobe suppression in frequency domain


    Parameters
    ----------
    x : tensor
        The input.
    axis : int, optional
        The axis for sidelobe-suppression.
    wtype : str or None, optional
        The type of window, default is None. see :func:`window`.
    dtype : torch's dtype or None, optional
        The data type. If None, use default dtype of torch.

    Returns
    -------
    tensor
        The suppressed.
    """


