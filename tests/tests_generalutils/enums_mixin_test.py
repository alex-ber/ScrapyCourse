
import logging
import pytest
import enum
from enum import Enum, auto
from alexber.utils import StrAsReprMixinEnum, LookUpMixinEnum, AutoNameMixinEnum, MissingNoneMixinEnum

logger = logging.getLogger(__name__)

#
# @pytest.fixture()
# def my_dependency():
#     return 42
#
# #@pytest.mark.ws
# def test_first(my_dependency ):
#     logger.info('Testing first')
#


class TestStandardEnum(object):
    @enum.unique
    class Color1(Enum):
        RED = 10
        BLUE = 20
        GREEN = 30

    @enum.unique
    class Color2(Enum):
        RED = 'r'
        BLUE = 'b'
        GREEN = 'g'

    @enum.unique
    class Color3(Enum):
        RED = auto()
        BLUE = auto()
        GREEN = auto()


    @pytest.mark.parametrize(
        'cls,is_by_name,value',
        [
            (Color1, True, 10),
            (Color1, False, 'RED'),
            (Color2, True, 'b'),
            (Color2, False, 'BLUE'),
            (Color3, True, 3),
            (Color3, False, 'GREEN'),
        ]
    )
    def test_builtin_enumuration(self, request, cls, is_by_name, value):
        logger.info(f'{request._pyfuncitem.name}()')
        some_enum = cls(value) if is_by_name else cls[value]
        logger.info(f'name is {some_enum!r}')
        sec_enum = cls[some_enum.name]
        assert some_enum == sec_enum

        logger.debug(some_enum)
        logger.debug(f'repr is {some_enum!r}')
        logger.debug(f'str is {some_enum!s}')
        [logger.debug(f'{member!r}') for member in cls.__members__.values()]

        with pytest.raises(KeyError) as excinfo:
            cls['missing_key_here_it_is']
            # logger.debug(excinfo.value, exc_info=(excinfo.type, excinfo.value, excinfo.tb))

        with pytest.raises(ValueError) as excinfo:
            cls('missing_value_here_it_is')
            # logger.debug(excinfo.value, exc_info=(excinfo.type, excinfo.value, excinfo.tb))


class TestStrAsReprMixinEnum(object):

    @enum.unique
    class ColorStr(StrAsReprMixinEnum):
        RED = auto()
        BLUE = auto()
        GREEN = auto()

    @enum.unique
    class ColorStr2(StrAsReprMixinEnum, Enum):
        RED = auto()
        BLUE = auto()
        GREEN = auto()



    @pytest.mark.parametrize(
         'cls',
        [
            ColorStr,
            ColorStr2
        ])
    def test_StrAsReprMixinEnum(self, request, cls):
        logger.info(f'{request._pyfuncitem.name}()')
        some_enum = cls(1)
        logger.info(f'name is {some_enum!r}')
        sec_enum = cls[some_enum.name]
        assert some_enum==sec_enum

        logger.debug(some_enum)
        logger.debug(f'repr is {some_enum!r}')
        logger.debug(f'str is {some_enum!s}')
        [logger.debug(f'{member!r}') for member in cls.__members__.values()]

        assert repr(some_enum) == str(some_enum)


class TestAutoNameMixinEnum(object):
    @enum.unique
    class ColorAutoName(AutoNameMixinEnum):
        RED = auto()
        BLUE = auto()
        GREEN = auto()

    @enum.unique #AutoNameMixinEnum has to be last (see EnumMeta.__prepare__())
                 #method _generate_next_value_() will be taken from theire
    class ColorAutoName2(StrAsReprMixinEnum, AutoNameMixinEnum):
        RED = auto()
        BLUE = auto()
        GREEN = auto()

    @enum.unique #AutoNameMixinEnum has to be last (see EnumMeta.__prepare__())
    class ColorAutoNameWrong(AutoNameMixinEnum, StrAsReprMixinEnum):
        RED = auto()
        BLUE = auto()
        GREEN = auto()

    @enum.unique #AutoNameMixinEnum has to be last (see EnumMeta.__prepare__())
    class ColorAutoNameWrong2(AutoNameMixinEnum, Enum):
        RED = auto()
        BLUE = auto()
        GREEN = auto()




    @pytest.mark.parametrize(
         'cls',
        [
            ColorAutoName,
            ColorAutoName2,
        ])
    def test_AutoNameMixinEnum(self, request, cls):
        logger.info(f'{request._pyfuncitem.name}()')
        some_enum = cls('RED')
        logger.info(f'name is {some_enum!r}')
        sec_enum = cls[some_enum.name]
        assert some_enum==sec_enum

    @pytest.mark.parametrize(
         'cls,is_rep_check',
        [
            (ColorAutoNameWrong, True),
            (ColorAutoNameWrong2, False),
        ])

    def test_AutoNameWrongMixinEnum(self, request, cls, is_rep_check):
        logger.info(f'{request._pyfuncitem.name}()')

        with pytest.raises(ValueError) as excinfo:
            some_enum = cls('RED')
            logger.debug(excinfo.value, exc_info=(excinfo.type, excinfo.value, excinfo.tb))

        some_enum = cls(1)
        logger.info(f'name is {some_enum!r}')
        sec_enum = cls[some_enum.name]
        assert some_enum==sec_enum

        logger.debug(some_enum)
        logger.debug(f'repr is {some_enum!r}')
        logger.debug(f'str is {some_enum!s}')
        [logger.debug(f'{member!r}') for member in cls.__members__.values()]

        if is_rep_check:
            assert repr(some_enum) == str(some_enum)


