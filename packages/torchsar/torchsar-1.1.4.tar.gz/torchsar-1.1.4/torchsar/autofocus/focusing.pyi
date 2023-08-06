def focus(x, pa=None, pr=None, isfft=True, ftshift=True):
    r"""Focus image with given phase error

    Focus image in azimuth by

    .. math::
        Y(k, n_r)=\sum_{n_a=0}^{N_a-1} X(n_a, n_r) \exp \left(-j \varphi_{n_a}\right) \exp \left(-j \frac{2 \pi}{N_a} k n_a\right)

    where, :math:`\varphi_{n_a}` is the estimated azimuth phase error of the :math:`n_a`-th azimuth line, :math:`y(k, n_r)` is
    the focused pixel.

    The focus method in range is the same as azimuth.

    Args:
        x (Tensor): Defocused image data :math:`{\mathbf X} \in{\mathbb C}^{N\times N_c\times N_a\times N_r}` or
            :math:`{\mathbf X} \in{\mathbb R}^{N\times N_a\times N_r\times 2}` or
            :math:`{\mathbf X} \in{\mathbb R}^{N\times N_c\times N_a\times N_r\times 2}`.
        pa (Tensor, optional): Focus parameters in azimuth, phase error in rad unit. (the default is None, not focus)
        pr (Tensor, optional): Focus parameters in range, phase error in rad unit. (the default is None, not focus)
        isfft (bool, optional): Is need do fft (the default is True)
        ftshift (bool, optional): Is shift zero frequency to center when do fft/ifft/fftfreq (the default is True)

    Returns:
        (Tensor): A tensor of focused images.

    Raises:
        TypeError: :attr:`x` is complex and should be in complex or real represent formation!
    """

def defocus(x, pa=None, pr=None, isfft=True, ftshift=True):
    r"""Defocus image with given phase error

    Defocus image in azimuth by

    .. math::
        Y(k, n_r)=\sum_{n_a=0}^{N_a-1} X(n_a, n_r) \exp \left(j \varphi_{n_a}\right) \exp \left(-j \frac{2 \pi}{N_a} k n_a\right)

    where, :math:`\varphi_{n_a}` is the estimated azimuth phase error of the :math:`n_a`-th azimuth line, :math:`y(k, n_r)` is
    the focused pixel.

    The defocus method in range is the same as azimuth.

    Args:
        x (Tensor): Focused image data :math:`{\mathbf X} \in{\mathbb C}^{N\times N_c\times N_a\times N_r}` or
            :math:`{\mathbf X} \in{\mathbb R}^{N\times N_a\times N_r\times 2}` or
            :math:`{\mathbf X} \in{\mathbb R}^{N\times N_c\times N_a\times N_r\times 2}`.
        pa (Tensor, optional): Defocus parameters in azimuth, phase error in rad unit. (the default is None, not focus)
        pr (Tensor, optional): Defocus parameters in range, phase error in rad unit. (the default is None, not focus)
        isfft (bool, optional): Is need do fft (the default is True)
        ftshift (bool, optional): Is shift zero frequency to center when do fft/ifft/fftfreq (the default is True)

    Returns:
        (Tensor): A tensor of defocused images.

    Raises:
        TypeError: :attr:`x` is complex and should be in complex or real represent formation!
    """


