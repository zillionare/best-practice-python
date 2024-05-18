import logging
from unittest import mock

import pytest
from sample.bar import get_operating_system, my_bark
from sample.core.foo import bar


def test_my_bark():
    with mock.patch("sample.core.foo.Foo.bark", return_value="mock_bark"):
        assert my_bark() == "mock_bark"


def test_get_operation_system():
    target_will_fail = "sample.core.foo.is_windows"
    target_will_succeed = "sample.bar.is_windows"
    with mock.patch(target_will_succeed, return_value=False):
        assert get_operating_system() == "Linux"


def test_mock_side_effect():
    with mock.patch('builtins.input', side_effect = ValueError):
        with pytest.raises(ValueError) as e:
            input()

def test_mock_multiple_return():
    with mock.patch('builtins.input', side_effect = [1, 2, 3]):
        assert input() == 1
        assert input() == 2
        assert input() == 3


def test_mock_object():
    logger = logging.getLogger('sample.core.foo')
    with mock.patch.object(logger, 'info') as m:
        bar()
        m.assert_called_once_with("please check if I was called")
