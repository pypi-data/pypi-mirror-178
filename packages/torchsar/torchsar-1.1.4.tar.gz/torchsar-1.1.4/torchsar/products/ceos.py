#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : ceos.py
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
import copy
import struct
import logging
import numpy as np
from tqdm import tqdm

from torchsar.products.utils import getnumber, splitfmt
from torchsar.products.record import readrcd, readrcd1item, printrcd


# B: number in binary format
# A: string
# I: char
SarDataFileFileDescriptorRecordCEOS = {
    # SAR DATA FILE - FILE DESCRIPTOR RECORD (FIXED SEGMENT)
    'Record sequence number': [(1, 4), '1B4', 0],

}

SarDataFileSignalDataRecordCEOS = {
    'Record sequence number': [(1, 4), '1B4', 0],

}

SarDataFileProcessedDataRecordCEOS = {
    'Record sequence number': [(1, 4), '1B4', 0],

}


def decfmtfceos(F, n, x, b, e='<'):
    r"""decode format descriptor of CEOS

    decode format descriptor of CEOS.

    ``'nFx'`` --> decode :attr:`b` x Bytes-by-x Bytes as format :attr:`F` specified,
    and do :attr:`n` times.

    Parameters
    ----------
    F : str
        formation string, ``C`` --> Complex(real, imag), ``F`` --> float, ``B`` --> Bytes, ``A`` --> String, ``I`` --> asicc
    n : int
        amount of elements with formation :attr:`F`
    x : int
        number of Bytes
    b : bytes
        bytes to be decoded
    e : str, optional
        endian, ``'<'`` --> little, ``'>'`` -- > big (the default is '<', which means little endian)

    Returns
    -------
    list
        decoded result list.
    """

    raise(ImportError('Not opened yet!'))


def _getdtype_component(fmtrcd, fmtuser):

    raise(ImportError('Not opened yet!'))


def read_ceos_sar_raw(filepath, sl=1, el=-1, rmbp=False):
    r"""read CEOS SAR raw data

    read CEOS SAR raw data pulse from line :attr:`sl` to line :attr:`el`.

    Parameters
    ----------
    filepath : str
        SAR raw data file path string, for ERS1/2 --> ``*.raw`` for RADARSAT --> ``DAT_01.001``
    sl : int, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : int, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : bool, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    S : 2d-array


    """

    logging.info("===In read_ceos_sar_raw...")

    raise(ImportError('Not opened yet!'))


def read_ceos_sar_slc(filepath, sl=1, el=-1, rmbp=False):
    r"""read CEOS SAR slc data

    read CEOS SAR slc data from line :attr:`sl` to line :attr:`el`.

    Parameters
    ----------
    filepath : str
        SAR slc data file path string, for ERS1/2 --> ``*.D`` for RADARSAT --> ``DAT_01.001``
    sl : int, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : int, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : bool, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    S : 2d-array
       Processed SLC SAR data matrix.

    """

    logging.info("===In read_ceos_sar_slc...")

    raise(ImportError('Not opened yet!'))



if __name__ == '__main__':
    from torchsar import decfmtfers
    disk = '/mnt/d/'
    filename = 'E2_84686_STD_L0_F203'
    # filename = 'E2_84699_STD_L0_F303'
    # filepath = disk + 'DataSets/sar/ERS/data/' + filename + '/' + filename + '.000.ldr'
    filepath = disk + 'DataSets/sar/ERS/data/' + \
        filename + '/' + filename + '.000.raw'

    endian = '>'

    D = copy.deepcopy(SarDataFileFileDescriptorRecordCEOS)
    # D = copy.deepcopy(SarDataFileSignalDataRecordERS)

    offset = 0
    # offset = 11644

    readrcd(filepath, decfmtfers, D, offset=offset, endian='>')

    print("===============")
    printrcd(D)
