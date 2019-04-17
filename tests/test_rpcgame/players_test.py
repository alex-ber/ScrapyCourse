import logging
logger = logging.getLogger(__name__)

import pytest
from alexber.rpsgame.players import NamedMixin, PlayMixin, StartedMixin, ConstantPlayer, \
    _as_type as synthetic_type, get_attr



PLAYER_NAME = 'John'

class ANamedPlayer(object):

    def name(self):
        return PLAYER_NAME

class ANamedPropPlayer(object):

    @property
    def name(self):
        return PLAYER_NAME

class AAttrPlayer(object):
    def __init__(self):
        self.name = PLAYER_NAME

    def foo(self):
        pass



class BNamedPlayer(NamedMixin):

    def name(self):
        return PLAYER_NAME

class BNamedPropPlayer(NamedMixin):

    @property
    def name(self):
        return PLAYER_NAME

class BAttrPlayer(NamedMixin):
    def __init__(self):
        self.name = PLAYER_NAME

    def name(self):
        raise NotImplementedError("Just to please ABCMetadata.")

    def foo(self):
        pass

class CNamedPlayer(ANamedPlayer, NamedMixin):
    pass


class CNamedPropPlayer(ANamedPropPlayer, NamedMixin):
    pass

class CAttrPlayer(AAttrPlayer, NamedMixin):
    def name(self):
        raise NotImplementedError("Just to please ABCMetadata.")


class ConstantMixinPlayer(PlayMixin):
    def __init__(self, move):
        self._move = move

    def move(self):
        return self._move

class DerivedPlayer(ConstantMixinPlayer, PlayMixin):
    def move(self):
        return super().move()




class StartedPlayer(StartedMixin,ConstantMixinPlayer):
    logger = logging.getLogger('.'.join([__name__, 'StartedPlayer']))

    def started(self, **kwargs):
        StartedPlayer.logger.info(f"started is called with {kwargs}")


@pytest.fixture(params=[
    #'mixin_obj',
        (ANamedPlayer),
        (ANamedPropPlayer),
        (AAttrPlayer),

        (BNamedPlayer),
        (BNamedPropPlayer),
        (BAttrPlayer),

        (CNamedPlayer),
        (CNamedPropPlayer),
        (CAttrPlayer),
    ])
def mixin_cls(request):
    return request.param



def test_interface_cls(request,  mixin_cls):
    logger.info(f'{request._pyfuncitem.name}()')

    NamedMixin.register(mixin_cls)

    if 'Attr' in mixin_cls.__name__:

        mixin_obj = mixin_cls()
        mixin_obj.__class__ = synthetic_type(mixin_obj, use_attr=True)

        b = isinstance(mixin_obj, NamedMixin)
    else:
        b = issubclass(mixin_cls, NamedMixin)
    assert b

def test_interface_obj(request,  mixin_cls):
    logger.info(f'{request._pyfuncitem.name}()')
    mixin_obj = mixin_cls()

    NamedMixin.register(mixin_obj)
    b = isinstance(mixin_obj, NamedMixin)
    assert b


def test_get_value(request,  mixin_cls):
    logger.info(f'{request._pyfuncitem.name}()')
    mixin_obj = mixin_cls()

    name = get_attr(mixin_obj, 'name')
    assert PLAYER_NAME==name

@pytest.mark.parametrize(
    'pl_cls',
    [   (ConstantPlayer),
        (ConstantMixinPlayer),
        (DerivedPlayer),
     ]
)
def test_play_mixin_get_value(request, pl_cls):
    logger.info(f'{request._pyfuncitem.name}()')

    exp_move = 'Z'
    player = pl_cls(exp_move)

    PlayMixin.register(player)

    b = isinstance(player, PlayMixin)
    pytest.assume(b)

    move = get_attr(player, 'move')
    pytest.assume(exp_move==move)


def _parse_started_result(mock_event):
    pytest.assume(mock_event.call_count == 1)
    (res,), _ = mock_event.call_args
    return res

def test_play_started_get_value(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    input = '.'.join([__name__, StartedPlayer.__name__, 'logger'])
    mock_logging = mocker.patch(input, side_effect=StartedPlayer.logger.info, autospec=True)

    player = StartedPlayer("")

    StartedMixin.register(player)

    b = isinstance(player, PlayMixin)
    pytest.assume(b)

    move = get_attr(player, 'started')
    mock_result = mock_logging.info
    result = _parse_started_result(mock_result)

    pytest.assume(result is not None)
    pytest.assume('started' in result)


