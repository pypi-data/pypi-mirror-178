#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : make_sar_params.py
# @author    : Zhi Liu
# @email     : zhiliu.mind@gmail.com
# @homepage  : http://iridescent.ink
# @date      : Sun Nov 27 2022
# @version   : 2.0
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

from __future__ import print_function
import math
import torch as th
import torchbox as tb


class SARParameterGenerator(object):

    """SAR Parameter Generator

    Attributes
    ----------
    prdict : dict
        ``{'p1': [low, high], 'p2': [low, high]...}``
    seed : int or None
        The seed for random generator.
    """

    def __init__(self, prdict, seed=None):
        self.prdict = prdict
        self.seed = seed
        if seed is not None:
            tb.setseed(seed)

    def mksarp(self, n=1, seed=None):
        """Makes SAR Parameters

        Parameters
        ----------
        n : int, optional
            The number of experiments.
        seed : None, optional
            The seed for random generator.

        Returns
        -------
        dict
            The SAR Parameter dict.
        """
        if seed is not None:
            tb.setseed(seed)

        pdict = {}
        for k, v in self.prdict.items():
            if v is not None:
                low, high = v
                if n == 1:
                    pdict[k] = th.rand(n).item() * (high - low) + low
                else:
                    pdict[k] = th.rand(n) * (high - low) + low

        return pdict


if __name__ == '__main__':

    seed = 2020
    prdict = {}
    prdict['H'] = (0, 100)
    prdict['V'] = (11, 22)

    sarg = SARParameterGenerator(prdict, seed=seed)

    pdict = sarg.mksarp()

    print(pdict)
