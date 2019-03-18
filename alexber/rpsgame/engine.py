# import logging
# _loggerDict = logging.root.manager.loggerDict
#
# #if logger is not configured
# if _loggerDict is None or not _loggerDict: #is None or {}
#     raise ValueError('Please configure logger first. '+\
#                      'This engine is useless without proper logger configuration.\n'+\
#                      'See https://docs.python.org/3/howto/logging.html#configuring-logging '+\
#                      'for details')
# del _loggerDict


#from functools import singledispatch
from multidispatch import multimethod
from mock.mock import _importer as importer


class Engine(object):


    @multimethod(object)
    def _set_playerA(self, player):
        print('fallback')
        pass

    @_set_playerA.dispatch(str)
    def _(self, st):
        player_cls = importer(st)
        player = player_cls()
        player.say()
        pass

    playerA = property(fset=_set_playerA)

class Player(object):
    def say(self):
        print('hello')

engine = Engine()
#engine.playerA='osx'
engine.playerA='__main__.Player'