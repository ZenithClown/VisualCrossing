# -*- encoding: utf-8 -*-

import json
import urllib
import requests
import warnings
import pandas as pd
from io import StringIO
from datetime import datetime as dt
from requests.exceptions import SSLError
from os.path import join, dirname, abspath

from .errors import *

class API(object):
    """A basic API for Visual-Crossing Weather Data

    :param date: Date for which weather data is required. Pass the date in `YYYY-MM-DD` format,
                 or pass `FORCAST` to get the forecasted data for a particular date.

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
            location : str or tuple,
            **kwargs
        ):
        # default constructor

        self.date     = date
        self.APIKey   = APIKey
        self._location = location

        # define keyword arguments
        self.endDate = kwargs.get("endDate", None)
        self.unitGroup = kwargs.get("unitGroup", "metric")
        self.contentType = kwargs.get("contentType", "csv")
        self.aggregateHours = kwargs.get("aggregateHours", 24)


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


    @property
    def BaseURL(self) -> str:
        """Base URL for fetching weather data. Check Visual-Crossing documentation for information."""

        return "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/" + \
               self.queryType() + \
               "&location=" + urllib.parse.quote(self._location) + \
               "&key=" + self.APIKey + \
               f"&contentType={self.contentType}"


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


    def get(self, type : str = pd.DataFrame, **kwargs):
        """Fetch API Data and Return in desirable Format"""

        ssl_verify = kwargs.get("ssl_verify", False)

        if ssl_verify:
            warnings.warn("using `ssl_verify = True`", VerificationWarning)

        try:
            data = requests.get(self.BaseURL, verify = ssl_verify)
        except SSLError as err:
            # raise ValueError(f"Failed for {err}. If you understand the risk, and want to continue, set `ssl_verify = False`")
            pass

        if data.status_code != 200:
            raise NoDataFetched(f"unable to fetch any data, recevied code {data.status_code}")

        if self.contentType == "csv":
            data = pd.read_csv(StringIO(data.text))
        else: # data type is JSON
            data = data.json()

        return data
