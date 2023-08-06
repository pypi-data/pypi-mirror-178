def sarstore(sardata, params, file):
    """Read SAR file

    Store SAR data and platform to a file (``.pkl`` , ``.h5`` or ``.mat``)

    Args:
        sardata (dict): The SAR raw data.

        params (dict): The SAR platform for obtain the SAR data.
        file (str): Description

    Returns:
        file (str): The file path for storing SAR data and platform
    """

def sarread(file):
    """Read SAR file

    Read SAR file (``.pkl`` or ``.mat``) and returns SAR data and platform

    Args:
        file (str): SAR data (contains platform) file path.

    Returns:
        sardata (Instance SarData): The SAR raw data.

        params (Instance of SarPlat): The SAR platform for obtain the SAR data.
    """

def format_data(X, modefrom='chnl_last', modeto='chnl_first'):
    """format data

    Format data to chanel first or chanel last.

    Args:
        X (numpy array): data to be formated
        modefrom (str, optional): chnl_last  --> chanel last; chnl_first  --> chanel first
            (the default is 'chnl_last', which chanel first)
        modeto (str, optional): chnl_last  --> chanel last; chnl_first  --> chanel first
            (the default is 'chnl_last', which chanel first)

    Returns:
        X (numpy array): Formated data

    Raises:
        TypeError: X should be a 3 or 4 dimention array!
        ValueError: Unknown mode of modefrom or modeto
    """


