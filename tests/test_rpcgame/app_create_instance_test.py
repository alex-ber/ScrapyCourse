import logging
logger = logging.getLogger(__name__)
from pathlib import Path

import pytest
from alexber.rpsgame import app_conf
from alexber.rpsgame.app_create_instance import create_instance

from collections import OrderedDict

init_prefix = 'init'
from .app_conf_test import prop_prefix


class PlayerEmpty(object):
    pass


class PlayerInitFull(object):
    def __init__(self, *args, **kwargs):
        pass

class PlayerInitArg(object):
    def __init__(self, first_name):
        self.first_name = first_name

class PlayerInitDefaultArg(object):
    def __init__(self, first_name='John', **kwargs):
        self.first_name = first_name



@pytest.mark.parametrize(
     'plcls,first_name',
    [(PlayerEmpty, None),
     (PlayerInitFull, None),
     (PlayerInitArg, 'John'),
     (PlayerInitDefaultArg, None),
     (PlayerInitDefaultArg, 'Silver'),
     ]
)
def test_new_instance_init(request, plcls, first_name):
    logger.info(f'{request._pyfuncitem.name}()')

    d = OrderedDict()
    d[app_conf.CLS_KEY] = '.'.join([__name__, plcls.__name__])
    if first_name is not None:
        d['.'.join([init_prefix, 'first_name'])] = first_name

    player = create_instance(**d)
    assert player is not None


def test_new_instance_prop(request, mocker, fixed_type):
    logger.info(f'{request._pyfuncitem.name}()')

    #faking type() to return expcted type of the Mock
    mocker.patch('alexber.rpsgame.app_create_instance.type', side_effect=fixed_type)

    exp_name = 'Jim'

    d = OrderedDict()
    plcls = '.'.join([__name__, PlayerEmpty.__name__])
    d[app_conf.CLS_KEY] = plcls
    d['.'.join([prop_prefix, 'name'])] = exp_name

    mock_cls = mocker.patch(plcls, autospec=True)
    prop_mock = mocker.PropertyMock()
    mock_cls.name = prop_mock

    player = create_instance(**d)

    prop_set_mock = prop_mock.fset
    pytest.assume(prop_set_mock.call_count == 1)
    (_, name), _ = prop_set_mock.call_args
    assert exp_name == name
    assert player is not None

#TODO: Alex

if __name__ == "__main__":
    pytest.main([__file__])
