#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
statistics
==========

functions related to general flow statistics

:First Added:   2016-03-17
:Author:        Lento Manickathan
"""

import numpy as _np
import pyFlowStat.io.hdf5 as _hdf5

def meanVelocity(HDF5Store,u,v,w,suffix=''):
    """ Mean velocity component

    .. math:: \overline{u}_i = \overline{u_ik}

    """
    # Calculate mean
    u_mean = _hdf5.dataset(HDF5Store,'u_mean'+suffix, _np.nanmean(u,axis=1))
    v_mean = _hdf5.dataset(HDF5Store,'v_mean'+suffix, _np.nanmean(v,axis=1))
    w_mean = _hdf5.dataset(HDF5Store,'w_mean'+suffix, _np.nanmean(w,axis=1))

    return u_mean, v_mean, w_mean

def fluctuatingVelocity(HDF5Store,u,v,w,suffix=''):
    """Fluctuating component of velocity:

    .. math:: u'_ik = u_ik - \overline{u}_i

    """
    N, M = _np.shape(u)
    # Calculate mean
    u_mean = _np.nanmean(u,axis=1)
    v_mean = _np.nanmean(v,axis=1)
    w_mean = _np.nanmean(w,axis=1)

    u_prime = _hdf5.dataset(HDF5Store,'u_prime'+suffix, _np.subtract(u,_np.tile(_np.reshape(u_mean,(N,1)),(1,M))))
    v_prime = _hdf5.dataset(HDF5Store,'v_prime'+suffix, _np.subtract(v,_np.tile(_np.reshape(v_mean,(N,1)),(1,M))))
    w_prime = _hdf5.dataset(HDF5Store,'w_prime'+suffix, _np.subtract(w,_np.tile(_np.reshape(w_mean,(N,1)),(1,M))))

    return u_prime, v_prime, w_prime

def reynoldsDecomposition(HDF5Store,u,v,w,suffix=''):
    """ Reynolds decomposition of velocity:

    .. math:: u_ik = \overline{u}_ik + u'_ik

    """
    N, M = _np.shape(u)
    # Calculate mean
    u_mean = _hdf5.dataset(HDF5Store,'u_mean'+suffix, _np.nanmean(u,axis=1))
    v_mean = _hdf5.dataset(HDF5Store,'v_mean'+suffix, _np.nanmean(v,axis=1))
    w_mean = _hdf5.dataset(HDF5Store,'w_mean'+suffix, _np.nanmean(w,axis=1))

    u_prime = _hdf5.dataset(HDF5Store,'u_prime'+suffix, _np.subtract(u,_np.tile(_np.reshape(u_mean,(N,1)),(1,M))))
    v_prime = _hdf5.dataset(HDF5Store,'v_prime'+suffix, _np.subtract(v,_np.tile(_np.reshape(v_mean,(N,1)),(1,M))))
    w_prime = _hdf5.dataset(HDF5Store,'w_prime'+suffix, _np.subtract(w,_np.tile(_np.reshape(w_mean,(N,1)),(1,M))))

    return (u_mean, u_prime), (v_mean, v_prime), (w_mean, w_prime)

def reynoldsStresses(HDF5Store,u_prime,v_prime,w_prime,suffix=''):
    """ Reynolds stresses tensor (incompressible, ..math::`\rho=1`)

    .. math:: R_ijk = \overline{u'_ik u'_jk}
    """
    # Reynolds streses
    R = HDF5Store.create_group('R'+suffix)
    _hdf5.dataset(R,'11'+suffix, _np.square(u_prime))
    _hdf5.dataset(R,'12'+suffix, _np.multiply(u_prime,v_prime))
    _hdf5.dataset(R,'13'+suffix, _np.multiply(u_prime,w_prime))
    _hdf5.dataset(R,'22'+suffix, _np.square(v_prime))
    _hdf5.dataset(R,'23'+suffix, _np.multiply(v_prime,w_prime))
    _hdf5.dataset(R,'33'+suffix, _np.square(w_prime))

    return R
