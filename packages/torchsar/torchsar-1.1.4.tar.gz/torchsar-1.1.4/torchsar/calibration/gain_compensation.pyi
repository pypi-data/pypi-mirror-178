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


