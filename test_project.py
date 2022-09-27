from project import cli, option, music, video
import pytest

def test_cli():
    assert cli("-m") == {'music': True, 'video': False}
    assert cli("--music") == {'music': True, 'video': False}
    assert cli("-v") == {'music': False, 'video': True}
    assert cli("--video") == {'music': False, 'video': True}


def test_option():
    print(option.tags)
