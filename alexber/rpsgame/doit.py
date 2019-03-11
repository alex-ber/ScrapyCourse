import logging

logger = logging.getLogger(__name__)

def run():
    logger.info('hello %s', 'world')

    from .utils import LookUpEnum

    class Color(LookUpEnum):
        RED = 'red',
        BLUE = 'blue',
        GREEN = 'green'

    logger.info(Color.RED)
    logger.warning('TADAM')
