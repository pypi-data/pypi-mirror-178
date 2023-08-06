#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : ers.py
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
import torchsar as ts
import torchbox as tb
from torchsar.products.ceos import decfmtfceos
from torchsar.products.utils import splitfmt
from torchsar.products.record import readrcd, readrcd1item, printrcd
from torchsar.sarcfg.sensor_satellite import SENSOR_SATELLITE


LeaderFileImportantImagingParametersRecordERS = {
    'Radar frequency (GHz)': [(720 + 493, 720 + 500), '1F8', 0],
    'Radar wavelength (meters)': [(720 + 501, 720 + 516), '1F16', 0],

}


# B: number in binary format
# A: string
# I: char
SarDataFileFileDescriptorRecordERS = {
    # SAR DATA FILE - FILE DESCRIPTOR RECORD (FIXED SEGMENT)
    'Record sequence number': [(1, 4), '1B4', 0],

}

SarDataFileSignalDataRecordERS = {
    'Record sequence number': [(1, 4), '1B4', 0],

}

SarDataFileProcessedDataRecordERS = {
    'Record sequence number': [(1, 4), '1B4', 0],

}


def _getdtype_component(fmtrcd, fmtuser):

    raise(ImportError('Not opened yet!'))



def get_ers_sar_plat_position(D):
    """get platform position data

    return a numpy array
        1st: X Y Z Vx Vy Vz
        2st: X Y Z Vx Vy Vz
           :
        nst: X Y Z Vx Vy Vz

    Parameters
    ----------
    D : dict
        LeaderFileImportantImagingParametersRecordALOS dict
    """

    logging.info("===In get_ers_sar_platform_position...")

    raise(ImportError('Not opened yet!'))


def read_ers_sar_ldr_iip(filepath, verbose=False):
    r"""Read important imaging parameters from leader file

    Read important imaging parameters from leader file.

    Parameters
    ----------
    filepath : str
        Leader file path string.
    """

    logging.info("===In read_ers_sar_ldr_iip...")

    raise(ImportError('Not opened yet!'))


def read_ers_sar_raw(rawfile, ledfile, sl=1, el=-1, rmbp=False):
    r"""read ERS SAR raw data

    read ERS1/2 SAR raw data pulse from line :attr:`sl` to line :attr:`el`.


    Parameters
    ----------
    rawfile : str
        ERS SAR raw data file path string, for ERS1/2 --> ``*.raw``
        e.g. ``E2_81988_STD_L0_F327.000.raw``
    ledfile : str
        ERS SAR leader file path string, ---> ``*.ldr``, e.g. ``E2_81988_STD_L0_F327.000.ldr``
    sl : int, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : int, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : bool, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    S : 2d-array
       SAR raw signal data matrix.

    Pd : dict
       Parameter dictionary.

    """

    logging.info("===In read_ers_sar_raw...")

    raise(ImportError('Not opened yet!'))


def read_ers_sar_slc(filepath, sl=1, el=-1, rmbp=False):
    r"""read ERS SAR SLC data

    read ERS1/2 SAR SLC data pulse from line :attr:`sl` to line :attr:`el`.


    Parameters
    ----------
    filepath : str
        ERS SAR raw data file path string, for ERS1/2 --> ``*.raw``
    sl : int, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : int, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : bool, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    S : 2d-array
       SAR SLC data matrix.

    """

    logging.info("===In read_ers_sar_slc...")

    raise(ImportError('Not opened yet!'))

