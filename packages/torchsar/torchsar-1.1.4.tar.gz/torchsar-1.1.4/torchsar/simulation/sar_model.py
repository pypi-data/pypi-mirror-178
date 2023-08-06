#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : sar_model.py
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

import pickle as pkl
import torch as th
from torchbox.utils.const import *
from torchbox.dsp import normalsignals as sig
from torchsar.sharing.antenna_pattern import antenna_pattern_azimuth


def sarmodel(pdict, mod='2D1', gdshape=None, device='cpu', islog=False):
    r"""model sar imaging process.

    SAR imaging model

    Parameters
    ----------
    pdict: dict
        SAR platform parameters
    mod: str, optional
        mod type(default: '2D1')

            if mod is '2D1':
                the model will be in vector mode:
                    s = A      g
                    MNx1      MNxHW  HWx1(M: Na, N: Nr, MN << HW)
            if mod is '2D2':
                the model will be in mat mode:
                    S = Aa     G     Be
                    MxN       MxH    HxW   WxN(M: Na, N: Nr, M << H, N << W)
            if mod is '1Da':
                    S = A      G
                    MxW       MxH    HxW(M: Na, N: Nr, M << H)
            if mod is '1Dr':
                    S'    =   A      G'
                    NxH       NxW    WxH(M: Na, N: Nr, N << W)

    gdshape: tuple, optional
        discrete scene size of G (default: None, sarplat.acquisition['SceneArea'], dx=dy=1)
    device: str
        device, default is 'cpu'
    islog : bool
        show log info (default: True)

    Returns
    -------
    A : torch tensor
        Imaging mapping matrix.
    """
    if islog:
        print("===In sarmodel...")

    Vg = pdict['Vg']
    Vr = pdict['Vr']
    Ar = pdict['Ar']
    H = pdict['H']
    V = Vr

    Kr, Tp = pdict['Kr'], pdict['Tp']
    Na, Nr = pdict['EchoSize']
    if pdict['GeometryMode'] == 'SceneGeometry':
        Rc = pdict['Rsc']
        R0 = pdict['Rs0']
        SC = th.tensor(pdict['SceneCenter'], device=device)
    if pdict['GeometryMode'] == 'BeamGeometry':
        Rc = pdict['Rbc']
        R0 = pdict['Rb0']
        SC = th.tensor(pdict['BeamCenter'], device=device)
    Wl, Fc, La = pdict['Wl'], pdict['Fc'], pdict['La']

    Na, Nr = pdict['EchoSize']
    SA = pdict['SceneArea']

    gX = SA[1] - SA[0]
    gY = SA[3] - SA[2]
    Xc, Yc = SC[0].item(), SC[1].item()
    ta = pdict['ta']
    tr = pdict['tr'].reshape(-1, 1)
    if type(ta) is not th.Tensor:
        ta = th.from_numpy(ta)
    if type(tr) is not th.Tensor:
        tr = th.from_numpy(tr)

    raise(ImportError('Not opened yet!'))



def __computeRmn(ta, tr, H, V, Xc, Yc, SA, gH, gW):
    r"""compute range at g(i, j)

    compute range at g(i, j)

    Arguments
    ------------
    m int
        current y coordinate of H
    n int
        current x coordinate of W
    ta {time in azimuth}
        azimuth time
    tr numpy array
        range time
    H int
        height of SAR platform
    V float
        velocity of SAR platform
    Yc float
        center coordinate in Y axis
    Xc float
        center coordinate in X axis
    SA list
        scene area: [xmin, xmax, ymin, ymax]
    H int
        height of scene(Y)
    W int
        width of scene(X)
    """

    xmin = SA[0] + Xc
    xmax = SA[1] + Xc
    ymin = SA[2] + Yc
    ymax = SA[3] + Yc

    yy = th.linspace(ymin, ymax, gH).to(ta.device)
    xx = th.linspace(xmin, xmax, gW).to(ta.device)
    ys, xs = th.meshgrid(yy, xx, indexing='ij')

    R = th.sqrt(xs ** 2 + (ys - V * ta) ** 2 + H ** 2)  # [gY, gX]
    R = R.reshape(1, -1)
    ys = ys.reshape(1, -1)
    xs = xs.reshape(1, -1)
    return R, xs, ys


def load_sarmodel(datafile, mod='AinvA'):
    r"""load sarmodel file

    load sarmodel file (``.pkl``)

    Parameters
    ----------
    datafile : str
        Model data file path.
    mod : str, optional
        Specify load which variable, ``A``, ``invA``, ``AinvA``
        (the default is 'AinvA', which :math:`\bm A`, :math:`{\bm A}^{-1}` )

    Returns
    -------
    A : numpy array
        Imaging mapping matrix.
    invA : numpy array
        Inverse of imaging mapping matrix.

    Raises
    ------
    ValueError
        wrong mod
    """
    print("===reading model file: ", datafile, "...")
    if datafile != "":
        # get map
        f = open(datafile, 'rb')
        # for python2
        if sys.version_info < (3, 1):
            if mod == 'A':
                A = pkl.load(f)
                f.close()
                return A
            if mod == 'invA':
                pkl.load(f)
                invA = pkl.load(f)
                f.close()
                return invA
            if mod == 'AinvA':
                A = pkl.load(f)
                invA = pkl.load(f)
                f.close()
                return A, invA
            if mod == 'AAH':
                A = pkl.load(f)
                pkl.load(f)
                AH = pkl.load(f)
                f.close()
                return A, AH
            if mod == 'AinvAAH':
                A = pkl.load(f)
                invA = pkl.load(f)
                AH = pkl.load(f)
                f.close()
                return A, invA, AH
            f.close()
            raise ValueError("mod: 'A', 'invA', 'AinvA', 'AAH', 'AinvAAH'")

        # for python3
        else:
            if mod == 'A':
                A = pkl.load(f, encoding='latin1')
                f.close()
                return A
            if mod == 'invA':
                pkl.load(f, encoding='latin1')
                invA = pkl.load(f, encoding='latin1')
                f.close()
                return invA
            if mod == 'AinvA':
                A = pkl.load(f, encoding='latin1')
                invA = pkl.load(f, encoding='latin1')
                f.close()
                return A, invA
            if mod == 'AAH':
                A = pkl.load(f, encoding='latin1')
                pkl.load(f, encoding='latin1')
                AH = pkl.load(f, encoding='latin1')
                f.close()
                return A, AH
            if mod == 'AinvAAH':
                A = pkl.load(f, encoding='latin1')
                invA = pkl.load(f, encoding='latin1')
                AH = pkl.load(f, encoding='latin1')
                f.close()
                return A, invA, AH
            f.close()
            raise ValueError("mod: 'A', 'invA', 'AinvA', 'AAH', 'AinvAAH'")
    else:
        return None


def save_sarmodel(A, invA=None, AH=None, datafile='./model.pkl'):
    r"""save model mapping matrix

    save model mapping matrix to a file.


    Parameters
    ----------
    A : numpy array
        Imaging mapping matrix
    invA : numpy array, optional
        Moore - Penorse inverse of A(default: {None})
    AH : numpy array, optional
        The Hermite :math:`{\bm A}^H` of the Imaging mapping matrix :math:`\bm A`
        (the default is None, which does not store)
    datafile : str, optional
        save file path(default: {'./model.pkl'})
    """

    f = open(datafile, 'wb')

    pkl.dump(A, f, 0)
    if invA is not None:
        pkl.dump(invA, f, 0)
    if AH is not None:
        pkl.dump(AH, f, 0)
    f.close()

