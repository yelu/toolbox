from setuptools import find_packages
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_cfgparser = Extension(
        "cfgparser.CFGParserPy", 
        ['cfgparser/CFGParserPy.pyx'], 
        language="c++", 
        extra_compile_args=["-std=c++11"],
        extra_link_args=["-std=c++11"],
        include_dirs=['./cfgparser/cfgparser/'])

setup(
	name = 'lutools',
    version='1.0',
    description='lu tools',
    author='Lu Ye',
    author_email='yelu27@gmail.com',
    packages = ['featurizer'],
	ext_modules=cythonize([ext_cfgparser]),
)

