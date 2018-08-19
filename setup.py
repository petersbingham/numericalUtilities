# -*- coding: utf-8 -*-

from distutils.core import setup
import os
import shutil
shutil.copy('README.md', 'pynumutil/README.md')

dir_setup = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_setup, 'pynumutil', 'release.py')) as f:
    # Defines __version__
    exec(f.read())

setup(name='pynumutil',
      version=__version__,
      description='Simple Python Numerical Utilities.',
      author="Peter Bingham",
      author_email="petersbingham@hotmail.co.uk",
      packages=['pynumutil'],
      package_data={'pynumutil': ['README.md']}
     )
