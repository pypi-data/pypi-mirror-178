#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : simulation_time_domain.py
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


def tgs2sar_td(targets, pdict, mode='Target', device='cpu'):
    """Time-domain simulation

    SAR raw data simulation by time-domain method.

    Parameters
    ----------
    targets : tensor
        A 2d-tensor contains the information of targets,
        each row is a target [x, y, z, vx, vy, vz, a].
    pdict : dict
        The SAR platform parameters.
    mode : str, optional
        Simulation mode.
    device : str, optional
        Specifies which device to be used.

    Returns
    -------
    tensor
        Simulated SAR raw data tensor.
    """
    # target --> [x, y, z, vx, vy, vz, a]
    platform = th.tensor(pdict['PlatCenter'], device=device)
    SC = th.tensor(pdict['SceneCenter'], device=device)
    if type(targets) is not th.Tensor:
        targets = th.tensor(targets)
    Kr, Tp = pdict['Kr'], pdict['Tp']
    Na, Nr = pdict['EchoSize']
    if pdict['GeometryMode'] == 'SceneGeometry':
        Rc = pdict['Rsc']
        R0 = pdict['Rs0']
    if pdict['GeometryMode'] == 'BeamGeometry':
        Rc = pdict['Rbc']
        R0 = pdict['Rb0']
    Wl, Fc, La = pdict['Wl'], pdict['Fc'], pdict['La']

    V = pdict['V']
    Vg = pdict['Vg']
    Vr = pdict['Vr']
    Ar = pdict['Ar']
    targets = targets.to(device)
    eta = pdict['ta'].to(device)
    tau = pdict['tr'].to(device)

    if th.is_complex(targets):
        rcss = targets[:, [-1]]
        targets = targets[:, 0:-1].real
    else:
        rcss = targets[:, [-1]]
        targets = targets[:, 0:-1]

    raise(ImportError('Not opened yet!'))

