from unittest.mock import patch

from where_to_patch.bar import Bar

tmp = Bar()

def test_where_to_path():
    with patch('where_to_patch.foo.get_name', return_value="Bob"):
        name = tmp.name()
        assert name == "Bob"
