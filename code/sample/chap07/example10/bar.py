
from .foo import Foo


class Bar(object):
    async def method_2(self):
        tmp = Foo()
        return await tmp.method_1()
