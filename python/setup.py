# -*- coding: utf-8 -*-

from distutils.core import setup

long_description = open("README.md").read()

setup(
    name = "PyOSB",
    version = '0.5.0',
    packages = ['osb', 'osb.metadata', 'osb.resources', 'osb.utils'],
    author = "Padraig Gleeson, Richard Gerkin",
    author_email = "p.gleeson@gmail.com",
    description = "A Python library for interacting with Open Source Brain version 1",
    long_description = long_description,
    license = "GPLv3",
    url="https://github.com/OpenSourceBrain/OSB_API",
    install_requires=["lxml"],
    classifiers = [
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GPLv3 License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        'Topic :: Scientific/Engineering']
)
