#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : channel_process.py
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

import math
import torch as th


def iq_correct(Sr):
    r"""IQ Correction performs the I Q data correction

    IQ Correction performs the I Q data correction

    - I/Q bias removal
    - I/Q gain imbalance correction
    - I/Q non-orthogonality correction

    see "Sentinel-1-Level-1-Detailed-Algorithm-Definition".

    Args:
        Sr (Tensor): SAR raw data matrix :math:`{\bm S}_r \in {\mathbb R}^{N_a×N_r×2}`

    Returns:
        Sr (Tensor): Corrected SAR raw data.
        Flag : dict

    """

    Na, Nr, _ = Sr.shape

    raise(ImportError('Not opened yet!'))



if __name__ == '__main__':

    Na, Nr = (4, 5)
    theta = th.rand(Na, Nr)

    Is = th.cos(theta)
    Qs = th.sin(theta)
    Sr = th.zeros((Na, Nr, 2))
    Sr[:, :, 0] = Is
    Sr[:, :, 1] = Qs

    print(Sr)
    Sr, Flag = iq_correct(Sr)
    print(Sr)
    print(Flag)
