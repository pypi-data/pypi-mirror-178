#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : antenna_pattern.py
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

import torchbox as tb


def antenna_pattern_azimuth(Wl, La, A):

    BWa = 0.886 * Wl / La

    Pa = tb.sinc(0.886 * A / BWa)

    return Pa


if __name__ == '__main__':

    Pa = antenna_pattern_azimuth(0.25, 2, 0.2)
    print(Pa)
