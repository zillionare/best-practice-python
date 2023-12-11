from unittest.async_case import IsolatedAsyncioTestCase
from unittest.mock import patch

from example10.bar import Bar


class BarTest(IsolatedAsyncioTestCase):
    async def test_bar(self):
        tmp = Bar()
        with patch('example10.foo.Foo.method_1', return_value="mocked!"):
            print(await tmp.method_2())
