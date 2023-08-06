#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : sensor_satellite.py
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

SENSOR_SATELLITE = {

    'GF3': {
        'Fc': 5.400012e9,  # Hz
        'H': 755000,  # height in m
        'V': 7570.67,  # velocity in m/s
        'Tp': 45.00e-6,  # Range pulse length in seconds
        'Kr': 13.3333e11,  # FM rate of radar pulse (Hz/s)
        'Lr': 1,  # antenna length (range) in m
        'La': 10.0,  # antenna length (azimuth) in m
        'PRF': 1413.8530,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 66.66e+6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [32768, 9288],
        'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 30.62 * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'GF3',
    },

    'ERS2': {
        'Fc': 5.30e+9,  # Hz
        'H': 780000,  # height in m
        'V': 7125.0,  # velocity in m/s
        'Tp': 37.12e-6,  # Range pulse length in seconds
        'Kr': 4.18989015e+11,  # FM rate of radar pulse (Hz/s)
        'Lr': 1,  # antenna length (range) in m
        'La': 10.0,  # antenna length (azimuth) in m
        'PRF': 1679.9023438,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 18.9599991e+6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [32768, 5616],
        'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 18.35 * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'ERS2',
    },

    'RADARSAT1': {
        'Fc': 5.30e+9,  # Hz
        'H': 793000,  # height in m
        'V': 7062.0,  # velocity in m/s
        'Tp': 41.75e-6,  # Range pulse length in seconds
        'Kr': -7.2135e+11,  # FM rate of radar pulse (Hz/s)
        'Lr': 1.5,  # antenna length (range) in m
        'La': 15.0,  # antenna length (azimuth) in m
        'PRF': 1256.98,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 32.32e+6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [19438, 9288],
        'As': -1.53 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 30.64 * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'RADARSAT1',
    },

    'ALOS': {
        'Fc': 1.27e+9,  # Hz
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
        'Ad': None,  # depression angle
        'Aon': 34.3 * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'Space3',
    },

}
