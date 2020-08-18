#!/usr/bin/env python

from setuptools import setup, find_packages

with open("./README.md") as f:
    long_description = f.read()

setup(name='Cah',
      version='0.1',
      description='A Python implementation of Cards Against Humanity',
      long_description=long_description,
      author='Christophe Vanlancker',
      author_email='carroarmato0@gmail.com',
      url='https://github.com/carroarmato0/cardsagainsthumanity',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'bottle',
          'bottle-mongo',
          'bottle-websocket',
          'pymongo',
          'iso-639',
      ],
      )
