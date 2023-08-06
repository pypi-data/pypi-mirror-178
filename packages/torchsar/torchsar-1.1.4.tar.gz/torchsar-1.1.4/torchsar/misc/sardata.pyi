class SarData(object):
    r"""SAR data class.
        rawdata
        image
        store
        read

    """

    def name(self):
        ...

    def name(self, value):
        ...

    def rawdata(self):
        ...

    def rawdata(self, value):
        ...

    def image(self):
        ...

    def image(self, value):
        ...

    def store(self, sarplat, file):
        ...

    def read(self, file):
        r"""Read SAR data file

        Read SAR data file (``.pkl`` or ``.mat``)

        Parameters
        ----------
        file : str
            SAR data file path}

        Returns
        -------
        sardata : Instance SarData
            The SAR raw data.

        sarplat : Instance of SarPlat
            The SAR platform for obtain the SAR data.
        """


