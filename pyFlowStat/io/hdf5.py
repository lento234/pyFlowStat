#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
hdf5
====

hdf5 specific input, out functions
:First Added:   2016-03-17
:Author:        Lento Manickathan
"""

def insert(HDF5Store, key, data, dtype='float64', compression='gzip'):
    '''Create dataset'''
    return HDF5Store.create_dataset(key, data=data, dtype=dtype, compression=compression)
