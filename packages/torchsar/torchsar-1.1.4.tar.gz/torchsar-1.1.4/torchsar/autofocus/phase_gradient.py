#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : phase_gradient.py
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

import numpy as np
import torch as th
import torchbox as tb
import torchsar as ts
from tqdm import tqdm
from torchbox.utils.const import *
import matplotlib.pyplot as plt


def spotlight_width(H, BWa, Lsar):
    return 2. * H * np.tan(BWa / 2.) - Lsar / (2. * H)


def phase_correction(x, phi, nsub=None, axis=-2, ftshift=True):

    if th.is_complex(x):
        # N, Na, Nr = x.size(0), x.size(-2), x.size(-1)
        cplxflag = True
    elif x.size(-1) == 2:
        # N, Na, Nr = x.size(0), x.size(-3), x.size(-2)
        x = th.view_as_complex(x)
        cplxflag = False
    else:
        raise TypeError('x is complex and should be in complex or real represent formation!')
    if axis == -2 or axis == 1:  # azimuth
        axis = -2
    if axis == -1 or axis == 2:  # range
        axis = -1

    if x.dim() == 2:
        x = x.unsqueeze(0)
    if phi.dim() == 1:
        phi = phi.unsqueeze(0)
    if phi.size(-1) != 1:
            phi = phi.unsqueeze(-1)
            phi = phi.unsqueeze(-1)

    N, Na, Nr = x.size()
    Nx = x.size(axis)
    pshape = [1, 1, 1]
    pshape[0] = N
    pshape[axis] = Nx
    phi = phi.reshape(pshape)

    if nsub is None:
        nsub = Nx

    # X = tb.fft(SI, axis=axis, shift=ftshift)
    # X = X * np.exp(-1j * phi)
    # SI = tb.ifft(X, axis=axis, shift=ftshift)
    xc = x.clone().detach()
    d = xc.dim()
    for n in range(0, Nx, nsub):
        idx = tb.sl(d, axis, range(n, n + nsub))
        xsub = x[idx]
        phisub = phi[idx]
        Xsub = tb.fft(xsub, axis=axis, shift=ftshift)
        xc[idx] = tb.ifft(Xsub * th.exp(-1j * phisub), axis=axis, shift=ftshift)
    if not cplxflag:
        xc = th.view_as_real(xc)
    return xc


def pgaf_sm_1iter(x, windb=None, est='ML', deg=4, axis=-2, isrmlpe=False, iscrct=False, isplot=False):
    r"""perform phase gradient autofocus 1 iter

    Perform phase gradient autofocus 1 iter as described in [1].

    revised for stripmap SAR

    - [1] C.V. Jakowatz, D.E. Wahl, P.H. Eichel, D.C. Ghiglia, P.A. Thompson,
    {\em Spotlight-mode Synthetic Aperture Radar: A Signal Processing
    Approach.} Springer, 1996.

    - [2] D.E. Wahl, P.H. Eichel, D.C. Ghiglia, C.V. Jakowatz, "Phase
    gradient autofocus-a robust tool for high resolution SAR phase
    correction," IEEE Trans. Aero. & Elec. Sys., vol. 30, no. 3, 1994.

    Args:
        x (Tensor): Complex SAR image :math:`{\bm X}\in {\mathbb C}^{N×N_a×N_r}`, where :math:`N` is the batchsize.
        windb (None or float, optional): Cutoff for window (the default is None, which use the mean as the cutoff.)
        est (str, optional): Estimator, ``'ML'`` for Maximum Likelihood estimation, ``'LUMV'`` for Linear Unbiased Minimum Variance estimation (the default is 'ML')
        deg (int): The degree of polynominal
        axis (int, optional): Autofocus axis.
        isrmlpe (bool, optional): Is remove linear phase error? (the default is False)
        iscrct (bool, optional): Is corrected image? (the default is False)
        isplot (bool, optional): Is plot estimated phase error? (the default is False)

    Returns:
        xc (Tensor): Corrected SAR image :math:`{\bm Y}\in {\mathbb C}^{N×N_a×N_r}`, only if :attr:`iscrct` is ``True``, xc is returned.
        phi (Tensor): Estimated phase error :math:`\phi\in {\mathbb R}^{N×N_a}`.

    Raises:
        TypeError: :attr:`x` is complex and should be in complex or real represent formation!
        ValueError: Not supported estimator! Supported are ``'ML'`` and ``'LUMV'``.

    """
    cmap, showidx = 'gray', -1
    raise(ImportError('Not opened yet!'))


