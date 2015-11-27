pyFlowStat
==========

    Python tools for statistical analyses of flow data.
    optimized structure, added license, contrib. files


Changelog
---------
version: 4.0
    * added `plotEnv`: custom plotting wrapper

Authors
-------
    * Marc Immer (aaa.aaa@aaa.com)
    * Marcel Vonlanthen (aaa.aaa@aaa.com)
    * Lento Manickathan (manickathan@arch.ethz.ch)

Dependencies
------------

### python version:
    tested on python 2.7.x

### python requirement:
    The following python modules must be installed:
        * h5py
        * numpy
        * matplotlib (plotting)
        * modred
        * scipy
        * seaborn (plotting)

    The following python modules should be installed for the advanced features:
        * h5py: for HDF5 save and load capabilites. See methods in
          "PointProbeFunctions.py", "SurfaceFunctions.py", and
          "TriSurfaceFunctions.py" for more information.
          (http://www.h5py.org/)
        * modred: for POD and DMD decomposition. See class POD and DMD.
          (https://pypi.python.org/pypi/modred)


Installation
------------

To install the development version, run

    pip install git+git://github.com/lento234/pyFlowStat.git@dev-lento
