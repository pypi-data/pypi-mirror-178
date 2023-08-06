import os
import setuptools

import dtcm2

setuptools.setup(
    name         = 'dtcm2',
    version      = dtcm2.__version__,
    author       = 'AXY',
    author_email = 'axy@declassed.art',
    description  = 'Declassed Tor Circuits Manager version 2',

    long_description = dtcm2.__doc__,
    long_description_content_type = 'text/x-rst',

    url = 'https://declassed.art/repository/dtcm2',

    py_modules = [
        'dtcm2'
    ],

    install_requires=[
        'torcontrol'
    ],

    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Topic :: Internet :: WWW/HTTP'
    ],

    python_requires = '>=3.7',
)
