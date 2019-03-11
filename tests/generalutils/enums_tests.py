
import logging

logger = logging.getLogger(__name__)



def test_first():
    logger.info('Testing first')

def test_second():
    print('Testing')


def addComp(enumeration):
    """Class decorator for enumerations """
    all = []
    for member in enumeration.__members__.values():
        all.append(member.value)

    enumeration.comp = all
    return enumeration

def test_run():
    logger.info('hello %s', 'world')

    from alexber.utils import LookUpEnum, AutoNameEnum
    from enum import auto
    import enum

    @enum.unique
    @addComp
    class Color(LookUpEnum, AutoNameEnum):
        RED = 'R'
        BLUE = 'B'
        GREEN = "G"




    logger.info(Color.RED)
    logger.warning('TADAM')
    logger.info(Color.comp)

