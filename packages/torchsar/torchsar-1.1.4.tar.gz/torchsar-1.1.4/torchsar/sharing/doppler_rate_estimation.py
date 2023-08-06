#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : doppler_rate_estimation.py
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
from torchbox.utils.const import *


def dre_geo(Wl, Vr, R, Ar=0.):
    """doppler rate estimation based on geometry

    doppler rate estimation based on geometry

    Parameters
    ----------
    Wl : float
        Wave length.
    Vr : float, list or array
        Equivalent velocity of radar.
    R : float, list or array
        Minimum slant range from radar to target.
    Ar : float, list or array
        Equivalent squint angle.
    """

    raise(ImportError('Not opened yet!'))


