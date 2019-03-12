
import logging
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture()
def my_dependency():
    return 42

#@pytest.mark.ws
def test_first(my_dependency    ):
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


def test_run(request):
    logger.info(f'{request.function.__name__}()')

    from alexber.utils import LookUpEnum, AutoNameEnum
    from enum import auto
    import enum

    @enum.unique
    @addComp
    class Color(LookUpEnum, AutoNameEnum):
        RED = 'R'
        BLUE = 'B'
        GREEN = "G"

    #from typing import NoReturn

    logger.info(Color.RED)
    logger.warning('TADAM')
    logger.info(Color.comp)


# class TestSome:
#     def test_some_test(self, request):
#         logger.info(f'{request.function.__name__}()')

