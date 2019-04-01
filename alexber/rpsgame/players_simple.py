
#TODO: Alex write unit tests
#TODO: Alex write integration tests
from random import Random, SystemRandom

MOVES = ['R', 'S', 'P']


class ConstantPlayer(object):

    def move(self):
        return 'R'

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


def main():
    pass
    # pl1=RandomPlayer(0)
    # limit =1000
    # result1 = [pl1.move() for i in range(limit)]
    # pl2 = RandomPlayer(0)
    # result2 = [pl2.move() for i in range(limit)]
    # assert result1==result2
    #
    # pl1=RandomPlayer(10)
    # limit =1000
    # result1 = [pl1.move() for i in range(limit)]
    # pl2 = RandomPlayer(10)
    # result2 = [pl2.move() for i in range(limit)]
    # assert result1==result2


if __name__ == '__main__':
    main()