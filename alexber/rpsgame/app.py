import logging.config

from alexber.rpsgame import app_conf as conf
from alexber.rpsgame.app_create_instance import importer, create_instance
from collections import OrderedDict
from alexber.utils import uuid1mc

def _create_player_factory(player_d):
    assert player_d is not None
    def factory_player():
        name_player = player_d.get(conf.NAME_PLAYER_KEY, None)
        player = create_instance(**player_d)
        return name_player, player

    return factory_player

def _mask_engine_params(engine_d):
    d = OrderedDict()

    for name, value in engine_d.items():
        if not name.startswith("init."):
            logger.debug(f"Skipping {name}, doesn't have prefix 'init'")
            continue

        real_name = name[len("init."):]
        d[real_name] = value
    return d


def run(**kwargs):
    """
    This method recieved all conf params in kwargs.
    All unexpected values will be ignored.
    It is expected that value type is correct.
    No conversion on the value of the dict kwargs will be applied.
    This method will built playerA, playerB, engine,
    and run engine with these players.

    Please, consult alexber.rpsgame.app_conf in order to construct kwargs.
    Command-line argument and ini-file are suppored out of the box.
    JSON/YML, etc. can be easiliy handled also.
    """

    #filter out unrelated params without implicit_convert
    #if you want to convert values do it explictely
    kwargs = conf.parse_dict(kwargs, implicit_convert=False)

    engine_d = kwargs.pop(conf.ENGINE_KEY, {})
    engine_str = engine_d.pop(conf.CLS_KEY, None)

    if engine_str is None:
        engine_str = conf.DEFAULT_ENGINE_CLS
    engine_cls = importer(engine_str)
    p_engine_d = _mask_engine_params(engine_d)

    kwargs.update(p_engine_d)

    playera_d = kwargs.pop(conf.PLAYER_A_KEY, {})
    playerb_d = kwargs.pop(conf.PLAYER_B_KEY, {})

    the_engine = engine_cls.from_configuration(playera_factory=_create_player_factory(playera_d),
                                               playerb_factory=_create_player_factory(playerb_d),
                                  **kwargs)
    the_engine.play()





def main(args=None):
    """
    main method
    :param args: if not None, suppresses sys.args
    """
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


