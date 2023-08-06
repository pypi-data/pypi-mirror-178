#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : record.py
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

import numpy as np
import re
from .utils import splitfmt


def readrcd(filepath, decfmtf, D, offset=0, endian='>'):
    """read file record

    read record information from a file. see :func:`read_ers_sar_raw` for reading ERS SAR raw data.

    Parameters
    ----------
    filepath : str
        file path string
    decfmtf : function
        format decoding function. see :func:`decfmtfers` for example.
    D : dict
        record descriptor dict, each value will be rewrited after reading.
    offset : int, optional
        record offset, read from the offset-th Byte (the default is 0)
    endian : str, optional
        endian, ``'<'`` --> little, ``'>'`` -- > big (the default is '<', which means little endian)

    Returns
    -------
    state : number
        reading status. 0 --> OK and done; 1 --> no such file; 2 --> bad record

    """

    state = 0

    raise(ImportError('Not opened yet!'))



def readrcd1item(filepath, decfmtf, adrfmt, offset=0, endian='>'):
    """read one file record item

    read one record item information from a file. see :func:`read_ceos_sar_raw` for reading ERS SAR raw data.

    Parameters
    ----------
    filepath : str
        file path string
    decfmtf : function
        format decoding function. see :func:`decfmtfers` for example.
    adrfmt : tuple
        address and formation of one record item, a tuple with two
        elements: ``(adr, fmt)``, where, ``adr`` = (start address, end address) is a tuple and specifies
        the address (unit Bytes), ``fmt`` is the formation string.
    offset : int, optional
        record address offset, begin from the offset-th Byte (the default is 0)
    endian : str, optional
        endian, ``'<'`` --> little, ``'>'`` -- > big (the default is '<', which means little endian)

    Returns
    -------
    v : {}
        readed record item value.

    """

    raise(ImportError('Not opened yet!'))



def printrcd(D):
    """print record

    print record in ascend address order.

    Parameters
    ----------
    D : dict
        descriptor dict
    """

    for k, v in sorted(D.items(), key=lambda item: item[1][0]):
        print(k, v)
