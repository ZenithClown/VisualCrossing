# -*- encoding: utf-8 -*-

from json import load

# set configuration option
def config(file : str = None) -> dict:
    """Read a defined configuration file from home-path,
    and set it to be used module wide."""

    if file:
        file = join(__homepath__, file)
        if not Path(file).is_file():
            raise FileNotFoundError(f"File {file} is not available.")
        else:
            status = 200 # use from configuration file

            # file exists, read as a json file
            params = load(open(file, "r")) # read as dictionary

            # check if the formatting is correct
            if "attributes" not in params.keys():
                from .errors import WrongConfigFile
                raise WrongConfigFile("Configuration file is wrong, check documentation.")
            else:
                # additionally, check other defined keys (as in generate file)
                # is present, which ensures data integrity
                optional = []
                for k in ["__header__", "platform", "timestamp"]:
                    if k not in params.keys():
                        optional.append(k)

                if optional:
                    import warnings
                    from .errors import VerificationWarning

                    warnings.warn(f"Config file missing {optional}", VerificationWarning)
        params = params["attributes"]

    else:
        status = 100 # continue
        params = None # use defualts

    return status, params

    # # set attribute to default class
    # for k, v in params.items():
    #     globals()[k] = v

# # always initialize api with default values
# # once initialized, all the attributes are now
# # available as module level attrbute, thus the same
# # can be referenced as `VisualCrossing.unitGroup`
# config()
