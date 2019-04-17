"""
#0.5 Not Feature complete. Basic CLI, 1-round game. Immediate reporting. Different players.
Limited support for players name.
"""

import logging
_loggerDict = logging.root.manager.loggerDict

from alexber.rpsgame.engine_common import RockScissorsPaperEnum, PlayerDecorator
from alexber.rpsgame import app_conf as conf
from collections import OrderedDict
from alexber.rpsgame.app_create_instance import new_instance






class Engine(object):

    def _init(self, **kwargs):
        self.player_a = kwargs['player_a']
        self.player_b = kwargs['player_b']
        kwargs['num_iters']


    @classmethod
    def from_instance(cls, player_a=None, player_b=None,
                     name_player_a=None,  name_player_b=None,
                      num_iters=1,
                      **kwargs):
        if player_a is None and player_b is None:
            raise ValueError("Both player's can't be None")

        if player_a is None:
            player_a = new_instance(conf.DEFAULT_PLAYER_CLS)

        if player_b is None:
            player_b = new_instance(conf.DEFAULT_PLAYER_CLS)


        player_a = PlayerDecorator(name_player=name_player_a,
                                   default_name=conf.DEFAULT_NAME_PLAYER_A,
                                   player=player_a)
        player_b = PlayerDecorator(name_player=name_player_b,
                                   default_name=conf.DEFAULT_NAME_PLAYER_B,
                                   player=player_b)

        engine_d = OrderedDict(kwargs)
        engine_d['player_a'] = player_a
        engine_d['player_b'] = player_b
        engine_d['num_iters'] = num_iters
        self = object.__new__(cls)
        cls._init(self, **engine_d)
        return self

    @classmethod
    def from_configuration(cls,
                     playera_factory, playerb_factory,
                      num_iters=1,
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

        name_player_a, player_a = playera_factory()
        name_player_b, player_b = playerb_factory()


        ret = cls.from_instance(player_a=player_a,
                                player_b=player_b,
                                name_player_a=name_player_a,
                                name_player_b=name_player_b,
                                num_iters=num_iters,
                                **kwargs
                               )
        return ret

    def play(self):
        resulta = self.player_a.move()
        resultb = self.player_b.move()

        self.player_a.started()
        self.player_b.started()

        logging.debug(f"{self.player_a.name} answer's is {resulta}")
        logging.debug(f"{self.player_b.name} answer's is {resultb}")

        if resulta==resultb:
            #FUTURE: send as event to players
            logging.info("draw!")
        else:
            b = resulta>resultb
            str =    f"{self.player_a.name} wins, {self.player_b.name} lose" if b \
                else f"{self.player_b.name} wins, {self.player_a.name} lose"
            logging.info(str)

        self.player_a.completed()
        self.player_b.completed()
