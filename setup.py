# -*- coding: utf-8 -*-
from setuptools import setup

dependencies = [
    # alask == 0.0.1
    'http://admire93.github.io/alask/alask-0.0.1.tar.gz',

    # s2protocol == 0.0.0admire, http://github.com/admire93/s2protocol
    'http://admire93.github.io/s2protocol/s2protocol-0.0.0admire.tar.gz'
]

setup(name='sc2statistics',
      version='0.0.1',
      author='Kang Hyojun',
      author_email='hyojun@admire.kr',
      install_requires=[
          'alask == 0.0.1',
          'mpyq', 's2protocol == 0.0.0admire',
          'humanize == 0.5'
      ],
      dependency_links=dependencies)
