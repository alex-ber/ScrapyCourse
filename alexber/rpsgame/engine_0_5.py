"""
#0.5 Not Feature complete. Basic CLI, 1-round game. Immediate reporting. Different players.
Limited support for players name.
"""

import logging
_loggerDict = logging.root.manager.loggerDict

from alexber.rpsgame.engine_common import RockScissorsPaperEnum
from alexber.rpsgame import app_conf as conf
from alexber.rpsgame.app_create_instance import create_instance
from collections import OrderedDict

#TODO: Alex write unit tests
#TODO: Alex write integration tests

class Engine(object):
    # #FUTURE: add name supports
    def __init__(self, **kwargs):
        # FUTURE: consult with player what is his name (optional method/property name)
        self.name_player_a = kwargs['name_player_a']
        self.name_player_b = kwargs['name_player_b']

        self.player_a = kwargs['player_a']
        self.player_b = kwargs['player_b']
        kwargs['num_iters']

    @classmethod
    def from_instance(cls, player_a=None, player_b=None,
                     name_player_a=conf.DEFAULT_NAME_PLAYER_A,  name_player_b=conf.DEFAULT_NAME_PLAYER_B,
                      num_iters=1,
                      **kwargs):
        if player_a is None and player_b is None:
            raise ValueError("Both player's can't be None")

        if player_a is None:
            player_a = conf.DEFAULT_PLAYER_CLS()

        if player_b is None:
            player_b = conf.DEFAULT_PLAYER_CLS()


        engine_d = OrderedDict(kwargs)
        engine_d['player_a'] = player_a
        engine_d['player_b'] = player_b
        engine_d['name_player_a'] = name_player_a
        engine_d['name_player_b'] = name_player_b
        engine_d['num_iters'] = num_iters
        self = object.__new__(cls)
        cls.__init__(self, **engine_d)
        return self

    @classmethod
    def from_configuration(cls, playera_d, playerb_d,
                     playera_factory=create_instance, playerb_factory=create_instance,
                      num_iters=1,
                     **kwargs):

        is_blank_playera_d = playera_d is None or not playera_d
        is_blank_playerb_d = playerb_d is None or not playerb_d

        if is_blank_playera_d and is_blank_playerb_d:
            raise ValueError("Both players can't be empty")

        if is_blank_playera_d:
            playera_d = OrderedDict()
            playera_d[conf.CLS_KEY] = conf.DEFAULT_PLAYER_CLS

        if is_blank_playerb_d:
            playerb_d = OrderedDict()
            playerb_d[conf.CLS_KEY] = conf.DEFAULT_PLAYER_CLS

        name_player_a = playera_d.get(conf.NAME_PLAYER_A_KEY, None)
        if name_player_a is None:
            name_player_a = conf.DEFAULT_NAME_PLAYER_A

        name_player_b = playerb_d.get(conf.NAME_PLAYER_B_KEY, None)
        if name_player_b is None:
            name_player_b = conf.DEFAULT_NAME_PLAYER_B


        player_a = playera_factory(**playera_d)
        player_b = playerb_factory(**playerb_d)

        ret = cls.from_instance(player_a=player_a,
                               player_b=player_b,
                               name_player_a=name_player_a,
                               name_player_b=name_player_b,
                               num_iters=num_iters,
                               **kwargs
                               )
        return ret

    def play(self):
        #FUTURE: make adapder for call to move() method
        answera = self.player_a.move()
        answerb = self.player_b.move()
        #FUTURE: send as event to players
        logging.debug(f"playera answer's is {answera}")
        logging.debug(f"playerb answer's is {answerb}")
        logging.debug(answerb)
        #FUTURE: make adapder for call to move() method
        resulta = RockScissorsPaperEnum(answera)
        resultb = RockScissorsPaperEnum(answerb)
        if resulta==resultb:
            #FUTURE: send as event to players
            logging.info("draw!")
        else:
            b = resulta>resultb
            #FUTURE: change to use player's names
            str =    f"{self.name_player_a} wins, {self.name_player_b} lose" if b \
                else f"{self.name_player_b} wins, {self.name_player_a} lose"
            logging.info(str)
