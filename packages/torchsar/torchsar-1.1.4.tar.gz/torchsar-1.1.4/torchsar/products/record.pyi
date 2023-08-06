def readrcd(filepath, decfmtf, D, offset=0, endian='>'):
    """read file record

    read record information from a file. see :func:`read_ers_sar_raw` for reading ERS SAR raw data.

    Parameters
    ----------
    filepath : str
        file path string
    decfmtf : function
        format decoding function. see :func:`decfmtfers` for example.
    D : dict
        record descriptor dict, each value will be rewrited after reading.
    offset : int, optional
        record offset, read from the offset-th Byte (the default is 0)
    endian : str, optional
        endian, ``'<'`` --> little, ``'>'`` -- > big (the default is '<', which means little endian)

    Returns
    -------
    state : number
        reading status. 0 --> OK and done; 1 --> no such file; 2 --> bad record

    """

def readrcd1item(filepath, decfmtf, adrfmt, offset=0, endian='>'):
    """read one file record item

    read one record item information from a file. see :func:`read_ceos_sar_raw` for reading ERS SAR raw data.

    Parameters
    ----------
    filepath : str
        file path string
    decfmtf : function
        format decoding function. see :func:`decfmtfers` for example.
    adrfmt : tuple
        address and formation of one record item, a tuple with two
        elements: ``(adr, fmt)``, where, ``adr`` = (start address, end address) is a tuple and specifies
        the address (unit Bytes), ``fmt`` is the formation string.
    offset : int, optional
        record address offset, begin from the offset-th Byte (the default is 0)
    endian : str, optional
        endian, ``'<'`` --> little, ``'>'`` -- > big (the default is '<', which means little endian)

    Returns
    -------
    v : {}
        readed record item value.

    """

def printrcd(D):
    """print record

    print record in ascend address order.

    Parameters
    ----------
    D : dict
        descriptor dict
    """


