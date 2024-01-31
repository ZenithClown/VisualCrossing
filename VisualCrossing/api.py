# -*- encoding: utf-8 -*-

"""
Python Wrapper for Visual Crossing API

A python wrapper function for the Visual Crossing weather API
services. The functionality is designed to fetch records using a
single date or a date range.

The Visual Crossing API returns data on an hourly basis under the key
`hours` which returns the results hourly. The code returns the result
on an hourly basis.
"""

import json
import urllib
import requests
import datetime as dt
from tqdm import tqdm as TQ

class base(object):
    """
    A Base Class for the Visual Crossing API Class
    
    :class:`base` is to be inherited by the class object for fetching the data
    from the Visual Crossing API. For the attributes accepted and default
    values check the child classes.
    """

    def __init__(self, start : str or dt.date, locations : list, key : str, **kwargs) -> None:
        self.start = self._date_formatter(start)
        
        # locations is iterable, and is iterated one by one
        self.locations = locations
        
        # add the main attribute key, and optionally allow end date
        self.key = key
        self.end = self._date_formatter(kwargs.get("end", start))


    @property
    def URI(self):
        _api_uri = "https://weather.visualcrossing.com/VisualCrossingWebServices"
        _endpoint = "/rest/services/timeline/{location}/{start}/{end}"
        _parameter = "?key={key}"

        return _api_uri + _endpoint + _parameter


    def _date_formatter(self, value : str or dt.date) -> str:
        _is_string = isinstance(value, str) # treat for str, dt.date
        
        if not any([_is_string, isinstance(value, dt.date)]):
            # string or dt.date format is not received
            raise ValueError(f"Start/End Value is Accepted as either `str` or `dt.date`, got ({type(value)}).")
        
        if _is_string:
            value = dt.datetime.strptime(value, "%Y-%m-%d").date()
        else:
            value = str(value)
            
        return value


    def write_json(self, values : dict, fname : str, **kwargs) -> bool:
        skipkeys = kwargs.get("skipkeys", False)
        ensure_ascii = kwargs.get("ensure_ascii", True)
        check_circular = kwargs.get("check_circular", True)
        allow_nan = kwargs.get("allow_nan", True)
        cls = kwargs.get("cls", None)
        indent = kwargs.get("indent", 4)
        separators = kwargs.get("separators", None)
        default = kwargs.get("default", str)
        sort_keys = kwargs.get("sort_keys", False)

        with open(fname, "w") as fh:
            json.dump(
                values, fh,
                skipkeys = skipkeys, ensure_ascii = ensure_ascii,
                check_circular = check_circular, allow_nan = allow_nan,
                cls = cls, indent = indent, separators = separators,
                default = default, sort_keys = sort_keys
            )
            
        return True


class API(base):
    """
    A python wrapper to fetch weather data from VisualCrossing

    The function is devised keeping in mind - minimal coding approach, and
    recurrent job-scheduling for any person. All the keyword arguments that
    the API accepts are same as that available in the Visual Crossing API
    Documentation (check README for more information). The API is configured
    with default values, which is easier to understand and retreive. However,
    the data requires certain required arguments defined below. The same can
    also be obtained from `config.json` file, but is not recommended.
    
    :type  start: str or dt.date
    :param start: The starting and ending data to fetch the data from the
        API. The date is to be either in `str("%Y-%m-%d")` format or an
        instance of the `dt.date()` class.
        
    :type  locations: list
    :param locations: A list of location, which can be either a list of place
        name with ISO2 parameter like: `["Delhi,IN", "Kolkata,IN", ...]` or
        can also pass the location as `latitude,longitude` combination like:
        `["28.704059,77.102490", "22.986757,87.854976", ...]`. The Visual
        Crossing API is designed to fetch data for one single location,
        however, this libraru sypports multiple location input and create an
        iterable object on the data response.
        
    :type  key: str
    :param key: Obtain an API key from https://www.visualcrossing.com/ and
        pass the value as a string. Typically, the key is a 25 digit
        alphanumeric key in all caps.
        
    Keyword Arguments
    -----------------
        * **`end`** (`str` or `dt.date`): The end date, which is optional, and
            the format is either `str("%Y-%m-%d")` or an instance of the
            `dt.date()` class.
    """
    
    def __init__(self, start : str or dt.date, locations : list, key : str, **kwargs) -> None:
        super().__init__(start, locations, key, **kwargs)


    def response(self, formatting : str = "json", onfail : str = "pass", verbose : bool = True) -> object:
        """
        Get the API Response from the Visual Crossing API
        
        Get the API response, and format the data based on the required
        formatting, which is by default `json` which is rendered as `dict`
        in python.
        
        :type  formatting: str
        :param formatting: Final output format of all the response in a
            consolidated format. The output format can be any of the following:
            `[json, csv]`. Defaults to `json`. # TODO other formatting.
            
        :type  onfail: str
        :param onfail: When a set of date, locations or any other iterable
            format is passed, the query may fail - server unavailable, calls
            exhausted, etc. The parameter can be set to either `pass` to
            return only the fetched/parsed records, while setting value to
            `fail` the code fails if any parsing is failed. Defaults to
            `pass`. # TODO other failing criteria
        """
        
        queryCost = 0
        responses = []
        for location in TQ(self.locations):
            _resolved_uri = self.URI.format(
                location = urllib.parse.quote(location), # iterate over all locations
                start = self.start, end = self.end, key = self.key
            )

            try:
                r = requests.get(_resolved_uri, verify = True)
                data = r.json()

                responses.append(data)
                queryCost += data["queryCost"]
            except Exception as err:
                pass
            
        if verbose: print(f"Total Query Cost: {queryCost:,}")
        return responses
