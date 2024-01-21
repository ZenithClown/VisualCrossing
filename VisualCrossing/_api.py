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

import os
import json
import urllib
import requests
import warnings
import numpy as np
import pandas as pd
from io import StringIO
from copy import deepcopy
from datetime import datetime as dt
from requests.exceptions import SSLError

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

        self.__set_attr__(response, **kwargs)


    def set_config(self, file : str, **kwargs):
        _, response = config(file)
        self.__set_attr__(response, **kwargs)


    def __set_attr__(self, response : dict, **kwargs):
        for k, v in response.items():
            # set all attribute as class attribute
            # to override any attribute just send the specific
            # attribute, and the same is given priority over configuration file
            if k in self.__optional_args__ and k not in kwargs.keys():
                setattr(self, k, v)
            else:
                setattr(self, k, kwargs[k] or v)


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


    def get_key_from_config(self):
        pass


class API(base):
    """A python wrapper to fetch weather data from VisualCrossing

    The function is devised keeping in mind - minimal coding approach, and recurrent job-scheduling
    for any person. All the keyword arguments that the API accepts are same as that available
    in the Visual Crossing API Documentation (check README for more information). The API is configured
    with default values, which is easier to understand and retreive. However, the data requires certain
    required arguments defined below. The same can also be obtained from `config.json` file, but is not
    recomended.

    :param date: Date for which weather data is required. Pass the date in `YYYY-MM-DD` format,
                 or pass `FORCAST` to get the forecasted data for a particular date.

    :param APIKey: All VisualCrossing API calls are made with an API key associated with your billing/free
                   account. Get yourself a new Key, if you do not have one. It is advised that the key
                   is not written to a configuration file, and suitable `environment variables` should
                   be called/defined. However, there is a dedicated function :func:`get_key_from_config`
                   which can be used to get `APIKey` from configuration file, which should be defined
                   under `__api_key__`. The key can also be written into file either passing `key` or
                   `__api_key__` as a keyword argument to :func:`generate_config`. # TODO

    :param location: Location of which the weather is required. Defaults to either a place name (like `india`),
                     or, you can directly pass the coordinates of the particular place as (like `(long, lat)`),
                     or, you can also pass a list/set of locations (either name or coordinates.) # TODO

    :Keyword Arguments:
        * *endDate* (``str``) -- When end date is defined, the api fetches data for a given date
          range which starts from :param:`date` to `endDate`, else only singe day data is fetched.
          By default, only a single day data is fetched by setting start and end date as :param:`date`.

        * *unitGroup* (``str``) -- specify unit group, defaults to metric.

        * *contentType* (``str``) -- specify content type, defaults to csv.

        * *aggregateHours* (``str``) -- specify aggregate hours, defaults to 24 (daily).
    """

    def __init__(
            self,
            date     : str,
            APIKey   : str,
            location : str or tuple or list or dict,
            **kwargs
        ):
        # get values from base class
        super().__init__(**kwargs)

        # default constructor values
        self.date     = date
        self.APIKey   = APIKey
        self._location = location if type(location) == str else iter(location)

        # define keyword arguments
        self.endDate = kwargs.get("endDate", None)

        # self.checkParams() # check all parameters


    # def checkParams(self): # TO-FIX
    #     """Check if all the Keyword Arguments/Parameters are as per API Documentation"""

    #     # uses valid_parameters.json file to find list of allowed parameters
    #     _allowed_params = json.load(open(join(dirname(abspath(__file__)), "valid_params.json"), "r"))

    #     for key in _allowed_params.keys():
    #         attr = getattr(self, key)
    #         if attr not in _allowed_params[key]:
    #             try:
    #                 HELP_URI, HELP_URI_DESC = links[key].values()
    #             except KeyError:
    #                 HELP_URI, HELP_URI_DESC = links["parameters"].values()

    #             errorLogger.error(f"`{attr}` is not in allowed {_allowed_params[key]} for `{key}`")

    #             raise ValueError(
    #                     f"`{attr}` is not in allowed {_allowed_params[key]} for `{key}`." +
    #                     f"\nCheck {HELP_URI} for {HELP_URI_DESC}"
    #                 )


    # @property
    def BaseURL(self, location : str) -> str:
        """Base URL for fetching weather data. Check Visual-Crossing documentation for information."""

        return "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/" + \
               self.queryType() + \
               "&location=" + urllib.parse.quote(location) + \
               "&key=" + self.APIKey + \
               f"&contentType=csv" # for now, always get as csv


    def queryType(self) -> str:
        """Set data query type to either `historical` or `forecast` as per given date choice"""

        if self.date == "FORECAST":
            return f"forecast?&aggregateHours={self.aggregateHours}" + \
                   f"&unitGroup={self.unitGroup}" + \
                   "&shortColumnNames=false"
        else:
            try:
                _ = dt.strptime(self.date, "%Y-%m-%d") # check date type
            except ValueError:
                # errorLogger.error(f"date is required in YYYY-MM-DD format, got {self.date}")
                raise WrongDateFormat("date is required in YYYY-MM-DD format")
            except Exception as err:
                # debugLogger.debug(f"unable to understand <date = {self.date}>. Got Exception : {err}")
                pass

        queryDate = "&startDateTime=" + self.date + "T00:00:00" + \
                    "&endDateTime=" + str(self.endDate or self.date) + "T23:59:59"

        return f"history?&aggregateHours={self.aggregateHours}" + \
               f"&unitGroup={self.unitGroup}" + \
               "&dayStartTime=0:0:00&dayEndTime=23:59:59" + queryDate


    def _get_df_converted_data(self, loc : str, ssl_verify : bool):
        """Retreive weather data, and convert it into a pandas dataframe"""

        link = self.BaseURL(loc)
        
        try:
            response = requests.get(link, verify = ssl_verify)
        except SSLError:
            pass

        code = response.status_code
        _weather_data_df = pd.read_csv(StringIO(response.text))

        return code, deepcopy(_weather_data_df)


    def get(self, **kwargs):
        """Fetch API Data and Return in desirable Format"""

        ssl_verify = kwargs.get("ssl_verify", False)

        if not ssl_verify:
            warnings.warn("using `ssl_verify = True`", VerificationWarning)
        
        # try:
        if type(self._location) != str:
            total = np.array([self._get_df_converted_data(loc, ssl_verify) for loc in self._location])
            code = set(total[:, 0])
            code = 200 if len(code) == 1 and list(code)[0] == 200 else list(code.discard(200))[0]
            data = pd.concat(total[:, 1])
            del total # house keeping - as pandas holds object into memory
        else:
            code, data = self._get_df_converted_data(self._location, ssl_verify)
        # except SSLError as err:
        #     # raise ValueError(f"Failed for {err}. If you understand the risk, and want to continue, set `ssl_verify = False`")
        #     pass

        if code != 200:
            raise NoDataFetched(f"unable to fetch any data, recevied code {data.status_code}")

        if self.contentType == "csv":
            data = data.to_csv(index = False)
            # data = pd.read_csv(StringIO(data.text))
        elif self.contentType == "dataframe":
            pass # return data as is
        else: # data type is JSON
            # currently, the DataFrame is directly converted into JSON
            # with `.to_json()` function instead of the `data.json()` as
            # obtained from the API
            data = data.to_json()

        return deepcopy(data)
