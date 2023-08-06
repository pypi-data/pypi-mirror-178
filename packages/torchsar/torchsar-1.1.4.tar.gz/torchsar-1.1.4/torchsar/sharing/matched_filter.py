#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : matched_filter.py
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
# import numexpr as ne
from torchbox.dsp.ffts import fft, fftfreq, padfft
from torchbox.utils.const import *
from torchbox.base.mathops import nextpow2
from torchbox.dsp.normalsignals import rect


def chirp_mf_td(K, Tp, Fs, Fc=0., Ns=None, mod='conv', scale=False, device='cpu'):
    """Generates matched filter of chirp signal in time domain

    Generates matched filter of chirp signal in time domain.

    Parameters
    ----------
    K : int
        The chirp rate.
    Tp : float
        The pulse width.
    Fs : float
        The sampling rate.
    Fc : float, optional
        The center frequency.
    Ns : int or None, optional
        The number of samples.
    mod : str, optional
        The mode of filter, ``'conv'`` or ``'corr'``
    scale : bool, optional
        Whether to scale the amplitude of the filter.
    device : str, optional
        Specifies the device to be used for computing.

    Returns
    -------
    tensor
        The matched filter tensor.

    Examples
    --------

    Do Pulse Compression with time/frequency domain filters.

    .. image:: ./_static/DemoPulseCompression.png
       :scale: 100 %
       :align: center

    The results shown in the above figure can be obtained by the following codes.

    ::

        #!/usr/bin/env python
        # -*- coding: utf-8 -*-
        # @Date    : 2019-02-18 10:14:12
        # @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
        # @Link    : http://iridescent.ink
        # @Version : $1.0$
        import torch as th
        import torchbox as tb
        import torchsar as ts
        import matplotlib.pyplot as plt

        from torchbox.utils.const import *
        from torchbox.dsp.ffts import fft, ifft, fftfreq

        mftdmod = 'conv'
        mffdmod = 'way1'
        ftshift = True

        # ===Generate tansmit= ted and recieved signals
        # ---Setting parameters
        R = [1.e3, 2.e3, 3.e3]
        G = [0.5, 1.0, 0.8]

        EPS = 2.2e-32
        K = 4.1e+11
        Tp = 37.0e-06
        B = abs(K) * Tp

        alp = 1.24588  # 1.1-1.4
        Fs = alp * B
        Fc = 5.3e9
        Fc = 0.

        Koff = 0.
        Koff = 1.e10
        Fcoff = 0.
        # Fcoff = 1.e8

        Ts = 2.1 * Tp
        Ns = round(Fs * Ts)
        Nh = round(Fs * Tp)
        t = th.linspace(-Ts / 2., Ts / 2, Ns)
        f = fftfreq(Ns, Fs, norm=False, shift=ftshift)

        N = Ns + Nh - 1
        Nfft = 2**tb.nextpow2(N)

        # ---Transmitted signal
        St = ts.chirp_tran(t, Tp, K, Fc, a=1.)

        # ---Recieved signal
        Sr = ts.chirp_recv(t, Tp, K, Fc, a=1., g=G, r=R)

        # ---
        chirp = ts.Chirp(Tp=Tp, K=K, Fc=Fc, a=1.)

        St = chirp.tran(t)
        Sr = chirp.recv(t, g=G, r=R)


        # ---Frequency domain
        Yt = fft(St, dim=0, shift=ftshift)
        Yr = fft(Sr, dim=0, shift=ftshift)

        fontsize = 12
        fonttype = 'Times New Roman'
        fontdict = {'family': fonttype, 'size': fontsize}

        # ---Plot signals
        plt.figure(figsize=(10, 8))
        plt.subplot(221)
        plt.plot(t * 1e6, th.real(St))
        plt.grid()
        plt.title('Real part', fontdict=fontdict)
        plt.xlabel(r'Time/$\mu s$', fontdict=fontdict)
        plt.ylabel('Amplitude', fontdict=fontdict)
        plt.xticks(fontproperties=fonttype, size=fontsize)
        plt.yticks(fontproperties=fonttype, size=fontsize)
        plt.subplot(222)
        plt.plot(t * 1e6, th.imag(St))
        plt.grid()
        plt.title('Imaginary part', fontdict=fontdict)
        plt.xlabel(r'Time/$\mu s$', fontdict=fontdict)
        plt.ylabel('Amplitude', fontdict=fontdict)
        plt.xticks(fontproperties=fonttype, size=fontsize)
        plt.yticks(fontproperties=fonttype, size=fontsize)
        plt.subplot(223)
        plt.plot(f, th.abs(Yt))
        plt.grid()
        plt.title('Spectrum', fontdict=fontdict)
        plt.xlabel('Frequency/Hz', fontdict=fontdict)
        plt.ylabel('Amplitude', fontdict=fontdict)
        plt.xticks(fontproperties=fonttype, size=fontsize)
        plt.yticks(fontproperties=fonttype, size=fontsize)
        plt.subplot(224)
        plt.plot(f, th.angle(Yt))
        plt.grid()
        plt.title('Spectrum', fontdict=fontdict)
        plt.xlabel('Frequency/Hz', fontdict=fontdict)
        plt.ylabel('Phase', fontdict=fontdict)
        plt.xticks(fontproperties=fonttype, size=fontsize)
        plt.yticks(fontproperties=fonttype, size=fontsize)
        plt.subplots_adjust(left=0.08, bottom=0.06, right=0.98, top=0.96, wspace=0.19, hspace=0.25)

        plt.show()

        print(th.sum(t), th.sum(St), th.sum(f))


        plt.figure(figsize=(10, 8))
        plt.subplot(221)
        plt.plot(t * 1e6, th.real(Sr))
        plt.grid()
        plt.title('Real part', fontdict=fontdict)
        plt.xlabel(r'Time/$\mu s$', fontdict=fontdict)
        plt.ylabel('Amplitude', fontdict=fontdict)
        plt.subplot(222)
        plt.plot(t * 1e6, th.imag(Sr))
        plt.grid()
        plt.title('Imaginary part', fontdict=fontdict)
        plt.xlabel(r'Time/$\mu s$', fontdict=fontdict)
        plt.ylabel('Amplitude', fontdict=fontdict)
        plt.subplot(223)
        plt.plot(f, th.abs(Yr))
        plt.grid()
        plt.title('Spectrum', fontdict=fontdict)
        plt.xlabel('Frequency/Hz', fontdict=fontdict)
        plt.ylabel('Amplitude', fontdict=fontdict)
        plt.subplot(224)
        plt.plot(f, th.angle(Yr))
        plt.grid()
        plt.title('Spectrum', fontdict=fontdict)
        plt.xlabel('Frequency/Hz', fontdict=fontdict)
        plt.ylabel('Phase/rad', fontdict=fontdict)
        plt.subplots_adjust(left=0.08, bottom=0.06, right=0.98, top=0.96, wspace=0.19, hspace=0.25)

        plt.show()


        # ===Matched filtering/Pulse compression in time domain

        # ---Matched filtering in time domain
        Sm, tm = ts.chirp_mf_td(K + Koff, Tp, Fs, Fc=Fc + Fcoff, Ns=None, mod=mftdmod)

        if mftdmod in ['conv', 'Conv']:
            # S1 = th.convolve(Sr, Sm, mode='same')
            # S1 = ts.conv1(Sr, Sm, shape='same')
            S1 = tb.fftconv1(Sr, Sm, shape='same')

        if mftdmod in ['corr', 'Corr']:
            # S1 = th.correlate(Sr, Sm, mode='same')
            # S1 = ts.corr1(Sr, Sm, shape='same')
            S1 = tb.fftcorr1(Sr, Sm, shape='same')

        # ===Matched filtering/Pulse compression in frequency domain

        # ---Matched filter in frequency domain
        # ~~~Method 1-4
        H, f = ts.chirp_mf_fd(K + Koff, Tp, Fs, Fc=Fc + Fcoff, Nfft=Nfft, mod=mffdmod, win=None, ftshift=ftshift)

        print(H.shape, t.shape, Sm.shape, "=======")

        # ---Tansform the recieved signal to frequency domain
        Yr = fft(tb.padfft(Sr, Nfft, 0, ftshift), Nfft, dim=0, shift=ftshift)

        # ---Matched filtering/Pulse compression
        Y = Yr * H

        # ---Tansform back to time domain
        S2 = ifft(Y, Nfft, dim=0, shift=ftshift)

        S2 = ts.mfpc_throwaway(S2, Ns, Nh, 0, mffdmod, ftshift)


        print(th.sum(th.abs(S1 - S2)))
        print(th.sum(th.abs(S1 - S2)))
        print(th.argmax(th.abs(S1)), th.argmax(th.abs(S2)))


        plt.figure(figsize=(12, 8))
        plt.subplot(421)
        plt.plot(t * 1e6, th.real(St), '-', linewidth=1)
        plt.plot(t * 1e6, th.abs(St), '--', linewidth=2)
        plt.grid()
        plt.legend(('Real part', 'Amplitude'))
        plt.title('Transmitted', fontdict=fontdict)
        plt.xlabel(r'Time/$\mu s$', fontdict=fontdict)
        plt.ylabel('Amplitude', fontdict=fontdict)
        plt.subplot(422)
        plt.plot(t * 1e6, th.real(Sr), '-', linewidth=1)
        plt.plot(t * 1e6, th.abs(Sr), '--', linewidth=2)
        plt.grid()
        plt.legend(('Real part', 'Amplitude'))
        plt.title('Recieved', fontdict=fontdict)
        plt.xlabel(r'Time/$\mu s$', fontdict=fontdict)
        plt.ylabel('Amplitude', fontdict=fontdict)
        plt.subplot(423)
        plt.plot(tm * 1e6, th.real(Sm), '-', linewidth=1)
        plt.plot(tm * 1e6, th.abs(Sm), '--', linewidth=2)
        plt.grid()
        plt.legend(('Real part', 'Amplitude'))
        plt.title('Filter (time domain)', fontdict=fontdict)
        plt.xlabel(r'Time/$\mu s$', fontdict=fontdict)
        plt.ylabel('Amplitude', fontdict=fontdict)
        plt.subplot(424)
        plt.plot(f, th.real(H), '-', linewidth=1)
        plt.plot(f, th.abs(H), '--', linewidth=2)
        plt.grid()
        plt.legend(('Real part', 'Amplitude'))
        plt.title('Filter (frequency domain,' + mffdmod + ')', fontdict=fontdict)
        plt.xlabel('Frequency/Hz', fontdict=fontdict)
        plt.ylabel('Amplitude', fontdict=fontdict)
        plt.subplot(425)
        plt.plot(t * 1e6, th.abs(S1))
        plt.grid()
        plt.title('Matched filtered with time domain filter', fontdict=fontdict)
        plt.xlabel(r'Time/$\mu s$', fontdict=fontdict)
        plt.ylabel('Amplitude', fontdict=fontdict)
        plt.subplot(426)
        plt.plot(t * 1e6, th.abs(S2))
        plt.grid()
        plt.title('Matched filtered with frequency domain filter', fontdict=fontdict)
        plt.xlabel(r'Time/$\mu s$', fontdict=fontdict)
        plt.ylabel('Amplitude', fontdict=fontdict)
        plt.subplot(427)
        plt.plot(t * 1e6, th.angle(S1))
        plt.grid()
        plt.title('Matched filtered with time domain filter', fontdict=fontdict)
        plt.xlabel(r'Time/${\mu s}$', fontdict=fontdict)
        plt.ylabel('Phase/rad', fontdict=fontdict)
        plt.subplot(428)
        plt.plot(t * 1e6, th.angle(S2))
        plt.grid()
        plt.title('Matched filtered with frequency domain filter', fontdict=fontdict)
        plt.xlabel(r'Time/${\mu s}$', fontdict=fontdict)
        plt.ylabel('Phase/rad', fontdict=fontdict)
        plt.subplots_adjust(left=0.06, bottom=0.06, right=0.99, top=0.96, wspace=0.14, hspace=0.60)
        plt.savefig('PulseCompressionDemoThreeTargetsKoff' + str(Koff) + '.pdf')

        plt.show()


    """
    tc = -Fc / K
    if Ns is None:
        Ns = int(round(Fs * Tp))
        t = th.linspace(-Tp / 2., Tp / 2., Ns).to(device)
    else:
        Ts = Ns / Fs
        t = th.linspace(-Ts / 2., Ts / 2., Ns).to(device)
    raise(ImportError('Not opened yet!'))



