# -*- encoding: utf-8 -*-

class WrongDateFormat(Exception):
    """Exception is raised when the passed date is not in `YYYY-MM-DD` format"""


class VerificationWarning(Warning):
    """Warning is raised when fetching data with flag `verify = False` or config file not verified"""


class NoDataFetched(Exception):
    """Exception is raised when data is not fetched, i.e. received `status_code != 200`"""

class ImproperFileName(Warning):
    """Warning is raised when a file name is received which is not of format `name.extension`"""

class FileExists(Warning):
    """Warning is raised when a given file name already exists, and needs to be modified"""

class WrongConfigFile(Exception):
    """Error is raised when the given configuration file does not have a key named `attributes`"""