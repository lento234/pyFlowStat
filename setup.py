from setuptools import setup
import glob, os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyFlowStat",
    version = "3.1",
    author='ETH/EMPA',
    author_email = "manickathan@arch.ethz.ch",
    description = ("Python tools for statistical analyses of flow data"),
    license = "GNU General Public License",
    url='http://www.carmeliet.arch.ethz.ch/',
    packages=['pyFlowStat'],
    package_data={'pyFlowStat':['ReadIMX64.dll']},
    long_description=read('README'),
    install_requires=['numpy',
                      'scipy',
                      'matplotlib',
                      'seaborn',
                      'modred',
                      'h5py'
                      ],
)
