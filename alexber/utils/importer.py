import importlib
import logging
import inspect

logger = logging.getLogger(__name__)

#
# def _new_instance(fullqname):
#     module_name, class_name = fullqname.rsplit(".", 1)
#     MyClass = getattr(importlib.import_module(module_name), class_name)
#     instance = MyClass()
#     return instance

#adopted from mock.mock._dot_lookup
def _dot_lookup(thing, comp, import_path):
    try:
        return getattr(thing, comp)
    except AttributeError:
        importlib.import_module(import_path)
        return getattr(thing, comp)


#adopted from mock.mock._importer
def importer(target):
    components = target.split('.')
    import_path = components.pop(0)
    thing = importlib.import_module(import_path)

    for comp in components:
        import_path += ".%s" % comp
        thing = _dot_lookup(thing, comp, import_path)
    return thing


'''
importer() method is called.
If target is class than __new__ and __init__ hooks are called on it and result is returned.
Note: __init_subclass__ hoook is not supported.
'''
def new_instance(target, *args, **kwargs):
    thing = importer(target)
    ret = thing
    if inspect.isclass(thing):
        ret = thing.__new__(thing, *args)
        thing.__init__(ret, *args, **kwargs)
        #tbd: take care of arguments __init_subclass__
    return ret