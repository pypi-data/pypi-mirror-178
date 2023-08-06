import os
import setuptools

import dtcm

setuptools.setup(
    name         = 'dtcm',
    version      = dtcm.__version__,
    author       = 'AXY',
    author_email = 'axy@declassed.art',
    description  = 'Declassed Tor Circuits Manager',

    long_description = dtcm.__doc__,
    long_description_content_type = 'text/x-rst',

    url = 'https://declassed.art/repository/dtcm',

    py_modules = [
        'dtcm'
    ],

    install_requires=[
        'stem'
    ],

    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Topic :: Internet :: WWW/HTTP'
    ],

    python_requires = '>=3.6',
)
