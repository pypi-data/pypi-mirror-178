#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : matched_filter.py
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
from torch.nn.parameter import Parameter


class RangeMatchedFilter(th.nn.Module):

    def __init__(self, Na, Tp, Fsr, Kr, Fc, trainable=True, dtype=th.float64):
        super(RangeMatchedFilter, self).__init__()
        self.Na = Na
        self.Tp = Tp
        self.dtype = dtype  # filters with float64 is better then float32

        raise(ImportError('Not opened yet!'))

    def forward(self):

        raise(ImportError('Not opened yet!'))


class AzimuthMatchedFilter(th.nn.Module):

    def __init__(self, Nr, Tp, Fsa, Ka, Fc, trainable=True, dtype=th.float32):
        super(AzimuthMatchedFilter, self).__init__()
        self.Nr = Nr
        self.Tp = Tp
        self.dtype = dtype  # filters with float64 is better then float32

        raise(ImportError('Not opened yet!'))

    def forward(self):

        raise(ImportError('Not opened yet!'))


class AzimuthMatchedFilterLinearFit(th.nn.Module):

    def __init__(self, Nr, Tp, Fsa, Ka, Fc, trainable=True, dtype=th.float32):
        super(AzimuthMatchedFilterLinearFit, self).__init__()
        self.Nr = Nr
        self.Tp = Tp
        self.dtype = dtype  # filters with float64 is better then float32

        if type(trainable) is bool:
            trainable = [trainable] * 2

        raise(ImportError('Not opened yet!'))

    def forward(self):

        raise(ImportError('Not opened yet!'))


if __name__ == '__main__':

    pass
