import ast
import numpy as np
from six import string_types

def get_config_from_string(parts):
    """
    Helper function to extract the configuration of a certain function from the column name.
    The column name parts (split by "__") should be passed to this function. It will skip the
    kind name and the function name and only use the parameter parts. These parts will be split up on "_"
    into the parameter name and the parameter value. This value is transformed into a python object
    (for example is "(1, 2, 3)" transformed into a tuple consisting of the ints 1, 2 and 3).

    Returns None of no parameters are in the column name.

    :param parts: The column name split up on "__"
    :type parts: list
    :return: a dictionary with all parameters, which are encoded in the column name.
    :rtype: dict
    """
    relevant_parts = parts[2:]
    if not relevant_parts:
        return

    config_kwargs = [s.rsplit("_", 1)[0] for s in relevant_parts]
    config_values = [s.rsplit("_", 1)[1] for s in relevant_parts]

    dict_if_configs = {}

    for key, value in zip(config_kwargs, config_values):
        if value.lower() == "nan":
            dict_if_configs[key] = np.NaN
        elif value.lower() == "-inf":
            dict_if_configs[key] = np.NINF
        elif value.lower() == "inf":
            dict_if_configs[key] = np.PINF
        else:
            dict_if_configs[key] = ast.literal_eval(value)

    return dict_if_configs


def convert_to_output_format(param):
    """
    Helper function to convert parameters to a valid string, that can be used in a column name.
    Does the opposite which is used in the from_columns function.

    The parameters are sorted by their name and written out in the form

       <param name>_<param value>__<param name>_<param value>__ ...

    If a <param_value> is a string, this method will wrap it with parenthesis ", so "<param_value>"

    :param param: The dictionary of parameters to write out
    :type param: dict

    :return: The string of parsed parameters
    :rtype: str
    """

    def add_parenthesis_if_string_value(x):
        if isinstance(x, string_types):
            return '"' + str(x) + '"'
        else:
            return str(x)

    return "__".join(str(key) + "_" + add_parenthesis_if_string_value(param[key]) for key in sorted(param))


def is_valid_ip_and_port_v4(s):
    """
    Checks if the string s contains an valid IPv4 ip address with port number. 
    For example 192.168.0.1:8786 would be an valid address
    
    :param s: the input
    :type s: string
    
    :return: true if s is an ip address
    :rtype: bool
    """
    s = s.strip()

    if s.count('.') == 3 and s.count(':') == 1:

        if s.count(".0") > 0 and s.count(".0") != s.count(".0.") + s.count(".0:"):
            return False

        if s[::-1].find(".") < s.find(":"):
            ip = s.split(".")
            ip[3], port = ip[3].split(":")

            if all(i.isdigit() for i in ip) and port.isdigit():
                return all(0 <= int(i) < 256 for i in ip)
            else:
                return False
        else:
            return False
    else:
        return False
