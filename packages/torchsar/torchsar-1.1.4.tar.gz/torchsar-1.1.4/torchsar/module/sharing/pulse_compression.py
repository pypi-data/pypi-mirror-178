#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : pulse_compression.py
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
import torch as th
import torchbox as tb
from torchsar.module.sharing.matched_filter import RangeMatchedFilter, AzimuthMatchedFilter, AzimuthMatchedFilterLinearFit


class RangeCompress(th.nn.Module):

    def __init__(self, Na, Nr, Tp, Fsr, Kr, Fc, trainable=True, dtype=th.float32):
        super(RangeCompress, self).__init__()
        self.Na = Na
        self.Nr = Nr
        self.Tp = Tp
        self.Fsr = Fsr
        self.Kr = Kr
        self.Fc = Fc
        self.dtype = dtype
        self.rgmf = RangeMatchedFilter(Na, Tp, Fsr, Kr, Fc, trainable=trainable, dtype=dtype)

    def forward(self, X):

        raise(ImportError('Not opened yet!'))


class AzimuthCompress(th.nn.Module):

    def __init__(self, Na, Nr, Tp, Fsa, Ka, Fc, trainable=True, dtype=th.float32):
        super(AzimuthCompress, self).__init__()
        self.Na = Na
        self.Nr = Nr
        self.Tp = Tp
        self.Fsa = Fsa
        self.Ka = Ka
        self.Fc = Fc
        self.dtype = dtype
        self.azmf = AzimuthMatchedFilter(Nr, Tp, Fsa, Ka, Fc, trainable=trainable, dtype=dtype)

    def forward(self, X):

        raise(ImportError('Not opened yet!'))


class AzimuthCompressLinearFit(th.nn.Module):

    def __init__(self, Na, Nr, Tp, Fsa, Ka, Fc, trainable=True, dtype=th.float32):
        super(AzimuthCompressLinearFit, self).__init__()
        self.Na = Na
        self.Nr = Nr
        self.Tp = Tp
        self.Fsa = Fsa
        self.Ka = Ka
        self.Fc = Fc
        self.dtype = dtype
        self.azmf = AzimuthMatchedFilterLinearFit(Nr, Tp, Fsa, Ka, Fc, trainable=trainable, dtype=dtype)

    def forward(self, X):

        raise(ImportError('Not opened yet!'))
