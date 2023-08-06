#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : minimum_entropy.py
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
from tqdm import tqdm


def __entropy(X):

    if th.is_complex(X):  # N-Na-Nr
        X = (X * X.conj()).real
    elif X.size(-1) == 2:  # N-Na-Nr-2
        X = th.sum(X.pow(2), axis=-1)

    logfunc, axis = th.log2, (1, 2)
    P = th.sum(X, axis=axis, keepdims=True)
    p = X / (P + tb.EPS)
    S = -th.sum(p * logfunc(p + tb.EPS), axis)
    return th.mean(S)


def meaf_ssa_sm(x, niter=10, delta=None, toli=1e-2, tolo=1e-2, ftshift=True, islog=False):
    r"""Stage-by-Stage minimum entropy

    [1] Morrison Jr, Robert Lee; Autofocus, Entropy-based (2002): Entropy-based autofocus for synthetic aperture radar.

    Parameters
    ----------
    x : Tensor
       Corrupt complex SAR image. N-Na-Nr(complex) or N-Na-Nr-2(real)
    niter : int, optional
       The number of iteration (the default is 10)
    delta : {float or None}, optional
       The change step (the default is None (i.e. PI))
    toli : int, optional
       Tolerance error for inner loop (the default is 1e-2)
    tolo : int, optional
       Tolerance error for outer loop (the default is 1e-2)
    ftshift : bool, optional
       Shift the zero frequency to center? (the default is True)
    islog : bool, optional
       Print log information? (the default is False)
    """

    if delta is None:
        delta = tb.PI

    if th.is_complex(x):
        x = th.view_as_real(x)
        cplxflag = True
    elif x.size(-1) == 2:
        cplxflag = False
    else:
        raise TypeError('x is complex and should be in complex or real represent formation!')

    d = x.dim()
    N, Na, Nr = x.size(0), x.size(-3), x.size(-2)

    wshape = [1] * d
    wshape[-3] = Na
    wshape[0] = N

    x = tb.fft(x, cdim=-1, dim=-3, keepcdim=True, shift=ftshift)
    phio = th.zeros(wshape, device=x.device, dtype=x.dtype)
    ephi = th.cat((th.cos(phio), th.sin(phio)), dim=-1)
    # print(wshape, phio.min(), phio.max(), ephi.min(), ephi.max())
    So = __entropy(tb.ifft(tb.ematmul(x, ephi), axis=-3, shift=ftshift))
    i, Soi0, Soo0 = 0, 1e13, 1e13
    # print(i, So, Soi0, Soo0)
    while(i < niter):
        Soo0 = So
        while True:
            Soi0 = So
            # print(i, "===")
            for a in range(Na):
                phi1, phi2 = phio.clone().detach(), phio.clone().detach()
                for n in range(N):
                    phi1[n, a] += delta
                    phi2[n, a] -= delta
                ephi = th.cat((th.cos(phi1), th.sin(phi1)), dim=-1)
                S1 = __entropy(tb.ifft(tb.ematmul(x, ephi), axis=-3, shift=ftshift))
                ephi = th.cat((th.cos(phi2), th.sin(phi2)), dim=-1)
                S2 = __entropy(tb.ifft(tb.ematmul(x, ephi), axis=-3, shift=ftshift))
                if S1 < So:
                    So = S1
                    phio = phi1.clone().detach()
                elif S2 < So:
                    So = S2
                    phio = phi2.clone().detach()
                # print(Soi0, So, S1, S2, abs(So - Soi0), i)
            if abs(So - Soi0) < toli:
                break
        if abs(So - Soo0) > tolo:
            i += 1
            delta /= 2.
        else:
            break
        # print(i, delta, abs(So - Soo0), tolo, abs(So - Soo0) < tolo, So, Soo0)
        # print(i, delta, abs(So - Soi0), tolo, abs(So - Soi0) < toli, So, Soi0)
    ephi = th.cat((th.cos(phio), th.sin(phio)), dim=-1)
    return tb.ifft(tb.ematmul(x, ephi)), ephi


