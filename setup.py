#!/usr/bin/env python

"""A setuptools based model for setting up python wrapper for VisualCrossing API"""

from os import makedirs
from os.path import (
        join,
        isdir
    )

from pathlib import Path
from setuptools import setup
from setuptools import find_packages

PKG = "VisualCrossing" # package-name

# Version File Implementation: https://stackoverflow.com/a/7071358
VERSIONFILE = join("static", "VERSION")
try:
    VERSION = open(VERSIONFILE, "rt").read() # always read as str()
except FileNotFoundError:
    raise RuntimeError("unable to run setuptools")

with open("README.md", "r") as fh:
    long_description = fh.read()

# create homepath for logging
# also, homepath can be used for finding API Key/Configuration File(s)
HOMEPATH = join(Path.home(), ".visualCrossing")

if not isdir(HOMEPATH):
    # create directory for first time installation
    # else, check additional configuration for the model
    # TODO setup additional details file for module configuration
    makedirs(HOMEPATH)

setup(
        name         = PKG,
        version      = VERSION,
        author       = "Debmalya Pramanik",
        author_email = "dPramanik.official@gmail.com",

        description                   = "A python wrapper for fetching weather data from VisualCrossing",
        long_description              = long_description,
        long_description_content_type = "text/markdown",

        url         = "https://github.com/ZenithClown/VisualCrossing",
        packages    = find_packages(),
        classifiers = [
            "Development Status :: 1 - Planning",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License"
        ],
        python_requires  = ">=3.7",
        install_requires = [],
        keywords = "weather-api, weather-forecast, visual-crossing, api-rest, wrapper"
    )
