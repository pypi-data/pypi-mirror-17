#!/usr/bin/env python
# encoding: utf-8
'''
Created on Aug 29, 2014

@author: tmahrt
'''
from setuptools import setup
import codecs
setup(name='promo',
      version='1.1.0',
      author='Tim Mahrt',
      author_email='timmahrt@gmail.com',
      url='https://github.com/timmahrt/ProMo',
      package_dir={'promo': 'promo'},
      packages=['promo',
                'promo.morph_utils'],
      license='LICENSE',
      long_description=codecs.open('README.rst', 'r', encoding="utf-8").read(),
#       install_requires=[], # No requirements! # requires 'from setuptools import setup'
      )
