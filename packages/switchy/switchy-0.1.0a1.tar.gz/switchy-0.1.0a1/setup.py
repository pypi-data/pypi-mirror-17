#!/usr/bin/env python
#
# Copyright 2014 Sangoma Technologies Inc.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from setuptools import setup
import os


reqs = ['python-ESL', 'click']


on_rtd = os.environ.get('READTHEDOCS') == 'True'
if on_rtd:
    # RTD doesn't package SWIG in their default env
    reqs.remove('python-ESL')


with open('README.rst') as f:
    readme = f.read()


setup(
    name="switchy",
    version='0.1.0.alpha1',
    description='A fast FreeSWITCH control library purpose-built on '
                'traffic theory and stress testing.',
    long_description=readme,
    license='Mozilla',
    author='Sangoma Technologies',
    author_email='qa@eng.sangoma.com',
    maintainer='Tyler Goodlet',
    maintainer_email='tgoodlet@sangoma.com',
    url='https://github.com/sangoma/switchy',
    platforms=['linux'],
    packages=[
        'switchy',
        'switchy.apps',
        'switchy.apps.measure',
    ],
    entry_points={
        'console_scripts': [
            'switchy = switchy.cli:cli',
        ]
    },
    install_requires=reqs,
    package_data={
        'switchy': ['../conf/switchydp.xml']
    },
    extras_require={
        'metrics': ['pandas>=0.18'],
        'hdf5': ['tables==3.2.1.1'],
        'graphing': ['matplotlib', 'pandas>=0.18'],
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Telephony',
        'Topic :: Software Development :: Testing :: Traffic Generation',
        'Topic :: System :: Clustering',
        'Environment :: Console',
    ],
)
