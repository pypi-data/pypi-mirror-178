# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 13:40:49 2022

@author: ruair
"""

from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Programming Language :: Python :: 3'
]

setup(
    name='PSF_Ruairi',
    version='0.0.1',
    description='Circular Aperture PSF Model',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url = '',
    author = 'Ruairi Brady',
    author_email = 'ruairi.brady@ucdconnect.ie',
    licence = 'MIT',
    classifiers = classifiers,
    keywords = 'PSF',
    packages = find_packages(),
    install_requires=['numpy']



)
