#!/usr/bin/env python

"""A setuptools based model for setting up python wrapper for VisualCrossing API"""

from os import makedirs
from os.path import (
        join,
        isdir,
        dirname,
        abspath
    )

from pathlib import Path
from setuptools import setup
from setuptools import find_packages

from VisualCrossing import (
        __name__,
        __version__,
        __homepath__
    )

with open("README.md", "r") as fh:
    long_description = fh.read()

if not isdir(__homepath__):
    # create directory for first time installation
    # else, check additional configuration for the model
    # TODO setup additional details file for module configuration
    makedirs(__homepath__)

setup(
        name         = __name__,
        version      = __version__,
        author       = "Debmalya Pramanik",
        author_email = "dPramanik.official@gmail.com",

        description                   = "A python wrapper for fetching weather data from VisualCrossing",
        long_description              = long_description,
        long_description_content_type = "text/markdown",

        url         = "https://github.com/ZenithClown/VisualCrossing",
        packages    = find_packages(),
        classifiers = [
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License"
        ],
        
        project_urls = {
            "Bug Tracker" : "https://github.com/ZenithClown/VisualCrossing/issues"
        },
        
        python_requires  = ">=3.7",
        install_requires = ["requests"],
        
        keywords = "weather-api, weather-forecast, visual-crossing, api-rest, wrapper"
    )
