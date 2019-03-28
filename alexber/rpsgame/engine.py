import logging
_loggerDict = logging.root.manager.loggerDict

#if logger is not configured
if _loggerDict is None or not _loggerDict: #is None or {}
    raise ValueError('Please configure logger first. '+\
                     'This engine is useless without proper logger configuration.\n'+\
                     'See https://docs.python.org/3/howto/logging.html#configuring-logging '+\
                     'for details')
del _loggerDict

from alexber.utils import LookUpMixinEnum, Enum
import enum

#TODO: Alex write unit tests
#TODO: Alex write integration tests

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



class Engine(object):
    #TODO: add name supports
    def __init__(self, **kwargs):
        # TODO: consult with player what is his name (optional method/property name)
        self.name_player_a = kwargs['name_player_a']
        self.name_player_b = kwargs['name_player_b']

        self.player_a = kwargs['player_a']
        self.player_b = kwargs['player_b']


    def play(self):
        #TODO: make adapder for call to move() method
        answera = self.player_a.move()
        answerb = self.player_b.move()
        #TODO: send as event to players
        logging.debug(f"playera answer's is {answera}")
        logging.debug(f"playerb answer's is {answerb}")
        logging.debug(answerb)
        #TODO: make adapder for call to move() method
        resulta = RockScissorsPaperEnum(answera)
        resultb = RockScissorsPaperEnum(answerb)
        if resulta==resultb:
            # TODO: send as event to players
            logging.info("draw!")
        else:
            b = resulta>resultb
            #TODO: change to use player's names
            str =    f"{self.name_player_a} wins, {self.name_player_b} lose" if b \
                else f"{self.name_player_b} wins, {self.name_player_a} lose"
            logging.info(str)




