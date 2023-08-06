#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : range_doppler_algorithm.py
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
import time
import torch as th
import torchbox as tb
import torchsar as ts


class LRDAnet(th.nn.Module):

    def __init__(self, Na, Nr, Fsa, Fsr, Ta, Tp, Ka, Kr, fdc, Fc, R0, Vr, La):
        super(LRDAnet, self).__init__()
        self.Na = Na
        self.Nr = Nr
        self.Fsa = Fsa
        self.Fsr = Fsr
        self.Ta = Ta
        self.Tp = Tp
        self.Ka = Ka
        self.Kr = Kr
        self.fdc = fdc
        self.Fc = Fc
        self.R0 = R0
        self.Vr = Vr
        self.La = La

        Noff, Wl = th.linspace(0, Nr, Nr), tb.C / Fc
        Rp = ts.min_slant_range(R0, Fsr, Noff)

        if Ka is None:
            Ka = ts.dre_geo(Wl, Vr, Rp)

        if Ta is None:
            FPa = ts.azimuth_footprint(Rp, Wl, La)
            Ta = th.mean(FPa).item() / Vr

        raise(ImportError('Not opened yet!'))


    def forward(self, X):
        # X --> Na-Nr-2

        raise(ImportError('Not opened yet!'))


    def focus(self, X, pa=None, pr=None):
        # X --> N-1-Na-Nr-2
        # pa --> N-Na
        # pr --> N-Nr

        if pa is None and pr is None:
            return X

        if pa is not None:
            X = tb.fft(X, nfft=None, axis=2, norm=False)
            pa = pa.reshape(pa.size(0), 1, int(pa.numel() / pa.size(0)), 1)
            epa = th.stack((th.cos(pa), th.sin(pa)), dim=-1)
            X = tb.ematmul(X, epa)
        if pr is not None:
            X = tb.fft(X, nfft=None, axis=3, norm=False)
            pr = pr.reshape(pr.size(0), 1, 1, int(pr.numel() / pr.size(0)))
            epr = th.stack((th.cos(pr), th.sin(pr)), dim=-1)
            X = tb.ematmul(X, epr)
        if pa is not None:
            X = tb.ifft(X, nfft=None, axis=2, norm=False)
        if pr is not None:
            X = tb.ifft(X, nfft=None, axis=3, norm=False)

        return X


if __name__ == "__main__":

    epochs = 10
    learning_rate = 1e-3
    device = th.device('cuda:1' if th.cuda.is_available() else 'cpu')
    # device = th.device('cpu')
    print(device)

    Na, Nr = 512, 512
    net = LRDAnet(Na, Nr)
    net.to(device=device)

    X = th.randn((4, Na, Nr, 2), requires_grad=False)
    X = X.to(device)

    loss_func = tb.Entropy(mode='shannon', cdim=-1, reduction='mean')
    optimizer = th.optim.Adam(net.parameters(), lr=learning_rate)

    for k in range(epochs):
        tstart = time.time()

        pa, Y = net.forward(X)
        loss = loss_func(Y)

        optimizer.zero_grad()

        # Backward pass: compute gradient of the loss with respect to model parameters
        loss.backward()

        # Calling the step function on an Optimizer makes an update to its parameters
        optimizer.step()

        tend = time.time()

        print("---loss: %s, time: %ss" % (loss.item(), tend - tstart))
