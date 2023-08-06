#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : fast_fourier_domain_optimization.py
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


def _compensation(X, phi, Na, Nr, ftshift=False, isfft=True):
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
        X = tb.ematmul(X, epa)
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
        X = tb.ematmul(X, epr)
        returns.append(pr.data)
    return [X] + returns


class AutoFocusFFO(th.nn.Module):

    def __init__(self, Na, Nr, Nb=None, ftshift=False, trainable=True):
        super(AutoFocusFFO, self).__init__()

        if Nb is None:
            Nb = 1

        self.Na = Na
        self.Nr = Nr
        self.Nb = Nb
        self.ftshift = ftshift

        self.barephi = ts.BarePhi(Na, Nr, Nb, pa=None, pr=None, Ma=7, Mr=7, shift=ftshift, trainable=trainable)

    def forward(self, X, isfft=True):

        phi = self.barephi()
        returns = _compensation(X, phi, self.Na, self.Nr, ftshift=self.ftshift, isfft=True)

        return returns

    def imaging(self, Xc):
        if self.Na is not None:
            Xc = tb.ifft(Xc, axis=-3, shift=self.ftshift)
        if self.Nr is not None:
            Xc = tb.ifft(Xc, axis=-2, shift=self.ftshift)
        return Xc

    def get_param(self):
        param = []
        if self.barephi.pa is not None:
            param.append(self.barephi.pa)
        if self.barephi.pr is not None:
            param.append(self.barephi.pr)
        return param

    def param_init(self, pa=None, pr=None):
        self.barephi.param_init(pa, pr)

