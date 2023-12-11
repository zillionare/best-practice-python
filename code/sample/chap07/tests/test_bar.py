from sample.bar import get_operating_system, my_bark
from sample.core.foo import bar
import logging
from unittest import mock


def test_my_bark(mocker):
    with mocker.patch("sample.core.foo.Foo.bark", return_value="mock_bark"):
        assert my_bark() == "mock_bark"


def test_get_operation_system(mocker):
    target_will_fail = "sample.core.foo.is_windows"
    target_will_succeed = "sample.bar.is_windows"
    with mocker.patch(target_will_succeed, return_value=False):
        assert get_operating_system() == "Linux"

import pytest
def test_mock_side_effect(mocker):
    with mocker.patch('builtins.input', side_effect = ValueError):
        with pytest.raises(ValueError) as e:
            input()

def test_mock_multiple_return(mocker):
    with mocker.patch('builtins.input', side_effect = [1, 2, 3]):
        assert input() == 1
        assert input() == 2
        assert input() == 3


def test_mock_object():
    logger = logging.getLogger('sample.core.foo')
    with mock.patch.object(logger, 'info') as m:
        bar()
        m.assert_called_once_with("please check if I was called")
