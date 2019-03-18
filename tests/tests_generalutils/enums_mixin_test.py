
import logging
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture()
def my_dependency():
    return 42

#@pytest.mark.ws
def test_first(my_dependency ):
    logger.info('Testing first')
    from collections import OrderedDict


@pytest.fixture(params=[
    # tuple with (input, expectedOutput)
    ('regular text', 'regular text</p>'),
    ('*em tags*', '<p><em>em tags</em></p>'),
    ('**strong tags**', '<p><strong>strong tags</em></p>')
])
def test_data(request):
    return request.param


def test_markdown(test_data):
    (the_input, the_expected_output) = test_data
    def run_markdown(x):
        return x

    the_output = run_markdown(the_input)
    #assert the_output == the_expected_output

def test_second(mocker):
    print('Testing')
    mocked_isfile = mocker.patch('os.path.isfile')
    print(mocked_isfile)
    print(type(mocked_isfile))
    #import mock.mock._imported as imported



def addComp(enumeration):
    """Class decorator for enumerations """
    all = []
    for member in enumeration.__members__.values():
        all.append(member.value)

    enumeration.comp = all
    return enumeration


def test_run(request):
    logger.info(f'{request.function.__name__}()')

    from alexber.utils import LookUpMixinEnum, AutoNameMixinEnum
    from enum import auto
    import enum

    @enum.unique
    @addComp
    class Color(LookUpMixinEnum, AutoNameMixinEnum):
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


if __name__ == "__main__":
    pytest.main([__file__])