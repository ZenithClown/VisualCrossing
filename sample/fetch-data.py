# -*- encoding: utf-8 -*-

"""Application of `VisualCrossing` to fecth Sample Data"""

import os

import numpy as np
import pandas as pd

# setting the environment
# if required, pip install python-dotenv
from dotenv import load_dotenv # Python 3.6+

import VisualCrossing as vc

if __name__ == "__main__":
    load_dotenv(verbose = True) # configure .env File or set Environment Variables

    # for checking which version of code is being executed
    print(vc.__version__)

    # setting api parameters, and using api key from environment variables
    api = vc.API("2021-09-25", APIKey = os.getenv("__api_key__"), location = "india", contentType = "dataframe")

    # get data from api and store them in csv file
    data = api.get(ssl_verify = True)
    data.to_csv("sample.csv", index = False)
