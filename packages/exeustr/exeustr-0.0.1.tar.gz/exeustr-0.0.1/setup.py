# -*- coding: utf-8 -*-

import io
import os
import re

from setuptools import find_packages
from setuptools import setup

# version
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'exeustr', '__init__.py'), 'r') as f:
  init_py = f.read()
version = re.search('__version__ = "(.*)"', init_py).groups()[0]

# obtain long description from README
with io.open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
  README = f.read()

# installation packages
packages = find_packages()

# setup
setup(
  name='exeustr',
  version=version,
  description='execute python code using string',
  long_description=README,
  long_description_content_type="text/markdown",
  author='dulingkang',
  author_email='dulingkang@163.com',
  packages=packages,
  python_requires='>=3.7',
  install_requires=[],
  url='https://github.com/dulingkang/exeu',
  project_urls={
    "Bug Tracker": "https://github.com/dulingkang/exeu/issues",
    "Documentation": "https://github.com/dulingkang/exeu",
    "Source Code": "https://github.com/dulingkang/exeu",
  },
  keywords=('exeucate eval, '
            'pipy test, '
            'python instruction, '),
  classifiers=[
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Software Development :: Libraries',
  ],
  license='Apache-2.0 license',
)