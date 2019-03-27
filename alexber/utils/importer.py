import importlib
import logging
import inspect

logger = logging.getLogger(__name__)



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



def new_instance(target, *args, **kwargs):
    thing = importer(target)
    ret = thing
    if inspect.isclass(thing):
        #TODO: Alex
        ret = thing()
        #ret = thing(*args, **kwargs)
    return ret