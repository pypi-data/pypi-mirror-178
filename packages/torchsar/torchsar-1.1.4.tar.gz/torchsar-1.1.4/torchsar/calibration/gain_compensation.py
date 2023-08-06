#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : gain_compensation.py
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


def vga_gain_compensation(S, V, mod='linear', fact=1.0):
    r"""vga gain compensation

    vga gain compensation

    .. math::
       \begin{aligned}
       {\bm F} &= (λ 10^{{\bm V}/20})\\
       {\bm S}_{c} &= {\bm F} \odot {\bm S}
       \end{aligned}

    Parameters
    ----------
    S : torch tensor
        :attr:`S` is an :math:`N_a×N_r×2` array, where, :math:`S[:,:,0]` is the I signal
        and :math:`S[:,:,1]` is the Q signal.
    V : torch tensor
        :attr:`S` is an :math:`N_a×N_r` or :math:`N_a×1` VGA gain array, the gain values are in
        ``dB`` unit.
    mod : str, optional
        compensation mode (the default is 'linear')
    fact : number, optional
        fact is the factor :math:`\lambda` (the default is 1.0)

    Returns
    -------
    torch tensor
        compensated signal, :math:`N_a×N_r×2` array.
    """

    Na, Nr, _ = S.shape
    S = S.to(th.float32)
    V = th.tensor(V).to(th.float32)[0:Na, ...]

    linear_gain_factor = fact * 10.**(V / 20.0)

    if V.dim() == 3:
        S = S * linear_gain_factor
    elif V.dim() == 2 and V.shape[1] + V.shape[0] > 2:
        S[:, :, 0] = S[:, :, 0] * linear_gain_factor
        S[:, :, 1] = S[:, :, 1] * linear_gain_factor
    else:
        # A = np.repeat(linear_gain_factor, Nr*2).reshape(Na, Nr, 2)
        # S = A * S

        for n in range(Na):
            S[n, ...] = linear_gain_factor[n] * S[n, ...]

    return S

# def vga_gain_compensation(S, V, mod='linear', fact=1.0):
#     r"""vga gain compensation

#     vga gain compensation

#     .. math::
#        \begin{aligned}
#        {\bm F} &= (λ 10^{{\bm V}/20})\\
#        {\bm S}_{c} &= {\bm F} \odot {\bm S}
#        \end{aligned}

#     Parameters
#     ----------
#     S : array
#         :attr:`S` is an :math:`N_a×N_r×2` array, where, :math:`S[:,:,0]` is the I signal
#         and :math:`S[:,:,1]` is the Q signal.
#     V : array
#         :attr:`S` is an :math:`N_a×N_r` or :math:`N_a×1` VGA gain array, the gain values are in
#         ``dB`` unit.
#     mod : str, optional
#         compensation mode (the default is 'linear')
#     fact : int, optional
#         fact is the factor :math:`\lambda` (the default is 1.0)

#     Returns
#     -------
#     array
#         compensated signal, :math:`N_a×N_r×2` array.
#     """

#     logging.info("===In vga_gain_compensation...")

#     Na, Nr, _ = S.shape
#     if type(S) is not th.Tensor:
#         S = th.from_numpy(S)
#     S = S.to(th.float)
#     V = th.from_numpy(V)[0:Na].reshape(Na, 1)

#     linear_gain_factor = (fact * 10.**(V / 20.0))

#     if np.ndim(V) == 3:
#         S = S * linear_gain_factor
#     elif np.ndim(V) == 2 and V.shape[1] + V.shape[0] > 2:
#         S[:, :, 0] = S[:, :, 0] * linear_gain_factor
#         S[:, :, 1] = S[:, :, 1] * linear_gain_factor
#     else:
#         # A = np.repeat(linear_gain_factor, Nr*2).reshape(Na, Nr, 2)
#         # S = A * S

#         for n in range(Na):
#             S[n, :, :] = linear_gain_factor[n] * S[n, :, :]

#     logging.info("===Out vga_gain_compensation.")

#     return S