import logging.config

import inspect
from alexber.utils.importer import new_instance
from alexber.utils.inpsects import issetdescriptor, issetmethod

#only for namepsace definitin
class conf(object):
    from alexber.rpsgame.app_conf import parse_sys_args, parse_ini, parse_config, \
        parse_flat_dict, parse_dict, \
        PLAYER_A_KEY, PLAYER_B_KEY, \
        NAME_PLAYER_A_KEY, NAME_PLAYER_B_KEY, \
        DEFAULT_NAME_PLAYER_A, DEFAULT_NAME_PLAYER_B, \
        PLAYER_CLS_KEY
    pass

def _checkParam(obj, key):
    if (obj is None):
        ValueError(f"run() expectes paramater {key}")

def _inject_properties(player, **kwargs):
    #__new__() could subsitute __class__, so re-evaluate it
    plcls = type(player)
    # finding @property.fset
    results = inspect.getmembers(plcls, predicate=issetdescriptor)
    d = {key: value for (key, value) in results}

    prop = None
    prop_setter = None

    for name, value in kwargs.items():
        if name.startswith("property."):
            name = name[len("property."):]

        if name in d:
            prop = d[name]  #safe, TODO: futher split of name needed?
            prop_setter = prop.fset #fset has default value of None
            if prop_setter is not None:
                prop_setter(self=player, value=value)

#undocumented feature: you can actually call any method with 1 parameter
def _inject_setters(player, **kwargs):
    #__new__() could subsitute __class__, so re-evaluate it
    plcls = type(player)
    # finding @property.fset
    results = inspect.getmembers(plcls, predicate=issetmethod)
    d = {key: value for key, value in results}

    prop = None
    prop_setter = None

    for name, value in kwargs.items():
        if name.startswith("set."):
            name = name[len("set."):]

        if name in d:
            setter = d[name]  #safe, TODO: futher split of name needed?
            if setter is not None: #just in case
                setter(self=player, value=value)


def create_player(**kwargs):
    '''This is mini DI Framework.
    https://pythonhosted.org/injector/ was consider and rejected
    as overcomplicated for defying players
    '''
    plcls = kwargs.get(conf.PLAYER_CLS_KEY, None)
    _checkParam(plcls, conf.PLAYER_CLS_KEY)
    del kwargs[conf.PLAYER_CLS_KEY]

    player = new_instance(plcls, **kwargs)
    _inject_properties(player, **kwargs)
    _inject_setters(player, **kwargs)

    return player


def run(**kwargs):
    from alexber.rpsgame.engine import Engine

    playera_d = kwargs.get(conf.PLAYER_A_KEY, None)
    _checkParam(playera_d, conf.PLAYER_A_KEY)
    del kwargs[conf.PLAYER_A_KEY]

    name_player_a = playera_d.setdefault(conf.NAME_PLAYER_A_KEY,
                                         conf.DEFAULT_NAME_PLAYER_A)

    playerb_d = kwargs.get(conf.PLAYER_B_KEY, None)
    _checkParam(playerb_d, conf.PLAYER_B_KEY)
    del kwargs[conf.PLAYER_B_KEY]

    name_player_b = playerb_d.setdefault(conf.NAME_PLAYER_B_KEY,
                                         conf.DEFAULT_NAME_PLAYER_B)

    player_a = create_player(**playera_d)
    player_b = create_player(**playerb_d)



    the_engine = Engine(player_a=player_a,
            player_b=player_b,
            name_player_a=name_player_a,
            name_player_b=name_player_b,
            **kwargs)
    the_engine.play()


def main(args=None):
    dd = conf.parse_config(args)
    run(**dd)


#see https://terryoy.github.io/2016/05/short-ref-python-logging.html
_config = {
        "log_config": {
            "version": 1,
            "formatters": {
                "brief": {
                    "format": "%(message)s",
                },
                "detail": {
                    "format": "%(asctime)-15s %(levelname)s [%(name)s.%(funcName)s] %(message)s",
                    "datefmt": '%Y-%m-%d %H:%M:%S',
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "brief",
                },
                # "file": {
                #     "class": "logging.handlers.RotatingFileHandler",
                #     "filename": "dev.log",
                #     "level": "DEBUG",
                #     "formatter": "detail",
                # },
            },
            "root": {
                # "handlers": ["console", "file"],
                "handlers": ["console"],
                "level": "DEBUG",
            },
            "loggers": {
                "requests": {
                    # "handlers": ["file"],
                    "handlers": ["console"],
                    "level": "DEBUG",
                    "propagate": False,
                }
            },
        },
    }


if __name__ == '__main__':
    logging.config.dictConfig(_config["log_config"])
    del _config
    logger = logging.getLogger(__name__)
    main()