def pgaf_sm(SI, nsar, nsub=None, windb=None, est='ML', deg=4, niter=None, tol=1.e-6, isplot=False, islog=False):
    r"""Phase gradient autofocus for stripmap SAR.

    Phase gradient autofocus for stripmap SAR.

    Args:
        SI (Tensor): Complex SAR image :math:`N_a×N_r`.
        nsar (int): Number of synthetic aperture pixels.
        nsub (int, optional): Number of sub-aperture pixels. (the default is :math:`{\rm min}{N_{sar}, N_a}`)
        windb (None or float, optional): cutoff for window (the default is None, which use the mean as the cutoff.)
        est (str, optional): estimator, ``'ML'`` for Maximum Likelihood estimation, ``'LUMV'`` for Linear Unbiased Minimum Variance estimation (the default is 'ML')
        deg (int): Polynomial degrees (default 4) to fit the error, once fitted, the term of deg=[0,1] will be removed.
            If :attr:`deg` is None or lower than 2, then we do not fit the error with polynominal and not remove the linear trend.
        niter (int, optional): Maximum iters (the default is None, which means using :attr:`tol` for stopping)
        tol (float, optional): Phase error tolerance. (the default is 1.e-6)
        isplot (bool, optional): Plot estimated phase error or corrected image. (the default is False)
        islog (bool, optional): Print log information? (the default is False)

    Returns:
        SI (Tensor): Corrected SAR image :math:`{\bm X}\in {\mathbb C}^{N_a×N_r}`.
        phi (Tensor): Estimated phase error :math:`{\phi}\in {\mathbb R}^{N_a×1}`.

    Raises:
        TypeError: The input is complex and should be in complex or real represent formation!
        ValueError: For stripmap SAR, processing sub aperture should be smaller than synthetic aperture!
    """

    cmap, showidx = 'gray', -1
    if islog:
        print("---In pgaf_sm...")

    if th.is_complex(SI):
        # N, Na, Nr = x.size(0), x.size(-2), x.size(-1)
        cplxflag = True
    elif SI.size(-1) == 2:
        # N, Na, Nr = x.size(0), x.size(-3), x.size(-2)
        SI = th.view_as_complex(SI)
        cplxflag = False
    else:
        raise TypeError('SI is complex and should be in complex or real represent formation!')

    if SI.dim() == 2:
        SI = SI.unsqueeze(0)
        # SI = SI.to(th.complex128)

    N, Na, Nr = SI.size()
    if nsub is None:
        nsub = 2**tb.prevpow2(nsar / 2. + 1)
        nsub = min(nsub, Na)
    if nsub > nsar:
        raise ValueError(
            "For stripmap SAR, processing sub aperture %d should be smaller than synthetic aperture %d!" % (nsub, nsar))

    Noverlap = 0

    if niter is None:
        niter = 100
    if islog:
        print("~~~Do Phase Gradient Autofocus...")
    phi0, k = (1.e10, 0)
    phi = th.zeros((N, Na), device=SI.device)
    phitotal = 0.
    for k in tqdm(range(niter)):
        phi0 = phi.clone().detach()
        for n in range(0, Na, nsub):
            idx = n + nsub + Noverlap
            ep, gp = pgaf_sm_1iter(SI[:, n:idx, :], windb=windb, est=est, deg=deg,
                                   isrmlpe=True, iscrct=False, isplot=isplot)
            phi[:, n:n + nsub] = ep[:, 0:nsub]

        phitotal = phitotal + phi
        SI = phase_correction(SI, phi, nsub, axis=-2, ftshift=True)

        if isplot:
            XX = th.abs(SI[showidx])
            XX = tb.mapping(XX)
            plt.figure()
            plt.imshow(XX.numpy(), cmap=cmap)
            plt.show()

        if (th.mean(th.abs(phi - phi0)) <= tol):
            break

    if not cplxflag:
        SI = th.view_as_real(SI)
    
    if islog:
        print("~~~Done.")
        print("---Out pgaf_sm.")

    return SI, phitotal


if __name__ == '__main__':

    datafile = 'data/sarimg/ALPSRP020160970_Vr7180_R3_FocusedEach_5x256x256_AutoFocusPolyPhiMinEntropy_Epoch1000.h5'
    SI = tb.loadmat(datafile)['SI']

    SI0 = SI
    # sa, ea, sr, er = 3500, 3500 + 2048, 5500, 5500 + 2048
    sa, ea, sr, er = 4600, 4600 + 1024, 5000, 5000 + 1024
    # sa, ea, sr, er = 3000, 3000 + 512, 5000, 5000 + 512
    # sa, ea, sr, er = 3200, 3200 + 256, 5000, 5000 + 256

    SI = SI[sa:ea, sr:er, 0] + 1j * SI[sa:ea, sr:er, 1]

    SI0 = SI0[sa:ea, sr:er, 0] + 1j * SI0[sa:ea, sr:er, 1]

    deg = 7
    # deg = None
    est = 'ML'
    est = 'LUMV'

    niter = 40

    SI = th.from_numpy(SI)
    SI0 = th.from_numpy(SI0)
    # SI = SI.to('cuda:0')
    SI, pa = ts.pgaf_sm(SI, 6785, nsub=None, windb=None, est=est, deg=deg, niter=niter, tol=1.e-6, isplot=False, islog=False)

    print(pa.shape)
    plt.figure()
    plt.plot(pa[-1])
    plt.grid()
    plt.xlabel('Aperture time (samples)')
    plt.ylabel('Phase (rad)')
    plt.title('Estimated phase error (polynomial degree ' + str(deg) + ')')
    plt.show()

    SI0 = th.abs(SI0)
    SI = th.abs(SI)
    print("ENT:", tb.entropy(SI0))
    print("ENT:", tb.entropy(SI))
    print("MSE", th.sum(SI0 - SI))

    print(SI.shape, SI0.shape)
    SI = tb.mapping(SI)
    SI0 = tb.mapping(SI0)
    print(SI.shape, SI0.shape)

    plt.figure()
    plt.subplot(121)
    plt.imshow(SI0, cmap='gray')
    plt.subplot(122)
    plt.imshow(SI[-1], cmap='gray')
    plt.show()
