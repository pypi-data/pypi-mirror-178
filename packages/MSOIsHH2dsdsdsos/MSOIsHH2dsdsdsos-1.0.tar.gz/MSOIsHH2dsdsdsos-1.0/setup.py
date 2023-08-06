#!/usr/bin/env python

from distutils.core import setup, Extension
from os import path
this_directory = path.abspath(path.dirname(__file__))
import pypandoc
long_descriptions = pypandoc.convert_file('README.md', 'rst')

setup(
      name='MSOIsHH2dsdsdsos',
      version='1.0',
      description='Flood Risk Analysis Tool',
      author='ADS project Team Nene',
      url = 'https://github.com/ese-msc-2022/ads-deluge-Nene',

      long_description = long_descriptions,
      packages=['flood_tool']
      )
