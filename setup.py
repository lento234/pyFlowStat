#! /usr/bin/env python

import os

DESCRIPTION   = "Python tools for statistical analyses of flow data"

PKGNAME = 'pyFlowStat'
MAINTAINER = 'ETH/EMPA'
MAINTAINER_EMAIL = 'manickathan@arch.ethz.ch'
URL = 'http://www.carmeliet.arch.ethz.ch/',
LICENSE = 'BSD (3-clause)'
VERSION = '3.1'

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup

def check_dependencies():
    install_requires = []
    try:
        import numpy
    except ImportError:
        install_requires.append('numpy')
    try:
        import scipy
    except ImportError:
        install_requires.append('scipy')
    try:
        import matplotlib
    except ImportError:
        install_requires.append('matplotlib')
    try:
        import seaborn
    except ImportError:
        install_requires.append('seaborn')
    try:
        import modred
    except ImportError:
        install_requires.append('modred')        
    try:
        import h5py
    except ImportError:
        install_requires.append('h5py')   

    return install_requires


if __name__ == "__main__":

    setup(name=PKGNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        version=VERSION,
        install_requires=check_dependencies(),
        packages=['pyFlowStat'],
        package_data={'pyFlowStat':['ReadIMX64.dll']},
        classifiers=[
                     'Intended Audience :: Science/Research',
                     'License :: OSI Approved :: BSD License',                     
                     'Operating System :: MacOS',                     
                     'Operating System :: POSIX :: Linux',
                     'Programming Language :: Python :: 2.7',
                     'Topic :: Scientific/Engineering :: Physics',
                     'Topic :: Scientific/Engineering :: Visualization']
    )

#setup(
#    name = "pyFlowStat",
#    version = "3.1",
#    author='ETH/EMPA',
#    author_email = "manickathan@arch.ethz.ch",
#    description = ("Python tools for statistical analyses of flow data"),
#    license = "GNU General Public License",
#    url='http://www.carmeliet.arch.ethz.ch/',
#    packages=['pyFlowStat'],
#    package_data={'pyFlowStat':['ReadIMX64.dll']},
#    long_description=read('README.md'),
#    install_requires=['numpy',
#                      'scipy',
#                      'matplotlib',
#                      'seaborn',
#                      'modred',
#                      'h5py'
#                      ],
#)
