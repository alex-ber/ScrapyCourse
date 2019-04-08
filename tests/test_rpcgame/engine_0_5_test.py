import logging
logger = logging.getLogger(__name__)

import pytest

from alexber.rpsgame.engine_0_5 import Engine
from alexber.rpsgame import app_conf
from alexber.rpsgame.players import ConstantPlayer
from alexber.utils import LookUpMixinEnum, enum
from alexber.rpsgame.engine import RockScissorsPaperEnum as RPS
from alexber.rpsgame.app import main as rpsgame_app_main
from .players_0_5 import HackerPlayer


@enum.unique
class ResultEnum(LookUpMixinEnum):
    LOSE_PLAYER_A = 0.0
    DRAW = 0.5
    WIN_PLAYER_A = 1.0



def _player_factory(name, player=object()):
    ret = lambda : (name, player)
    return ret


@pytest.mark.parametrize(
    'name_a, name_b, exp_name_a, exp_name_b',
    [('John', 'Jim',  'John', 'Jim'),
     ('John', None,  'John', None),
     (None, 'Jim',  None, 'Jim'),
     (None, None,  None, None)
     ]
)
def test_from_configuration_both_players(request, mocker,
            name_a, name_b, exp_name_a, exp_name_b):
    logger.info(f'{request._pyfuncitem.name}()')

    mock_result = mocker.patch.object(Engine, 'from_instance', autospec=Engine.from_instance, spec_set=True)

    exp_num_iters = 2

    Engine.from_configuration(_player_factory(name_a),
                              _player_factory(name_b),
                              num_iters=exp_num_iters)


    pytest.assume(mock_result.call_count == 1)
    _, from_instance_param_d =  mock_result.call_args
    name_player_a = from_instance_param_d['name_player_a']
    name_player_b = from_instance_param_d['name_player_b']
    num_iters = from_instance_param_d['num_iters']

    pytest.assume(exp_name_a == name_player_a)
    pytest.assume(exp_name_b == name_player_b)
    pytest.assume(exp_num_iters == num_iters)


@pytest.mark.parametrize(
    'playera_factory, playerb_factory',
    [
     (_player_factory('John'), None),
     (None, _player_factory('John')),
     (None, None)
     ]
)

def test_from_configuration_both_players_none(request, mocker, playera_factory, playerb_factory):
    logger.info(f'{request._pyfuncitem.name}()')

    with pytest.raises(ValueError):
        Engine.from_configuration(playera_factory,
                                  playerb_factory,
                                  num_iters=1
                                  )

