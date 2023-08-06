def multilook_spatial(Sslc, nlooks):
    r"""spatial multilook processing

    spatial averaging in azimuth or range direction.

    Args:
        Sslc (Tensor): Processed single look complex (or intensity) sar data tensor with size :math:`N_a×N_r`.
        nlooks (tuple or list): The number of looks in azimuth and range direction, [na, nr] or (na, nr).

    Returns:
        Smlc (Tensor): Processed multi-look complex tensor.

    """


