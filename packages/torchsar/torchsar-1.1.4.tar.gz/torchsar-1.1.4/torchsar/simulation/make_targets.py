#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : make_targets.py
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
from torchbox.utils.const import *
from torchbox.dsp import normalsignals as sig
from torchbox import setseed


def gpoints(SceneArea, npoints, amin=0., amax=1., seed=None):
    """Generates point targets

    Parameters
    ----------
    SceneArea : tuple or list
        The area of scene.
    npoints : int
        The number of points.
    amin : float, optional
        The minimum amplitude. (default is 0)
    amax : float, optional
        The maximum amplitude. (default is 1)
    seed : int or None, optional
        The seed for random generator.

    Returns
    -------
    tensor
        A tensor contains coordinate and amplitude information.
    """
    if seed is not None:
        setseed(seed)
    xmin, xmax, ymin, ymax = SceneArea

    xs = th.rand(npoints, 1) * (xmax - xmin) + xmin
    ys = th.rand(npoints, 1) * (ymax - ymin) + ymin
    amps = th.rand(npoints, 1) * (amax - amin) + amin

    targets = th.zeros(npoints, 7)

    targets[:, [0]] = xs
    targets[:, [1]] = ys
    targets[:, [-1]] = amps

    return targets
