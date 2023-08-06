#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : slant_ground_range.py
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
from torchbox.utils.const import *


def slantr2groundr(R, H, Ar, Xc):
    """slant range to ground range

    Convert slant range :math:`R` to ground range :math:`X`.

    Parameters
    ----------
    R : 1d-tensor
        slant range array
    H : float
        sarplat height
    Ar : float
        squint angle (unit, rad) in line geometry

    Returns
    -------
    X : 1d-tensor
        ground range

    """
    return th.sqrt(th.abs((R * math.cos(Ar))**2 - H * H) + EPS) - Xc
    # return th.sqrt(th.abs((R * math.cos(Ar))**2 - H * H) + EPS)


def slantt2groundr(tr, H, Ar):
    """slant time to ground range

    Convert slant range time :math:`t_r` to ground range :math:`X`.

    Parameters
    ----------
    tr : 1d-tensor
        range time array
    H : float
        sarplat height
    Ar : float
        squint angle (unit, rad) in line geometry

    Returns
    -------
    X : 1d-tensor
        ground range

    """

    return th.sqrt(th.abs(((tr * C / 2.) * math.cos(Ar))**2 - H * H) + EPS)


def groundr2slantr(X, H, Ar, Xc):
    """ground range to slant range

    Convert ground range :math:`R` to slant range :math:`X`.

    Parameters
    ----------
    X : 1d-tensor
        ground range array
    H : float
        sarplat height
    Ar : float
        squint angle (unit, rad) in line geometry

    Returns
    -------
    R : 1d-tensor
        slant range

    """

    return th.sqrt((X + Xc)**2 + H * H + EPS) / (math.cos(Ar) + EPS)
    # return th.sqrt((X)**2 + H * H + EPS) / (math.cos(Ar) + EPS)


def groundr2slantt(X, H, Ar):
    """ground range to slant time

    Convert ground range :math:`X` to slant time :math:`t_r`.

    Parameters
    ----------
    X : 1d-tensor
        ground range
    H : float
        sarplat height
    Ar : float
        squint angle (unit, rad) in line geometry

    Returns
    -------
    tr : 1d-tensor
        range time array

    """

    return 2. * th.sqrt(X**2 + H * H + EPS) / (math.cos(Ar) + EPS) / C


def min_slant_range(Rnear, Fsr, Noff):
    """minimum slant range from radar to target

    Compute the minimum slant range from radar to target.

    Parameters
    ----------
    Rnear : float
        The nearest range (start sampling) from radar to the target.
    Fsr : float
        Sampling rate in range direction
    Noff : 1d-tensor
        Offset from the start distance (start sampling) cell.

    Returns
    -------
    r : 1d-tensor
        Minimum slant range of each range cell.
    """
    r = Rnear + Noff * (C / (2. * Fsr))
    return r


def min_slant_range_with_migration(Rnear, Fsr, Noff, Wl, Vr, fdc):
    r = Rnear + Noff * (C / (2. * Fsr))
    return r / th.sqrt(1. - (Wl * fdc / (Vr + Vr))**2)
