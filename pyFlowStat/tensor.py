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
import h5py as _h5py
#import pyFlowStat as _pyFlowStat
import pyFlowStat.io.hdf5 as _hdf5

def mean(HDF5Store, key, T, symm=False):
    """ Time-average of a Tensor of rank-n

    .. math:: \overline{T} = \frac{1}{N}\sum_k T_k
    where `N` is number of snapshots.
    """

    if isinstance(T, dict) or isinstance(T, _h5py.Group):
        # Tensor properties
        #K, N, M = _np.shape(T[T.keys()[0]])

        # Mean of tensor
        T_mean = HDF5Store.create_group(key)
        for ielem in T.keys():
            _hdf5.insert(T_mean, ielem, _np.nanmean(T[ielem], axis=0))

    else: # Not a dictonary
        T_mean = _hdf5.insert(HDF5Store, key, _np.nanmean(T, axis=0))

    return T_mean

def norm(HDF5Store, key, T,nDim=3,suffix=''):
    """Euclidean norm (magnitude) of Tensor of rank >0

    rank 1 : .. math:: |v| = \sqrt{v\cdotv}
    rank 2 : .. math:: |T| = \sqrt{T:T}

    """
    if isinstance(T, dict) or isinstance(T, _h5py.Group):
        # Tensor properties
        rank = int(_np.round(_np.log(len(T.keys()))/_np.log(nDim)))

        # Euclidean norm of tensor
        if rank==1:
            if nDim==3:
                T_norm = _hdf5.insert(HDF5Store,key,_np.linalg.norm((T['x'][:],T['y'][:],T['z'][:]),axis=0))
            elif nDim==2:
                T_norm = _hdf5.insert(HDF5Store,key,_np.linalg.norm((T['x'][:],T['y'][:]),axis=0))
            else:
                raise TypeError('Tensor must have dimensions > 1')
        else:
            raise NotImplementedError('Euclidean norm of rank >1 tensor not implemented')

    else: # Not a dictonary
        raise TypeError('Tensor must be rank > 0')

    return T_norm

def gradient(HDF5Store, key, T, dx=1.0, dy=1.0, dt=1.0, suffix=''):
    """Gradient of a tensor
    """
    if isinstance(T, dict) or isinstance(T, _h5py.Group):
        # Tensor properties
        rank = int(_np.round(_np.log(len(T.keys()))/_np.log(3)))
        K, N, M = _np.shape(T[T.keys()[0]])
        
        if rank==1:
            T_grad = HDF5Store.create_group(key)
            for ielem in T.keys():
                T_grad_i = T_grad.create_group(ielem)
                T_grad_i_dt, T_grad_i_dy, T_grad_i_dx = _np.gradient(T[ielem], dt, dy, dx)
                _hdf5.insert(T_grad_i,'dt',T_grad_i_dt)
                _hdf5.insert(T_grad_i,'dx',T_grad_i_dx)
                _hdf5.insert(T_grad_i,'dy',T_grad_i_dy)
        else:
            raise NotImplementedError('Higher order tensor gradient not implemented')
    else:
        T_grad = HDF5Store.create_group(key)
        T_grad_dt, T_grad_dy, T_grad_dx = _np.gradient(T, dt, dy, dx)
        _hdf5.insert(T_grad,'dt',T_grad_dt)
        _hdf5.insert(T_grad,'dx',T_grad_dx)
        _hdf5.insert(T_grad,'dy',T_grad_dy)
        
    return T_grad
            
            #T_grad = HDF5Store.create_group('x')
            
# def gradient_HDF5(HDF5Store, key, s, dy, dx, suffix=''):
#     """Gradient of a scalar field (rank 0) in cartesian coordinates
#
#     rank 0 : \nabla s = \frac{\partial s}{\partial x_i}
#     """
#
#     dsdy, dsdx = _np.gradient(s, dy, dx)
#
#     return dsdx, dsdy




# def norm(v,axis=0):
#     """Norm (magnitude) of vector field (rank 1)
#
#     rank 1 : .. math:: |T| = \sqrt{T\cdotT}
#     """
#     v_norm = _np.linalg.norm(v,axis=0)
#
#     return v_norm
