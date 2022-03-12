from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='pairwise_dist_cython',
    ext_modules = cythonize("pairwise_dist_cython.pyx"),
    include_dirs=[numpy.get_include()]
)