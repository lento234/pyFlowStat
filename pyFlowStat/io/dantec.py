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
                gridSize = _re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)
    h5file['gridSize'] = [int(gridSize[1]),int(gridSize[0])]

    # Store coordinate data
    data = _np.loadtxt(csvList[0], delimiter=';', skiprows=skiprows)
    constDataKeys = ['ix','iy','x','y'] # ['xi','yi','xpx','ypx','x','y']
    for k, key in enumerate(constDataKeys):
        h5file.create_dataset(key, data=data[:,k], dtype='float64', compression='gzip')

    # Create empty dataset / groups
    nonconstDataKeys = ['u','v','w','u_norm','vectorStatus'] #['upx','vpx','u','v','Unorm','status']
    for k, key in enumerate(nonconstDataKeys):
        h5file.create_dataset(key, (int(gridSize[0])*int(gridSize[1]),nSnapshots), dtype='float64', compression='gzip')
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
            h5file[key][:,i] = data[:,k+len(constDataKeys)]
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
                gridSize = _re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)
    h5file['gridSize'] = [int(gridSize[1]),int(gridSize[0])]

    # Store coordinate data
    data = _np.loadtxt(csvList[0], delimiter=';', skiprows=skiprows)
    constDataKeys = ['ix','iy','x','y'] # ['xi','yi','xpx','ypx','x','y']
    for k, key in enumerate(constDataKeys):
        h5file.create_dataset(key, data=data[:,k], dtype='float64', compression='gzip')

    # Create empty dataset / groups
    nonconstDataKeys = ['u','v','w','u_norm','vectorStatus']
    for k, key in enumerate(nonconstDataKeys):
        h5file.create_dataset(key, (int(gridSize[0])*int(gridSize[1]),nSnapshots), dtype='float64', compression='gzip')
    # Time series
    h5file.create_dataset('t',(nSnapshots,), dtype='float64', compression='gzip')
    # Mask
    h5file.create_dataset('mask', (int(gridSize[0])*int(gridSize[1]),nSnapshots), dtype='bool', compression='gzip')

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
        h5file['mask'][:,i] = (data[:,-1] != 0.) & (data[:,-1] != 16.)

        # Store velocity data
        for k, key in enumerate(nonconstDataKeys[:-1]):
            idata = data[:,k+len(constDataKeys)]
            idata[h5file['mask'][:,i]] = _np.NaN
            h5file[key][:,i] = idata
        # Store vector status
        h5file['vectorStatus'][:,i] = data[:,k+1+len(constDataKeys)]

    _sys.stdout.write('\nDone.')

    return h5file
