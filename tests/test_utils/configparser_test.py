import logging
import pytest

from alexber.utils.configparsers import ConfigParser

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


if __name__ == "__main__":
    pytest.main([__file__])
