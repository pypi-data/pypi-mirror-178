import os
import setuptools

import torcontrol

setuptools.setup(
    name         = 'torcontrol',
    version      = torcontrol.__version__,
    author       = 'AXY',
    author_email = 'axy@declassed.art',
    description  = 'Minimalistic Tor Controller',

    long_description = torcontrol.__doc__,
    long_description_content_type = 'text/x-rst',

    url = 'https://declassed.art/repository/torcontrol',

    packages = [
        'torcontrol'
    ],

    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Topic :: Internet :: WWW/HTTP'
    ],

    python_requires = '>=3.7',
)
