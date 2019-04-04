import logging
logger = logging.getLogger(__name__)

import pytest

import alexber.rpsgame.app as app
from alexber.rpsgame.app import conf as app_conf

_real_parse_config = app_conf.parse_config





def test_main(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    _parse_config_return_value = None

    def _mock_parse_config(args=None):
        ret = _real_parse_config(args)
        nonlocal _parse_config_return_value
        _parse_config_return_value = ret
        return ret

    #mocker.spy(app_conf, 'parse_config')
    mocker.patch.object(app_conf, 'parse_config', side_effect=_mock_parse_config, autospec=True, spec_set=True)
    mocker.patch.object(app, 'run', autospec=True, spec_set=True)

    exp_playera_cls = '--playera.cls=alexber.rpsgame.players.ConstantPlayer'
    exp_playerb_cls = '--playerb.cls=alexber.rpsgame.players.ConstantPlayer'

    argsv = f'{exp_playera_cls} ' \
            f'{exp_playerb_cls}' \
        .split()
    app.main(argsv)

    pytest.assume(app_conf.parse_config.call_count == 1)
    ((playera_cls, playerb_cls),), _ =  app_conf.parse_config.call_args
    pytest.assume( (exp_playera_cls, exp_playerb_cls) == (playera_cls, playerb_cls) )

    pytest.assume(app.run.call_count == 1)
    _, run_d = app.run.call_args

    pytest.assume(_parse_config_return_value == run_d)


def test_run(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')
    d = {'playera': {'cls': 'alexber.rpsgame.players.ConstantPlayer'},
         'playerb': {'cls': 'alexber.rpsgame.players.ConstantPlayer'},
         }


    mocker.spy(app_conf, 'parse_dict')
    mock_cls = mocker.patch(app_conf.DEFAULT_ENGINE_CLS, autospec=True, spec_set=True)
    mock_create_instance = mocker.patch.object(app, 'create_instance', autospec=True, spec_set=True,
                                               side_effect=[ d['playera'], d['playerb'] ])

    app.run(**d)

    mock_parse_dict = app_conf.parse_dict
    pytest.assume(mock_parse_dict.call_count == 1)
    _, parse_dict_d = mock_parse_dict.call_args
    implicit_convert_value = parse_dict_d['implicit_convert']
    pytest.assume(False == implicit_convert_value)


    mock_from_configuration = mock_cls.from_configuration
    mock_play = mock_from_configuration.return_value.play

    pytest.assume(mock_from_configuration.call_count == 1)
    _, engine_d = mock_from_configuration.call_args

    _, engine_d['playera'] = engine_d.pop('playera_factory')()
    _, engine_d['playerb'] = engine_d.pop('playerb_factory')()

    pytest.assume(d == engine_d)

    pytest.assume(mock_play.call_count == 1)
    play_args, _ = mock_play.call_args
    pytest.assume(()==play_args )

    pytest.assume(mock_create_instance.call_count == 2)
    _, param_playera_d = mock_create_instance.call_args_list[0]
    _, param_playerb_d = mock_create_instance.call_args_list[1]

    pytest.assume(d['playera'], param_playera_d)
    pytest.assume(d['playerb'], param_playerb_d)


def test_create_player_factory_none(request, mocker):
     logger.info(f'{request._pyfuncitem.name}()')

     with pytest.raises(AssertionError):
         player = app._create_player_factory(None)

def test_create_player_factory_without_name(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    mocker.patch.object(app, 'create_instance', autospec=True, spec_set=True, return_value=object())
    d= {}

    factory_fun = app._create_player_factory(d)
    assert factory_fun is not None

    name_player, player = factory_fun()

    pytest.assume(name_player is None)
    pytest.assume(player is not None)


def test_create_player_factory_with_name(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    mocker.patch.object(app, 'create_instance', autospec=True, spec_set=True, return_value=object())

    exp_name = "John"
    d = {app_conf.NAME_PLAYER_KEY:exp_name}

    factory_fun = app._create_player_factory(d)
    assert factory_fun is not None

    name_player, player = factory_fun()

    pytest.assume(exp_name==name_player)
    pytest.assume(player is not None)




if __name__ == "__main__":
    pytest.main([__file__])
