from project import cli, option, music, video
import pytest

def test_cli():
    assert cli("-m") == {'music': True, 'video': False}
    assert cli("--music") == {'music': True, 'video': False}
    assert cli("-v") == {'music': False, 'video': False}
    assert cli("-viedo") == {'music': False, 'video': False}
