#! /usr/bin/env python

import os

DESCRIPTION   = "Python tools for statistical analyses of flow data"

PKGNAME = 'pyFlowStat'
MAINTAINER = 'ETH/EMPA'
MAINTAINER_EMAIL = 'manickathan@arch.ethz.ch'
URL = 'http://www.carmeliet.arch.ethz.ch/',
LICENSE = 'BSD (3-clause)'
VERSION = '4.0.1.dev'

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

    return install_requires


if __name__ == "__main__":

    setup(name=PKGNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        license=LICENSE,
        keywords='flow statistics',
        url=URL,
        version=VERSION,
        install_requires=check_dependencies(),
        packages=['pyFlowStat'],
        package_data={'pyFlowStat':['ReadIMX64.dll']},
        classifiers=['Intended Audience :: Science/Research',
                     'License :: OSI Approved :: BSD License',
                     'Topic :: Scientific/Engineering :: Physics',
                     'Operating System :: POSIX',
                     'Programming Language :: Python :: 2.7',
                     ])
