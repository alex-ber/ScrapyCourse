import logging

logger = logging.getLogger(__name__)

from alexber.utils.parsers import ConfigParser, ArgumentParser
from pathlib import Path
from collections import OrderedDict
import ast

PLAYER_CLS_KEY ='cls'
NAME_PLAYER_A_KEY='name'
NAME_PLAYER_B_KEY='name'
PLAYER_A_KEY='playera'
PLAYER_B_KEY='playerb'
DEFAULT_NAME_PLAYER_A = 'Player A'
DEFAULT_NAME_PLAYER_B = 'Player B'

_WHITELIST_FULL_NAMES = {'cls', 'name'}
_WHITELIST_PREFIX = {'init', 'prop', 'set'}
_WHITELIST_FLAT_PREFIX = {'playera', 'playerb'}

#TODO: Alex write unit tests

#insipred by https://stackoverflow.com/a/14258151/1137529
#
def _convert(value):
    '''
    The purpose of this function is convert numbers from str to correct type.
    This function support convertion of built-in Python number to correct type (int, float)
    This function doesn't support decimal.Decimal.
    '''
    try:
        ret = ast.literal_eval(value)
    except ValueError:
        ret = value
    return ret





def _mask_value(value, implicit_convert):
    ret = _convert(value) \
        if implicit_convert \
        else value
    return ret

def _mask_key(key):
    if key in _WHITELIST_FULL_NAMES:
        logger.debug(f'Key {key} is in _WHITELIST_FULL_NAMES')
        return key

    if '.' not in key:
        logger.info(f"Key {key} doen't has dot in it (and not whitelisted)")
        return None

    prefix, real_key = key.split(".", 1)

    if prefix in _WHITELIST_PREFIX:
        logger.debug(f'Key {key} is in _WHITELIST_PREFIX')
        return key

    logger.info(f'Unexpected key {key}')
    return None



def parse_dict(d, implicit_convert=True):
    dd = OrderedDict()
    playera_dd = OrderedDict()
    playerb_dd = OrderedDict()
    dd[PLAYER_A_KEY] = playera_dd
    dd[PLAYER_B_KEY] = playerb_dd

    playera_d = d.get(PLAYER_A_KEY, {})
    playerb_d = d.get(PLAYER_B_KEY, {})

    for key, value in playera_d.items():
        key = _mask_key(key)
        if key is None:
            logger.info(f"Skipping key {key}")
            continue
        playera_dd[key] = _mask_value(value, implicit_convert)


    for key, value in playerb_d.items():
        key = _mask_key(key)
        if key is None:
            logger.info(f"Skipping key {key}")
            continue
        playerb_dd[key] = _mask_value(value, implicit_convert)

    return dd



def parse_flat_dict(d, implicit_convert=True):
    dd = OrderedDict()
    dd[PLAYER_A_KEY] = OrderedDict()
    dd[PLAYER_B_KEY] = OrderedDict()

    for flat_key, value in d.items():
        if '.' not in flat_key:
            logger.info(f"Skipping key {flat_key}. It doesn't contain dot.")
            continue

        key, real_key = flat_key.split(".", 1)

        if key not in _WHITELIST_FLAT_PREFIX:
            logger.info(f"Skipping key {flat_key}. It is whitelisted in flat prefix.")
            continue

        real_key = _mask_key(real_key)
        if real_key is None:
            logger.info(f"Skipping key {flat_key}")
            continue

        dd[key][real_key] = _mask_value(value, implicit_convert)


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
