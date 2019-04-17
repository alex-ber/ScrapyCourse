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
from .players import get_attr, PlayMixin as _PlayMixin, StartedMixin as _StartedMixin, \
    CompletedMixin as _CompletedMixin, \
    NamedMixin as _NamedMixin

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




class PlayMixin(_PlayMixin):
    def __init__(self, player, **kwargs):
        self.player_move = player.move
        #consume player
        super().__init__(**kwargs)

    def move(self):
        answera = self.player_move()
        resulta = RockScissorsPaperEnum(answera)
        if resulta is None:
            raise ValueError(f'Unexpected move {answera}')
        return resulta


def _init_mixin(self, player, mixincls, methodname):
    mixincls.register(player)
    b = isinstance(player, mixincls)
    attr_name = f'player_{methodname}'
    if b:
        attr_value = get_attr(player, methodname)
    else:
        attr_value = None

    setattr(self, attr_name, attr_value)


class NamedMixin(object):
    def __init__(self, name_player, default_name, player, **kwargs):
        _NamedMixin.register(player)
        # consult player_a first
        b = isinstance(player, _NamedMixin)
        if b:
            name_player = get_attr(player, 'name')
        # name_player_a is still not resolved
        if name_player is None:
            name_player = default_name

        self.name_player = name_player

        kwargs['player'] = player
        super().__init__(**kwargs)

    @property
    def name(self):
        return self.name_player


class StartedMixin(object):
    def __init__(self, player, **kwargs):
        _init_mixin(self, player, mixincls=_StartedMixin, methodname='started')
        kwargs['player'] = player
        super().__init__(**kwargs)

    def started(self, **kwargs):
        if self.player_started is not None:
            self.player_started()


class CompletedMixin(object):
    def __init__(self, player, **kwargs):
        _init_mixin(self, player, mixincls=_CompletedMixin, methodname='completed')
        kwargs['player'] = player
        super().__init__(**kwargs)

    def completed(self, **kwargs):
        if self.player_completed is not None:
            self.player_completed()

class PlayerDecorator(NamedMixin, StartedMixin, CompletedMixin, PlayMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)




