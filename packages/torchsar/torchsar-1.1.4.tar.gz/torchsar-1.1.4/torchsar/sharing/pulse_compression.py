#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : pulse_compression.py
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
from torchbox.base.arrayops import cut
from torchbox.utils.const import *


def mfpc_throwaway(X, No, Nh, axis=0, mffdmod='way1', ftshift=False):
    r"""Throwaway invalid pulse compressed data

    Throwaway invalid pulse compressed data

    Parameters
    ----------
    X : Tensor
        Data after pulse compression.
    No : int
        Output size.
    Nh : int
        Filter size.
    axis : int, optional
        Throwaway dimension. (the default is 0)
    mffdmod : str, optional
        Frequency filter mode. (the default is 'way1')
    ftshift : bool, optional
        Whether to shift frequency (the default is False)
    """

    if axis is None:
        axis = 1
    if ftshift is None:
        ftshift = False

    Nfft = np.size(X, axis)
    Nfft, No, Nh = np.uint([Nfft, No, Nh])

    if No > Nfft:
        raise ValueError('Output size is bigger than input size!')
    elif No == Nfft:
        return X

    N = Nfft - No

    if ftshift:
        if mffdmod in ['way1', 'WAY1', 'Way1', 'way2', 'WAY2', 'Way2', 'way3', 'WAY3', 'Way3', 'way4', 'WAY4', 'Way4']:
            Nstart = np.uint(np.floor((N + 1) / 2.))
            Nend = np.uint(Nfft - (N - Nstart))
            X = cut(X, ((Nstart, Nend),), axis)
        else:
            raise ValueError('Unsupported frequency domain matched filter: ' + mfmod)

    else:
        if mffdmod in ['way1', 'WAY1', 'Way1']:
            Nstart = np.uint(np.fix(Nh / 2.))
            Nend = np.uint(Nstart + No)
            X = cut(X, ((Nstart, Nend),), axis)
        elif mffdmod in ['way2', 'WAY2', 'Way2']:
            Nend1 = Nfft
            Nstart1 = np.uint(Nend1 - (Nh - 1))
            X = cut(X, ((Nstart1, Nend1), (0, No)), axis)
            Nstart = np.uint(np.fix(Nh / 2.))
            Nend = np.uint(Nstart + No)
            X = cut(X, ((Nstart, Nend),), axis=axis)
        elif mffdmod in ['way3', 'WAY3', 'Way3']:
            Nstart = 0
            Nend = No
            X = cut(X, ((Nstart, Nend),), axis)
        elif mffdmod in ['way4', 'WAY4', 'Way4']:
            Nstart = 0
            Nend = No
            X = cut(X, ((Nstart, Nend),), axis)
        else:
            raise ValueError('Unsupported frequency domain matched filter: ' + mfmod)
    return X


if __name__ == '__main__':

    X = th.tensor(range(32))
    print(X, X.shape[0])

    No, Nh = (24, 7)
    X = mfpc_throwaway(X, No, Nh, axis=0, mffdmod='way1', ftshift=True)
    print(X)
