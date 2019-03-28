import logging.config

import inspect
from alexber.utils.importer import new_instance
from alexber.utils.inpsects import issetdescriptor, issetmethod
from alexber.rpsgame.app_create_player import create_player

#TODO: Alex write unit tests
#TODO: Alex write integration tests


#only for namepsace definition
class conf(object):
    from alexber.rpsgame.app_conf import parse_dict, parse_flat_dict, \
        parse_sys_args, parse_ini, parse_config, \
        PLAYER_CLS_KEY, NAME_PLAYER_A_KEY, NAME_PLAYER_B_KEY, \
        PLAYER_A_KEY, PLAYER_B_KEY, DEFAULT_NAME_PLAYER_A, DEFAULT_NAME_PLAYER_B
    pass

def _checkParam(obj, key):
    if (obj is None):
        ValueError(f"run() expectes paramater {key}")


def run(**kwargs):
    from alexber.rpsgame.engine import Engine

    #filter out unrelated params without implicit_convert
    #if you want to convert values do it explictely
    kwargs = conf.parse_dict(kwargs, implicit_convert=False)

    playera_d = kwargs.pop(conf.PLAYER_A_KEY, None)
    _checkParam(playera_d, conf.PLAYER_A_KEY)

    name_player_a = playera_d.get(conf.NAME_PLAYER_A_KEY, None)
    if name_player_a is None:
        name_player_a = conf.DEFAULT_NAME_PLAYER_A

    playerb_d = kwargs.pop(conf.PLAYER_B_KEY, None)
    _checkParam(playerb_d, conf.PLAYER_B_KEY)

    name_player_b = playera_d.get(conf.NAME_PLAYER_B_KEY, None)
    if name_player_b is None:
        name_player_b = conf.DEFAULT_NAME_PLAYER_B

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


