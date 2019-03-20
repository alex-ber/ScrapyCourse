import pytest
import logging
import sys

logger = logging.getLogger(__name__)
from alexber.utils.importer import importer, new_instance

class TestImporter(object):
    def test_imported(self, request, mocker):
        logger.info(f'{request._pyfuncitem.name}()')
        namespace = sys.modules[__name__]

        importer = mocker.spy(namespace, 'importer')

        cls_name = 'pathlib.Path'
        kls = importer(cls_name)

        path = kls()
        logger.info(path.absolute())

        assert namespace.importer == importer


class PlayerEmpty(object):
    pass


class PlayerInitFull(object):
    def __init__(self, *args, **kwargs):
        pass

class PlayerInitArg(object):
    def __init__(self, first_name):
        self.first_name = first_name

class PlayerNewAndInitEmpty(object):
    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls)
        return self

class PlayerNewOnlyEmpty(object):
    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls)
        return self

    def __init__(self, *args, **kwargs):
        pass

class PlayerPhilosopher:
    def __init_subclass__(cls, default_name, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"Called __init_subclass({cls}, {default_name})")
        cls.default_name = default_name

from abc import ABCMeta, abstractmethod

class PlayerAbstractWithAbstractMethod(object, metaclass=ABCMeta):
    @abstractmethod
    def foo(self):
        raise NotImplementedError


class PlayerAbstractEmptyWithoutAbstractMethod(object, metaclass=ABCMeta):
    pass

class PlayerAbstractFullWithoutAbstractMethod(object, metaclass=ABCMeta):
    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls)
        return self

    def __init__(self, *args, **kwargs):
        pass



def test_new_instance_arg(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')
    mock = mocker.spy(PlayerInitArg, '__init__')

    input = '.'.join([__name__, PlayerInitArg.__name__])
    first_name = 'Alex'
    player=new_instance(input, first_name)
    assert player.first_name == first_name
    assert player.__init__.call_count == 1



@pytest.mark.parametrize(
     'plcls',
    (PlayerEmpty, PlayerInitFull,PlayerNewOnlyEmpty, PlayerEmpty, PlayerNewOnlyEmpty,PlayerNewAndInitEmpty,
     PlayerAbstractEmptyWithoutAbstractMethod, PlayerAbstractFullWithoutAbstractMethod),
)
def test_new_instance(request, mocker, plcls):
    logger.info(f'{request._pyfuncitem.name}()')

    mocker.spy(plcls, '__new__')
    mocker.spy(plcls, '__init__')

    input = '.'.join([__name__, plcls.__name__])
    player = new_instance(input)

    assert player.__new__.call_count > 0
    assert player.__init__.call_count == 1

@pytest.mark.skip(reason="__init_subclass__() hook is unimplemented in new_instance."\
                         +"See https://github.com/alex-ber/RocketPaperScissorsGame/issues/1 for details."
                   )
def test_new_instance_init_subclass(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')
    mocker.spy(PlayerPhilosopher, '__new__')
    mocker.spy(PlayerPhilosopher, '__init__')
    mocker.spy(PlayerPhilosopher, '__init_subclass__')

    input = '.'.join([__name__, PlayerPhilosopher.__name__])
    player=new_instance(input, default_name="Nietzsche")
    assert player.__new__.call_count > 0
    assert player.__init__.call_count == 1
    assert player.__init_subclass__.call_count == 1


def test_new_instance_abstract_method(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')
    #mock = mocker.spy(PlayerAbstractWithAbstractMethod, '__init__')

    input = '.'.join([__name__, PlayerAbstractWithAbstractMethod.__name__])

    with pytest.raises(TypeError, match='abstract method') as excinfo:
        player = new_instance(input)
    logger.debug((excinfo.value, excinfo.traceback))



if __name__ == "__main__":
    pytest.main([__file__])