#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : beamwidth_footprint.py
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
import numpy as np
from torchbox.utils.const import *


def azimuth_beamwidth(Wl, La):
    BWa = 0.886 * Wl / La
    return BWa


def azimuth_footprint(R, Wl, La):

    BWa = 0.886 * Wl / La
    return R * BWa


def compute_range_beamwidth2(Nr, Fsr, H, Aon):
    r"""computes beam angle in range direction


    Parameters
    ----------
    Nr : int
        Number of samples in range direction.
    Fsr : float
        Sampling rate in range direction.
    H : float
        Height of the platform.
    Aon : float
        The off-nadir angle (unit: rad).

    Returns
    -------
    float
        The beam angle (unit, rad) in range direction.

    """

    Rnear = H / (np.cos(Aon) + EPS)
    Rfar = Rnear + Nr * (C / (2. * Fsr))

    return np.arccos(H / Rfar) - abs(Aon)


def cr_footprint(Wl, H, La, Ad):
    r"""cross range (azimuth) foot print

    .. math::
       R_{CR} \approx \frac{\lambda}{L_a}\frac{H}{{\rm cos}\theta_d}

    Parameters
    ----------
    Wl : float
        wave length
    H : float
        height of SAR platform
    La : float
        length of antenna aperture (azimuth)
    Ad : float
        depression angle

    Returns
    -------
    float
        foot print size in azimuth
    """

    FPa = (Wl * H) / (La * np.cos(Ad))

    return FPa
