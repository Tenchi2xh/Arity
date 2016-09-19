# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from os.path import join, dirname


setup(
    name="Arity",
    version="0.1.0",
    description="Functional Programming for Python",
    author="Hamza Haiken",
    author_email="tenchi@team2xh.net",
    packages=["arity"],
    url="http://github.com/Tenchi2xh/Arity",
    long_description=open("README.md").read(),
    install_requires=["forbiddenfruit"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
      ],
)
