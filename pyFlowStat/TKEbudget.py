#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
TKE budget
==========

functions related to determining TKE budget

:First Added:   2016-03-17
:Author:        Lento Manickathan
"""


import numpy as _np
import pyFlowStat as _pyFlowStat
import pyFlowStat.io.hdf5 as _hdf5

def TKE_from_R(HDF5Store,R,force_2D_TKE=False,suffix=''):
    """
    Determine TKE from reynolds stresses
    """
    # Calculate mean
    if force_2D_TKE:
        k = _hdf5.dataset(HDF5Store, 'k'+suffix, 0.5*_np.add(R['11'],R['22']))
    else:
        if '33' in R.keys():
            k = _hdf5.dataset(HDF5Store, 'k'+suffix, 0.5*(R['11'].value+R['22'].value+R['33'].value))
        else:
            k = _hdf5.dataset(HDF5Store, 'k'+suffix, 0.75*_np.add(R['11'],R['22']))

    return k


def TKE_from_velocity(HDF5Store,u,v,w,storeAll=True,suffix=''):
    """
    Determine the mean component
    """
    # Calculate mean
    if storeAll:
        # Velocity fluctuations
        u_prime, v_prime, w_prime = _pyFlowStat.fluctuatingVelocity(HDF5Store,u,v,w,suffix=suffix)

        # Calculate reynolds stresses
        R = _pyFlowStat.reynoldsStresses(HDF5Store,u_prime,v_prime,w_prime,suffix=suffix)

        # Calculate TKE
        k = _pyFlowStat.TKE_from_R(HDF5Store,R,suffix=suffix)

    else:
        raise NotImplementedError('use storeAll=True. More efficient')

    return k
