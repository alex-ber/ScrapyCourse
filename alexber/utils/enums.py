
from enum import Enum


class StrAsReprMixinEnum(Enum):
    def __str__(self):
        return self.__repr__()


class AutoNameMixinEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class MissingNoneMixinEnum(Enum):

    @classmethod
    def _missing_(cls, value):
        # print('missing')
        # raise ValueError("%r is not a valid %s" % (value, cls.__name__))
        return None


class LookUpMixinEnum(StrAsReprMixinEnum, MissingNoneMixinEnum):
    pass

