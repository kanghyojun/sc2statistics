# -*- coding: utf-8 -*-
from setuptools import setup

dependencies = [
    # alask == 0.0.1
    'http://admire93.github.io/alask/alask-0.0.1.tar.gz'
]

setup(name='sc2statistics',
      version='0.0.1',
      author='Kang Hyojun',
      author_email='hyojun@admire.kr',
      install_requires=[
          'sc2reader == 0.6.4', 'alask==0.0.1'
      ],
      dependency_links=dependencies)
