import logging
logger = logging.getLogger(__name__)
from pathlib import Path

import pytest
from alexber.rpsgame import app_conf
from alexber.rpsgame.app_create_instance import create_instance

from collections import OrderedDict

init_prefix = 'init'
from .app_conf_test import prop_prefix
set_prefix = 'set'

class PlayerEmpty(object):
    pass

class PlayerReadOnlyProp(object):

    def name(self, name):
        self._name = name

    name = property(fset=name)


class PlayerInitFull(object):
    def __init__(self, *args, **kwargs):
        pass

class PlayerInitArg(object):
    def __init__(self, first_name):
        self.first_name = first_name

class PlayerInitDefaultArg(object):
    def __init__(self, first_name='John', **kwargs):
        self.first_name = first_name

class PlayerExample(PlayerInitArg):
    def __init__(self, first_name):
        super().__init__(first_name)
        self._name = None
        self._first_name = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def set_first_name(self, first_name):
        self._first_name = first_name

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

    #faking type() to return expceted type of the Mock
    mocker.patch('alexber.rpsgame.app_create_instance.type', side_effect=fixed_type, create=True)

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
    pytest.assume(exp_name == name)
    pytest.assume(player is not None)


def test_new_instance_prop_read_only(request, mocker, fixed_type):
    logger.info(f'{request._pyfuncitem.name}()')

    exp_name = 'Jim'

    #Is there a way to force PropertyMock to have only setter?
    #it's easier to not to use Mock in this case

    d = OrderedDict()
    plcls = '.'.join([__name__, PlayerReadOnlyProp.__name__])
    d[app_conf.CLS_KEY] = plcls
    d['.'.join([prop_prefix, 'name'])] = exp_name

    player = create_instance(**d)

    pytest.assume(player is not None)
    pytest.assume(exp_name == player._name)


def test_new_instance_setter(request, mocker, fixed_type, fixed_inspect_signature):
    logger.info(f'{request._pyfuncitem.name}()')

    #faking type() to return expected type of the Mock
    mocker.patch('alexber.rpsgame.app_create_instance.type', side_effect=fixed_type, create=True)
    # faking inspect.signature() to return expected signature of the Mock
    from alexber.utils.inspects import inspect as _inspect
    mocker.patch.object(_inspect, 'signature', side_effect=fixed_inspect_signature, autospec=True)

    exp_name = 'Jim'

    d = OrderedDict()
    plcls = '.'.join([__name__, PlayerEmpty.__name__])
    d[app_conf.CLS_KEY] = plcls
    d['.'.join([init_prefix, 'first_name'])] = exp_name
    d['.'.join([set_prefix, 'set_first_name'])] = exp_name

    mock_cls = mocker.patch(plcls, autospec=True)
    mock_setter = mocker.MagicMock(spec_set=lambda a,b:None)
    mock_cls.set_first_name = mock_setter


    player = create_instance(**d)

    pytest.assume(mock_setter.call_count == 1)
    (_, name), _ = mock_setter.call_args
    pytest.assume(exp_name == name)
    pytest.assume(player is not None)


def test_new_instance_all(request, mocker, fixed_type, fixed_inspect_signature):
    logger.info(f'{request._pyfuncitem.name}()')

    exp_name = 'Jim'

    d = OrderedDict()
    plcls = '.'.join([__name__, PlayerExample.__name__])
    d[app_conf.CLS_KEY] = plcls
    d['.'.join([init_prefix, 'first_name'])] = exp_name
    d['.'.join([prop_prefix, 'name'])] = exp_name
    d['.'.join([set_prefix, 'set_first_name'])] = exp_name


    #can't mock __init__ method
    #mock_cls = mocker.patch(plcls, autospec=True)
    # mock_init = mocker.MagicMock(spec_set=PlayerInitArg.__init__)

    player = create_instance(**d)

    pytest.assume(player is not None)
    pytest.assume(exp_name == player.first_name)
    pytest.assume(exp_name == player._name)
    pytest.assume(exp_name == player._first_name)



if __name__ == "__main__":
    pytest.main([__file__])
