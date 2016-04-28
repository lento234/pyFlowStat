"""
import out plotenv modules
"""

# Define DTYPES
import numpy as _np
#FLOAT_RANK0 = _np.dtype('float64')
#FLOAT_RANK1 = _np.dtype([('x',FLOAT_RANK0),('y',FLOAT_RANK0),('z',FLOAT_RANK0)])
#FLOAT_RANK2 = _np.dtype([('x',FLOAT_RANK1),('y',FLOAT_RANK1),('z',FLOAT_RANK1)])
#INT_RANK0 = _np.dtype('int64')
#INT_RANK1 = _np.dtype([('x',INT_RANK0),('y',INT_RANK0),('z',INT_RANK0)])
#INT_RANK2 = _np.dtype([('x',INT_RANK1),('y',INT_RANK1),('z',INT_RANK1)])

# Import functions
from . import old
from . import io
from statistics import *
import TKE
from tensor import *

# Expose documentation
#__doc__ = plotenv.__doc__

# Unset recursive module
#del statistics
#del tensor
#del TKEbudget