def meaf_sm(x, phi=None, niter=10, tol=1e-4, eta=0.1, method='N-MEA', selscat=False, isunwrap=True, deg=None, axis=-2, ftshift=True, islog=False):
    r"""Entropy based autofocus

    Minimum-Entropy based Autofocus (MEA)

    Args:
        x (Tensor): complex image with shape :math:`N×N_a×N_r` or :math:`N×N_a×N_r×2`
        phi (Tensor, optional): initial value of :math:`\phi` (the default is None, which means zeros)
        niter (int, optional): number of iterations (the default is 10)
        tol (float, optional): Error tolerance.
        eta (float, optional): Learning rate.
        method (str, optional): method used to update the phase error
            - ``'FP-MEA'`` --> Fix Point
            - ``'CD-MEA'`` --> Coordinate Descent
            - ``'SU-MEA'`` --> Simultaneous Update
            - ``'N-MEA'`` --> Newton, see [2], [1] has problem when used to small image
            - ``'SN-MEA'`` --> Simplified Newton
            - ``'MN-MEA'`` --> Modified Newton
        selscat (bool, optional): Select brighter scatters (default: False).
        isunwrap (bool, optional): Unwrap radian phase (default: True).
        deg (int or None, optional): The degree of polynominal, if None, no fitting.
        axis (int, optional): Compensation axis.
        ftshift (bool, optional): Does shift zero frequency to center?
        islog (bool, optional): Does print log info.


        see [1] Zhang S , Liu Y , Li X . Fast Entropy Minimization Based Autofocusing Technique for ISAR Imaging[J]. IEEE Transactions on Signal Processing, 2015, 63(13):3425-3434.
            [2] Zeng T , Wang R , Li F . SAR Image Autofocus Utilizing Minimum-Entropy Criterion[J]. IEEE Geoence & Remote Sensing Letters, 2013, 10(6):1552-1556.

    Returns:
        (Tensor): Description
    """

    if not th.is_complex(x):
        x = th.view_as_complex(x)

    if selscat:
        x = ts.center_dominant_scatters(x)
        x = ts.window_data(x, win=None)

    if x.dim() == 2:
        x = x.unsqueeze(0)

    if axis == -2 or axis == 1:
        axisc, axiso = -2, -1
    if axis == -1 or axis == 2:
        axisc, axiso = -1, -2

    N, Na, Nr = x.size()

    if islog:
        print("---Do Minimum Entropy Autofocus(%s)..." % method)

    phi = th.tensor([0], device=x.device)
    raise(ImportError('Not opened yet!'))


if __name__ == '__main__':

    import matplotlib.pyplot as plt

    matfile = '/mnt/e/ws/github/psar/psar/examples/imaging/data/ALPSRP020160970_Vr7180_R3.mat'
    SI = tb.loadmat(matfile)['SI']

    SI0 = SI
    # sa, ea, sr, er = 3500, 3500 + 2048, 5500, 5500 + 2048
    sa, ea, sr, er = 4600, 4600 + 1024, 5000, 5000 + 1024
    sa, ea, sr, er = 3000, 3000 + 512, 5000, 5000 + 512
    # sa, ea, sr, er = 3200, 3200 + 256, 5000, 5000 + 256

    SI = SI[sa:ea, sr:er, 0] + 1j * SI[sa:ea, sr:er, 1]

    SI0 = SI0[sa:ea, sr:er, 0] + 1j * SI0[sa:ea, sr:er, 1]

    deg = 7
    method, niter = 'N-MEA', 160
    # method, niter = 'FP-MEA', 400

    SI = th.from_numpy(SI)
    SI0 = th.from_numpy(SI0)
    # SI = SI.to('cuda:0')
    SI, pa = ts.meaf_sm(SI, phi=None, niter=niter, tol=1e-4, eta=0.1, method=method, selscat=False, ftshift=True, islog=True)

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
