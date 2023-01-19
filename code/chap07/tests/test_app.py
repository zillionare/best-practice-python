import pytest
from sample.app import add_user
import pytest_asyncio
import asyncio

def test_assertion():
    # 判断基本变量相等
    assert "loud noises".upper() == "LOUD NOISES"

    # 判断列表相等
    assert [1, 2, 3] == list((1, 2, 3))

    # 判断集合相等
    assert set([1, 2, 3]) == {1, 3, 2}

    # 判断字典相等
    assert dict({
        "one": 1,
        "two": 2
    }) == {
        "one": 1,
        "two": 2
    }

    # 判断浮点数相等
    # 缺省地， origin  ± 1e-06
    assert 2.2 == pytest.approx(2.2 + 1e-6)
    assert 2.2 == pytest.approx(2.3, 0.1)

    # 如果要判断两个浮点数组是否相等，我们需要借助numpy.testing
    import numpy

    arr1 = numpy.array([1., 2., 3.])
    arr2 = arr1 + 1e-6
    numpy.testing.assert_array_almost_equal(arr1, arr2)

    # 异常断言：有些用例要求能抛出异常
    with pytest.raises(ValueError) as e:
        raise ValueError("some error")
    
    msg = e.value.args[0]
    assert msg == "some error"

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope='session')
# @pytest.fixture(scope='session')
async def db():
    import asyncpg
    conn = await asyncpg.connect('postgresql://zillionare:123456@localhost/bpp')
    yield conn

    await conn.close()

@pytest.mark.asyncio
async def test_add_user(db):
    import datetime
    user_id = await add_user(db, 'Bob', datetime.date(2022, 1, 1))
    assert user_id == 1
