#!/usr/bin/env python

#+
#
# This file is part of quantities, a python package for handling physical
# quantities based on numpy.
#
# Copyright (C) 2009 Darren Dale
# http://packages.python.org/quantities
# License: BSD  (See doc/users/license.rst for full license)
#
# $Date$
#
#-

"""
    setup script for the quantities package

    options:

    * Unicode

      Units are presented using unicode by default, but this can be problematic
      on some platforms like windows. Unicode can be disabled, and units
      presented as simple ASCII text by passing the "--no-unicode" flag to the
      setup script::

        python setup.py build --no-unicode
"""

from __future__ import with_statement

import os
import sys

if 'develop' in sys.argv or 'nosetests' in sys.argv:
    from setuptools import setup
else:
    from distutils.core import setup

if os.path.exists('MANIFEST'): os.remove('MANIFEST')

with file('quantities/constants/NIST_codata.txt') as f:
    data = f.read()
data = data.split('\n')[10:-1]

with file('quantities/constants/_codata.py', 'w') as f:
    f.write('# THIS FILE IS AUTOMATICALLY GENERATED\n')
    f.write('# ANY CHANGES MADE HERE WILL BE LOST\n\n')
    f.write('physical_constants = {}\n\n')
    for line in data:
        name = line[:55].rstrip().replace('mag.','magnetic')
        name = name.replace('mom.', 'moment')
        val = line[55:77].replace(' ','').replace('...','')
        prec = line[77:99].replace(' ','').replace('(exact)', '0')
        unit = line[99:].rstrip().replace(' ', '*').replace('^', '**')
        d = "{'value': %s, 'precision': %s, 'units': '%s'}"%(val, prec, unit)
        f.write("physical_constants['%s'] = %s\n"%(name, d))

desc = 'Support for physical quantities based on the popular numpy library'

long_desc = "Quantities is designed to handle arithmetic and conversions of \
physical quantities, which have a magnitude, dimensionality specified by \
various units, and possibly an uncertainty. Quantities is based on the popular \
numpy library. It is undergoing active development, and while the current \
features and API are fairly stable, test coverage is incomplete and the \
package is not ready for production use."

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Education',
    'Topic :: Scientific/Engineering',
]

execfile('quantities/version.py')

package_data = {
    'quantities':['tests/*', 'constants/NIST_codata.txt']
}

setup(
    name = "quantities",
    version = __version__,
    author = 'Darren Dale',
    author_email = 'dsdale24@gmail.com',
    description = desc,
    keywords = ['quantities', 'physical quantities', 'units'],
    license = 'BSD',
    long_description = long_desc,
    classifiers = classifiers,
    platforms = 'Any',
    url = "http://packages.python.org/quantities",
    packages = [
        'quantities',
        'quantities.units',
        'quantities.constants',
        'quantities.umath'
    ],
    package_data = package_data,
    requires = ['numpy (>=1.3)'],
)
