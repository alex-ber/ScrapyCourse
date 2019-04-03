import logging
logger = logging.getLogger(__name__)
from pathlib import Path

import pytest

from collections import OrderedDict
import alexber.rpsgame.app as app
from alexber.rpsgame.app import conf as app_conf


_real_parse_config = app_conf.parse_config

_parse_config_return_value = []

def _mock_parse_config(args=None):
    ret = _real_parse_config(args)
    # global _parse_config_return_value
    # _parse_config_return_value = ret
    # globals()['_parse_config_return_value'] = ret
    _parse_config_return_value.append(ret)
    return ret


def test_main(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    #mocker.spy(app_conf, 'parse_config')
    mocker.patch.object(app_conf, 'parse_config', side_effect=_mock_parse_config, autospec=True)
    mocker.patch.object(app, 'run', autospec=True)

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

    pytest.assume(1, len(_parse_config_return_value))
    pytest.assume(_parse_config_return_value[0] == run_d)


def test_run(request, mocker):
    d = {'playera': {'cls': 'alexber.rpsgame.players.ConstantPlayer'},
         'playerb': {'cls': 'alexber.rpsgame.players.ConstantPlayer'},
         }

    mock_cls = mocker.patch(app_conf.DEFAULT_ENGINE_CLS, autospec=True)

    app.run(**d)

    mock_from_configuration = mock_cls.from_configuration
    mock_play = mock_from_configuration.return_value.play

    pytest.assume(mock_from_configuration.call_count == 1)
    _, engine_d = mock_from_configuration.call_args

    d['playera_d'] = d.pop('playera')
    d['playerb_d'] = d.pop('playerb')
    pytest.assume(d == engine_d)

    pytest.assume(mock_play.call_count == 1)
    play_args, _ = mock_play.call_args
    pytest.assume(()==play_args )

if __name__ == "__main__":
    pytest.main([__file__])
