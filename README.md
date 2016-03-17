pyFlowStat
==========

    Python tools for statistical analyses of flow data.
    optimized structure, added license, contrib. files


Changelog
---------

#### 4.0.1.dev :

Authors
-------

    * Marc Immer (marc.immer@empa.ch)
    * Marcel Vonlanthen (marcel.vonlanthen@empa.ch)
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

    The following python modules should be installed for the advanced features:
        * h5py: for HDF5 save and load capabilites. See methods in
          "PointProbeFunctions.py", "SurfaceFunctions.py", and
          "TriSurfaceFunctions.py" for more information.
          (http://www.h5py.org/)
        * modred: for POD and DMD decomposition. See class POD and DMD.
          (https://pypi.python.org/pypi/modred)


Installation
------------

From source code:

    pip install -e /path/to/pyFlowStat

or from remote repository:

    pip install git+git://github.com/lento234/pyFlowStat.git@dev-lento

Uninstall
---------

    pip uninstall pyFlowStat
