#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : sidelobe_suppression.py
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

from __future__ import division, print_function
import torch as th
from torchbox.dsp.ffts import fft, ifft
from torchbox.dsp.window_function import window


def sls_fd(x, axis=0, wtype=None, dtype=None):
    """Sidelobe suppression in frequency domain

    Sidelobe suppression in frequency domain


    Parameters
    ----------
    x : tensor
        The input.
    axis : int, optional
        The axis for sidelobe-suppression.
    wtype : str or None, optional
        The type of window, default is None. see :func:`window`.
    dtype : torch's dtype or None, optional
        The data type. If None, use default dtype of torch.

    Returns
    -------
    tensor
        The suppressed.
    """

    raise(ImportError('Not opened yet!'))