def test_from_instance_none(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    exp_name_player_a = 'John A'
    exp_name_player_b = 'John B'

    with pytest.raises(ValueError):
        engine = Engine.from_instance(None,
                                  None,
                                  exp_name_player_a,
                                  exp_name_player_b,
                                  num_iters=1
                                  )


@pytest.mark.parametrize(
    'name_player_a, name_player_b, is_none_player_a, is_none_player_b, exp_name_player_a, exp_name_player_b',
    [
     ('John A', 'John B', False, False, 'John A', 'John B'),
     (None, 'John B', False, False, app_conf.DEFAULT_NAME_PLAYER_A, 'John B'),
     ('John A', None, False, False, 'John A', app_conf.DEFAULT_NAME_PLAYER_B),
     ('John A', 'John B', True, False, 'John A', 'John B'),
     ( 'John A', 'John B', False, True, 'John A', 'John B'),
     ]
)

def test_from_instance(request, mocker, name_player_a, name_player_b, is_none_player_a, is_none_player_b,
                       exp_name_player_a, exp_name_player_b):
    logger.info(f'{request._pyfuncitem.name}()')

    mock_player_a = None if is_none_player_a else mocker.create_autospec(ConstantPlayer, spec_set=True)
    mock_player_b = None if is_none_player_b else mocker.create_autospec(ConstantPlayer, spec_set=True)

    engine = Engine.from_instance(mock_player_a,
                                  mock_player_b,
                                  name_player_a,
                                  name_player_b,
                                  num_iters=1
                                  )

    pytest.assume(exp_name_player_a == engine.name_player_a)
    pytest.assume(exp_name_player_b == engine.name_player_b)
    if mock_player_a is not None:
        pytest.assume(mock_player_a == engine.player_a)
    else:
        pytest.assume(engine.player_a is not None)
        pytest.assume(not isinstance(engine.player_a, mocker.Mock)) # default player


    if mock_player_b is not None:
        pytest.assume(mock_player_b == engine.player_b)
    else:
        pytest.assume(engine.player_b is not None)
        pytest.assume(not isinstance(engine.player_b, mocker.Mock)) # default player


def _parse_event(mock_event):
    pytest.assume(mock_event.call_count == 2)
    (stra,), _ = mock_event.call_args_list[0]
    (strb,), _ = mock_event.call_args_list[1]

    a_name, a_answer = stra.split("answer's is")
    b_name, b_answer = strb.split("answer's is")
    return a_name.strip(), a_answer.strip(), b_name.strip(), b_answer.strip()

def _parse_result(mock_event, a_name, b_name):
    pytest.assume(mock_event.call_count == 1)
    (res,), _ = mock_event.call_args
    if '!' in res:
        return ResultEnum.DRAW
    player_name,_ = res.split("wins")
    player_name = player_name.strip()

    if(a_name==player_name):
        return ResultEnum.WIN_PLAYER_A

    if (b_name == player_name):
        return ResultEnum.LOSE_PLAYER_A
    raise AssertionError(f"Unexpected player {player_name} wins")



def test_play_default_names(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    mock_logging = mocker.patch('alexber.rpsgame.engine_0_5.logging', autospec=True, spec_set=True)

    player_a = ConstantPlayer()
    player_b = ConstantPlayer()

    engine = Engine.from_instance(player_a,
                                  player_b)
    engine.play()
    mock_event =  mock_logging.debug
    mock_result = mock_logging.info

    a_name, a_answer, b_name, b_answer = _parse_event(mock_event)
    pytest.assume(app_conf.DEFAULT_NAME_PLAYER_A == a_name)
    pytest.assume(player_a._move == a_answer)
    pytest.assume(app_conf.DEFAULT_NAME_PLAYER_B == b_name)
    pytest.assume(player_b._move == b_answer)

    result = _parse_result(mock_result, a_name, b_name)
    pytest.assume(ResultEnum.DRAW == result)


#R>S
#S>P
#P>R

@pytest.mark.parametrize(
    'a_move, b_move, exp_result',
    [(RPS.ROCK, RPS.ROCK, ResultEnum.DRAW),
     (RPS.ROCK, RPS.SCISSORS, ResultEnum.WIN_PLAYER_A),
     (RPS.ROCK, RPS.PAPER, ResultEnum.LOSE_PLAYER_A),

     (RPS.SCISSORS, RPS.ROCK, ResultEnum.LOSE_PLAYER_A),
     (RPS.SCISSORS, RPS.SCISSORS, ResultEnum.DRAW),
     (RPS.SCISSORS, RPS.PAPER, ResultEnum.WIN_PLAYER_A),

     (RPS.PAPER, RPS.ROCK, ResultEnum.WIN_PLAYER_A),
     (RPS.PAPER, RPS.SCISSORS, ResultEnum.LOSE_PLAYER_A),
     (RPS.PAPER, RPS.PAPER, ResultEnum.DRAW),
     ]
)
def test_play(request, mocker, a_move, b_move, exp_result):
    logger.info(f'{request._pyfuncitem.name}()')

    mock_logging = mocker.patch('alexber.rpsgame.engine_0_5.logging', autospec=True, spec_set=True)

    exp_name_player_a = 'John A'
    exp_name_player_b = 'John B'

    player_a = ConstantPlayer(a_move.value)
    player_b = ConstantPlayer(b_move.value)

    engine = Engine.from_instance(player_a,
                                  player_b,
                                  exp_name_player_a,
                                  exp_name_player_b)
    engine.play()
    mock_event =  mock_logging.debug
    mock_result = mock_logging.info

    a_name, a_answer, b_name, b_answer = _parse_event(mock_event)

    pytest.assume(exp_name_player_a == a_name)
    pytest.assume(player_a._move == a_answer)
    pytest.assume(exp_name_player_b == b_name)
    pytest.assume(player_b._move == b_answer)

    result = _parse_result(mock_result, a_name, b_name)
    pytest.assume(exp_result == result)

@pytest.mark.parametrize(
    'invalid_move',
    [
     ('invalid'),
     (100),
	 (0.0),
	 (1.0),
     ]
)
def test_play_invalid_move_a(request, mocker, invalid_move):
    logger.info(f'{request._pyfuncitem.name}()')

    mock_logging = mocker.patch('alexber.rpsgame.engine_0_5.logging', autospec=True, spec_set=True)

    player_a = ConstantPlayer(invalid_move)

    engine = Engine.from_instance(player_a,
                                  None)

    with pytest.raises(ValueError, match='nexpected'):
        engine.play()

@pytest.mark.parametrize(
    'invalid_move',
    [
     ('invalid'),
     (100),
	 (0.0),
	 (1.0),
     ]
)
def test_play_invalid_move_b(request, mocker, invalid_move):
    logger.info(f'{request._pyfuncitem.name}()')

    mock_logging = mocker.patch('alexber.rpsgame.engine_0_5.logging', autospec=True, spec_set=True)

    player_b = ConstantPlayer("invalid")

    engine = Engine.from_instance(None,
                                  player_b)

    with pytest.raises(ValueError, match='nexpected'):
        engine.play()


def test_play_invalid_move_a_exception(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    mock_logging = mocker.patch('alexber.rpsgame.engine_0_5.logging', autospec=True, spec_set=True)

    player_a = ConstantPlayer("invalid")
    player_a.move = lambda: exec('raise(TypeError("Whohaha"))')

    engine = Engine.from_instance(player_a,
                                  None)

    with pytest.raises(TypeError, match='Whohaha'):
        engine.play()


def test_play_invalid_move_b_exception(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    mock_logging = mocker.patch('alexber.rpsgame.engine_0_5.logging', autospec=True, spec_set=True)

    player_b = ConstantPlayer("invalid")
    player_b.move = lambda: exec('raise(TypeError("Whohaha"))')

    engine = Engine.from_instance(None,
                                  player_b)

    with pytest.raises(TypeError, match='Whohaha'):
        engine.play()

@pytest.mark.it
def test_play_it(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    mock_logging = mocker.patch('alexber.rpsgame.engine_0_5.logging', autospec=True, spec_set=True)

    args = '--playera.cls=alexber.rpsgame.players.ConstantPlayer --playerb.cls=alexber.rpsgame.players.ConstantPlayer'\
        .split()
    rpsgame_app_main(args)

    mock_result = mock_logging.info

    result = _parse_result(mock_result, app_conf.DEFAULT_NAME_PLAYER_A, app_conf.DEFAULT_NAME_PLAYER_B)
    pytest.assume(ResultEnum.DRAW == result)


@pytest.mark.it

@pytest.mark.parametrize(
    'constant_move',
    [
        member.value for member in RPS.__members__.values()

     ]
)

def test_hacker_player(request, mocker, constant_move):
    logger.info(f'{request._pyfuncitem.name}()')

    mock_logging = mocker.patch('alexber.rpsgame.engine_0_5.logging', autospec=True, spec_set=True)

    hacker_player_name = '.'.join([HackerPlayer.__module__, HackerPlayer.__name__])

    args = f'--playera.cls={HackerPlayer.__qualname__} --playerb.cls=alexber.rpsgame.players.ConstantPlayer '\
        f'--playerb.init.move={constant_move}' \
        .split()
    rpsgame_app_main(args)

    mock_result = mock_logging.info

    result = _parse_result(mock_result, app_conf.DEFAULT_NAME_PLAYER_A, app_conf.DEFAULT_NAME_PLAYER_B)
    pytest.assume(ResultEnum.WIN_PLAYER_A == result)





if __name__ == "__main__":
    pytest.main([__file__])
