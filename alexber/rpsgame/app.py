import logging.config


from alexber.rpsgame.app_create_instance import create_instance
from alexber.rpsgame.app_create_instance import importer

#TODO: Alex write unit tests
#TODO: Alex write integration tests


from alexber.rpsgame import app_conf as conf
from collections import OrderedDict


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
    from alexber.rpsgame.engine import Engine

    #filter out unrelated params without implicit_convert
    #if you want to convert values do it explictely
    kwargs = conf.parse_dict(kwargs, implicit_convert=False)

    engine_str = kwargs.pop(conf.ENGINE_KEY, None)
    if engine_str is None:
        engine_str = conf.DEFAULT_ENGINE_CLS
    engine_cls = importer(engine_str)

    playera_d = kwargs.pop(conf.PLAYER_A_KEY, None)
    playerb_d = kwargs.pop(conf.PLAYER_B_KEY, None)

    the_engine = engine_cls.from_configuration(playera_d=playera_d,
                                  playerb_d=playerb_d,
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


