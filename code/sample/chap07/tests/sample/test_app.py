import asyncio

import pytest
import pytest_asyncio
from gino import Gino
from sample.app import add_user

engine = Gino()
class User(engine.Model):
    global engine
    __tablename__ = "users"

    id = engine.Column(engine.Integer(), primary_key=True)
    name = engine.Column(engine.Unicode(), default="noname")
    dob = engine.Column(engine.Date(), nullable=False)

@pytest_asyncio.fixture(scope="session")
async def setup():
    global engine

    await engine.set_bind("postgresql://zillionare:123456@localhost/pbp")
    await engine.gino.create_all()

# pytest-asyncio已经提供了一个event_loop的fixture,但它是function级别的
# 这里我们需要一个session级别的fixture，所以我们需要自己实现
@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db():
    import asyncpg

    conn = await asyncpg.connect("postgresql://zillionare:123456@localhost/pbp")
    yield conn

    await conn.close()


@pytest.mark.asyncio(scope="session")
async def test_add_user(db, setup):
    import datetime

    user_id = await add_user(db, "Bob", datetime.date(2022, 1, 1))
    assert user_id == 1
    print("userid is", user_id)
