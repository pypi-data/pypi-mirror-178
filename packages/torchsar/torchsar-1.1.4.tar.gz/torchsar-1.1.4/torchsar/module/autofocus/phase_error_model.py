#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : phase_error_model.py
# @author    : Zhi Liu
# @email     : zhiliu.mind@gmail.com
# @homepage  : http://iridescent.ink
# @date      : Sun Nov 27 2022
# @version   : 2.0
# @license   : The Apache License 2.0
# @note      : 
# 
# The Apache 2.0 License
# Copyright (C) 2013- Zhi Liu
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
#

from __future__ import print_function
import math
import torch as th
import torchbox as tb
import torchsar as ts
from torch.nn.parameter import Parameter


class BarePhi(th.nn.Module):

    def __init__(self, Na, Nr, Nb=None, pa=None, pr=None, Ma=None, Mr=None, xa=None, xr=None, shift=False, trainable=True):
        super(BarePhi, self).__init__()

        if Nb is None:
            Nb = 1

        self.Na = Na
        self.Nr = Nr
        self.Nb = Nb
        self.Ma = Ma  # for remove linear trend
        self.Mr = Mr  # for remove linear trend
        self.shift = shift

        raise(ImportError('Not opened yet!'))


    def forward(self):
        returns = []
        raise(ImportError('Not opened yet!'))


    def get_param(self):
        param = []
        if self.Na is not None:
            param.append(self.pa)
        if self.Nr is not None:
            param.append(self.pr)
        return param

    def param_init(self, pa=None, pr=None):
        if self.pa is not None:
            if pa is None:
                pa = th.zeros(self.Nb, self.Na, dtype=self.pa.dtype, device=self.pa.device)
            self.pa.data = pa
        if self.pr is not None:
            if pr is None:
                pr = th.zeros(self.Nb, self.Nr, dtype=self.pr.dtype, device=self.pr.device)
            self.pr.data = pr


class PolyPhi(th.nn.Module):

    def __init__(self, Na, Nr, Nb=None, ca=None, cr=None, Ma=2, Mr=2, xa=None, xr=None, shift=False, trainable=True):
        super(PolyPhi, self).__init__()

        if type(Ma) is int:
            Ma = (2, Ma)
        if type(Mr) is int:
            Mr = (2, Mr)
        if Nb is None:
            Nb = 1

        self.Na = Na
        self.Nr = Nr
        self.Nb = Nb
        self.Ma = Ma
        self.Mr = Mr
        self.shift = shift

        raise(ImportError('Not opened yet!'))


    def forward(self):
        returns = []
        raise(ImportError('Not opened yet!'))


    def get_param(self):
        param = []
        if self.Na is not None:
            param.append(self.ca)
        if self.Nr is not None:
            param.append(self.cr)
        return param

    def param_init(self, ca=None, cr=None):
        if self.ca is not None:
            if ca is None:
                ca = th.zeros(self.Nb, self.Ma[1] - self.Ma[0] + 1, dtype=self.ca.dtype, device=self.ca.device)
            self.ca.data = ca
        if self.cr is not None:
            if cr is None:
                cr = th.zeros(self.Nb, self.Mr[1] - self.Mr[0] + 1, dtype=self.cr.dtype, device=self.cr.device)
            self.cr.data = cr


class DctPhi(th.nn.Module):

    def __init__(self, Na, Nr, Nb=None, ca=None, cr=None, Pa=4, Pr=4, shift=False, trainable=True):
        super(DctPhi, self).__init__()
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

        if Nb is None:
            Nb = 1

        self.Na = Na
        self.Nr = Nr
        self.Nb = Nb
        self.Pa = Pa
        self.Pr = Pr
        self.shift = shift

        if Na is not None:
            if ca is None:
                ca = th.zeros(Nb, Pa)
            self.ca = Parameter(ca, requires_grad=trainable)
            xa = th.linspace(0, Na, Na).reshape(1, Na)
            raise(ImportError('Not opened yet!'))


        if Nr is not None:
            if cr is None:
                cr = th.zeros(Nb, Pr)
            self.cr = Parameter(cr, requires_grad=trainable)
            xr = th.linspace(0, Nr, Nr).reshape(1, Nr)

            raise(ImportError('Not opened yet!'))


    def forward(self):
        returns = []
        raise(ImportError('Not opened yet!'))


    def get_param(self):
        param = []
        if self.Na is not None:
            param.append(self.ca)
        if self.Nr is not None:
            param.append(self.cr)
        return param

    def param_init(self, ca=None, cr=None):
        if self.ca is not None:
            if ca is None:
                ca = th.zeros(self.Nb, self.Pa, dtype=self.ca.dtype, device=self.ca.device)
            self.ca.data = ca
        if self.cr is not None:
            if cr is None:
                cr = th.zeros(self.Nb, self.Pr, dtype=self.cr.dtype, device=self.cr.device)
            self.cr.data = cr


class SinPhi(th.nn.Module):

    def __init__(self, Na, Nr, Nb=None, aa=None, fa=None, ar=None, fr=None, shift=False, trainable=True):
        super(SinPhi, self).__init__()
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

        if Nb is None:
            Nb = 1

        self.Na = Na
        self.Nr = Nr
        self.Nb = Nb
        self.shift = shift

        raise(ImportError('Not opened yet!'))


    def forward(self):
        returns = []
        raise(ImportError('Not opened yet!'))


    def get_param(self):
        param = []
        if self.Na is not None:
            param.append(self.aa)
            param.append(self.fa)
        if self.Nr is not None:
            param.append(self.ar)
            param.append(self.fr)
        return param

    def param_init(self, fa=None, aa=None, fr=None, ar=None):
        if self.aa is not None:
            if aa is None:
                aa = th.ones(self.Nb, 1, dtype=self.aa.dtype, device=self.aa.device)
            self.aa.data = aa
        if self.fa is not None:
            if fa is None:
                fa = th.zeros(self.Nb, 1, dtype=self.fa.dtype, device=self.fa.device)
            self.fa.data = fa

        if self.ar is not None:
            if ar is None:
                ar = th.ones(self.Nb, 1, dtype=self.ar.dtype, device=self.ar.device)
            self.ar.data = ar
        if self.fr is not None:
            if fr is None:
                fr = th.zeros(self.Nb, 1, dtype=self.fr.dtype, device=self.fr.device)
            self.fr.data = fr
