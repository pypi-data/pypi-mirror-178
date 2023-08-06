class SARParameterGenerator(object):
    """SAR Parameter Generator

    Attributes
    ----------
    prdict : dict
        ``{'p1': [low, high], 'p2': [low, high]...}``
    seed : int or None
        The seed for random generator.
    """

    def __init__(self, prdict, seed=None):
        ...

    def mksarp(self, n=1, seed=None):
        """Makes SAR Parameters

        Parameters
        ----------
        n : int, optional
            The number of experiments.
        seed : None, optional
            The seed for random generator.

        Returns
        -------
        dict
            The SAR Parameter dict.
        """


