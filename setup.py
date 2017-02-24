import os
import sys

from setuptools import setup, find_packages

VERSION = '0.1.0'

setup(
    name='smachine',
    version=VERSION,
    description='State machine implementation in python',
    license='Mozilla Public License 2.0 (MPL 2.0)',
    url='https://github.com/chriscz/smachine',

    author='Chris Coetzee',
    author_email='chriscz93@gmail.com',

    py_modules=["smachine"],
    include_package_data=True,
    zip_safe=False,
)
