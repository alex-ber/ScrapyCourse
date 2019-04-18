
from random import Random, SystemRandom

MOVES = ['R', 'S', 'P']
import itertools

def _is_iterable(item):
    try:
        iter(item)
        return True
    except TypeError:
        return False



# class ConstantPlayer(object):
#     def __init__(self, move='R'):
#         #no validation is done here by intent
#         self._move = move
#
#     def move(self):
#         return self._move
#
class ConstantPlayer(object):
    def __init__(self, move=['R']):
        #no validation is done here by intent
        #str is iterable, but we want to treat it as scalar
        if isinstance(move, str) or not _is_iterable(move):
            iterable = [move]
        else:
            iterable = move

        self._moves = itertools.cycle(iterable)

    def move(self):
        # return self._move
        ret = next(self._moves)
        #for backward-compatibility
        self._move = ret
        return ret

class RandomPlayer(object):

    def __init__(self, seed=None):
        self.random = Random(x=seed)

    def move(self):

        ret = self.random.choice(MOVES)
        return ret


class CryptoRandomPlayer(RandomPlayer):

    def __init__(self, seed=None):
        self.random = SystemRandom(x=seed)

DefaultPlayer = RandomPlayer


class HumanPlayer(object):

    def move(self):
        return input("Valid inputs are 'R', 'S', 'P'. Please make you move: ")


class HumanValidPlayer(object):

    def __init__(self, num_retry=None):
        self.num_retry = num_retry

    def _move(self, limit):
        if limit is None:
            while True:
                move = input("Valid inputs are 'R', 'S', 'P'. Please make you move: ")
                if move in MOVES:
                    return move

        for _ in range(limit):
            move = input("Valid inputs are 'R', 'S', 'P'. Please make you move: ")
            if move in MOVES:
                return move

        raise ValueError("Too many wrong attempts")



    def move(self):
        return self._move(self.num_retry)




