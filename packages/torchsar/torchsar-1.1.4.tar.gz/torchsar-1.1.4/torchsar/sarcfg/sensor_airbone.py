#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : sensor_airbone.py
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

from torchbox.utils.const import *

SENSOR_AIRBONE = {

    'AIRSAR-P': {
        'Fc': 0.45e9,  # Hz
        'H': 8000,  # height in m
        'V': 215.0,  # velocity in m/s
        'Tp': 5e-6,  # Range pulse length in seconds
        'Kr': 8e+12,  # FM rate of radar pulse (Hz/s)
        'Lr': 12,  # antenna length (range) in m
        'La': 15.0,  # antenna length (azimuth) in m
        'PRF': 1800.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 48.e6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [2048, 2048],
        'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 0.05 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 23.4 * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'Space3',
    },

    'UAVSAR': {
        'Fc': 1.27e9,  # Hz
        'H': 800000,  # height in m
        'V': 7153.0,  # velocity in m/s
        'Tp': 27e-6,  # Range pulse length in seconds
        'Kr': -28.e6 / 27.0e-6,  # FM rate of radar pulse (Hz/s)
        'Lr': 2.9,  # antenna length (range) in m
        'La': 8.9,  # antenna length (azimuth) in m
        'PRF': 1912.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 32.e6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        # 'EchoSize': [512, 1024],
        'EchoSize': [35345, 12040],
        'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 0.05 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 34.3 * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'Space3',
    },

    'MSTAR': {
        'Fc': 9.60e9,  # Hz
        'H': 1480.75,  # height in m
        'V': 39.457031,  # velocity in m/s
        'Tp': 0.1e-6,  # Range pulse length in seconds
        'Kr': 591.0e6 / 0.1e-6,  # FM rate of radar pulse (Hz/s)
        'Lr': 0.6,  # antenna length (range) in m
        'La': 0.8,  # antenna length (azimuth) in m
        'PRF': 180.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 712.e6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        # 'EchoSize': [512, 1024],
        'EchoSize': [128, 128],
        'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 0.05 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 17. * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'MSTAR',
    },

}
