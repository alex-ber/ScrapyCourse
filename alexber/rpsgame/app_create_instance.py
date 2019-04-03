import logging.config
import logging

logger = logging.getLogger(__name__)

import inspect
from alexber.utils.importer import new_instance, importer
from alexber.utils.inspects import issetdescriptor, issetmethod
from collections import OrderedDict

from alexber.rpsgame import app_conf as conf

#TODO: Alex write unit tests


def _checkParam(obj, key):
    if (obj is None):
        raise ValueError(f"run() expectes paramater {key}")

def _inject_properties(player, **kwargs):
    #__new__() could subsitute __class__, so re-evaluate it
    plcls = type(player)
    # finding @property.fset
    results = inspect.getmembers(plcls, predicate=issetdescriptor)
    d = {key: value for (key, value) in results}

    for name, value in kwargs.items():
        if not name.startswith("prop."):
            logger.debug(f"Skipping {name}, doesn't have prefix 'prop'")
            continue

        real_name = name[len("prop."):]

        if real_name not in d:
            raise ValueError(f"Property {name} not found in the class {plcls}")

        prop = d.pop(real_name)  # safe
        prop_setter = prop.fset  # fset has default value of None
        if prop_setter is None:
            raise ValueError(f"Property {name} found, but it doesn't support setter.")

        prop_setter(player, value)



#undocumented feature: you can actually call any method with 1 parameter
#Limitation: no special treatment for default parameters
def _inject_setters(player, **kwargs):
    #__new__() could subsitute __class__, so re-evaluate it
    plcls = type(player)
    # finding @property.fset
    results = inspect.getmembers(plcls, predicate=issetmethod)
    d = {key: value for key, value in results}

    for name, value in kwargs.items():
        if not name.startswith("set."):
            logger.debug(f"Skipping {name}, doesn't have prefix 'set'")
            continue

        real_name = name[len("set."):]

        if real_name not in d:
            raise ValueError(f"Setter {name} not found in the class {plcls}")

        setter = d.pop(real_name)  # safe
        if setter is None: # just in case
            raise ValueError(f"Setter {name} is None")

        setter(player, value)




def create_instance(**kwargs):
    '''This is mini DI Framework.
    Existing DI Frameworks, such as https://pythonhosted.org/injector/ were consider and rejected
    as overcomplicated for defying players
    '''
    plcls = kwargs.pop(conf.CLS_KEY, None)
    _checkParam(plcls, conf.CLS_KEY)

    d = OrderedDict()

    for name, value in kwargs.items():
        if not name.startswith("init."):
            logger.debug(f"Skipping {name}, doesn't have prefix 'init'")
            continue

        real_name = name[len("init."):]
        d[real_name] = value


    player = new_instance(plcls, **d)
    _inject_properties(player, **kwargs)
    _inject_setters(player, **kwargs)

    return player

