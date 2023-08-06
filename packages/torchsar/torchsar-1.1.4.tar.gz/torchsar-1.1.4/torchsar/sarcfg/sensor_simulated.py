#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : sensor_simulated.py
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

SENSOR_SIMULATED = {

    'Air1': {
        'Fc': 5.3e9,  # Hz
        'H': 10000,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 2.5e-6,  # Range pulse length in seconds
        'Kr': 20e+12,  # FM rate of radar pulse (Hz/s)
        'Lr': 12,  # antenna length (range) in m
        'La': 3.0,  # antenna length (azimuth) in m
        'PRF': 120.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 60.0e6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [256, 320],
        'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 2 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        # 'Aon': 59.3392 * PI / 180.0,  # off-nadir angle |\
        'Aon': 59.33 * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'Air1',
    },

    'Air2': {
        'Fc': 9.4e9,  # Hz
        'H': 8000,  # height in m
        'V': 200.0,  # velocity in m/s
        'Tp': 1e-6,  # Range pulse length in seconds
        'Kr': 160e+12,  # FM rate of radar pulse (Hz/s)
        'Lr': 12,  # antenna length (range) in m
        'La': 3.0,  # antenna length (azimuth) in m
        'PRF': 90.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 96e6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [128, 128],
        'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 0.5 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 58.7 * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'Air2',
    },

    'Air3': {
        'Fc': 9.4e9,  # Hz
        'H': 8000,  # height in m
        'V': 200.0,  # velocity in m/s
        'Tp': 1e-6,  # Range pulse length in seconds
        'Kr': 160e+12,  # FM rate of radar pulse (Hz/s)
        'Lr': 12,  # antenna length (range) in m
        'La': 3,  # antenna length (azimuth) in m
        'PRF': 300.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 192.e6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [256, 256],
        # 'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        'As': 0. * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 67.7 * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'Air3',
    },

    'Air4': {
        'Fc': 9.4e9,  # Hz
        'H': 8000,  # height in m
        'V': 200.0,  # velocity in m/s
        'Tp': 1e-6,  # Range pulse length in seconds
        'Kr': 80e+12,  # FM rate of radar pulse (Hz/s)
        'Lr': 12,  # antenna length (range) in m
        'La': 6,  # antenna length (azimuth) in m
        'PRF': 100.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 96.e6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [64, 64],
        # 'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        'As': 0. * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 67.7 * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'Air4',
    },

    'Air5': {
        'Fc': 9.6e9,  # Hz
        'H': 8000,  # height in m
        'V': 200.0,  # velocity in m/s
        'Tp':1e-6,  # Range pulse length in seconds
        'Kr': 80e+12,  # FM rate of radar pulse (Hz/s)
        'Lr': 4,  # antenna length (range) in m
        'La': 4,  # antenna length (azimuth) in m
        'PRF': 124.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 96.e6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [128, 128],
        # 'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        'As': 0. * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 73.0 * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'Air5',
    },

    'Air6': {
        'Fc': 9.6e9,  # Hz
        'H': 8000,  # height in m
        'V': 200.0,  # velocity in m/s
        'Tp':1e-6,  # Range pulse length in seconds
        'Kr': 80e+12,  # FM rate of radar pulse (Hz/s)
        'Lr': 4,  # antenna length (range) in m
        'La': 4,  # antenna length (azimuth) in m
        'PRF': 62.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 48.e6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [64, 64],
        # 'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        'As': 0. * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 73.0 * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'Air6',
    },

    'Sim1': {
        'Fc': 5.3e9,  # Hz
        'H': 1000,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 2.5e-6,  # Range pulse length in seconds
        'Kr': 40.e+12,  # FM rate of radar pulse (Hz/s)
        'Lr': 2,  # antenna length (range) in m
        'La': 3,  # antenna length (azimuth) in m
        'PRF': 180.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 120.e6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [512, 512],
        # 'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        'As': 0. * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 67.7 * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'Sim1',
    },

    'Sim2': {
        'Fc': 5.3e9,  # Hz
        'H': 1000,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 2.5e-6,  # Range pulse length in seconds
        'Kr': 40.e+12,  # FM rate of radar pulse (Hz/s)
        'Lr': 2,  # antenna length (range) in m
        'La': 3,  # antenna length (azimuth) in m
        'PRF': 180.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 120.e6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [256, 256],
        # 'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        'As': 0. * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 67.7 * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'Sim2',
    },

    'Sim3': {
        'Fc': 5.3e9,  # Hz
        'H': 10000,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 0.5e-6,  # Range pulse length in seconds
        'Kr': 160e+12,  # FM rate of radar pulse (Hz/s)
        'Lr': 2,  # antenna length (range) in m
        'La': 3,  # antenna length (azimuth) in m
        'PRF': 160.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 96.e6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [128, 128],
        # 'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        'As': 0. * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 45. * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'Sim3',
    },

    'Sim4': {
        'Fc': 5.3e9,  # Hz
        'H': 1000,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 0.5e-6,  # Range pulse length in seconds
        'Kr': 160.e+12,  # FM rate of radar pulse (Hz/s)
        'Lr': 2,  # antenna length (range) in m
        'La': 3,  # antenna length (azimuth) in m
        'PRF': 80.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 48.e6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [64, 64],
        # 'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        'As': 0. * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 45. * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'Sim4',
    },

    'Sim5': {
        'Fc': 5.3e9,  # Hz
        'H': 1100,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 0.5e-6,  # Range pulse length in seconds
        'Kr': 80.e+12,  # FM rate of radar pulse (Hz/s)
        'Lr': 2,  # antenna length (range) in m
        'La': 5,  # antenna length (azimuth) in m
        'PRF': 100.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 48.e6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [64, 64],
        # 'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        'As': 0. * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 30. * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'Sim5',
    },

    'Sim6': {
        'Fc': 5.3e9,  # Hz
        'H': 1100,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 0.5e-6,  # Range pulse length in seconds
        'Kr': 80.e+12,  # FM rate of radar pulse (Hz/s)
        'Lr': 2,  # antenna length (range) in m
        'La': 5,  # antenna length (azimuth) in m
        'PRF': 100.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 48.e6,

        'StateVector': None,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        'SceneCenter': None,
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        'SceneArea': None,
        'EchoSize': [32, 32],
        # 'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        'As': 0. * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': None,  # depression angle
        'Aon': 30. * PI / 180.0,  # off-nadir angle |\
        'Aba': None,  # antenna azimuth beamwidth
        'Abr': None,  # antenna range beamwidth
        'Name': 'Sim6',
    },

}
