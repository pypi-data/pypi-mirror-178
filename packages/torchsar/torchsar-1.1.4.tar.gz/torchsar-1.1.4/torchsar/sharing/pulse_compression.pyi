def mfpc_throwaway(X, No, Nh, axis=0, mffdmod='way1', ftshift=False):
    r"""Throwaway invalid pulse compressed data

    Throwaway invalid pulse compressed data

    Parameters
    ----------
    X : Tensor
        Data after pulse compression.
    No : int
        Output size.
    Nh : int
        Filter size.
    axis : int, optional
        Throwaway dimension. (the default is 0)
    mffdmod : str, optional
        Frequency filter mode. (the default is 'way1')
    ftshift : bool, optional
        Whether to shift frequency (the default is False)
    """


