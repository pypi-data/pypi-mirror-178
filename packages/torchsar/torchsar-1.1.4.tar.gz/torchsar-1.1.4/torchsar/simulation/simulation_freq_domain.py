#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : simulation_freq_domain.py
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
import torchbox as tb
import torchsar as ts
import matplotlib.pyplot as plt


def dsm2sar_fd(g, pdict, mode='StationaryTarget2D', ftshift=True, device='cpu'):
    """Frequency-domain simulation

    SAR raw data simulation by frequency-domain method.

    Parameters
    ----------
    g : tensor
        The digital scene matrix.
    pdict : dict
        The SAR platform parameters.
    mode : str, optional
        Simulation mode.
    ftshift : bool, optional
        Shift zero-frequency to center?
    device : str, optional
        Specifies which device to be used.

    Returns
    -------
    tensor
        Simulated SAR raw data.
    """
    Vg = pdict['Vg']
    Vr = pdict['Vr']
    Ar = pdict['Ar']
    SC = th.tensor(pdict['SceneCenter'], device=device)

    Kr, Tp = pdict['Kr'], pdict['Tp']
    Na, Nr = pdict['EchoSize']
    if pdict['GeometryMode'] == 'SceneGeometry':
        Rc = pdict['Rsc']
        R0 = pdict['Rs0']
    if pdict['GeometryMode'] == 'BeamGeometry':
        Rc = pdict['Rbc']
        R0 = pdict['Rb0']
    Wl, Fc, La = pdict['Wl'], pdict['Fc'], pdict['La']

    raise(ImportError('Not opened yet!'))

