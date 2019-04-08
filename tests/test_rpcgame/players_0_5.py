import logging
logger = logging.getLogger(__name__)


from alexber.utils import LookUpMixinEnum, enum


def _compare(enumeration):
    """Class decorator for enumerations """

    enums = [None]
    for member in enumeration.__members__.values():
        enums.append(member)

    MAXIMUM = 1
    ROCK = 2
    PAPER = 3
    SCISSORS = 4

    #S<=R
    #P<=S
    #R<=P
    #S<=S
    #P<=P
    #R<=R

    #we can't reference RockScissorsPaperEnum by name
    #it is not yet defined
    enumeration._le_r = frozenset([
        (enums[SCISSORS], enums[ROCK]),
        (enums[PAPER], enums[SCISSORS]),
        (enums[ROCK], enums[PAPER]),

        (enums[SCISSORS], enums[MAXIMUM]),
        (enums[PAPER], enums[MAXIMUM]),
        (enums[ROCK], enums[MAXIMUM]),

        (enums[ROCK], enums[ROCK]),
        (enums[PAPER], enums[PAPER]),
        (enums[SCISSORS], enums[SCISSORS]),
    ])
    return enumeration

@_compare
@enum.unique
class _HackedEnum(LookUpMixinEnum):
    MAXIMUM = 'Z'
    ROCK = 'R'
    SCISSORS = 'S'
    PAPER = 'P'


    def __ge__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented
        b = self == other or self > other
        return b

    def __gt__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented
        b = self <= other
        return not b

    def __le__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented
        b = (self, other) in self._le_r
        return b

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented
        b = self != other and self <= other
        return b

class HackerPlayer(object):

    def __init__(self):
        from alexber.rpsgame import engine_0_5 as engine
        setattr(engine, 'RockScissorsPaperEnum', _HackedEnum)
        pass

    def move(self):
        return 'Z'



