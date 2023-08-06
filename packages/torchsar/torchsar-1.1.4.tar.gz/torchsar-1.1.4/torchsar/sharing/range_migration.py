#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : range_migration.py
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
import torchbox as tb


def rcmc_interp(Sr, tr, D):
    r"""range migration correction with linear interpolation

    Range migration correction with linear interpolation.

    Parameters
    ----------
    Sr : tensor
        SAR raw data :math:`N_a×N_r` in range dopplor domain
    tr : 1d-tensor
        time array :math:`N_r×1` in range
    D : 1d-tensor
        :math:`N_a×1` migration factor vector

    Returns
    -------
    Srrcmc
        data after range migration correction :math:`N_a×N_r`
    """

    if Sr.shape[1] != tr.shape[1]:
        raise ValueError('Sr has shape: ', Sr.shape,
                         'tr has shape: ', tr.shape)
    if Sr.shape[0] != D.shape[0]:
        raise ValueError('Sr has shape: ', Sr.shape,
                         'D has shape: ', D.shape)
    Sr = th.view_as_real(Sr)
    Sr = Sr.double()

    raise(ImportError('Not opened yet!'))

