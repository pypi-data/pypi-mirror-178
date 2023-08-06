#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : target_background.py
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

import numpy as np
import torch as th
from skimage import filters
from torchbox.utils.const import EPS
import matplotlib.pyplot as plt


def extract_targets(x, region=None, thresh=None, cdim=None, isshow=False):
    r"""Extracts the pixels of targetss

    Parameters
    ----------
    x : tensor or numpy array
        The input image, if it's complex-valued, it's amplitude is used.
    region : list or None, optional
        The region ([top-left, bottom-right]) that contains targets for computing TBR.
        If :obj:`None`, :attr:`region` equals to ``([0, 0], [H, W])``, where :math:`H,W` 
        are the height and width of the image.
    thresh : float or None, optional
        The threshold targets.
    cdim : int or None, optional
        Specifies the complex axis of :attr:`x`. ``None`` --> complex or real
    isshow : bool, optional
        Show pixels of the extracted targets?
    """

    if th.is_complex(x):
        cdim = None
    if cdim is not None:
        x = x.pow(2).sum(cdim).sqrt()
    else:
        x = x.abs()
    x = x.numpy()

    if region is None:
        region = [min(targets[0]), min(targets[1]), max(targets[0]), max(targets[1])]

    x = x[region[0]:region[2], region[1]:region[3]]

    thresh = filters.threshold_otsu(x) if thresh is None else thresh

    idx = np.where(x > thresh)

    if isshow:
        plt.figure
        plt.subplot(121)
        plt.imshow(x)
        y = np.zeros(x.shape)
        y[idx] = 1
        plt.subplot(122)
        plt.imshow(x * y)
        plt.show()
    idx = list(idx)
    idx[0] += region[0]
    idx[1] += region[1]

    return tuple(idx), thresh


def tbr(x, targets, region=None, cdim=None, isshow=False):
    r"""Target-to-Background Ratio (TBR)

    .. math::
        \begin{align}
        {\rm TBR} = 20{\rm log}_{10}\left(\frac{{\rm max}_{i\in{\mathbb T}}(|{\bf X}_i|)}{{(1/N_{\mathbb B})}\Sigma_{j\in \mathbb B}|{\bf X}_j|)}\right)
        \label{equ:TBR}
        \end{align}

    Parameters
    ----------
    x : tensor
        The input image, if it's complex-valued, it's amplitude is used.
    targets : list or tuple
        The targets pixels. ([row1, row2, ...], [col1, col2, ...])
    region : list, tuple or None, optional
        The region ([top-left, bottom-right]) that contains targets for computing TBR.
        If :obj:`None`, :attr:`region` equals to ``([0, 0], [H, W])``, where :math:`H,W` 
        are the height and width of the image.
    cdim : int or None, optional
        Specifies the complex axis of :attr:`x`. ``None`` --> complex or real
    isshow : bool, optional
        Show target mask? (default: False)
    """

    if th.is_complex(x):
        cdim = None
    if cdim is not None:
        x = x.pow(2).sum(cdim).sqrt()
    else:
        x = x.abs()

    if region is None:
        region = [min(targets[0]), min(targets[1]), max(targets[0]), max(targets[1])]

    TGM = th.zeros(x.shape, dtype=th.int8)
    TGM[targets] = 1
    TGM = TGM[region[0]:region[2], region[1]:region[3]].to(x.device)
    x = x[region[0]:region[2], region[1]:region[3]]

    # mask of BG
    BGM = 1 - TGM

    # pixel number of bgs
    NB = BGM.sum()

    R = th.max(x * TGM) / (((1 / NB) * th.sum(x * BGM)) + EPS)

    TBR = 20 * th.log10(R).item()

    if isshow:
        plt.figure
        plt.subplot(131)
        plt.imshow(x)
        plt.subplot(132)
        plt.imshow(TGM)
        plt.subplot(133)
        plt.imshow(x * TGM)
        plt.show()

    return TBR


def tbr2(X, tgrs, subrs=None, isshow=False):
    r"""Target-to-Background Ratio (TBR)

    .. math::
        \begin{align}
        {\rm TBR} = 20{\rm log}_{10}\left(\frac{{\rm max}_{i\in{\mathbb T}}(|{\bf X}_i|)}{{(1/N_{\mathbb B})}\Sigma_{j\in \mathbb B}|{\bf X}_j|)}\right)
        \label{equ:TBR}
        \end{align}

    Parameters
    ----------
    X : tensor
        The input image, if it's complex-valued, it's amplitude is used.
    tgrs : list, optional
        target regions:[[TG1], [TG2], ..., [TGn]], [TGk] = [lefttop, rightbottom]]
    subrs : list, optional
        sub regions:[[SUB1], [SUB2], ..., [SUBn]], [SUBk] = [lefttop, rightbottom]]
    isshow : bool, optional
        show target mask given by :attr:`tgrs` (default: False)

    Returns
    -------
    TBR : float
        Target-to-Background Ratio (TBR)

    Raises
    ------
    TypeError
        tgrs mast be given
    """

    if th.is_complex(X):
        Xabs = X.abs()
    elif X.shape[-1] == 2:
        Xabs = X.pow(2).sum(-1).sqrt()
    else:
        Xabs = X.abs()

    if tgrs is None:
        raise TypeError("Please give the regions of targets!")

    if subrs is not None:
        # mask of Subregion
        SUBM = th.zeros(Xabs.shape, device=Xabs.device, dtype=th.int8)

        for subr in subrs:
            SUBM[subr[0]:subr[2], subr[1]:subr[3]] = 1
        Xabs = Xabs * SUBM

    # mask of TG
    TGM = th.zeros(Xabs.shape, device=Xabs.device, dtype=th.int8)

    for tgr in tgrs:
        TGM[tgr[0]:tgr[2], tgr[1]:tgr[3]] = 1

    # mask of BG
    BGM = 1 - TGM

    # pixel number of bgs
    NB = BGM.sum()

    R = th.max(Xabs * TGM) / (((1 / NB) * th.sum(Xabs * BGM)) + EPS)

    TBR = 20 * th.log10(R).item()

    if isshow:
        plt.figure
        plt.subplot(131)
        plt.imshow(Xabs)
        plt.subplot(132)
        plt.imshow(TGM)
        plt.subplot(133)
        plt.imshow(Xabs * TGM)
        plt.show()

    return TBR


if __name__ == '__main__':

    X = th.zeros((6, 6))
    X = th.rand((6, 6))
    # X = th.rand((6, 6)) + 1j * th.rand((6, 6))

    targets = [[2, 2, 3, 3], [2, 3, 2, 3]]

    X[2:4, 2:4] = 10

    print(X)

    TBR = tbr(X, targets=targets, region=[0, 0, 6, 6])

    print("TBR", TBR)
