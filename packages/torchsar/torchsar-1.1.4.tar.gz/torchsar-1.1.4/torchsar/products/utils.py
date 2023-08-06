#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : utils.py
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

import re


def getnumber(b):
    r"""obtain number in string or bytes

    obtain number in string/bytes, e.g. b' 123 45 ' --> [123, 45],
    b' 123, 45 ' --> [123, 45] and b'  ' --> []

    Parameters
    ----------
    b : bytes
        bytes string for extracting numbers.

    Returns
    -------
    n : number list or number
        extracted number list, if there only one element, return a number.
    """
    n = [int(i) for i in re.findall(r'\d+', str(b))]
    if len(n) == 1:
        n = n[0]
    return n


def splitfmt(fmt):
    n, F, x = re.findall(r'[0-9]+|[a-z,A-Z]+|[0-9]', fmt)

    return (int(n), F, int(x))


if __name__ == '__main__':

    print(getnumber(b' 1 23'))
    print(getnumber(b' 1,23'))
    print(getnumber(b'  '))

    print(splitfmt('100IU33'))
