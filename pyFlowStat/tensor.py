#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tensor operations
=================

List of tensor operations for:
    - 3 dimensional space
    - cartesian coordinates

:First Added:   2016-03-21
:Author:        Lento Manickathan
"""

import numpy as _np
import pyFlowStat as _pyFlowStat
import pyFlowStat.io.hdf5 as _hdf5

def norm(T,rank=1,axis=0):
    """Norm (i.e magnitude) of rank 1 tensor

    rank 1 : .. math:: |T| = \sqrt{T\cdotT}
    """
    if rank==1:
        magT = _np.linalg.norm(T,axis=0)
    elif rank==2:
        raise NotImplementedError('Rank 2 tensor norm not implemented')

    return magT

def norm_HDF5(HDF5Store,key,T,rank=1,dim=3,axis=0,suffix=''):
    """Norm (i.e magnitude) of rank 1 tensor

    rank 1 : .. math:: |T| = \sqrt{T\cdotT}
    """

    if dim==3:
        T = (T[0].value,T[1].value,T[2].value)
    else:
        T = (T[0].value,T[1].value)

    magT = _hdf5.dataset(HDF5Store,key+suffix, _pyFlowStat.tensor.norm(T,rank=rank,axis=axis))

    return magT
