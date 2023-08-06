#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="SaturdayMorning",
    version='0.1',
    description="A script for copying files and directories on a schedule.",
    long_description='',
    author='Ludovic Chabant',
    author_email='ludovic@chabant.com',
    license="Apache License 2.0",
    url="http://bolt80.com/saturdaymorning",
    keywords='',
    packages=find_packages(),
    install_requires=[],
    tests_require=[],
    classifiers=[],
    use_2to3=True,
    entry_points={'console_scripts': [
        'saturdaymorning = saturdaymorning:main'
    ]}
)
