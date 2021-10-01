# -*- encoding: utf-8 -*-

"""Visual Crossing Weather Data Fetching using Python"""

from os.path import join
from pathlib import Path

from .version import __version__ # define version

__name__ = "VisualCrossing"

# setting homepath, as provided in setup.py
# TODO detailed documentation for API/Configuration File
__homepath__ = join(Path.home(), ".visualCrossing")

# set affiliation details
__affiliation__ = "Indian Institute of Technology (IIT-ISM), Dhanbad"

# init-time option registrations
from .api import API
