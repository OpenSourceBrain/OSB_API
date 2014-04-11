# -*- coding: utf-8 -*-

from distutils.core import setup

long_description = open("README.md").read()

setup(
    name = "PyOSB",
    version = '0.3.0',
    packages = ['osb', 'osb.metadata', 'osb.resources', 'osb.utils'],
    author = "Padraig Gleeson, Richard Gerkin",
    author_email = "p.gleeson@gmail.com",
    description = "A Python library for interacting with the Open Source Brain repository",
    long_description = long_description,
    license = "GPLv3",
    url="https://github.com/OpenSourceBrain/OSB_API",
    classifiers = [
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GPLv3 License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering']
)