class TestMissingNoneMixinEnum(object):

    @enum.unique
    class ColorMissingNone(MissingNoneMixinEnum):
        RED = auto()
        BLUE = auto()
        GREEN = auto()


    def test_MissingNoneEnum(self, request):
        logger.info(f'{request._pyfuncitem.name}()')

        some_enum = TestMissingNoneMixinEnum.ColorMissingNone(1)
        logger.info(f'name is {some_enum!r}')
        sec_enum = TestMissingNoneMixinEnum.ColorMissingNone[some_enum.name]
        assert some_enum==sec_enum

        with pytest.raises(KeyError) as excinfo:
            TestMissingNoneMixinEnum.ColorMissingNone[10_000]
            #logger.debug(excinfo.value, exc_info=(excinfo.type, excinfo.value, excinfo.tb))
        value = TestMissingNoneMixinEnum.ColorMissingNone(10_000)
        assert value is None
#

class TestLookUpMixinEnum(object):

    @enum.unique
    class ColorLookUp(LookUpMixinEnum):
        RED = 'r'
        BLUE = 'b'
        GREEN = 'g'

    @enum.unique
    class ColorLookUpAuto(LookUpMixinEnum, AutoNameMixinEnum):
        RED = auto()
        BLUE = auto()
        GREEN = auto()



    def test_ColorLookUp(self, request):
        logger.info(f'{request._pyfuncitem.name}()')

        some_enum = TestLookUpMixinEnum.ColorLookUp('r')
        logger.info(f'name is {some_enum!r}')
        sec_enum = TestLookUpMixinEnum.ColorLookUp[some_enum.name]
        assert some_enum == sec_enum

        with pytest.raises(KeyError) as excinfo:
            TestLookUpMixinEnum.ColorLookUp['missing_value_here_it_is']
            # logger.debug(excinfo.value, exc_info=(excinfo.type, excinfo.value, excinfo.tb))
        value = TestLookUpMixinEnum.ColorLookUp('missing_value_here_it_is')
        assert value is None

    def test_ColorLookUpAuto(self, request):
        logger.info(f'{request._pyfuncitem.name}()')

        some_enum = TestLookUpMixinEnum.ColorLookUpAuto('RED')
        logger.info(f'name is {some_enum!r}')
        sec_enum = TestLookUpMixinEnum.ColorLookUpAuto[some_enum.name]
        assert some_enum == sec_enum

        with pytest.raises(KeyError) as excinfo:
            TestLookUpMixinEnum.ColorLookUpAuto['missing_value_here_it_is']
            # logger.debug(excinfo.value, exc_info=(excinfo.type, excinfo.value, excinfo.tb))
        value = TestLookUpMixinEnum.ColorLookUpAuto('missing_value_here_it_is')
        assert value is None


class TestLookUpAutoNameMixinEnum(object):

    def addComp(enumeration):
        """Class decorator for enumerations """
        all = []
        for member in enumeration.__members__.values():
            all.append(member.value)

        enumeration.comp = all
        return enumeration

    @enum.unique
    @addComp
    class Color(LookUpMixinEnum, AutoNameMixinEnum):
        RED = 'R'
        BLUE = 'B'
        GREEN = "G"

    def test_Color(self, request):
        logger.info(f'{request._pyfuncitem.name}()')

        some_enum = TestLookUpAutoNameMixinEnum.Color('R')
        logger.info(f'name is {some_enum!r}')
        sec_enum = TestLookUpAutoNameMixinEnum.Color[some_enum.name]
        assert some_enum == sec_enum

        with pytest.raises(KeyError) as excinfo:
            TestLookUpAutoNameMixinEnum.Color['missing_value_here_it_is']
            # logger.debug(excinfo.value, exc_info=(excinfo.type, excinfo.value, excinfo.tb))
        value = TestLookUpAutoNameMixinEnum.Color('missing_value_here_it_is')
        assert value is None

        value = TestLookUpAutoNameMixinEnum.Color.comp
        assert value is not None



if __name__ == "__main__":
    pytest.main([__file__])

