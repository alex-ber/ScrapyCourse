import logging
logger = logging.getLogger(__name__)
from pathlib import Path
import pytest

from alexber.utils.props import Properties


def test_parse_java_properties_alternative_delim(request, mocker):
    logger.info(f'{request._pyfuncitem.name}()')
    mocker.patch.object(Properties, 'PLACEHOLDER_TOKEN', new_callable=lambda :'@')
    exp_cls_name_a = 'alexber.rpsgame.players.ConstantPlayer'
    exp_cls_name_b = exp_cls_name_a
    expdd = {'playera.cls': 'alexber.rpsgame.players.ConstantPlayer',
             'playerb.cls': 'alexber.rpsgame.players.ConstantPlayer', }

    dir = Path(__file__).parent

    p = Properties()
    with open(dir / 'config2.properties') as f:
        p.load(f)
    dd = p.as_dict()

    assert expdd == dd


def test_parse_java_properties(request):
    logger.info(f'{request._pyfuncitem.name}()')
    exp_cls_name_a = 'alexber.rpsgame.players.ConstantPlayer'
    exp_cls_name_b = exp_cls_name_a
    expdd = {'playera.cls': 'alexber.rpsgame.players.ConstantPlayer',
             'playerb.cls': 'alexber.rpsgame.players.ConstantPlayer',}

    dir = Path(__file__).parent

    p = Properties()
    with open(dir / 'config.properties') as f:
        p.load(f)
    dd = p.as_dict()
    #we want to ignore key inner.*
    a_cls_name = dd['playera.cls']
    b_cls_name = dd['playerb.cls']

    d = {'playera.cls': a_cls_name,
         'playerb.cls': b_cls_name,}

    assert expdd==d





if __name__ == "__main__":
    pytest.main([__file__])
