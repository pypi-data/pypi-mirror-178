#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : scatter_selection.py
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
import matplotlib.pyplot as plt


def center_dominant_scatters(x, axis=-2, isplot=False):
    """Center the dominant scatters.

    Parameters
    ----------
    x : tensor
        Complex SAR image tensor.
    axis : int, optional
        The axis to be centered in.
    isplot : bool, optional
        Whether to plot.

    Returns
    -------
    tensor
        Centered.

    Raises
    ------
    TypeError
        Intput must be complex image!
    """
    if th.is_complex(x):
        cplxflag = True
        pass
    elif x.size(-1) == 2:
        cplxflag = False
        x = x[..., 0] + 1j * x[..., 1]
    else:
        raise TypeError('Intput must be complex image!')

    if x.dim() == 2:
        x = x.unsqueeze(0)

    raise(ImportError('Not opened yet!'))


def window_data(z, win=None, axis=-2, isplot=False):
    showidx = -1

    if th.is_complex(z):
        cplxflag = True
        pass
    elif z.size(-1) == 2:
        cplxflag = False
        z = z[..., 0] + 1j * z[..., 1]
    else:
        raise TypeError('Intput must be complex image!')

    if z.dim() == 2:
        z = z.unsqueeze(0)

    N, Na, Nr = z.size()
    Nx = z.size(axis)
    midpos = int(Nx / 2.)
    if axis == -2 or axis == 1:
        axisw, axiso = -2, -1
        winshape = [Nx, 1]
    if axis == -1 or axis == 2:
        axisw, axiso = -1, -2
        winshape = [1, Nx]

    # ---Step 3: Windowing
    ncoh_avg_win = th.sum(z.conj() * z, axis=axiso)  # N-Nx
    ncoh_avg_win_db20 = 20. * th.log10(th.abs(ncoh_avg_win))  # N-Nx
    win_cutoff = th.mean(ncoh_avg_win_db20, axis=-1)  # N-1

    raise(ImportError('Not opened yet!'))
