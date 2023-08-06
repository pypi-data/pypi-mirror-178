#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : alos.py
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


LeaderFileImportantImagingParametersRecordALOS = {
    'Scene identifier': [(720 + 21, 720 + 52), '1A32', 0],
    'Ellipsoid designator = "GRS80bbbbbbbbbbb":Fixed': [(720 + 165, 720 + 180), '1A16', 0],
    'Mass of earth (10^24kg)': [(720 + 213, 720 + 228), '1F16', 0],

}

# B: number in binary format
# A: string
# I: char
SarDataFileFileDescriptorRecordALOSPALSAR = {
    # SAR DATA FILE - FILE DESCRIPTOR RECORD (FIXED SEGMENT)
    'Record sequence number': [(1, 4), '1B4', 0],

}

SarDataFileSignalDataRecordALOSPALSAR = {  # level1.0
    'Record sequence number': [(1, 4), '1B4', 0],

}


# B: number in binary format
# A: string
# I: char
SarImageFileFileDescriptorRecordALOSPALSAR = {
    # SAR DATA FILE - FILE DESCRIPTOR RECORD (FIXED SEGMENT)
    'Record sequence number': [(1, 4), '1B4', 0],
}

SarImageFileSignalDataRecordALOSPALSAR = {  # level1.1
    'Record sequence number': [(1, 4), '1B4', 0],
}

SarImageFileProcessedDataRecordALOSPALSAR = {  # level1.5
    'Record sequence number': [(1, 4), '1B4', 0],
}


def _getdtype_component(fmtrcd, fmtuser):
    raise(ImportError('Not opened yet!'))


def get_alos_palsar_plat_position(D):
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

    logging.info("===In get_alos_palsar_plat_position...")

    P = []

    P.append(D['1st data point position vector as (X, Y, Z) co-ordinates for spaceborne sensor platform in a reference system (X) (meters)'][2][0])
    P.append(D['1st data point position vector as (X, Y, Z) co-ordinates for spaceborne sensor platform in a reference system (Y) (meters)'][2][0])
    P.append(D['1st data point position vector as (X, Y, Z) co-ordinates for spaceborne sensor platform in a reference system (Z) (meters)'][2][0])
    P.append(D['1st data point velocity vector (Vx, Vy, Vz) in a reference system (Vx) [m/sec]'][2][0])
    P.append(D['1st data point velocity vector (Vx, Vy, Vz) in a reference system (Vy) [m/sec]'][2][0])
    P.append(D['1st data point velocity vector (Vx, Vy, Vz) in a reference system (Vz) [m/sec]'][2][0])
    P = P + D['2nd, 3rd, ... data point position & velocity vectors'][2]

    nPlatformPositionPoints = D['Number of data points'][2][0]
    P = np.array(P)
    P = np.reshape(P, (nPlatformPositionPoints, 6))

    logging.info("===Out get_alos_palsar_plat_position.")
    return P


def get_alos_palsar_attitude(D):
    """get attitude data

    return a numpy array
        1st: Pitch Roll Yaw PitchRate RollRate YawRate
        2st: Pitch Roll Yaw PitchRate RollRate YawRate
           :
        nst: Pitch Roll Yaw PitchRate RollRate YawRate

    Parameters
    ----------
    D : dict
        LeaderFileImportantImagingParametersRecordALOS dict
    """

    logging.info("===In get_alos_palsar_attitude...")

    A = []
    A.append(D['1st Pitch (degrees)'][2][0])
    A.append(D['1st Roll (degrees)'][2][0])
    A.append(D['1st Yaw (degrees)'][2][0])
    A.append(D['1st Pitch rate (degrees/sec)'][2][0])
    A.append(D['1st Roll rate (degrees/sec)'][2][0])
    A.append(D['1st Yaw rate (degrees/sec)'][2][0])
    A = A + D['2nd, 3rd, ... attitude data points'][2]

    nAttitudeDataPoints = D['Number of attitude data points="bb22", "bb62"'][2][0]
    A = np.array(A)
    A = np.reshape(A, (nAttitudeDataPoints, 6))

    logging.info("===Out get_alos_palsar_attitude.")

    return A


def read_alos_palsar_ldr_iip(ledfile, verbose=False):
    r"""Read important imaging parameters from leader file

    Read important imaging parameters from leader file.

    For example, ``LED-ALPSRP050500980-H1.0__A``

    Parameters
    ----------
    ledfile : str
        Leader file path string.
    """

    logging.info("===In read_alos_palsar_ldr_iip...")
    raise(ImportError('Not opened yet!'))


def read_alos_palsar_raw(rawfile, ledfile, sl=1, el=-1, rmbp=False):
    r"""read ALOS PALSAR raw data

    read ALOS PALSAR raw data pulse from line :attr:`sl` to line :attr:`el`. This function call
    function :func:`read_ceos_sar_raw` firstly and do some post-process.


    Parameters
    ----------
    rawfile : str
        ALOS PALSAR raw data file path string, ---> ``IMG*.0__A``, e.g. ``IMG-HH-ALPSRP050500980-H1.0__A``
    ledfile : str
        ALOS PALSAR leader file path string, ---> ``LED*.0__A``, e.g. ``LED-ALPSRP050500980-H1.0__A``
    sl : int, optional
        start line (azimuth) (the default is 1, which means the first line)
    el : int, optional
        end line (azimuth) (the default is -1, which means the last line)
    rmbp : bool, optional
        If you want to remove the padded border pixels, set :attr:`rmbp` to ``True``, else set to ``False`` (the default is ``False``).

    Returns
    -------
    Sr : 2d-array
       SAR raw signal data matrix.

    Pd : dict
       Parameter dictionary.

    """

    logging.info("===In read_alos_palsar_raw...")

    raise(ImportError('Not opened yet!'))



def read_alos_palsar_slc(filepath, sl=1, el=-1, rmbp=False):
    r"""read ALOS PALSAR SLC data

    read ALOS PALSAR SLC data pulse from line :attr:`sl` to line :attr:`el`. This function call
    function :func:`read_ceos_sar_slc` firstly.


    Parameters
    ----------
    filepath : str
        ALOS PALSAR raw data file path string, for ALOSPALSAR --> ``IMG*.1__A``
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

    logging.info("===In read_alos_palsar_slc...")

    raise(ImportError('Not opened yet!'))

