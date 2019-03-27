
import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

from configparser import ConfigParser
from argparse import ArgumentParser
import sys



def _as_dict(parser):
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
