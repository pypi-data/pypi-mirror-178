import torch as __torch
import sys as __sys

def __dim2axis(func):
    def wrapper(*params, axis : int = 0, **kwparams):
        return func(*params, **kwparams, dim = axis)
    wrapper.__name__ = func.__name__
    return wrapper

from torch import (
    bool, int8, uint8, int16, int32, int64,
    float32, float64, complex64, complex128,
)
uint16 = getattr(__torch, 'uint16', int32)
uint32 = getattr(__torch, 'uint32', int64)
uint64 = getattr(__torch, 'uint64', int64)

from torch import e, inf, nan, pi
newaxis = getattr(__torch, 'newaxis', None)

from torch import (
    Tensor as array,
    tensor as asarray,
)
array.__array_namespace__ = lambda self, *, api_version = None: __sys.modules[__name__]
def astype(array, dtype, /, *, copy = True):
    return array.to(dtype, copy = copy)

from torch import (
    arange, empty, full, ones, zeros, # subset
    abs, ceil, floor, exp, log, log2, pow, isinf, isnan, remainder, sign, sqrt, trunc, # subset
    concat, reshape, stack, # subset
    all, any,
)
def floor_divide(x1, x2, /):
    return __torch.div(x1, x2, rounding_mode='floor')
stack = __dim2axis(__torch.stack)
concat = __dim2axis(__torch.concat)

