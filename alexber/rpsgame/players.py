
from .players_simple import *
from abc import ABCMeta
from abc import abstractmethod
import inspect


#obj can be object or class
def _as_type(obj, use_attr=False):
    basecls = obj \
        if inspect.isclass(obj) \
        else type(obj)

    if not use_attr:
        return basecls

    dict = {} \
        if inspect.isclass(obj)  \
        else  obj.__dict__


    name = basecls.__name__
    cls = type(name, (basecls,), dict)

    if not inspect.isclass(obj):
        obj.__class__= cls
    return cls

def _issublass(C, name):
    results = inspect.getmembers(C)
    members = {key for (key, _) in results}
    ret = name in members
    return ret

def get_attr(obj, name):
    ret = getattr(obj, name)
    if ret is None:
        return None
    b = callable(ret)
    if b:
        ret = ret()
    return ret


class NamedMixin(object, metaclass=ABCMeta):

    @abstractmethod
    def name(self):
        raise NotImplementedError("Please, use get_attr() function.")



    @classmethod
    def __subclasshook__(cls, C):
        if cls is NamedMixin:
            ret = _issublass(C, 'name')
            return ret
        return NotImplemented

    @classmethod
    def register(cls, obj):
        ABCMeta.register(cls, _as_type(obj, use_attr=True))

class PlayMixin(object, metaclass=ABCMeta):

    @abstractmethod
    def move(self):
        raise NotImplementedError("Please, use get_attr() function.")

    @classmethod
    def __subclasshook__(cls, C):
        if cls is PlayMixin:
            ret = _issublass(C, 'move')
            return ret
        return NotImplemented

    @classmethod
    def register(cls, obj):
        ABCMeta.register(cls, _as_type(obj))


class StartedMixin(object, metaclass=ABCMeta):

    @abstractmethod
    def started(self, **kwargs):
        raise NotImplementedError("Please, use get_attr() function.")

    @classmethod
    def __subclasshook__(cls, C):
        if cls is StartedMixin:
            ret = _issublass(C, 'started')
            return ret
        return NotImplemented

    @classmethod
    def register(cls, obj):
        ABCMeta.register(cls, _as_type(obj))

class RoundResultMixin(object, metaclass=ABCMeta):

    @abstractmethod
    def round_result(self, **kwargs):
        raise NotImplementedError("Please, use get_attr() function.")

    @classmethod
    def __subclasshook__(cls, C):
        if cls is RoundResultMixin:
            ret = _issublass(C, 'round_result')
            return ret
        return NotImplemented

    @classmethod
    def register(cls, obj):
        ABCMeta.register(cls, _as_type(obj))



class CompletedMixin(object, metaclass=ABCMeta):

    @abstractmethod
    def completed(self, **kwargs):
        raise NotImplementedError("Please, use get_attr() function.")

    @classmethod
    def __subclasshook__(cls, C):
        if cls is CompletedMixin:
            ret = _issublass(C, 'completed')
            return ret
        return NotImplemented

    @classmethod
    def register(cls, obj):
        ABCMeta.register(cls, _as_type(obj))


class RepeadLastMove(RoundResultMixin):
    def __init__(self, move='R'):
        self._move = move

    def move(self):
        return self._move

    def round_result(self, **kwargs):
        self._move = kwargs["OTHER"]['move']


