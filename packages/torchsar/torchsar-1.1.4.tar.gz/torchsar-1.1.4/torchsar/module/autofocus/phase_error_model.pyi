class BarePhi(th.nn.Module):
    ...

    def __init__(self, Na, Nr, Nb=None, pa=None, pr=None, Ma=None, Mr=None, xa=None, xr=None, shift=False, trainable=True):
        ...

    def forward(self):
        ...

    def get_param(self):
        ...

    def param_init(self, pa=None, pr=None):
        ...

class PolyPhi(th.nn.Module):
    ...

    def __init__(self, Na, Nr, Nb=None, ca=None, cr=None, Ma=2, Mr=2, xa=None, xr=None, shift=False, trainable=True):
        ...

    def forward(self):
        ...

    def get_param(self):
        ...

    def param_init(self, ca=None, cr=None):
        ...

class DctPhi(th.nn.Module):
    ...

    def __init__(self, Na, Nr, Nb=None, ca=None, cr=None, Pa=4, Pr=4, shift=False, trainable=True):
        r"""

        .. math::
            \begin{array}{l}
            \phi_{e}(h)=\sum_{p=0}^{P} a(p) \cdot d c t(p) \cdot \cos \left[\frac{\pi\left(2
             h_{a}+1\right) p}{2 N}\right] \\
            a(p)=\left\{\begin{array}{l}
            1 / \sqrt{N} \quad p=0 \\
            \sqrt{2 / N} \quad p \neq 0
            \end{array},\right. \text { and }\left\{\begin{array}{l}
            p=0,1,2, \cdots \cdots \cdots, P \\
            h_{a}=[0,1,2, \cdots \cdots, N-1]
            \end{array}\right.
            \end{array}


        see Azouz, Ahmed Abd Elhalek, and Zhenfang Li. "Improved phase gradient autofocus algorithm based on segments of variable lengths and minimum-entropy phase correction." IET Radar, Sonar & Navigation 9.4 (2015): 467-479.


        Parameters
        ----------
        Na : int
            the number of samples in azimuth.
        Nr : int
            the number of samples in range.
        Nb : int, optional
            batch size (the default is None, which means 1)
        ca : tensor, optional
            DCT coefficients (the default is None, initialize with zeros)
        cr : tensor, optional
            DCT coefficients (the default is None, initialize with zeros)
        Pa : int, optional
            The number of DCT coefficients (the default is 2)
        Pr : int, optional
            The number of DCT coefficients (the default is 2)
        shift : bool, optional
            shift the frequency (the default is False, which means don't shift)
        trainable : bool, optional
            enable train (the default is True)
        """

    def forward(self):
        ...

    def get_param(self):
        ...

    def param_init(self, ca=None, cr=None):
        ...

class SinPhi(th.nn.Module):
    ...

    def __init__(self, Na, Nr, Nb=None, aa=None, fa=None, ar=None, fr=None, shift=False, trainable=True):
        r"""

        The sinusoidal phase error can be expressed as

        .. math::
            \Phi_{e}=\phi_{0} \sin \left(2 \pi f_{e} t\right)

        The Bessel approximation to a sinusoidal phase error is

        .. math::
            e^{j \phi_{0} \sin \left(2 \pi f_{e} t\right)}=\sum_{n=-\infty}^{\infty} J_{n}\left(\phi_{0}\right) e^{j 2 \pi n f_{e} t}

        For small :math:`\phi_{0}`, :math:`J_0 \simeq 1`, :math:`J_{1}\left(\phi_{0}\right)=-J_{-1}\left(\phi_{0}\right) \simeq \phi_{0} / 2`, it can be rewritten as

        .. math::
            e^{j \phi_{0} \sin \left(2 \pi f_{e} t\right)} & \simeq J_{0}\left(\phi_{0}\right)+
            J_{1}\left(\phi_{0}\right) e^{j 2 \pi f_{e} t}+J_{-1}\left(\phi_{0}\right) e^{-j 2 \
            pi f_{e} t} \\
            & \simeq 1+\frac{\phi_{0}}{2}\left(e^{j 2 \pi f_{e} t}-e^{-j 2 \pi f_{e} t}\right)


        [1] Satyaprasad, Shruthi B., et al. "Autofocusing SAR images using multistage wiener filter."
        2016 IEEE International Conference on Recent Trends in Electronics, Information & Communication
        Technology (RTEICT). IEEE, 2016.

        [2] Kim, Jin-Woo, et al. "Fast Fourier-Domain Optimization Using Hybrid $L_1 / L_{p}$-Norm for
        Autofocus in Airborne SAR Imaging." IEEE Transactions on Geoscience and Remote Sensing 57.10 (2019): 7934-7954.


        Parameters
        ----------
        Na : int
            the number of samples in azimuth.
        Nr : int
            the number of samples in range.
        Nb : int, optional
            batch size (the default is None, which means 1)
        aa : float, optional
            amplitude (the default is None, initialize with zeros)
        fa : float, optional
            frequency (the default is None, initialize with zeros)
        ar : float, optional
            amplitude (the default is None, initialize with zeros)
        fr : float, optional
            frequency (the default is None, initialize with zeros)
        shift : bool, optional
            shift the frequency (the default is False, which means don't shift)
        trainable : bool, optional
            enable train (the default is True)
        """

    def forward(self):
        ...

    def get_param(self):
        ...

    def param_init(self, fa=None, aa=None, fr=None, ar=None):

