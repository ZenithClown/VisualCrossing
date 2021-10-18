# -*- encoding: utf-8 -*-

import json
import time
import platform
import warnings

from time import ctime
from uuid import uuid4
from sys import modules
from shutil import copy
from os.path import join
from pathlib import Path

from . import (
        __name__,
        __version__,
        __homepath__,
    )
from .errors import * # noqa: F403
from ._config import config

class base(object):
    """A base class that wraps essential utilities for :class:`API`

    :class:`API` is a python wrapper, to fetch API data from VisualCrossing,
    which can be used to fetch historic as well as forecasted weather data.
    """

    def __init__(self, **kwargs):
        status, response = config()
        if status == 100:
            # use defaults
            response = self.__args_default__()

        for k, v in response.items():
            setattr(self, k, v)


    def __args_default__(self) -> dict:
        """Defines a Dictionary of Default Values for Keyword Arguments (or Attributes)"""

        return {
            "unitGroup"      : "metric",
            "contentType"    : "csv",
            "aggregateHours" : 24
        }


    def __get_args_default__(self, args : str):
        """Get the Default Value associated with a Keyword Argument"""

        return self.__args_default__().get(args, None) # None if key not available


    @property
    def __optional_args__(self):
        """Get List of all the Optional Keyword Arguments Accepted by the API"""

        return self.__args_default__().keys()


    def generate_config(
            self,
            defaultSettings : bool = True,
            fileName : str  = "config.json",
            overwrite : bool = False,
            keepBackup : bool = True,
            **kwargs
        ) -> bool:
        """Generate configuration file at `__homepath__` when executed

        The configuration file can be generated with default settings as defined at
        :func:`__args_default__` else, user is requested to pass all necessary settings
        in a correct format (as required by API) to the function, setting `key` as the
        attribute name, and `value` as the desired value. Users are also advised not to
        save the `API_KEY` in the configuration file (for security purpose), and to use
        :func:`_generate_key` to save the key file in an encrypted format.

        :param defaultSettings: Should you wish to save the configuration file with
                                the default settings. If set to `False` then user is
                                requested to pass all necessary attributes (`key`) and
                                their values. Defaults to `True`.

        :param fileName: Output file name (with extension - `json`). Defaults to
                         `config.json`.

        :param overwrite: Overwrite existing configuration file, if exists (same filename).
                          Defaults to `False`.

        :param keepBackup: If same file name exists, then setting the parameter to `True` will
                           create a backup of the file with the following format
                           `<original-name>.<UUID>.json` where `UUID` is a randomly generated
                           7-charecters long name. Defaults to `True`.

        Accepts n-Keyword Arguments, which are all default settings that can be used to initialize
        the API.
        """

        outfile = join(__homepath__, fileName)

        # get attributes to write to file
        if defaultSettings:
            attrs = self.__args_default__()
        else:
            attrs = kwargs # get all attribute from kwargs

        # re-format attrs to a defined type, with meta-informations
        attrs = {
            "__header__" : {
                "program"  : __name__,
                "version"  : __version__,
                "homepath" : __homepath__
            },

            "platform" : {
                "platform"     : platform.platform(),
                "architecture" : platform.machine(),
                "version"      : platform.version(),
                "system"       : platform.system(),
                "processor"    : platform.processor(),
                "uname"        : platform.uname()
            },

            "attributes" : attrs,
            "timestamp"  : ctime()
        }

        # lambda to write to json file
        # where `kv` is the key-value pair, which is typically `attrs`
        # defined/reformatted in the above section
        def write_json(kv : dict, file : str):
            with open(file, "w") as f:
                json.dump(kv, f, sort_keys = False, indent = 4, default = str)

        if Path(outfile).is_file(): # file exists
            warnings.warn(f"{outfile} already exists.", FileExists)
            if keepBackup:
                try:
                    name, extension = fileName.split(".")
                except ValueError as err:
                    name = fileName.split(".")[0]
                    extension = "json"
                    warnings.warn(f"{fileName} is not of proper type. Setting name as: {name}", ImproperFileName)

                new_file = ".".join([name, str(uuid4())[:7], extension])

                # copy to a new file
                print(f"Old configuration file is available at {new_file}")
                try:
                    # python 3.8+
                    copy(outfile, join(__homepath__, new_file))
                except TypeError:
                    # python <= 3.7
                    # https://stackoverflow.com/a/33626207/6623589
                    copy(str(outfile), str(join(__homepath__, new_file)))
            else:
                warnings.warn(f"{outfile} will be overwritten without a backup.", FileExists)

            if overwrite:
                write_json(attrs, outfile) # write to file
            else:
                raise ValueError(f"{outfile} already exists, and `overwrite` is set to `False`")

        else:
            # same file does not exists, other parameters are not required for validation
            write_json(attrs, outfile) # write to file

        return True
