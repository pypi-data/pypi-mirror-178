def convert_ppec(cs, degs=None, mode='fftfreq->2fftfreq'):
    r"""convert polynominal phase error

    Convert polynominal phase error.

    Args:
        cs (Tensor): The polynominal coefficients.
        degs (None, optional): The degrees of polynominal.
        mode (str, optional): ``'fftfreq->2fftfreq'`` or ``'2fftfreq->fftfreq'`` (the default is 'fftfeq->2fftfreq')

    Returns:
        Tensor: Converted phase error tensor.

    Raises:
        ValueError: Not support mode.
    """

def ppeaxis(n, norm=True, shift=True, mode='fftfreq', dtype=th.float32, device='cpu'):
    r"""Return the sample axis

    Return the sample frequencies axis.

    Parameters
    ----------
    n : int
        Number of samples.
    norm : bool
        Normalize the frequencies.
    shift : bool
        Does shift the zero frequency to center.
    mode : str or None
        Frequency sampling mode. ``'fftfreq'`` or ``'freq'`` normalize the frequencies in (-1/2, 1/2).
        ``'2fftfreq'`` or ``'2freq'`` normalize the frequencies in (-1, 1). If ``None``, return ``None``.
    dtype : Tensor
        Data type, default is ``th.float32``.
    device : str
        device string, default is ``'cpu'``.

    Returns
    -------
    torch array
        Frequency array with size :math:`n×1`.
    """

def polype(c, x, deg=None):
    r"""compute phase error with polynominal model

    compute phase error with polynominal model

    Args:
        c (Tensor, optional): The polynominal coefficients matrix :math:`{\bf P} = [{\bf p}_1, {\bf p}_2, \cdots, {\bf p}_N ]^T ∈{\mathbb R}^{N × (M -1)}`,
            where, :math:`{\bf p}_n = [p_2, \cdots, p_M]^T`).
        x (Tensor or None, optional): Axis, such as a vector in range of (-1, 1). If :attr:`x` is None, return :attr:`c` directly.
        deg (tuple or None, optional): The degree of the coefficients, :math:`[p_{\rm min}, p_{\rm_max}]`, default is ``None``, which means ``[2, size(c, 1) + 1]``

    Returns:
        (Tensor): The phase error tensor.

    Raises:
        TypeError: :attr:`c` should not be None!
    """

def dctpe(c, x, deg=None):
    r"""compute phase error with DCT model

    compute phase error with DCT model

    .. math::
        \phi_{e}(h)=\sum_{p=0}^{P} a(p) \cdot d c t(p) \cdot \cos \left[\frac{\pi\left(2 h_{a}+1\right) p}{2 N}\right]

    where, :math:`a(p)=\left{\begin{array}{ll}1 / \sqrt{N} p=0 \ \sqrt{2 / N} p \neq 0\end{array},\right.` and
    :math:`\left{\begin{array}{l}p=0,1,2, \cdots \cdots \cdots, P \ h_{a}=[0,1,2, \cdots \cdots, N-1]\end{array}\right.`

    Args:
        c (Tensor, optional): The DCT coefficients matrix :math:`{\bf P} = [{\bf p}_1, {\bf p}_2, \cdots, {\bf p}_N ]^T ∈{\mathbb R}^{N × (M + 1)}`,
            where, :math:`{\bf p}_n = [p_0, \cdots, p_M]^T`).
        x (Tensor, optional): Axis, such as :math:`(0, Na)`.
        deg (tuple or None, optional): The degree of the coefficients, :math:`[p_{\rm min}, p_{\rm_max}]`, default is ``None``, which means ``[0, size(c, 1)]``

    Returns:
        (Tensor): The phase error tensor.

    Raises:
        TypeError: :attr:`c` should not be None!
    """

def rmlpe(phi, mode='poly', deg=4, ftshift=True):
    r"""remove linear phase error

    Remove linear phase error based on linear fitting, the linear phase error
    will cause image shift.

    Args:
        phi (Tensor): A :math:`N×N_x` phase error tensor with linear trend, where, :math:`N` is the batchsize, :math:`N_x` is the samples numbers in direction x.
        mode (str): model mode, default is polynominal
        deg (int): Polynomial degrees (default 4) to fit the error, once fitted, the term of deg=[0,1] will be removed. If :attr:`deg` is None or lower than 2, then we do not fit the error with polynominal and not remove the linear trend.
        ftshift (bool): Shift zero frequency to center when do fft/ifft/fftfreq? (the default is False)

    Returns:
        phi (tensor): Phase without linear trend.
    """

class PolyPhaseErrorGenerator(object):
    ...

    def __init__(self, carange=None, crrange=None, seed=None):
        """Polynominal phase error generator.

        Args:
            carange (None or tuple or list, optional): List of coefficients range of phase error in azimuth direction.
            crrange (None or tuple or list, optional): List of coefficients range of phase error in range direction.
            seed (None or int, optional): The random seed.
        """

    def mkpec(self, n, seed=None):
        """Make phase error

        Args:
            n (int): The number of phase errors.
            seed (None or int, optional): The random seed.

        Returns:
            TYPE: Description
        """


