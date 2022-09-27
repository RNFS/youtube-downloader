from project import cli, option, get_tag, music, video
import pytest

def test_cli():
    assert cli("-m") == {'music': True, 'video': False}
    assert cli("--music") == {'music': True, 'video': False}
    assert cli("-v") == {'music': False, 'video': True}
    assert cli("--video") == {'music': False, 'video': True}


def test_get_tag():
    dict = {
        "l_options":[{'itag': '139', 'qu': '48', 'num': 1}, {'itag': '140', 'qu': '128', 'num': 2}],
        "type_":"audio"
        }
    assert get_tag(dict) ==  "140"


# def test_option():
#     print(option.tags)
