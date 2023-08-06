#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : maximum_contrast.py
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


def mcaf_sm(x, phi=None, niter=10, tol=1e-4, eta=0.1, method='N-MCA', selscat=False, axis=-2, ftshift=True, islog=False):
    r"""Contrast based autofocus

    Maximum-Contrast based Autofocus (MCA)

    Parameters
    ----------
    x : Tensor
        complex image with shape :math:`N×N_a×N_r` or :math:`N×N_a×N_r×2`
    phi : float, optional
        initial value of :math:`\phi` (the default is None, which means zeros)
    niter : int, optional
        number of iterations (the default is 10)
    method : str, optional
        method used to update the phase error
        - ``'FP-MCA'`` --> Fix Point
        - ``'CD-MCA'`` --> Coordinate Descent
        - ``'SU-MCA'`` --> Simultaneous Update
        - ``'N-MCA'`` --> Newton, see [2], [1] has problem when used to small image
        - ``'SN-MCA'`` --> Simplified Newton
        - ``'MN-MCA'`` --> Modified Newton
    selscat : bool, optional
        Select brighter scatters.
    axis : int, optional
        Compensation axis.
    ftshift :  bool, optional
        Does shift zero frequency to center?
    islog :  bool, optional
        Does print log info.


    see [1] Zhang S , Liu Y , Li X . Fast Entropy Minimization Based Autofocusing Technique for ISAR Imaging[J]. IEEE Transactions on Signal Processing, 2015, 63(13):3425-3434.
        [2] Zeng T , Wang R , Li F . SAR Image Autofocus Utilizing Minimum-Entropy Criterion[J]. IEEE Geoence & Remote Sensing Letters, 2013, 10(6):1552-1556.
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

    raise(ImportError('Not opened yet!'))


if __name__ == '__main__':

    import matplotlib.pyplot as plt

    matfile = '/mnt/e/ws/github/psar/psar/examples/imaging/data/ALPSRP020160970_Vr7180_R3.mat'
    SI = tb.loadmat(matfile)['SI']

    SI0 = SI
    # sa, ea, sr, er = 3500, 3500 + 2048, 5500, 5500 + 2048
    # sa, ea, sr, er = 4600, 4600 + 1024, 5000, 5000 + 1024
    sa, ea, sr, er = 3000, 3000 + 512, 5000, 5000 + 512
    # sa, ea, sr, er = 3200, 3200 + 256, 5000, 5000 + 256

    SI = SI[sa:ea, sr:er, 0] + 1j * SI[sa:ea, sr:er, 1]

    SI0 = SI0[sa:ea, sr:er, 0] + 1j * SI0[sa:ea, sr:er, 1]

    deg = 7
    method, niter = 'N-MCA', 300

    SI = th.from_numpy(SI)
    SI0 = th.from_numpy(SI0)
    # SI = SI.to('cuda:0')
    SI, pa = ts.mcaf_sm(SI, phi=None, niter=niter, tol=1e-4, eta=0.1, method=method, selscat=False, ftshift=True, islog=True)

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
