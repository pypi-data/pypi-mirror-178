#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : sar_signal.py
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

import torch as th
from torchbox.utils.const import *
from torchbox.dsp.normalsignals import rect


def sar_tran(t, Tp, Kr, Fc, A=1.):

    return A * rect(t / Tp) * th.exp(2j * PI * Fc * t + 1j * PI * Kr * t**2)


def sar_recv(t, tau, Tp, Kr, Fc, A=1.):

    t = t - tau
    return A * rect(t / Tp) * th.exp(2j * PI * Fc * t + 1j * PI * Kr * t**2)


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    from torch.fft import fft, fftshift

    Kr = 40e+12
    Tp = 2.5e-06
    Br = abs(Kr) * Tp

    alpha = 1.24588  # 1.1-1.4
    Fsr = alpha * Br
    # Fc = 5.3e9
    Fc = 0.

    Tsr = 1.2 * Tp
    Nsr = int(Fsr * Tsr)
    t = th.linspace(-Tsr / 2., Tsr / 2, Nsr)
    f = th.linspace(-Fsr / 2., Fsr / 2, Nsr)

    St = sar_tran(t, Tp, Kr, Fc)

    Yt = fftshift(fft(fftshift(St, dim=0), dim=0), dim=0)

    plt.figure(1)
    plt.subplot(221)
    plt.plot(t * 1e6, th.real(St))
    plt.plot(t * 1e6, th.abs(St))
    plt.grid()
    plt.legend({'Real part', 'Amplitude'})
    plt.title('Matched filter')
    plt.xlabel('Time/μs')
    plt.ylabel('Amplitude')
    plt.subplot(222)
    plt.plot(t * 1e6, th.angle(St))
    plt.grid()
    plt.subplot(223)
    plt.plot(f, th.abs(Yt))
    plt.grid()
    plt.subplot(224)
    plt.plot(f, th.angle(Yt))
    plt.grid()
    plt.show()
