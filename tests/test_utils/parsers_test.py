import logging
import pytest

from alexber.utils.parsers import ConfigParser, ArgumentParser

logger = logging.getLogger(__name__)
from pathlib import Path



def test_parse_config(request):
    logger.info(f'{request._pyfuncitem.name}()')

    parser = ConfigParser()
    dir = Path(__file__).parent

    parser.read(dir / 'config.ini')

    dd = parser.as_dict()
    da = dd['PLAYERA']
    clsa = da['cls']
    namea = da['name']

    db = dd['PLAYERB']
    clsb = da['cls']
    nameb = da['name']

    assert clsa==clsb
    assert namea == nameb


@pytest.fixture(params=[
    #'args,exp_d',
    ('--key=value --single',
     dict([('key', 'value'), ('single', None)])),

    ('wrong=pair',
         dict([('wrong=pair', None)])),

    ('--conf --prop1=value1 --prop2=value --prop1=value9',
         dict([('conf', None), ('prop1', 'value9'), ('prop2', 'value')])),

])
def arg_parse_param(request):
    return request.param

def test_args_parse(request, mocker, arg_parse_param):
    logger.info(f'{request._pyfuncitem.name}()')
    args, exp_d = arg_parse_param

    parser = ArgumentParser()

    mock_args = mocker.patch('alexber.utils.parsers.sys.argv', new_callable=list)
    mock_args.append(__file__)
    mock_args[1:] = args.split()

    d = parser.as_dict()
    assert exp_d==d


def test_args_parse_explicit_args(request, arg_parse_param):
    logger.info(f'{request._pyfuncitem.name}()')
    args, exp_d = arg_parse_param

    parser = ArgumentParser()

    sys_args = args.split()

    d = parser.as_dict(args=sys_args)
    assert exp_d==d

if __name__ == "__main__":
    pytest.main([__file__])
