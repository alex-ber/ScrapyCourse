
import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

from configparser import ConfigParser
from argparse import ArgumentParser
import sys
import ast


def _as_dict(parser):
    """
    Go over all sections in the parser,
    convert's there's key/value as dictionary that
    for every section in the parser has dictionary
    with key/value pairs (both str).

    :param parser: (self)
    :return: dict with key/value as str
    """
    d = OrderedDict()
    for section in parser.sections():
        d[section] = OrderedDict()
        for key in parser.options(section):
            d[section][key] = parser.get(section, key)
    return d

ConfigParser.as_dict = _as_dict

#inspired by
#https://stackoverflow.com/questions/21920989/parse-non-pre-defined-argument
#https://stackoverflow.com/questions/51267814/argparse-for-unknown-number-of-arguments-and-unknown-names
def _args_as_dict(parser, args=None):
    """
    Go over source for arguments, takes argument of the form --key=value.
    Create dictionary.
    Strip out '--' prefix from the key and put key/value (as str) to dict.

    If args is None, sys.argv[1:] will be used as source for arguments.
    Note: sys.argv[0] is ignored as it contain the name of main .py file to run.

    :param parser: ArgumentParser (self)
    :param args: if is not None, will be used as source for arguments.
    :return:
    """

    #see #argumentParser.parse_known_args()
    if args is None:
        # args default to the system args
        args = sys.argv[1:]
    else:
        # make sure that args are mutable
        args = list(args)

    d = OrderedDict()

    key = None
    value = None
    for arg in args:
        if arg.startswith('--') and '=' in arg:
            key, value = arg.rsplit("=", 1)
        else:
            key = arg
            value = None
        if key.startswith('--'):
            key = key[2:]

        d[key] = value

    return d


ArgumentParser.as_dict = _args_as_dict


#insipred by https://stackoverflow.com/a/14258151/1137529
#
def safe_eval(value):
    '''
    The purpose of this function is convert numbers from str to correct type.
    This function support convertion of built-in Python number to correct type (int, float)
    This function doesn't support decimal.Decimal or datetime.datetime or numpy types.
    '''
    try:
        ret = ast.literal_eval(value)
    except ValueError:
        ret = value
    return ret

