#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : data.py
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

import os
import sys
import numpy as np
import torch as th
import pickle as pkl
from torchbox import savemat, saveh5, loadmat, loadh5


def sarstore(sardata, params, file):
    """Read SAR file

    Store SAR data and platform to a file (``.pkl`` , ``.h5`` or ``.mat``)

    Args:
        sardata (dict): The SAR raw data.

        params (dict): The SAR platform for obtain the SAR data.
        file (str): Description

    Returns:
        file (str): The file path for storing SAR data and platform
    """

    if np.iscomplex(sardata['raw']).any():
        sardata['raw'] = np.stack((sardata['raw'].real, sardata['raw'].imag), dim=-1)

    folder, filename = os.path.split(file)
    _, ext = os.path.splitext(filename)
    if os.path.exists(folder) is False:
        os.makedirs(folder)

    if ext == '.pkl':
        f = open(file, 'wb')
        pkl.dump(sardata, f, 0)
        pkl.dump(params, f, 0)
        f.close()
    elif ext == '.mat':
        savemat(file, {'sardata': sardata, 'params': params})
    elif ext in ['.hdf5', '.h5']:
        saveh5(file, {'sardata': sardata, 'params': params})

    return 0


def sarread(file):
    """Read SAR file

    Read SAR file (``.pkl`` or ``.mat``) and returns SAR data and platform

    Args:
        file (str): SAR data (contains platform) file path.

    Returns:
        sardata (Instance SarData): The SAR raw data.

        params (Instance of SarPlat): The SAR platform for obtain the SAR data.
    """

    filename, EXT = os.path.splitext(file)

    if EXT == '.pkl':
        f = open(file, 'rb')
        # for python2
        if sys.version_info < (3, 1):
            sardata = pkl.load(f)
            params = pkl.load(f)
        # for python3
        else:
            sardata = pkl.load(f, encoding='latin1')
            params = pkl.load(f, encoding='latin1')
        f.close()
    elif EXT == '.mat':
        data = loadmat(file)
        sardata = data['sardata']
        params = data['params']
        del data

    elif EXT in ['.hdf5', '.h5']:
        data = loadh5(file)
        sardata = data['sardata']
        params = data['params']
        del data
    else:
        raise(TypeError("Not supported! Only support: (pkl, mat, hdf5)!"))

    return sardata, params


def format_data(X, modefrom='chnl_last', modeto='chnl_first'):
    """format data

    Format data to chanel first or chanel last.

    Args:
        X (numpy array): data to be formated
        modefrom (str, optional): chnl_last  --> chanel last; chnl_first  --> chanel first
            (the default is 'chnl_last', which chanel first)
        modeto (str, optional): chnl_last  --> chanel last; chnl_first  --> chanel first
            (the default is 'chnl_last', which chanel first)

    Returns:
        X (numpy array): Formated data

    Raises:
        TypeError: X should be a 3 or 4 dimention array!
        ValueError: Unknown mode of modefrom or modeto
    """

    if modefrom == modeto:
        return X
    if X.dim() == 4:
        s = 1
        m = 2
        e = 3
    elif X.dim() == 3:
        s = 0
        m = 1
        e = 2
    else:
        raise TypeError("X should be a 3 or 4 dimention array!")
    if modefrom == 'chnl_last':
        if modeto == 'chnl_first':
            X = th.transpose(X, s, e)  # N H W C --> N C W H
            X = th.transpose(X, m, e)  # N C W H --> N C H W
        else:
            raise ValueError("Unknown mode of: ", modeto)
    elif modefrom == 'chnl_first':
        if modeto == 'chnl_last':
            X = th.transpose(X, s, e)  # N C H W --> N W H C
            X = th.transpose(X, s, m)  # N W H C --> N H W C
    return X
