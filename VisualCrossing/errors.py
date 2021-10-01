# -*- encoding: utf-8 -*-

import warnings

class WrongDateFormat(Exception):
    """Exception is raised when the passed date is not in `YYYY-MM-DD` format"""


class VerificationWarning(Warning):
    """Warning is raised when fetching data with flag `verify = False`"""


class NoDataFetched(Exception):
    """Exception is raised when data is not fetched, i.e. received `status_code != 200`"""
