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
import h5py as _h5py
import os as _os
import pyFlowStat as _pyFlowStat
import pyFlowStat.io.hdf5 as _hdf5

def TKE(HDF5Store,R,suffix=''):
    """Determine TKE from reynolds stresses

    .. math:: k = 0.5*(R_ii) = 0.5*(R_11 + R_22 + R_33)

    """
    # Calculate TKE from trace of R
    k = _hdf5.insert(HDF5Store, 'k'+suffix, 0.5*(R['xx'][:]+R['yy'][:]+R['zz'][:]))

    return k


def TKE_from_velocity(HDF5Store,U,suffix=''):
    """Determine TKE from instantaneous velocity snapshots

    Methodology
    -----------
    1. Determine fluctating component from Reynolds decomposition
    2. Determine Reynolds stresses from flucutations
    3. Calculate TKE from reynolds stresses
    """
    # Temp storage
    f = _h5py.File('temp_TKE_from_velocity_calculation.h5')

    # Velocity fluctuations
    U_prime = _pyFlowStat.fluctuatingVelocity(f, U)

    # Calculate reynolds stresses
    R = _pyFlowStat.reynoldsStresses(f, U_prime)

    # Calculate TKE
    k = _pyFlowStat.TKE_from_R(HDF5Store, R, suffix=suffix)

    # Remove temp
    f.close()
    _os.remove('temp_TKE_from_velocity_calculation.h5')

    return k


def production_from_velocity(HDF5Store, U, suffix=''):
    pass

def production2D(HDF5Store, R, S_mean, suffix=''):
    """Calculate TKE from Mean velocity and Reynolds stresses
    """
    # Production rate in of 2D turbulence
    P = _hdf5.insert(HDF5Store, 'P2D'+suffix, - (  R['xx']*S_mean['xx']
                                                 + R['xy']*S_mean['xy']*2.0
                                                 + R['yy']*S_mean['yy']))
    return P

def production3Dtrunc(HDF5Store, R, S_mean, suffix=''):
    """Calculate truncated 3D production
    """
    # Truncated production rate 3D turbulence
    P = _hdf5.insert(HDF5Store, 'P3Dtrunc'+suffix, - (  R['xx']*S_mean['xx']
                                                      + R['xy']*S_mean['xy']*2.0
                                                      + R['yy']*S_mean['yy']
                                                      + R['xz']*S_mean['xz']*2.0
                                                      + R['yz']*S_mean['yz']*2.0
                                                      + R['zz']*S_mean['zz']))

    return P
