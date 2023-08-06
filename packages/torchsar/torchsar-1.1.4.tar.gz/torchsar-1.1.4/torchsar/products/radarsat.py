#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : radarsat.py
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
import logging
import numpy as np
from tqdm import tqdm

from torchsar.products.ceos import decfmtfceos
from torchsar.products.utils import splitfmt
from torchsar.products.record import readrcd, readrcd1item
from torchsar.sarcfg.sensor_satellite import SENSOR_SATELLITE

# B: number in binary format
# A: string
# I: char
SarDataFileFileDescriptorRecordRADARSAT = {
    # SAR DATA FILE - FILE DESCRIPTOR RECORD (FIXED SEGMENT)
    'Record sequence number': [(1, 4), '1B4', 0],
    
}

SarDataFileSignalDataRecordRADARSAT = {
    'Record sequence number': [(1, 4), '1B4', 0],
}


def _getdtype_component(fmtrcd, fmtuser):

    raise(ImportError('Not opened yet!'))



def read_radarsat_sar_raw(filepath, sl=1, el=-1, rmbp=False):
    r"""read RADARSAT SAR raw data

    read RADARSAT raw data pulse from line :attr:`sl` to line :attr:`el`. This function call
    function :func:`read_ceos_sar_raw` firstly and do some post-process.


    Parameters
    ----------
    filepath : str
        RADARSAT SAR raw data file path string with format ``.001``, such as ``DAT_01.001``.
    sl : int, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : int, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : bool, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    S : 2d-array
        SAR raw data.

    """

    sensor_name = 'RADARSAT1'
    logging.info("===In read_radarsat_sar_raw...")

    raise(ImportError('Not opened yet!'))
