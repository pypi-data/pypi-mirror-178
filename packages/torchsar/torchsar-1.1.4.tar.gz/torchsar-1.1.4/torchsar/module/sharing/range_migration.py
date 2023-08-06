#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : range_migration.py
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


class RangeMigrationCorrection(th.nn.Module):

    def __init__(self, Na, Nr, R0, Vr, Fc, Fsa, Fsr, D=None):
        super(RangeMigrationCorrection, self).__init__()
        self.Na = Na
        self.Nr = Nr
        self.R0 = R0
        self.Vr = Vr
        self.Fc = Fc
        self.Fsa = Fsa
        self.Fsr = Fsr

        raise(ImportError('Not opened yet!'))

    def forward(self, X):
        raise(ImportError('Not opened yet!'))


if __name__ == '__main__':

    Na, Nr = 8, 8
    X = th.randn(Na, Nr, 2)
    print(X)

    rcmclayer = RangeMigrationCorrection(Na, Nr)

    X = rcmclayer(X)
    print(X)
