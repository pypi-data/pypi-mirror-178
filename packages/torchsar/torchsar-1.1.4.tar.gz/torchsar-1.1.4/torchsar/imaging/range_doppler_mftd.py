#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : range_doppler_mftd.py
# @author    : Zhi Liu
# @email     : zhiliu.mind@gmail.com
# @homepage  : http://iridescent.ink
# @date      : Sun Nov 27 2022
# @version   : 0.0
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

import torch as th
import numpy as np
import torchbox as tb
import torchsar as ts
import matplotlib.pyplot as plt


def rda_mftd(Sr, pdict, mfmod='fftconv', iqc=False, rcmc=False, dcem=None, win=None, afa=None, ftshift=False, isplot=False, islog=True):
    r"""Range Doppler Algorithm with time domain matched filters

    Args:
        Sr (Tensor): The SAR complex echo data representated in real format :math:`{\bm S}_r \in \mathbb{R}^{N_a×N_r×2}`.
        pdict (dict): Parameters used in RDA, which are show as follows:
            ``{'Vr', 'R0', 'La', 'Fc', 'Tp', 'Kr',  Fsr', 'Fsa'}``
        mfmod (str, optional): Matched filter mode, supported are:

            - ``'corr1'`` : 1d correlation filter and use standard correlation
            - ``'conv1'`` : 1d convolution filter and use standard convolution
            - ``'fftcorr1'`` : 1d correlation filter and use fft for operating correlation
            - ``'fftconv1'`` : 1d convolution filter and use fft for operating convolution (default)

        iqc (bool, optional): Whether do IQ data correction, see :func:`iq_correct`:

            - I/Q bias removal
            - I/Q gain imbalance correction
            - I/Q non-orthogonality correction

        rcmc (bool, int, optional): Range Migration Correction: integer-->kernel size, ``False``-->no rcmc (default: {8})
        dcem (str, optional): Dopplor centroid frequency estimation method (the default is None, does not estimate)
            - ``'abdce_wda'`` :
        win (list, tuple or None, optional): the window function for matched filter of azimuth and range. If None, no window is added (default), e.g. ['kaiser 12', 'hanning'], this will add kaiser window and hanning window in azimuth and range respectively.
        afa (str, optional): Dopplor rate estimation (autofocus) method (the default is None, does not do autofocusing)
        ftshift (bool, optional): Whether to shift zeros frequency to center when use fft, ifft, fftfreq (the default is ``False``)
        isplot (bool, optional): Plot part of processing result, such as DCE result (default: ``False``)
        islog (bool, optional): Display processing info (default: ``True``)

    Returns:
        Tensor: Focused complex image :math:`{\bm S}_i \in \mathbb{C}^{N_a×N_r}`.
    """

    device = Sr.device
    Na, Nr, _ = Sr.shape

    Vr = pdict['Vr']
    Rnear = pdict['Rnear']
    La = pdict['La']
    Fc = pdict['Fc']
    Tp = pdict['Tp']
    Kr = pdict['Kr']
    Fsr = pdict['Fsr']
    Fsa = pdict['Fsa']
    fdc = pdict['fdc']
    Nsar = pdict['Nsar']
    if type(fdc) is float or type(fdc) is int or type(fdc) is np.float64 or type(fdc) is np.float32:
        fdc = th.tensor([fdc] * Nr, device=device)

    Wl = tb.C / Fc
    Rfar = ts.min_slant_range(Rnear, Fsr, Nr)

    tnear = 2. * Rnear / tb.C
    tfar = tnear + Nr / Fsr
    # tfar = tnear + Nr / Fsr + Tp
    tr = th.linspace(tnear, tfar, Nr).reshape(1, Nr).to(device)

    # tr = pdict['tr'].to(device)
    # Rnear = pdict['Rnear']

    fa = tb.fftfreq(Na, Fsa, norm=False, shift=ftshift).to(device)

    if mfmod in ['fftconv1', 'FFTCONV1', 'fftconv', 'FFTCONV']:
        mffunc, mftdmod = tb.fftconv1, 'conv'
    if mfmod in ['fftcorr1', 'FFTCORR1', 'fftcorr', 'FFTCORR']:
        mffunc, mftdmod = tb.fftcorr1, 'corr'
    if mfmod in ['conv1', 'CONV1', 'conv', 'CONV']:
        mffunc, mftdmod = ts.conv1, 'conv'
    if mfmod in ['corr1', 'CORR1', 'corr', 'CORR']:
        mffunc, mftdmod = ts.corr1, 'corr'

    if iqc:
        Sr, Flag = ts.iq_correct(Sr)
        if islog:
            print(Flag)
    Sr = Sr[..., 0] + 1j * Sr[..., 1]
    # Sr = th.view_as_complex(Sr)

    raise(ImportError('Not opened yet!'))
