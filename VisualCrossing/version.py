# -*- encoding: utf-8 -*-

from os.path import join
from pathlib import Path

__version__ = open(join(Path(__file__).parent.resolve(), "static", "VERSION"), "rt").read()
