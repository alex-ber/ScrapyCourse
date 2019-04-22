import pytest

iswebfound = False
try:
    from web import application
    iswebfound = True
except ImportError:
    pass

from _functools import partial
import inspect

# @pytest.fixture()
# def my_dependency():
#     return 42
#
# @pytest.mark.ws
# def test_first(my_dependency ):
#     pass


# def pytest_addoption(parser):
#     parser.addoption(
#         "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
#     )
#
# @pytest.fixture
# def cmdopt(request):
#     return request.config.getoption("--cmdopt")
#
# # content of test_sample.py
# def test_answer(cmdopt):
#     if cmdopt == "type1":
#         print("first")
#     elif cmdopt == "type2":
#         print("second")
#     assert 0  # to see what was printed

#isn't really needed, type() is built-in function
#we will only shadow it in particular package
_real_type = type

def _type(obj, mockType):
    if isinstance(obj, mockType):
        ret = obj
    else:
        ret = _real_type(obj)
    return ret

_real_inspect_signature = inspect.signature

def _inspect_signature(obj, mockType):
    if isinstance(obj, mockType):
        sig = obj._spec_signature
    else:
        sig = _real_inspect_signature(obj)
    return sig

@pytest.fixture
def fixed_type(mocker):
    # faking type() to return expected type of the Mock
    l_type = partial(_type, mockType=mocker.Mock)
    return l_type

@pytest.fixture
def fixed_inspect_signature(mocker):
    # faking inspect.signature() to return expected signature of the Mock
    ret = partial(_inspect_signature, mockType=mocker.Mock)
    return ret


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


#see https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
def skip_tests(config=None, items=None, keyword=None, reason=None):
    if items is None:
        TypeError("items can't be None")

    if reason is None:
        TypeError("reason can't be None")

    if keyword is None:
        TypeError("keyword can't be None")

    skip = pytest.mark.skip(reason=reason)
    for item in items:
        if keyword in item.keywords:
            item.add_marker(skip)



#see https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
def pytest_collection_modifyitems(config, items):
    if not config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        skip_tests(items=items, keyword="slow", reason="need --runslow option to run")

    if not iswebfound:
        # --runslow given in cli: do not skip slow tests
        skip_tests(items=items, keyword="ws", reason="ws is not installed. See documentation for\
        more details.")




# # content of test_module.py
# import pytest
#
#
# def test_func_fast():
#     pass
#
#
# @pytest.mark.slow
# def test_func_slow():
#     pass

#see https://docs.pytest.org/en/latest/example/simple.html#incremental-testing-test-steps
def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


#see https://docs.pytest.org/en/latest/example/simple.html#incremental-testing-test-steps
def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" % previousfailed.name)

# # content of test_module.py
# import pytest
#
#
# @pytest.mark.incremental
# class TestUserHandling(object):
#     def test_login(self):
#         pass
#
#     def test_modification(self):
#         assert 0
#
#     def test_deletion(self):
#         pass
#
#
# def test_normal():
#     pass

# Parametrized Test
#see http://pythontesting.net/framework/pytest/pytest-fixtures-nuts-bolts/#real (1)
#see alternative also in  https://docs.pytest.org/en/latest/example/parametrize.html + (2)
#                    https://stackoverflow.com/questions/42228895/how-to-parametrize-a-pytest-fixture/52611167#52611167
#see also https://stackoverflow.com/questions/42228895/how-to-parametrize-a-pytest-fixture/44568273#44568273 (3)
# # content of test_module.py
# from http://pythontesting.net/framework/pytest/pytest-fixtures-nuts-bolts/#real
# (1)
# @pytest.fixture(params=[
#     # tuple with (input, expectedOutput)
#     ('regular text', 'regular text</p>'),
#     ('*em tags*', '<p><em>em tags</em></p>'),
#     ('**strong tags**', '<p><strong>strong tags</em></p>')
# ])
# def test_data(request):
#     return request.param
#
#
# def test_markdown(test_data):
#     (the_input, the_expected_output) = test_data
#     the_output = run_markdown(the_input)
#     assert the_output == the_expected_output

#from https://stackoverflow.com/questions/42228895/how-to-parametrize-a-pytest-fixture/52611167#52611167
#(2)
# import pytest
#
# class TimeLine:
#     def __init__(self, instances=[0, 0, 0]):
#         self.instances = instances
#
#
# @pytest.fixture(params=[
#     [1, 2, 3], [2, 4, 5], [6, 8, 10]
# ])
# def timeline(request):
#     return TimeLine(request.param)
#
#
# def test_timeline(timeline):
#     for instance in timeline.instances:
#         assert instance % 2 == 0

#from https://stackoverflow.com/questions/42228895/how-to-parametrize-a-pytest-fixture/44568273#44568273
#(3)
# import pytest
#
# class TimeLine:
#     def __init__(self, instances):
#         self.instances = instances
#
# @pytest.fixture
# def timeline(request):
#     return TimeLine(request.param)
#
# @pytest.mark.parametrize(
#     'timeline',
#     ([1, 2, 3], [2, 4, 6], [6, 8, 10]),
#     indirect=True
# )
# def test_timeline(timeline):
#     for instance in timeline.instances:
#         assert instance % 2 == 0
#
# if __name__ == "__main__":
#     pytest.main([__file__])


