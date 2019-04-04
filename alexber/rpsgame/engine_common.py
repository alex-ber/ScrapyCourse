import logging
_loggerDict = logging.root.manager.loggerDict

#if logger is not configured
if _loggerDict is None or not _loggerDict: #is None or {}
    raise ValueError('Please configure logger first. '+\
                     'This engine is useless without proper logger configuration.\n'+\
                     'See https://docs.python.org/3/howto/logging.html#configuring-logging '+\
                     'for details')
del _loggerDict

from alexber.utils import LookUpMixinEnum, Enum, enum



class _OrderedEnum(Enum):

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

def _compare(enumeration):
    """Class decorator for enumerations """

    enums = [None]
    for member in enumeration.__members__.values():
        enums.append(member)

    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    #we can't reference RockScissorsPaperEnum by name
    #it is not yet defined
    enumeration._le_r = frozenset([
        (enums[ROCK], enums[SCISSORS]),
        (enums[SCISSORS], enums[PAPER]),
        (enums[PAPER], enums[ROCK]),

        (enums[ROCK], enums[ROCK]),
        (enums[PAPER], enums[PAPER]),
        (enums[SCISSORS], enums[SCISSORS]),
    ])
    return enumeration


#R>S rock crushes scissors
#S>P scissors cuts paper
#P>R paper covers rock
@_compare
@enum.unique
class RockScissorsPaperEnum(LookUpMixinEnum, _OrderedEnum):
    ROCK = 'R'
    SCISSORS = 'S'
    PAPER = 'P'

# TypeError: Cannot extend enumerations
# Player can't hacked in RockScissorsPaperEnum, so I leave it public
#class HackedEum(RockScissorsPaperEnum):
#    INVALID = 'X'


