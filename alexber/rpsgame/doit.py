import logging.config

logger = logging.getLogger(__name__)

def run():
    logger.info(__name__)
    logger.info('hello %s', 'world')
    # try:
    #     raise ValueError("%r is not a valid %s" % ('value', 'cls.__name__'))
    # except ValueError as e:
    #     logger.info("Houston, we have a %s", "interesting problem", exc_info=e)

    #from alexber.rpsgame.utils.stuff import LookUpEnum
    from .utils import LookUpEnum

    class Color(LookUpEnum):
        RED = 'red',
        BLUE = 'blue',
        GREEN = 'green'

    logger.info(Color.RED)
