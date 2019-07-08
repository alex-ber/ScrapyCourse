import logging

logger = logging.getLogger(__name__)

from alexber.reqync.utils.parsers import ConfigParser, ArgumentParser
from pathlib import Path
from collections import OrderedDict


def parse_dict(d, implicit_convert=True):
    """
    This function is intented also for external use.
    For example, if we have configuration in JSON/YML, etc.
    It is better to provide exact type for the values (JSON and YML parser do it easily)
    and not to use implicit_convert.

    This function assume following structure of the dict d:

    engine:
        cls: ...
        ...
    playera:
        cls: ...
        ...
    playerb:
        cls: ...
        ...

    By default implicit_convert is True and this function will try to guess it.

    :param d: dict
    :param implicit_convert: whether to guess the value type and to convert it. Default True.
    :return: ready to use dict
    """

    dd = OrderedDict()
    playera_d = d.get(PLAYER_A_KEY, {})
    playerb_d = d.get(PLAYER_B_KEY, {})
    engine_d =  d.get(ENGINE_KEY,   {})

    for key, value in playera_d.items():
        key = _mask_key(key)
        if key is None:
            logger.info(f"Skipping key {key}")
            continue
        #playera_dd[key] = _mask_value(value, implicit_convert)
        inner_d = dd.setdefault(PLAYER_A_KEY, OrderedDict())
        inner_d[key] = _mask_value(value, implicit_convert)


    for key, value in playerb_d.items():
        key = _mask_key(key)
        if key is None:
            logger.info(f"Skipping key {key}")
            continue
        #playerb_dd[key] = _mask_value(value, implicit_convert)
        inner_d = dd.setdefault(PLAYER_B_KEY, OrderedDict())
        inner_d[key] = _mask_value(value, implicit_convert)

    for key, value in engine_d.items():
        key = _mask_key(key)
        if key is None:
            logger.info(f"Skipping key {key}")
            continue
        #engine_d[key] = _mask_value(value, implicit_convert)
        inner_d = dd.setdefault(ENGINE_KEY, OrderedDict())
        inner_d[key] = _mask_value(value, implicit_convert)
    return dd



def parse_flat_dict(d, implicit_convert=True):
    """
    This function can be in external use.
    It's main usage is to parse command line arguments.
    If for what ever reason, your ML is flat (like key:value in the command line arguments),
    you can use this function.

    This function assume following structure of the dict d:

    engine.cls=...,
    playera.cls=...,
    playerb.cls=...,

    By default implicit_convert is True and this function will try to guess it.

    :param d:
    :param implicit_convert: whether to guess the value type and to convert it. Default True.
    :return: ready to use dict
    """

    dd = OrderedDict()

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

        innder_d = dd.setdefault(key, OrderedDict())
        innder_d[real_key] = _mask_value(value, implicit_convert)


    return dd


def parse_sys_args(argumentParser=None, args=None):
    """
    This function can be in external use.
    This function parses command line arguments.

    :param argumentParser:
    :param args: if not None, suppresses sys.args
    :return:
    """
    if argumentParser is None:
        argumentParser = ArgumentParser()
    argumentParser.add_argument("--config_file", nargs='?', dest='config_file', default='config.ini',
                                const='config.ini')
    params, unknown_arg = argumentParser.parse_known_args(args=args)

    dd = argumentParser.as_dict(args=unknown_arg)
    dd = parse_flat_dict(dd)
    return params, dd


def parse_ini(config_file='config.ini'):
    """
    This function can be in external use.
    This function parses ini file.

    :param config_file: path to the ini file. Default value is config.ini. Can be str or os.PathLike.
    :return: dict ready to use
    """

    parser = ConfigParser()
    full_path = Path(config_file).resolve() #relative to cwd

    parser.read(full_path)
    dd = parser.as_dict()
    dd = parse_dict(dd)
    return dd

def parse_config(args=None):
    """
    This function can be in external use, but it is not intended for.
    This function parses command line arguments.
    Than it parse ini file.
    Command line arguemnts overrides ini file arguments.

    In more detail, command line arguments of the form --key=value are parsed first.
    If exists --config_file it's value is used to search for ini file.
    if --config_file is absent, 'config.ini' is used for ini file.
    If ini file is not found, only command line arguments are used.
    If ini file is found, both arguments are used, while
    command line arguments overrides ini arguments.

    :param args: if not None, suppresses sys.args
    :return: dict ready to use
    """
    params, cli_dd = parse_sys_args(args=args)
    config_dd = parse_ini(params.config_file)
    dd = OrderedDict()
    dd.update(config_dd)
    dd.update(cli_dd)
    return dd




