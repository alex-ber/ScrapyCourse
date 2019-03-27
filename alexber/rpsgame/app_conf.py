import logging

logger = logging.getLogger(__name__)

from alexber.utils.parsers import ConfigParser, ArgumentParser
from pathlib import Path
from collections import OrderedDict
import ast

PLAYER_CLS_KEY ='cls'
NAME_PLAYER_A_KEY='nameplayera'
NAME_PLAYER_B_KEY='nameplayerb'
PLAYER_A_KEY='playera'
PLAYER_B_KEY='playerb'
DEFAULT_NAME_PLAYER_A = 'Player A'
DEFAULT_NAME_PLAYER_B = 'Player B'

#TODO: Alex write unit tests
convert = ast.literal_eval

def parse_dict(d, implicit_convert=True):
    dd = {key: convert(value) for key, value in d.items()} \
            if implicit_convert \
            else d
    return dd


def parse_flat_dict(d, implicit_convert=True):
    dd = OrderedDict()
    dd[PLAYER_A_KEY] = OrderedDict()
    dd[PLAYER_B_KEY] = OrderedDict()
    #TODO: Alex remove it
    implicit_convert = False

    for flat_key, value in d.items():
        if '.' in flat_key:
            key, new_key = flat_key.split(".", 1)
            dd[key][new_key] = convert(value) \
                        if implicit_convert  \
                        else value


    return dd


def parse_sys_args(argumentParser=None, args=None):
    if argumentParser is None:
        argumentParser = ArgumentParser()
    argumentParser.add_argument("--config_file", nargs='?', dest='config_file', default='config.ini',
                                const='config.ini')
    params, unknown_arg = argumentParser.parse_known_args(args=args)

    dd = argumentParser.as_dict(args=unknown_arg)
    dd = parse_flat_dict(dd)
    return params, dd


def parse_ini(config_file='config.ini'):
    parser = ConfigParser()
    full_path = Path(config_file).resolve() #relative to cwd

    parser.read(full_path)
    dd = parser.as_dict()

    dd = parse_dict(dd)
    return dd

def parse_config(args=None):
    params, cli_dd = parse_sys_args(args=args)
    config_dd = parse_ini(params.config_file)
    dd = {**config_dd, **cli_dd}
    return dd



if __name__ == '__main__':
    main()
