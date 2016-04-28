#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
dantec
======

dantec specific input, out functions
:First Added:   2016-03-17
:Author:        Lento Manickathan
"""

import numpy as _np
import h5py as _h5py
import re as _re
import os as _os
import sys as _sys
#from pyFlowStat import INT_RANK0, INT_RANK1, INT_RANK2
#import glob as _glob

def csv2hdf5_stereo(csvList,outputPath,skiprows=9):
    """
    Convert stereo piv snapshot csv list to hdf5 container

    Features:
        - compression (gzip)
        - removed duplicate data
        - efficient memory management
    """

    # Export file
    outputPath = _os.path.splitext(outputPath)[0] + '.h5'
    h5file = _h5py.File(outputPath)

    # Store measurement parameters
    h5file['nSnapshots'] = nSnapshots = len(csvList)

    # Get PIV grid size
    with open(csvList[0],'r') as f:
        for j in range(4):
            line = f.readline()
            if j==3:
                gridSize = _np.int64(_re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line))[::-1]
    h5file['gridSize'] = gridSize

    # Store coordinate data
    data = _np.loadtxt(csvList[0], delimiter=';', skiprows=skiprows)
    constDataKeys = ['ix','iy','x','y'] # ['xi','yi','xpx','ypx','x','y']
    for k, key in enumerate(constDataKeys):
        h5file.create_dataset(key, data=_np.reshape(data[:,k],gridSize), dtype='float64', compression='gzip')

    # Create empty dataset / groups
    nonconstDataKeys = ['u','v','w','u_norm','vectorStatus'] #['upx','vpx','u','v','Unorm','status']
    for k, key in enumerate(nonconstDataKeys):
        h5file.create_dataset(key, (nSnapshots, gridSize[0], gridSize[1]), dtype='float64', compression='gzip')
    h5file.create_dataset('t',(nSnapshots,), dtype='float64', compression='gzip')

    # store raw piv data
    for i, path in enumerate(csvList):
        _sys.stdout.write('\rConverting %d of %d' % (i+1,nSnapshots))
        _sys.stdout.flush()
        # Extract timestamp
        with open(path,'r') as f:
            for j in range(skiprows-1):
                line = f.readline()
                if j==skiprows-3:
                    t = _re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)[1]
        h5file['t'][i] = _np.float64(t)
        # Extract displacement and velocity
        data = _np.loadtxt(path, delimiter=';', skiprows=skiprows)
        for k, key in enumerate(nonconstDataKeys):
            h5file[key][i] = _np.reshape(data[:,k+len(constDataKeys)], gridSize)
    _sys.stdout.write('\nDone.')

    return h5file

def csv2hdf5_stereo_masked(csvList,outputPath,skiprows=9):
    """
    Convert stereo piv snapshot csv list to hdf5 container

    Features:
        - compression (gzip)
        - removed duplicate data
        - efficient memory management
    """

    # Export file
    outputPath = _os.path.splitext(outputPath)[0] + '.h5'
    h5file = _h5py.File(outputPath)

    # Store measurement parameters
    h5file['nSnapshots'] = nSnapshots = len(csvList)

    # Get PIV grid size
    with open(csvList[0],'r') as f:
        for j in range(4):
            line = f.readline()
            if j==3:
                gridSize = _np.int64(_re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line))[::-1]
    h5file['gridSize'] = gridSize

    # Store coordinate data
    data = _np.loadtxt(csvList[0], delimiter=';', skiprows=skiprows)
    constDataKeys = ['ix','iy','x','y'] # ['xi','yi','xpx','ypx','x','y']
    for k, key in enumerate(constDataKeys):
        h5file.create_dataset(key, data=_np.reshape(data[:,k],gridSize), dtype='float64', compression='gzip')

    # Create empty dataset / groups
    nonconstDataKeys = ['u','v','w','u_norm','vectorStatus']
    for k, key in enumerate(nonconstDataKeys):
        h5file.create_dataset(key, (nSnapshots, gridSize[0], gridSize[1]), dtype='float64', compression='gzip')

    # Time series
    h5file.create_dataset('t',(nSnapshots,), dtype='float64', compression='gzip')
    # Mask
    h5file.create_dataset('mask', (nSnapshots, gridSize[0], gridSize[1]), dtype='bool', compression='gzip')

    # store raw piv data
    for i, path in enumerate(csvList):
        _sys.stdout.write('\rConverting %d of %d' % (i+1,nSnapshots))
        _sys.stdout.flush()
        # Extract timestamp
        with open(path,'r') as f:
            for j in range(skiprows-1):
                line = f.readline()
                if j==skiprows-3:
                    t = _re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)[1]
        h5file['t'][i] = _np.float64(t)

        # Extract displacement and velocity
        data = _np.loadtxt(path, delimiter=';', skiprows=skiprows)

        # Define mask per snapshot
        h5file['mask'][i] = _np.reshape((data[:,-1] != 0.) & (data[:,-1] != 16.), gridSize)

        # Store velocity data
        for k, key in enumerate(nonconstDataKeys[:-1]):
            idata = _np.reshape(data[:,k+len(constDataKeys)], gridSize)
            idata[h5file['mask'][i]] = _np.NaN
            h5file[key][i] = idata
        # Store vector status
        h5file['vectorStatus'][i] = _np.reshape(data[:,k+1+len(constDataKeys)], gridSize)

    _sys.stdout.write('\nDone.')

    return h5file


def csv2hdf5_stereo_masked_new(csvList,outputPath,skiprows=9):
    """
    Convert stereo piv snapshot csv list to hdf5 container

    Features:
        - compression (gzip)
        - removed duplicate data
        - efficient memory management
    """

    # Export file
    outputPath = _os.path.splitext(outputPath)[0] + '.h5'
    h5file = _h5py.File(outputPath)

    # Store measurement parameters
    h5file['nSnapshots'] = nSnapshots = len(csvList)

    # Get PIV grid size
    with open(csvList[0],'r') as f:
        for j in range(4):
            line = f.readline()
            if j==3:
                gridSize = _np.int64(_re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line))[::-1]
    h5file['gridSize'] = gridSize

    # Store coordinate data
    data = _np.loadtxt(csvList[0], delimiter=';', skiprows=skiprows)
    constDataKeys = ['ix','iy','x','y'] # ['xi','yi','xpx','ypx','x','y']

    # Interrogation window indices
    # iX = _np.zeros(gridSize, dtype=FLOAT_RANK1)
    # iX['x'] = _np.reshape(data[:,0], gridSize)
    # iX['y'] = _np.reshape(data[:,1], gridSize)
    # h5file.create_dataset('iX', data=iX, dtype=FLOAT_RANK1, compression='gzip')
    # h5file.create_dataset('iX', data=iX, dtype=FLOAT_RANK1, compression='gzip')\
    h5file.create_group('iX')
    for i, dim in enumerate(('x','y')):
        h5file['iX'].create_dataset(dim, data=_np.reshape(data[:,i], gridSize), dtype='float64', compression='gzip')

    # Interrogation window coordinates
    # X  = _np.zeros(gridSize, dtype=FLOAT_RANK1)
    # X['x'] = _np.reshape(data[:,2], gridSize)
    # X['y'] = _np.reshape(data[:,3], gridSize)
    # h5file.create_dataset('X', data=X, dtype=FLOAT_RANK1, compression='gzip')
    h5file.create_group('X')
    for i, dim in enumerate(('x','y')):
        h5file['X'].create_dataset(dim, data=_np.reshape(data[:,i+2], gridSize), dtype='float64', compression='gzip')

    # Create empty dataset / groups
    nonconstDataKeys = ['u','v','w','u_norm']

    # Velocity field
    h5file.create_group('U')
    for i, dim in enumerate(('x','y','z')):
        h5file['U'].create_dataset(dim, (nSnapshots, gridSize[0], gridSize[1]), dtype='float64', compression='gzip')

    # Time series
    h5file.create_dataset('t',(nSnapshots,), dtype='float64', compression='gzip')
    # Mask
    h5file.create_dataset('mask', (nSnapshots, gridSize[0], gridSize[1]), dtype='bool', compression='gzip')
    # Mask
    h5file.create_dataset('vectorStatus', (nSnapshots, gridSize[0], gridSize[1]), dtype='int', compression='gzip')

    # store raw piv data
    for i, path in enumerate(csvList):
        _sys.stdout.write('\rConverting %d of %d' % (i+1,nSnapshots))
        _sys.stdout.flush()
        # Extract timestamp
        with open(path,'r') as f:
            for j in range(skiprows-1):
                line = f.readline()
                if j==skiprows-3:
                    t = _re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)[1]
        h5file['t'][i] = _np.float64(t)

        # Extract displacement and velocity
        data = _np.loadtxt(path, delimiter=';', skiprows=skiprows)

        # Define mask per snapshot
        h5file['mask'][i] = _np.reshape((data[:,-1] != 0.) & (data[:,-1] != 16.), gridSize)

        # Store velocity data
        for k, dim in enumerate(('x','y','z')):
            idata = _np.reshape(data[:,k+len(constDataKeys)], gridSize)
            idata[h5file['mask'][i]] = _np.NaN
            h5file['U'][dim][i] = idata

        # Store vector status
        h5file['vectorStatus'][i] = _np.reshape(data[:,-1], gridSize)

    _sys.stdout.write('\nDone.')

    return h5file
