import logging
logger = logging.getLogger(__name__)

import pytest
import datetime

from collections.abc import Iterable
from alexber.rpsgame.players import ConstantPlayer, RandomPlayer, CryptoRandomPlayer, HumanPlayer, HumanValidPlayer
from alexber.rpsgame.engine import RockScissorsPaperEnum as RPS
from alexber.utils import LookUpMixinEnum, enum
from collections import Counter

def test_constant_player(request):
    logger.info(f'{request._pyfuncitem.name}()')

    exp_move = 'Z'
    player = ConstantPlayer(exp_move)
    move = player.move()

    assert exp_move==move

#TODO: Alex more ConstantPlayer unit-tests


def get_epochtime_ms():
    return round(datetime.datetime.utcnow().timestamp() * 1000)

_player_random_limit = 1_000

@pytest.mark.parametrize(
    'seed',
    [
	 (100),
     (2000),
	 (get_epochtime_ms()),
     ]
)
def test_random_player(request, seed):
    logger.info(f'{request._pyfuncitem.name}()')
    exp_player = RandomPlayer(seed)
    exp_result = [exp_player.move() for _ in range(_player_random_limit)]

    player2 = RandomPlayer(seed)
    result2 = [player2.move() for _ in range(_player_random_limit)]
    assert exp_result==result2

@enum.unique
class ResultEnum(LookUpMixinEnum):
    LOSE_PLAYER_A = 0.0
    DRAW = 0.5
    WIN_PLAYER_A = 1.0



def _comp(move1, move2):
    enum1 = RPS(move1)
    enum2 = RPS(move2)
    if enum1==enum2:
        return ResultEnum.DRAW
    if enum1>enum2:
        return ResultEnum.WIN_PLAYER_A
    return ResultEnum.LOSE_PLAYER_A



_player_crypto_limit = 1_000 -1

def test_crypto_random_player(request):
    logger.info(f'{request._pyfuncitem.name}()')

    random_player = RandomPlayer()
    crypto_player = CryptoRandomPlayer()

    result = [_comp(crypto_player.move(), random_player.move()) for _ in range(_player_crypto_limit)]
    counter = Counter(result)
    crypto_wins =  counter[ResultEnum.WIN_PLAYER_A]
    random_wins = counter[ResultEnum.LOSE_PLAYER_A]
    draws = counter[ResultEnum.DRAW]
    pytest.assume(crypto_wins > 300)
    pytest.assume(random_wins > 300)
    pytest.assume(draws > 300)

def test_input(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    exp_move = 'Z'
    mocker.patch('alexber.rpsgame.players_simple.input', return_value=exp_move, create=True)

    humanPlayer = HumanPlayer()
    move  = humanPlayer.move()

    assert exp_move==move

_TEST_VALID_SEQUENCE = ['U', 'W', 'W', 'X', 'Y', 'Z', RPS.PAPER.value]

def test_input_valid_without_limitation(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    humanPlayer = HumanValidPlayer(num_retry=None)

    exp_move = _TEST_VALID_SEQUENCE[-1]
    mocker.patch('alexber.rpsgame.players_simple.input', side_effect=_TEST_VALID_SEQUENCE, create=True)

    move = humanPlayer.move()

    assert exp_move == move

@pytest.mark.parametrize(
    'limit',
    [
	 (1),
     (2),
	 (3),
     (4),

     ]
)
def test_input_valid(request, mocker, limit):
    logger.info(f'{request._pyfuncitem.name}()')

    humanPlayer = HumanValidPlayer(num_retry=limit)

    exp_move = _TEST_VALID_SEQUENCE[-1]
    mocker.patch('alexber.rpsgame.players_simple.input', side_effect=_TEST_VALID_SEQUENCE[-limit:], create=True)

    move = humanPlayer.move()

    assert exp_move == move


if __name__ == "__main__":
    pytest.main([__file__])
