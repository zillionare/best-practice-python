from unittest.mock import patch

from where_to_patch.bar import Bar

tmp = Bar()

with patch('where_to_patch.foo.get_name', return_value="Bob"):
    name = tmp.name()
    assert name == "Bob"
