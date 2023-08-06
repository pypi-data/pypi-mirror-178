def iq_correct(Sr):
    r"""IQ Correction performs the I Q data correction

    IQ Correction performs the I Q data correction

    - I/Q bias removal
    - I/Q gain imbalance correction
    - I/Q non-orthogonality correction

    see "Sentinel-1-Level-1-Detailed-Algorithm-Definition".

    Args:
        Sr (Tensor): SAR raw data matrix :math:`{\bm S}_r \in {\mathbb R}^{N_a×N_r×2}`

    Returns:
        Sr (Tensor): Corrected SAR raw data.
        Flag : dict

    """


