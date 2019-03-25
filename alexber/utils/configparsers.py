
import logging
logger = logging.getLogger(__name__)
import collections

from configparser import ConfigParser


def _as_dict(parser):
    d = collections.OrderedDict()
    for section in parser.sections():
        d[section] = collections.OrderedDict()
        for key in parser.options(section):
            d[section][key] = parser.get(section, key)
    return d

ConfigParser.as_dict = _as_dict