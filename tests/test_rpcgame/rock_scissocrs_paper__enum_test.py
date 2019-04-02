import logging
import pytest

logger = logging.getLogger(__name__)

from alexber.rpsgame.engine import RockScissorsPaperEnum as RPS

def assert_result(resulta, resultb, exp_res, comparator):
    cmp = comparator(resulta, resultb) #(resulta == resultb)
    if exp_res:
        pytest.assume(cmp)
    else:
        pytest.assume(not cmp)

#R>S
#S>P
#P>R

@pytest.mark.parametrize(
     'resulta, resultb, is_eq, is_noteq, is_less_or_eq,is_less,is_great_or_eq,is_great',
    [
        (RPS.PAPER,RPS.PAPER,        True,False,True,False,      True,False),
        (RPS.PAPER,RPS.ROCK,         False,True, True,True,     False,False),
        (RPS.PAPER, RPS.SCISSORS,    False, True,False,False,     True,True),

        (RPS.ROCK, RPS.PAPER,        False, True, False, False, True, True),
        (RPS.ROCK, RPS.ROCK,         True, False, True, False,  True, False),
        (RPS.ROCK, RPS.SCISSORS,     False, True, True, True,  False, False),

        (RPS.SCISSORS, RPS.PAPER,    False, True, True, True,  False, False),
        (RPS.SCISSORS, RPS.ROCK,     False, True, False, False,  True, True),
        (RPS.SCISSORS, RPS.SCISSORS, True, False, True, False,   True, False),

    ]
)


def test_rock_paper_scissocrs_enum(request, resulta, resultb, is_eq, is_noteq, is_less_or_eq,is_less,
                                   is_great_or_eq,is_great):
    logger.info(f'{request._pyfuncitem.name}()')

    assert_result(resulta, resultb, exp_res=is_eq,                                     comparator = lambda x, y: x == y)
    assert_result(resulta, resultb, exp_res=is_noteq,                                  comparator = lambda x, y: x != y)

    assert_result(resulta, resultb, exp_res=is_less_or_eq,                             comparator = lambda x, y: x <= y)
    assert_result(resulta, resultb, exp_res=is_less,                                   comparator = lambda x, y: x <  y)

    assert_result(resulta, resultb, exp_res=is_great_or_eq,                            comparator = lambda x, y: x >= y)
    assert_result(resulta, resultb, exp_res=is_great,                                  comparator = lambda x, y: x >  y)


if __name__ == "__main__":
    pytest.main([__file__])
