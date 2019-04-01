
import inspect
import logging
logger = logging.getLogger(__name__)


def issetdescriptor(object):
    """Return true if the object is a method descriptor with setters.

    But not if ismethod() or isclass() or isfunction() are true.
    """
    if inspect.isclass(object) or inspect.ismethod(object) or inspect.isfunction(object):
        # mutual exclusion
        return False
    tp = type(object)

    return hasattr(tp, "__set__")


def issetmethod(object):
    '''
    If object is class, return false.
    If object is not function, return false.
    Otherwise, return true iff signature of the function has 2 params. (first param is self, second is value to set).

    :param object:
    :return: false if object is not a class and not a function. Otherwise, return true iff signature has 2 params.
    '''
    if inspect.isclass(object):
        return False

    if not inspect.isfunction(object):
        return False

    sig = inspect.signature(object)
    length = len(sig.parameters.keys())

    return length==2    #2=|{self,param}|
