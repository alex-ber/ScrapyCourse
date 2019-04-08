
#TODO: Alex write unit tests
#
from random import Random, SystemRandom

MOVES = ['R', 'S', 'P']


class ConstantPlayer(object):
    def __init__(self, move='R'):
        #no validation is done here by intent
        self._move = move

    def move(self):
        return self._move

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




if __name__ == '__main__':
    main()
