
import inspect
import logging
logger = logging.getLogger(__name__)


def issetdescriptor(object):
    """Return true if the object is a method descriptor with setters.

    But not if ismethod() or isclass() or isfunction() are true.

    This is new in Python 2.2, and, for example, is true of int.__add__.
    An object passing this test has a __get__ attribute but not a __set__
    attribute, but beyond that the set of attributes varies.  __name__ is
    usually sensible, and __doc__ often is.

    Methods implemented via descriptors that also pass one of the other
    tests return false from the ismethoddescriptor() test, simply because
    the other tests promise more -- you can, e.g., count on having the
    __func__ attribute (etc) when an object passes ismethod()."""
    if inspect.isclass(object) or inspect.ismethod(object) or inspect.isfunction(object):
        # mutual exclusion
        return False
    tp = type(object)

    return hasattr(tp, "__set__")


def issetmethod(object):
    if inspect.isclass(object):
        return False

    if not inspect.isfunction(object):
        return False

    sig = inspect.signature(object)
    length = len(sig.parameters.keys())

    return length==2    #2=|{self,param}|
