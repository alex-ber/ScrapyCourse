import logging
_loggerDict = logging.root.manager.loggerDict

from alexber.rpsgame.engine_common import RockScissorsPaperEnum

#TODO: Alex write unit tests
#TODO: Alex write integration tests


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
