#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : autofocus.py
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
import torch as th
import torchbox as tb
import torchsar as ts


def _focusing(X, phi, Na, Nr, ftshift=False, isfft=True):
    if th.is_complex(X):
        # N, Na, Nr = X.size(0), X.size(-2), X.size(-1)
        X = th.view_as_real(X)
        crepflag = True
    elif X.size(-1) == 2:
        # N, Na, Nr = X.size(0), X.size(-3), X.size(-2)
        crepflag = False
    else:
        raise TypeError('X is complex and should be in complex or real represent formation!')

    d = X.dim()
    sizea, sizer = [1] * d, [1] * d
    returns = []
    if Na is not None:
        pa = phi[0]
        sizea[0], sizea[-3], sizea[-1] = pa.size(0), pa.size(1), 2
        epa = th.stack((th.cos(pa), -th.sin(pa)), dim=-1)
        epa = epa.reshape(sizea)

        if isfft:
            X = tb.fft(X, cdim=-1, dim=-3, keepcdim=True, shift=ftshift)
        X = tb.ematmul(X, epa, cdim=-1)
        X = tb.ifft(X, cdim=-1, dim=-3, keepcdim=True, shift=ftshift)
        returns.append(pa.data)

    if Nr is not None:
        if Na is None:
            pr = phi[0]
        else:
            pr = phi[1]
        sizer[0], sizer[-2], sizer[-1] = pr.size(0), pr.size(1), 2
        epr = th.stack((th.cos(pr), -th.sin(pr)), dim=-1)
        epr = epr.reshape(sizer)

        if isfft:
            X = tb.fft(X, cdim=-1, dim=-2, keepcdim=True, shift=ftshift)
        X = tb.ematmul(X, epr, cdim=-1)
        X = tb.ifft(X, cdim=-1, dim=-2, keepcdim=True, shift=ftshift)
        returns.append(pr.data)
    
    if crepflag:
        X = th.view_as_complex(X)

    return [X] + returns


class AutoFocusBarePhi(th.nn.Module):

    def __init__(self, Na, Nr, Nb=None, pa=None, pr=None, Ma=None, Mr=None, xa=None, xr=None, ftshift=False, trainable=True):
        super(AutoFocusBarePhi, self).__init__()

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
        self.ftshift = ftshift

        self.barephi = ts.BarePhi(Na, Nr, Nb, pa=pa, pr=pr, Ma=Ma, Mr=Mr, xa=xa, xr=xr, shift=ftshift, trainable=trainable)

    def forward(self, X, isfft=True):

        phi = self.barephi()

        returns = _focusing(X, phi, self.Na, self.Nr, ftshift=self.ftshift, isfft=isfft)

        return returns

    def get_param(self):
        param = []
        if self.barephi.pa is not None:
            param.append(self.barephi.pa)
        if self.barephi.pr is not None:
            param.append(self.barephi.pr)
        return param

    def param_init(self, pa=None, pr=None):
        self.barephi.param_init(pa, pr)


class AutoFocusPolyPhi(th.nn.Module):

    def __init__(self, Na, Nr, Nb=None, ca=None, cr=None, Ma=2, Mr=2, xa=None, xr=None, ftshift=False, trainable=True):
        super(AutoFocusPolyPhi, self).__init__()

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
        self.ftshift = ftshift

        self.polyphi = ts.PolyPhi(Na, Nr, Nb, ca=ca, cr=cr, Ma=Ma, Mr=Mr, xa=xa, xr=xr, shift=ftshift, trainable=trainable)

    def forward(self, X, isfft=True):

        phi = self.polyphi()

        returns = _focusing(X, phi, self.Na, self.Nr, ftshift=self.ftshift, isfft=isfft)

        return returns

    def get_param(self):
        param = []
        if self.polyphi.ca is not None:
            param.append(self.polyphi.ca)
        if self.polyphi.cr is not None:
            param.append(self.polyphi.cr)
        return param

    def param_init(self, ca=None, cr=None):
        self.polyphi.param_init(ca, cr)


class AutoFocusDctPhi(th.nn.Module):

    def __init__(self, Na, Nr, Nb=None, ca=None, cr=None, Pa=4, Pr=4, ftshift=False, trainable=True):
        super(AutoFocusDctPhi, self).__init__()

        if Nb is None:
            Nb = 1

        self.Na = Na
        self.Nr = Nr
        self.Nb = Nb
        self.Pa = Pa
        self.Pr = Pr
        self.ftshift = ftshift

        self.dctphi = ts.DctPhi(Na, Nr, Nb, ca=ca, cr=cr, Pa=Pa, Pr=Pr, shift=ftshift, trainable=trainable)

    def forward(self, X, isfft=True):

        phi = self.dctphi()

        returns = _focusing(X, phi, self.Na, self.Nr, ftshift=self.ftshift, isfft=isfft)

        return returns

    def get_param(self):
        param = []
        if self.dctphi.ca is not None:
            param.append(self.dctphi.ca)
        if self.dctphi.cr is not None:
            param.append(self.dctphi.cr)
        return param

    def param_init(self, ca=None, cr=None):
        self.dctphi.param_init(ca, cr)


class AutoFocusSinPhi(th.nn.Module):

    def __init__(self, Na, Nr, Nb=None, aa=None, fa=None, ar=None, fr=None, ftshift=False, trainable=True):
        super(AutoFocusSinPhi, self).__init__()

        if Nb is None:
            Nb = 1

        self.Na = Na
        self.Nr = Nr
        self.Nb = Nb
        self.ftshift = ftshift

        self.sinphi = ts.SinPhi(Na, Nr, Nb, aa=aa, fa=fa, ar=ar, fr=fr, shift=ftshift, trainable=trainable)

    def forward(self, X, isfft=True):
        d = X.dim()

        phi = self.sinphi()

        returns = _focusing(X, phi, self.Na, self.Nr, ftshift=self.ftshift, isfft=isfft)

        return returns

    def get_param(self):
        param = []
        if self.sinphi.fa is not None:
            param.append(self.sinphi.aa)
            param.append(self.sinphi.fa)
        if self.sinphi.fr is not None:
            param.append(self.sinphi.ar)
            param.append(self.sinphi.fr)
        return param

    def param_init(self, aa=None, fa=None, ar=None, fr=None):
        self.sinphi.param_init(aa, fa, ar, fr)
