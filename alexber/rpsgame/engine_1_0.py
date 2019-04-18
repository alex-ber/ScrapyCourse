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
from collections import deque
from alexber.rpsgame.players import StartedMixin, RoundResultMixin, CompletedMixin

class DefaultListener(StartedMixin, RoundResultMixin, CompletedMixin):
    def started(self, **kwargs):
        a_d = kwargs['A']
        b_d = kwargs['B']
        length = kwargs['num_iters']

        self.player_a_name = a_d['name']
        self.player_b_name = b_d['name']
        self.events = deque(maxlen=length)

    def completed(self, **kwargs):
        for i, event in enumerate(self.events):
            logging.debug(f"***************** Round {i} ***************")
            self._print_result(**event)

    def _print_result(self, **event):
        round_result_a_d = event["A"]
        round_result_b_d = event["B"]

        movea = round_result_a_d['move']
        moveb = round_result_b_d['move']
        resulta = round_result_a_d['result']
        resultb = round_result_b_d['result']

        logging.debug(f"{self.player_a_name} answer's is {movea}")
        logging.debug(f"{self.player_b_name} answer's is {moveb}")

        if resulta == resultb:
            logging.info("draw!")
        else:
            b = resulta > resultb
            str = f"{self.player_a_name} wins, {self.player_b_name} lose" if b \
                else f"{self.player_b_name} wins, {self.player_a_name} lose"
            logging.info(str)

    def round_result(self, **kwargs):
        self.events.append(kwargs)


class Engine(object):

    def _init(self, **kwargs):
        self.player_a = kwargs['player_a']
        self.player_b = kwargs['player_b']

        self.listeners = [DefaultListener(), self.player_a, self.player_b]

        self.num_iters = kwargs['num_iters']


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
                                   technical_name = 'A',
                                   player=player_a)
        player_b = PlayerDecorator(name_player=name_player_b,
                                   default_name=conf.DEFAULT_NAME_PLAYER_B,
                                   technical_name='B',
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
        started_event = OrderedDict()
        started_result_a = started_event.setdefault(self.player_a.technical_name, OrderedDict())
        started_result_b = started_event.setdefault(self.player_b.technical_name, OrderedDict())
        started_result_a['name'] = self.player_a.name_player
        started_result_b['name'] = self.player_b.name_player
        started_event['num_iters'] = self.num_iters

        #TODO: Alex make ListenerSupport
        for listener in self.listeners:
            listener.started(**started_event)

        for i in range(self.num_iters):
            round_result_event = OrderedDict()
            round_result_event['iter'] = i
            round_result_a = round_result_event.setdefault(self.player_a.technical_name, OrderedDict())
            round_result_b = round_result_event.setdefault(self.player_b.technical_name, OrderedDict())

            resulta = self.player_a.move()
            resultb = self.player_b.move()

            round_result_a['move'] = resulta
            round_result_b['move'] = resultb

            if resulta == resultb:
                round_result_a['result'] = 0
                round_result_b['result'] = 0
            else:
                b = resulta > resultb
                if b:
                    round_result_a['result'] = 1
                    round_result_b['result'] = 0
                else:
                    round_result_a['result'] = 0
                    round_result_b['result'] = 1

            for listener in self.listeners:
                listener.round_result(**round_result_event)

        # TODO: Alex make ListenerSupport
        completed_event = OrderedDict()
        for listener in self.listeners:
            listener.completed(**completed_event)



