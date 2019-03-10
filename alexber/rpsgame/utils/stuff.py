
from enum import Enum

class LookUpEnum(Enum):

    def __str__(self):
        return self.__repr__()

    @classmethod
    def _missing_(cls, value):
         # print('missing')
         # raise ValueError("%r is not a valid %s" % (value, cls.__name__))
         return None
