def _compensation(X, phi, Na, Nr, ftshift=False, isfft=True):
    ...

class AutoFocusFFO(th.nn.Module):
    ...

    def __init__(self, Na, Nr, Nb=None, ftshift=False, trainable=True):
        ...

    def forward(self, X, isfft=True):
        ...

    def imaging(self, Xc):
        ...

    def get_param(self):
        ...

    def param_init(self, pa=None, pr=None):

