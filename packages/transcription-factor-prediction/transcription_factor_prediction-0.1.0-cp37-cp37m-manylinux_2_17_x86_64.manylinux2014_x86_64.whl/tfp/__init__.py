from .tfp import *

__doc__ = tfp.__doc__
if hasattr(tfp, "__all__"):
    __all__ = tfp.__all__