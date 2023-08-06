#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : focusing.py
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
from torch.nn.parameter import Parameter
from torchsar.autofocus.focusing import focus


class AutoFocus(th.nn.Module):

    def __init__(self, Na, Nr, pa=None, pr=None, ftshift=False, trainable=True):
        super(AutoFocus, self).__init__()

        self.Na = Na
        self.Nr = Nr
        self.ftshift = ftshift

        if Na is not None:
            if pa is None:
                pa = th.zeros(1, Na)
            self.pa = Parameter(pa, requires_grad=trainable)

        if Nr is not None:
            if pr is None:
                pr = th.zeros(1, Nr)
            self.pr = Parameter(pr, requires_grad=trainable)

    def forward(self, X, isfft=True):
        X = focus(X, pa=self.pa, pr=self.pr, isfft=isfft, ftshift=self.ftshift)

        return X
