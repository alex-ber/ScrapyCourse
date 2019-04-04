import logging
logger = logging.getLogger(__name__)
from pathlib import Path

import pytest
from alexber.rpsgame import app_conf

import yaml
import json

from collections import OrderedDict


prop_prefix = 'prop'

class TestFreeStyle(object):

    def test_parse_yaml(self, request):
        logger.info(f'{request._pyfuncitem.name}()')
        expdd = {'playera':{'cls': 'alexber.rpsgame.players.ConstantPlayer'},
                 'playerb':{'cls': 'alexber.rpsgame.players.ConstantPlayer'}}

        dir = Path(__file__).parent

        with open(dir / 'config.yml') as f:
            d = yaml.safe_load(f)
        d = d['treeroot']
        dd = app_conf.parse_dict(d)
        assert expdd == dd


    def test_parse_json(self, request):
        logger.info(f'{request._pyfuncitem.name}()')
        expdd = {'playera':{'cls': 'alexber.rpsgame.players.ConstantPlayer'},
                 'playerb':{'cls': 'alexber.rpsgame.players.ConstantPlayer'}}

        dir = Path(__file__).parent

        with open(dir / 'config.json') as f:
            d = json.load(f)
        dd = app_conf.parse_dict(d)
        assert expdd == dd

    def test_parse_ini(self, request):
        logger.info(f'{request._pyfuncitem.name}()')
        expdd = {'playera':{'cls': 'alexber.rpsgame.players.ConstantPlayer'},
                 'playerb':{'cls': 'alexber.rpsgame.players.ConstantPlayer'}}

        dir = Path(__file__).parent

        dd = app_conf.parse_ini(config_file=dir / 'config.ini')
        assert expdd == dd


    def test_parse_sys_args(self, request):
        logger.info(f'{request._pyfuncitem.name}()')
        expdd = {'playera':{'cls': 'alexber.rpsgame.players.ConstantPlayer'},
                 'playerb':{'cls': 'alexber.rpsgame.players.ConstantPlayer'}}


        argsv = '--playera.cls=alexber.rpsgame.players.ConstantPlayer ' \
                '--playerb.cls=alexber.rpsgame.players.ConstantPlayer' \
             .split()

        _, dd = app_conf.parse_sys_args(args=argsv)

        assert expdd == dd

    def test_config_with_override(self, request):
        logger.info(f'{request._pyfuncitem.name}()')
        expdd = {'playera':{'cls': 'alexber.rpsgame.players.MyPlayer'},
                 'playerb':{'cls': 'alexber.rpsgame.players.ConstantPlayer'}}

        dir = Path(__file__).parent

        argsv = f'--config_file={dir / "config.ini"} ' \
                '--playera.cls=alexber.rpsgame.players.MyPlayer ' \
            .split()
        dd = app_conf.parse_config(args=argsv)
        assert expdd == dd




