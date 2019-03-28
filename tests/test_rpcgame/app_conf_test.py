import logging
logger = logging.getLogger(__name__)
from pathlib import Path

import pytest
from alexber.rpsgame import app_conf

import yaml
import json


@pytest.mark.parametrize(
     'value, exp_value, exp_type',

    [
        ('John', 'John', str),
        ('alexber.rpsgame.players.ConstantPlayer', 'alexber.rpsgame.players.ConstantPlayer', str),
        ('1000', 1000, int),
        ('0.1', 0.1, float),
        ('0.0', 0.0, float),
        ('-0.0', 0.0, float),
        ('-5', -5, int),

    ]
)
def test_convert(request, value, exp_value, exp_type):
    logger.info(f'{request._pyfuncitem.name}()')
    result = app_conf._convert(value)
    type_result = type(result)
    pytest.assume(exp_value == result)
    pytest.assume(exp_type == type_result)


def test_parse_yaml(request):
    logger.info(f'{request._pyfuncitem.name}()')
    expdd = {'playera':{'cls': 'alexber.rpsgame.players.ConstantPlayer'},
             'playerb':{'cls': 'alexber.rpsgame.players.ConstantPlayer'}}

    dir = Path(__file__).parent

    with open(dir / 'config.yml') as f:
        d = yaml.safe_load(f)
    d = d['treeroot']
    dd = app_conf.parse_dict(d)
    assert expdd == dd


def test_parse_json(request):
    logger.info(f'{request._pyfuncitem.name}()')
    expdd = {'playera':{'cls': 'alexber.rpsgame.players.ConstantPlayer'},
             'playerb':{'cls': 'alexber.rpsgame.players.ConstantPlayer'}}

    dir = Path(__file__).parent

    with open(dir / 'config.json') as f:
        d = json.load(f)
    dd = app_conf.parse_dict(d)
    assert expdd == dd

def test_parse_ini(request):
    logger.info(f'{request._pyfuncitem.name}()')
    expdd = {'playera':{'cls': 'alexber.rpsgame.players.ConstantPlayer'},
             'playerb':{'cls': 'alexber.rpsgame.players.ConstantPlayer'}}

    dir = Path(__file__).parent

    dd = app_conf.parse_ini(config_file=dir / 'config.ini')
    assert expdd == dd


def test_parse_sys_args(request):
    logger.info(f'{request._pyfuncitem.name}()')
    expdd = {'playera':{'cls': 'alexber.rpsgame.players.ConstantPlayer'},
             'playerb':{'cls': 'alexber.rpsgame.players.ConstantPlayer'}}


    argsv = '--playera.cls=alexber.rpsgame.players.ConstantPlayer ' \
            '--playerb.cls=alexber.rpsgame.players.ConstantPlayer' \
         .split()

    _, dd = app_conf.parse_sys_args(args=argsv)

    assert expdd == dd

def test_config_with_override(request):
    logger.info(f'{request._pyfuncitem.name}()')
    expdd = {'playera':{'cls': 'alexber.rpsgame.players.ConstantPlayer'},
             'playerb':{'cls': 'alexber.rpsgame.players.MyPlayer'}}

    dir = Path(__file__).parent

    argsv = f'--config_file={dir / "config.ini"}' \
            '--playera.cls=alexber.rpsgame.players.MyPlayer ' \
        .split()
    dd = app_conf.parse_config(args=argsv)
    logger.debug('expdd == dd')

if __name__ == "__main__":
    pytest.main([__file__])
