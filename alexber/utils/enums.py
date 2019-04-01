
from enum import Enum
import logging
logger = logging.getLogger(__name__)

class StrAsReprMixinEnum(Enum):
    '''
    This is Enum Mixin that has __str__() equal to __repr__().
    '''
    def __str__(self):
        return self.__repr__()


class AutoNameMixinEnum(Enum):
    '''
    This is Enum Mixin that generate value equal to the name.
    '''
    def _generate_next_value_(name, start, count, last_values):
        return name


class MissingNoneMixinEnum(Enum):
    '''
    This is Enum Mixin will return None if value will not be found.
    '''

    @classmethod
    def _missing_(cls, value):
        # raise ValueError("%r is not a valid %s" % (value, cls.__name__))
        return None


class LookUpMixinEnum(StrAsReprMixinEnum, MissingNoneMixinEnum):
    '''
    This is Enim Mixin that is designed to be used for lookup by value.
    If lookup fail, None will be return.
    Also, __str__() will return the same value as __repr__()
    '''
    pass

