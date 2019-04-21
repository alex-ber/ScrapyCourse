#see https://stackoverflow.com/questions/1785503/when-should-i-use-uuid-uuid1-vs-uuid-uuid4-in-python
#https://stackoverflow.com/questions/703035/when-are-you-truly-forced-to-use-uuid-as-part-of-the-design/786541#786541

from os import urandom
from uuid import uuid1 as _uuid1
_int_from_bytes = int.from_bytes  # py3 only

from random import SystemRandom as _SystemRandom

system_random = _SystemRandom()

def uuid1mc():
    #return uuid1(_int_from_bytes(urandom(6), "big") | 0x010000000000)
    node = system_random.getrandbits(8) #6 and not 8, because this function round up to bits / 8 and rounded up
    # NOTE: The constant here is required by the UUIDv1 spec...
    return  _uuid1(node | 0x010000000000)