def test_parse_config(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    mocker.spy(app_conf, 'parse_sys_args')
    mocker.spy(app_conf, 'parse_ini')


    dir = Path(__file__).parent
    exp_config_ini = dir / "config.ini"

    argsv = f'--config_file={exp_config_ini} ' \
            '--playera.cls=alexber.rpsgame.players.MyPlayer ' \
        .split()
    app_conf.parse_config(args=argsv)

    pytest.assume(app_conf.parse_sys_args.call_count == 1)
    pytest.assume(app_conf.parse_ini.call_count == 1)

    params, _ = app_conf.parse_sys_args()
    # params return from parse_sys_args() contains exp_config_ini
    pytest.assume(exp_config_ini == Path(dir / params.config_file))

    #exp_config_ini was passed to parse_ini()
    (config_file,), _ =  app_conf.parse_ini.call_args
    pytest.assume(exp_config_ini==Path(config_file))

def test_parse_ini(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    mocker.spy(app_conf, 'parse_dict')

    exp_cls = 'alexber.rpsgame.players.ConstantPlayer'

    exp_cls_type = type('') #str
    exp_max = 100
    exp_max_type = type(int)
    exp_str = '0'
    exp_str_type = type('') #str
    exp_cost = 0.1
    exp_cost_type = type(float)

    dir = Path(__file__).parent

    dd = app_conf.parse_ini(config_file=dir / 'numbers.ini')
    d= dd['playera']

    pytest.assume(app_conf.parse_dict.call_count == 1)
    _, parse_dict_d = app_conf.parse_dict.call_args
    implicit_convert_param = parse_dict_d.get('implicit_convert', True) #True is default value
    pytest.assume(implicit_convert_param is True)

    cls = d['cls']
    max = d['prop.max']
    str = d['prop.str']
    cost = d['prop.cost']

    pytest.assume(exp_cls==cls)
    pytest.assume(exp_cls_type==type(cls))
    pytest.assume(exp_max==max)
    pytest.assume(exp_max_type==type(max))
    pytest.assume(exp_str==str)
    pytest.assume(exp_str_type==type(str))
    pytest.assume(exp_cost==cost)
    pytest.assume(exp_cost_type==type(cost))



def test_parse_sys_args(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    mocker.spy(app_conf, 'parse_flat_dict')

    exp_cls = 'alexber.rpsgame.players.ConstantPlayer'

    exp_cls_type = type('') #str
    exp_max = 100
    exp_max_type = int
    exp_str = '0'
    exp_str_type = type('') #str
    exp_cost = 0.1
    exp_cost_type = float


    argsv = '--playera.cls=alexber.rpsgame.players.ConstantPlayer ' \
            '--playera.prop.max=100 ' \
            "--playera.prop.str='0' " \
            '--playera.prop.cost=0.1 ' \
            '--playerb.cls=alexber.rpsgame.players.ConstantPlayer' \
         .split()

    _, dd = app_conf.parse_sys_args(args=argsv)

    d = dd['playera']

    pytest.assume(app_conf.parse_flat_dict.call_count == 1)
    _, parse_flat_dict_d = app_conf.parse_flat_dict.call_args
    implicit_convert_param = parse_flat_dict_d.get('implicit_convert', True)  # True is default value
    pytest.assume(implicit_convert_param is True)

    cls = d['cls']
    max = d['prop.max']
    str = d['prop.str']
    cost = d['prop.cost']

    pytest.assume(exp_cls == cls)
    pytest.assume(exp_cls_type == type(cls))
    pytest.assume(exp_max == max)
    pytest.assume(exp_max_type == type(max))
    pytest.assume(exp_str == str)
    pytest.assume(exp_str_type == type(str))
    pytest.assume(exp_cost == cost)
    pytest.assume(exp_cost_type == type(cost))

def test_parse_flat_dict_without_impicit_convert(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    mocker.spy(app_conf, '_convert')


    exp_playera_d = OrderedDict()
    exp_playera_d['.'.join([app_conf.PLAYER_A_KEY, app_conf.CLS_KEY])] = 'alexber.rpsgame.players.ConstantPlayer'
    exp_playera_d['.'.join([app_conf.PLAYER_A_KEY, prop_prefix, 'max'])] = 100
    exp_playera_d['.'.join([app_conf.PLAYER_A_KEY, prop_prefix, 'str'])] = "'0'"
    exp_playera_d['.'.join([app_conf.PLAYER_A_KEY, prop_prefix, 'cost'])] = 0.1

    exp_playerb_d = OrderedDict()
    exp_playerb_d['.'.join([app_conf.PLAYER_B_KEY, app_conf.CLS_KEY])] = 'alexber.rpsgame.players.MyPlayer'

    d = {**exp_playera_d, **exp_playerb_d}

    res = app_conf.parse_flat_dict(d, implicit_convert=False)
    pytest.assume(app_conf._convert.call_count == 0)

    playera_d = res[app_conf.PLAYER_A_KEY]
    playerb_d = res[app_conf.PLAYER_B_KEY]

    pytest.assume(exp_playera_d, playera_d)
    pytest.assume(exp_playerb_d, playerb_d)

def test_parse_flat_dict_with_impicit_convert(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    mocker.spy(app_conf, '_convert')


    exp_max = 100
    exp_max_type = int
    exp_str = '0'
    exp_str_type = type('') #str
    exp_cost = 0.1
    exp_cost_type = float

    exp_playera_d = OrderedDict()
    exp_playera_d['.'.join([app_conf.PLAYER_A_KEY, app_conf.CLS_KEY])] = 'alexber.rpsgame.players.ConstantPlayer'
    exp_playera_d['.'.join([app_conf.PLAYER_A_KEY, prop_prefix, 'max'])] = exp_max
    exp_playera_d['.'.join([app_conf.PLAYER_A_KEY, prop_prefix, 'str'])] = exp_str
    exp_playera_d['.'.join([app_conf.PLAYER_A_KEY, prop_prefix, 'cost'])] = exp_cost_type

    exp_playerb_d = OrderedDict()
    exp_playerb_d_cls = 'alexber.rpsgame.players.MyPlayer'
    exp_playerb_d['.'.join([app_conf.PLAYER_B_KEY, app_conf.CLS_KEY])] = exp_playerb_d_cls

    d = {**exp_playera_d, **exp_playerb_d}

    res = app_conf.parse_flat_dict(d, implicit_convert=True)
    pytest.assume(app_conf._convert.call_count > 0)

    playera_d = res[app_conf.PLAYER_A_KEY]
    playerb_d = res[app_conf.PLAYER_B_KEY]

    res_max = playera_d['.'.join([prop_prefix, 'max'])]
    res_str = playera_d['.'.join([prop_prefix, 'str'])]
    res_cost = playera_d['.'.join([prop_prefix, 'cost'])]

    pytest.assume(exp_max, res_max)
    pytest.assume(exp_max_type, type(res_max))
    pytest.assume(exp_str, res_str)
    pytest.assume(exp_str_type, type(res_str))
    pytest.assume(exp_cost, res_cost)
    pytest.assume(exp_cost_type, type(res_cost))

    playerb_d_cls = playerb_d[app_conf.CLS_KEY]
    pytest.assume(exp_playerb_d_cls, playerb_d)


def test_parse_dict_without_impicit_convert(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    mocker.spy(app_conf, '_convert')

    dd = OrderedDict()

    d=dd.setdefault(app_conf.PLAYER_A_KEY, OrderedDict())
    d[app_conf.CLS_KEY] = 'alexber.rpsgame.players.ConstantPlayer'

    d['.'.join([prop_prefix, 'max'])] = 100
    d['.'.join([prop_prefix, 'str'])] = "'0'"
    d['.'.join([prop_prefix, 'cost'])] = 0.1

    res = app_conf.parse_dict(dd, implicit_convert=False)

    pytest.assume(app_conf._convert.call_count == 0)
    pytest.assume(res == dd)

def test_parse_dict_with_impicit_convert(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')

    mocker.spy(app_conf, '_convert')

    dd = OrderedDict()

    d=dd.setdefault(app_conf.PLAYER_A_KEY, OrderedDict())
    d[app_conf.CLS_KEY] = 'alexber.rpsgame.players.ConstantPlayer'


    exp_max = 100
    exp_max_type = int
    exp_str = '0'
    exp_str_type = type('') #str
    exp_cost = 0.1
    exp_cost_type = float

    d['.'.join([prop_prefix,'max'])] = exp_max
    d['.'.join([prop_prefix,'str'])] = f"'{exp_str}'"
    d['.'.join([prop_prefix,'cost'])] = exp_cost

    result = app_conf.parse_dict(dd, implicit_convert=True)
    res = result[app_conf.PLAYER_A_KEY]

    pytest.assume(app_conf._convert.call_count >0)
    pytest.assume(res != dd)
    res_max = res['.'.join([prop_prefix, 'max'])]
    res_str = res['.'.join([prop_prefix, 'str'])]
    res_cost = res['.'.join([prop_prefix,'cost'])]

    pytest.assume(exp_max, res_max)
    pytest.assume(exp_max_type, type(res_max))
    pytest.assume(exp_str, res_str)
    pytest.assume(exp_str_type, type(res_str))
    pytest.assume(exp_cost, res_cost)
    pytest.assume(exp_cost_type, type(res_cost))


if __name__ == "__main__":
    pytest.main([__file__])
