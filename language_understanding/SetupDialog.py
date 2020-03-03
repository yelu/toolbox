from setuptools import find_packages
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

setup(
	name = 'lutools',
    version='1.0',
    description='lu tools',
    author='Lu Ye',
    author_email='yelu27@gmail.com',
    packages = ['dialog', 'dialog.TaskEngine'],
	ext_modules=cythonize([]),
)

