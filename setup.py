#!/usr/bin/env python3

from setuptools import setup, find_packages

NAME = "tkscrollableframe"
VERSION = "2.0"
AUTHOR = "edf1101"
AUTHOR_EMAIL = "blank@blank.com"
DESCRIPTION = "Scrollable frame widget for Tkinter"

with open("README.md", "r") as readme:
    LONG_DESCRIPTION = readme.read()

URL = "https://github.com/edf1101/tkinter-Scrollable-Frame"
PACKAGES = find_packages()
CLASSIFIERS = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

setup(name=NAME,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/markdown",
      url=URL,
      packages=PACKAGES,
      classifiers=CLASSIFIERS)
