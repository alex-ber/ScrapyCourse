import logging.config


from alexber.rpsgame.app_create_instance import create_instance, _checkParam

#TODO: Alex write unit tests
#TODO: Alex write integration tests


from alexber.rpsgame import app_conf as conf



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

    #TODO: engine key
    player_a = create_instance(**playera_d)
    player_b = create_instance(**playerb_d)



    the_engine = Engine(player_a=player_a,
            player_b=player_b,
            name_player_a=name_player_a,
            name_player_b=name_player_b,
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


