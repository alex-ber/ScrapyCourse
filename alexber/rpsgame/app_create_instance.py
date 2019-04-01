import logging.config
import logging

logger = logging.getLogger(__name__)

import inspect
from alexber.utils.importer import new_instance
from alexber.utils.inpsects import issetdescriptor, issetmethod

from alexber.rpsgame import app_conf as conf

#TODO: Alex write unit tests


def _checkParam(obj, key):
    if (obj is None or not obj):
        raise ValueError(f"run() expectes paramater {key}")

def _inject_properties(player, **kwargs):
    #__new__() could subsitute __class__, so re-evaluate it
    plcls = type(player)
    # finding @property.fset
    results = inspect.getmembers(plcls, predicate=issetdescriptor)
    d = {key: value for (key, value) in results}

    prop = None
    prop_setter = None

    for name, value in kwargs.items():
        if not name.startswith("prop."):
            logger.debug("Skipping {name}, doesn't have prefix 'prop'")
            continue

        real_name = name[len("prop."):]

        if real_name not in d:
            raise ValueError(f"Property {name} not found in the class {plcls}")

        prop = d.pop(real_name)  # safe
        prop_setter = prop.fset  # fset has default value of None
        if prop_setter is None:
            raise ValueError(f"Property {name} found, but it doesn't support setter.")

        prop_setter(self=player, value=value)



#undocumented feature: you can actually call any method with 1 parameter
def _inject_setters(player, **kwargs):
    #__new__() could subsitute __class__, so re-evaluate it
    plcls = type(player)
    # finding @property.fset
    results = inspect.getmembers(plcls, predicate=issetmethod)
    d = {key: value for key, value in results}

    prop = None
    prop_setter = None

    for name, value in kwargs.items():
        if not name.startswith("set."):
            logger.debug("Skipping {name}, doesn't have prefix 'set'")
            continue

        real_name = name[len("set."):]

        if real_name not in d:
            raise ValueError(f"Setter {name} not found in the class {plcls}")

        setter = d.pop(name)  # safe
        if setter is None: # just in case
            raise ValueError(f"Setter {name} is None")

        setter(self=player, value=value)




def create_instance(**kwargs):
    '''This is mini DI Framework.
    Existing DI Frameworks, such as https://pythonhosted.org/injector/ were consider and rejected
    as overcomplicated for defying players
    '''
    plcls = kwargs.pop(conf.PLAYER_CLS_KEY, None)
    _checkParam(plcls, conf.PLAYER_CLS_KEY)

    player = new_instance(plcls, **kwargs)
    _inject_properties(player, **kwargs)
    _inject_setters(player, **kwargs)

    return player

