"""
#0.5 Not Feature complete. Basic CLI, 1-round game. Immediate reporting. Different players.
Limited support for players name.
"""

import logging
_loggerDict = logging.root.manager.loggerDict

from alexber.rpsgame.engine_common import RockScissorsPaperEnum
from alexber.rpsgame import app_conf as conf
from collections import OrderedDict
from alexber.rpsgame.app_create_instance import new_instance


class Engine(object):
    # #FUTURE: add name supports
    def __init__(self, **kwargs):
        self.name_player_a = kwargs['name_player_a']
        self.name_player_b = kwargs['name_player_b']

        self.player_a = kwargs['player_a']
        self.player_b = kwargs['player_b']
        kwargs['num_iters']
        kwargs['id']

    @classmethod
    def from_instance(cls, player_a=None, player_b=None,
                     name_player_a=conf.DEFAULT_NAME_PLAYER_A,  name_player_b=conf.DEFAULT_NAME_PLAYER_B,
                      num_iters=1,
                      id=None,
                      **kwargs):
        if player_a is None and player_b is None:
            raise ValueError("Both player's can't be None")

        if player_a is None:
            player_a = new_instance(conf.DEFAULT_PLAYER_CLS)

        if player_b is None:
            player_b = new_instance(conf.DEFAULT_PLAYER_CLS)

        if name_player_a is None:
            name_player_a = conf.DEFAULT_NAME_PLAYER_A

        if name_player_b is None:
            name_player_b = conf.DEFAULT_NAME_PLAYER_B


        engine_d = OrderedDict(kwargs)
        engine_d['player_a'] = player_a
        engine_d['player_b'] = player_b
        engine_d['name_player_a'] = name_player_a
        engine_d['name_player_b'] = name_player_b
        engine_d['num_iters'] = num_iters
        engine_d['id'] = id
        self = object.__new__(cls)
        cls.__init__(self, **engine_d)
        return self

    @classmethod
    def from_configuration(cls,
                     playera_factory, playerb_factory,
                      num_iters=1,
                      id=None,
                     **kwargs):
        """
        NOTE: that factory for player's instantiation are DI agnostic.
        Player's name can be None. In such case, default name will be used.

        :param playera_factory: factory method that will instantiate Player A.It should return player's name and player.
        :param playerb_factory: factory method that will instantiate Player B.It should return player's name and player.
        :param num_iters: Number of iteration to play.
        :param kwargs:
        :return:
        """
        if playera_factory is None:
            raise ValueError("playera_factory can't be None")
        if playerb_factory is None:
            raise ValueError("playerb_factory can't be None")

        # FUTURE: consult with player what is his name (optional method/property name)
        name_player_a, player_a = playera_factory()
        name_player_b, player_b = playerb_factory()


        ret = cls.from_instance(player_a=player_a,
                                player_b=player_b,
                                name_player_a=name_player_a,
                                name_player_b=name_player_b,
                                num_iters=num_iters,
                                id=id,
                                **kwargs
                               )
        return ret

    def play(self):
        #FUTURE: make adapder for call to move() method
        answera = self.player_a.move()
        answerb = self.player_b.move()
        #FUTURE: send as event to players
        logging.debug(f"{self.name_player_a} answer's is {answera}")
        logging.debug(f"{self.name_player_b} answer's is {answerb}")
        #FUTURE: make adapder for call to move() method
        resulta = RockScissorsPaperEnum(answera)
        if resulta is None:
            raise ValueError(f'Unexpected move {answera}')
        resultb = RockScissorsPaperEnum(answerb)
        if resultb is None:
            raise ValueError(f'Unexpected move {answerb}')
        if resulta==resultb:
            #FUTURE: send as event to players
            logging.info("draw!")
        else:
            b = resulta>resultb
            str =    f"{self.name_player_a} wins, {self.name_player_b} lose" if b \
                else f"{self.name_player_b} wins, {self.name_player_a} lose"
            logging.info(str)
