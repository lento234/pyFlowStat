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
from pyFlowStat import tensor as _tensor

def meanVelocity(HDF5Store,U,suffix=''):
    """ Mean velocity component

    .. math:: \overline{u}_i = \overline{u_ik}

    """
    # Tensor properties
    elements = U.keys()
    K, N, M = _np.shape(U[elements[0]])

    # Calculate mean
    U_mean = HDF5Store.create_group('U_mean'+suffix)
    for ielem in elements:
        _hdf5.insert(U_mean, ielem, _np.nanmean(U[ielem], axis=0))

    return U_mean

def fluctuatingVelocity(HDF5Store,U,suffix=''):
    """Fluctuating component of velocity:

    .. math:: u'_ik = u_ik - \overline{u}_i

    """
    # Tensor properties
    elements = U.keys()
    K, N, M = _np.shape(U[elements[0]])

    # Calculate mean
    U_mean = {} # Not stored
    U_prime = HDF5Store.create_group('U_prime'+suffix)
    for ielem in elements:
        U_mean[ielem] = _np.nanmean(U[ielem], axis=0)
        _hdf5.insert(U_prime, ielem, _np.subtract(U[ielem],_np.tile(U_mean[ielem],(K,1,1))))

    return U_prime

def reynoldsDecomposition(HDF5Store,U,suffix=''):
    """ Reynolds decomposition of velocity:

    .. math:: u_ik = \overline{u}_ik + u'_ik

    """
    # Tensor properties
    elements = U.keys()
    K, N, M = _np.shape(U[elements[0]])

    # Calculate mean and fluctuations
    U_mean = HDF5Store.create_group('U_mean'+suffix)
    U_prime = HDF5Store.create_group('U_prime'+suffix)
    for ielem in elements:
        _hdf5.insert(U_mean, ielem, _np.nanmean(U[ielem], axis=0))
        _hdf5.insert(U_prime, ielem, _np.subtract(U[ielem],_np.tile(U_mean[ielem],(K,1,1))))

    return U_mean, U_prime

def reynoldsStresses(HDF5Store,U_prime,suffix=''):
    """ Reynolds stresses tensor (incompressible, ..math::`\rho=1`)

    .. math:: R_ijk = \overline{u'_ik u'_jk}
    """

    # Reynolds streses
    R = HDF5Store.create_group('R'+suffix)
    _hdf5.insert(R,'xx', _np.square(U_prime['x']))
    _hdf5.insert(R,'xy', _np.multiply(U_prime['x'],U_prime['y']))
    _hdf5.insert(R,'xz', _np.multiply(U_prime['x'],U_prime['z']))
    _hdf5.insert(R,'yy', _np.square(U_prime['y']))
    _hdf5.insert(R,'yz', _np.multiply(U_prime['y'],U_prime['z']))
    _hdf5.insert(R,'zz', _np.square(U_prime['z']))

    return R

def strainRateTensor(HDF5Store, U, dx=1.0, dy=1.0, dt=1.0, suffix=''):
    """Truncated strain rate tensor.
    *Note: If incompressible, viscous stress is equal to strain rate

    Truncation:
    ----------
    Off-plane gradient unknown: dudz, dvdz = ?, dwdz assumed from
        divergence free relation

    .. math:: S = 0.5*(J + J^T) = 0.5 ( \partial_j u_i + \partial_i u_j )
    """
    U_grad = _tensor.gradient(HDF5Store, 'U_grad', U, dx, dy, dt, suffix)

    S = HDF5Store.create_group('S'+suffix)
    _hdf5.insert(S,'xx', U_grad['x']['dx'])
    _hdf5.insert(S,'xy', 0.5*_np.add(U_grad['x']['dy'], U_grad['y']['dx']))
    _hdf5.insert(S,'xz', 0.5*U_grad['z']['dx'])
    _hdf5.insert(S,'yy', U_grad['y']['dy'])
    _hdf5.insert(S,'yz', 0.5*U_grad['z']['dy'])
    _hdf5.insert(S,'zz', -(_np.add(U_grad['x']['dx'], U_grad['y']['dy'])))

    return S
