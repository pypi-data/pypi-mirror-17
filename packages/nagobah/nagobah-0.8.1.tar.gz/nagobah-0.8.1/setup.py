""" this script is design for dagobah"""
# _*_ coding: utf-8 _*_

from distutils.core import setup
from setuptools import find_packages

setup(
        name = "nagobah",
        packages = find_packages(),
        version = "0.8.1",
        classifiers = [
            "Programming Language :: Python",
            ],
        entry_points = {
            "console_scripts": [
                "niiu = niiu.niiu:main",
                ],
            }
        )