def chirp_mf_fd(K, Tp, Fs, Fc=0., Nfft=None, mod='way1', win=None, ftshift=False, scale=False, device='cpu'):
    """Summary

    Parameters
    ----------
    K : int
        The chirp rate.
    Tp : float
        The pulse width.
    Fs : float
        The sampling rate.
    Fc : float, optional
        The center frequency.
    Nfft : int or None, optional
        The number of points for doing FFT.
    mod : str, optional
        The mode of matched filter.
    win : tensor or None, optional
        The window function.
    ftshift : bool, optional
        Shift the zero-frequecy in center?
    scale : bool, optional
        Scale the filter?
    device : str, optional
        Specifies the device to be used for computing.

    Returns
    -------
    tensor
        The matched filter tensor.
    """
    Nh = round(Fs * Tp)
    if Nfft is None:
        Nfft = 2 ** nextpow2(Nh)
    t = th.linspace(-Tp / 2., Tp / 2., Nh).to(device)
    # t = th.linspace(-Ts / 2., Ts / 2., Nfft)
    f = fftfreq(Nfft, Fs, norm=False, shift=ftshift).to(device)

    raise(ImportError('Not opened yet!'))


if __name__ == '__main__':

    import matplotlib.pyplot as plt

    Kr = 4.1e+11
    Tp = 37.0e-06
    Br = abs(Kr) * Tp

    alpha = 1.24588  # 1.1-1.4
    Fsr = alpha * Br
    Fc = 5.3e9
    # Fc = 0.

    Tsr = 2.1 * Tp
    Nsr = int(Fsr * Tsr)
    tr = th.linspace(-Tsr / 2., Tsr / 2., Nsr)
    fr = th.linspace(-Fsr / 2., Fsr / 2., Nsr)
    t = th.linspace(-Tsr / 2., Tsr / 2., Nsr)

    Sm1, t = chirp_mf_td(Kr, Tp, Fsr, Fc=Fc, Ns=Nsr, mod='conv')
    Sm2, t = chirp_mf_td(Kr, Tp, Fsr, Fc=Fc, Ns=Nsr, mod='corr')

    f = th.linspace(-Fsr / 2., Fsr / 2., len(Sm1))
    Ym1 = fft(Sm1, dim=0, shift=True)

    f = th.linspace(-Fsr / 2., Fsr / 2., len(Sm2))
    Ym2 = fft(Sm2, dim=0, shift=True)

    plt.figure(1)
    plt.subplot(221)
    plt.plot(t * 1e6, th.real(Sm1))
    plt.plot(t * 1e6, th.abs(Sm1))
    plt.grid()
    plt.legend(['Real part', 'Amplitude'])
    plt.title('Convolution matched filter')
    plt.xlabel(r'Time/$\mu s$')
    plt.ylabel('Amplitude')
    plt.subplot(222)
    plt.plot(t * 1e6, th.imag(Sm1))
    plt.plot(t * 1e6, th.abs(Sm1))
    plt.grid()
    plt.legend(['Imaginary part', 'Amplitude'])
    plt.title('Convolution matched filter')
    plt.xlabel(r'Time/$\mu s$')
    plt.ylabel('Amplitude')
    plt.subplot(223)
    plt.plot(f, th.abs(Ym1))
    plt.grid()
    plt.subplot(224)
    plt.plot(f, th.angle(Ym1))
    plt.grid()

    plt.figure(2)
    plt.subplot(221)
    plt.plot(t * 1e6, th.real(Sm2))
    plt.plot(t * 1e6, th.abs(Sm2))
    plt.grid()
    plt.legend(['Real part', 'Amplitude'])
    plt.title('Correlation matched filter')
    plt.xlabel(r'Time/$\mu s$')
    plt.ylabel('Amplitude')
    plt.subplot(222)
    plt.plot(t * 1e6, th.imag(Sm2))
    plt.plot(t * 1e6, th.abs(Sm2))
    plt.grid()
    plt.legend(['Imaginary part', 'Amplitude'])
    plt.title('Correlation matched filter')
    plt.xlabel(r'Time/$\mu s$')
    plt.ylabel('Amplitude')
    plt.subplot(223)
    plt.plot(f, th.abs(Ym2))
    plt.grid()
    plt.subplot(224)
    plt.plot(f, th.angle(Ym2))
    plt.grid()
    plt.show()
