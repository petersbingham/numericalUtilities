# -*- coding: utf-8 -*-

from distutils.core import setup
import shutil
shutil.copy('README.md', 'pynumutil/README.md')

setup(name='pynumutil',
      version='0.2',
      description='Simple Numerical Utilities',
      author="Peter Bingham",
      author_email="petersbingham@hotmail.co.uk",
      packages=['pynumutil'],
      package_data={'pynumutil': ['README.md']}
     )
