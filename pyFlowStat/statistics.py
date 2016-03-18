#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
statistics
==========

functions related to determining TKE budget

:First Added:   2016-03-17
:Author:        Lento Manickathan
"""

import numpy as _np
from pyFlowStat.io.hdf5 import dataset as _dataset

def mean(HDF5Store,u,v,w):
    """
    Determine the mean component
    """
    # Calculate mean
    u_mean = _dataset(HDF5Store,'u_mean', _np.nanmean(u,axis=1))
    v_mean = _dataset(HDF5Store,'v_mean', _np.nanmean(v,axis=1))
    w_mean = _dataset(HDF5Store,'w_mean', _np.nanmean(w,axis=1))

    return u_mean, v_mean, w_mean

def reynoldsStresses(HDF5Store,u_prime,v_prime,w_prime,mask=None):
    """
    Determine the reynolds stress of a single u,v,w snapshot
    """
    # Reynolds streses
    R = HDF5Store.create_group('R')
    R.create_dataset('11', data=u_prime**2, dtype='float64', compression='gzip')
    R.create_dataset('12', data=u_prime*v_prime, dtype='float64', compression='gzip')
    R.create_dataset('13', data=u_prime*w_prime, dtype='float64', compression='gzip')
    R.create_dataset('22', data=v_prime**2, dtype='float64', compression='gzip')
    R.create_dataset('23', data=v_prime*w_prime, dtype='float64', compression='gzip')
    R.create_dataset('33', data=w_prime**2, dtype='float64', compression='gzip')

    return R
