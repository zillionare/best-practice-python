# 代码单元测试——基于Unittest、Pytest、Pycoverage和Tox
## 测试代码的组织结构
## Unittest框架
### 测试文件的基本结构
### 如何使用Mock（内含案例）
### 使用断言（内含案例）
## Pytest测试库


# 单元测试

单元测试的概念可能多数读者都有接触过。作为开发人员，我们编写一个个测试用例，测试框架则用来发现和组装测试suite，收集测试报告，并且提供测试基础设施（断言、mock、setup和teardown等）。Python当中最主流的单元测试框架有三种，Pytest, nose和Unittest，其中Unittest是标准库，其它两种是第三方工具。在向导生成的项目中，就使用了Pytest来驱动测试。

这里主要比较一下pytest和unittest。多数情况下，当我们选择单元测试框架时，选择二者之一就好了。unitttest基于类来组织测试用例，而pytest则是函数式的，基于模块来组织测试用例，同时它也提供了group概念来组织测试用例。pytest的mock是基于第三方的pytest-mock，而pytest-mock实际上只是对标准库中的mock的简单封装。单元测试都会有setup和teardown的概念，unittest直接使用了setUp和tearDown作为测试入口和结束的API，在pytest中，则是通过fixture来实现，这方面学习曲线可能稍微陡峭一点。在断言方面，pytest使用python的关键字assert进行断言，比unittest更为简洁，不过断言类型上没有unittest丰富。

另外一个值得一提的区别是，unittest从python 3.8起就内在地支持asyncio，而在pytest中，则需要插件pytest-asyncio来支持。但两者在测试的兼容性上并没有大的不同。

pytest的主要优势是有：
1. pytest的测试用例更简洁。由于测试用例并不是正式代码，开发者当然希望少花时间在这些代码上，因此代码的简洁程度很重要。
2. 提供了命令行工具。如果我们仅使用unittest，则执行单元测试必须要使用`python -m unittest`来执行；而通过pytest来执行单元测试，我们只需要调用`pytest .`即可。
3. pytest提供了marker，可以更方便来决定哪些用例执行或者不执行。
4. pytest提供了参数化测试。

这里我们简要地举例说明一下什么是参数化测试，以便读者理解为什么参数化测试是一个值得一提的优点。
```python {class='line-numbers'}
import pytest
from datetime import datetime
from src.example import get_time_of_day

@pytest.mark.parametrize(
    "datetime_obj, expect",
    [
        (datetime(2016, 5, 20, 0, 0, 0), "Night"),
        (datetime(2016, 5, 20, 1, 10, 0), "Night"),
        (datetime(2016, 5, 20, 6, 10, 0), "Morning"),
        (datetime(2016, 5, 20, 12, 0, 0), "Afternoon"),
        (datetime(2016, 5, 20, 14, 10, 0), "Afternoon"),
        (datetime(2016, 5, 20, 18, 0, 0), "Evening"),
        (datetime(2016, 5, 20, 19, 10, 0), "Evening"),
    ],
)
def test_get_time_of_day(datetime_obj, expect, mocker):
    mock_now = mocker.patch("src.example.datetime")
    mock_now.now.return_value = datetime_obj

    assert get_time_of_day() == expect​
```
如果使用unittest，我们需要写一个循环，依次调用get_time_of_day()，然后对比结果。代码量要多出不少。

基于以上原因，在后面的内容中，我们将以pytest为例进行介绍。
## 测试代码的组织

我们一般将所有的测试代码都归类在项目根目录下的tests文件夹中。每个测试文件的名字，要么使用test_*.py，要么使用*_test.py。这是测试框架的要求。如此以来，当我们执行命令如``pytest tests``时，测试框架就能从这些文件中发现测试用例，并组合成一个个待执行的suite。

在test_*.py中，函数名一样要遵循一定的模式，比如使用test_xxx。不遵循规则的测试函数，不会被执行。

一般来说，测试文件应该与功能模块文件一一对应。如果被测代码有多重文件夹，对应的测试代码也应该按同样的目录来组织。这样做的目的，是为了方便查找对应的测试代码，方便我们添加新的测试用例。

比如在ppw生成的示例工程中，我们有：
```
sample
├── sample
│   ├── __init__.py
│   ├── app.py
│   └── cli.py
├── tests
│   ├── __init__.py
│   ├── test_app.py
│   └── test_cli.py
```
注意这里面的__init__.py，如果缺少的话，tests就不会成为一个合法的包，从而导致pytest无法正确导入测试用例。
## Pytest
使用pytest写测试用例很简单。假设sample\app.py如下所示：
```
def inc(x:int)->int:
    return x + 1
```
则我们的test_app.py只需要有以下代码即可完成测试：
```
import pytest
from sample.app import inc

def test_inc():
    assert inc(3) == 4
```
这比unittest下的代码要简洁很多。

### 测试用例的组装
在pytest中，pytest会按传入的文件（或者文件夹），搜索其中的测试用例并组装成测试集合(suite)。除此之外，它还能通过pytest.mark来标记哪些测试用例是需要执行的，哪些测试用例是需要跳过的。

```python {class='line-numbers'}
import pytest

@pytest.mark.webtest
def test_send_http():
    pass  # perform some webtest test for your app


def test_something_quick():
    pass


def test_another():
    pass


class TestClass:
    def test_method(self):
        pass
```

然后我们就可以选择只执行标记为webtest的测试用例：
```bash {class='line-numbers'}
pytest -v -m webtest

=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-7.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 4 items / 3 deselected / 1 selected

test_server.py::test_send_http PASSED                                [100%]

===================== 1 passed, 3 deselected in 0.12s ======================
```
从输出可以看出，只有test_send_http被执行了。

这里的webtest是自定义的标记。pytest还内置了这些标记，有的也可以用来筛选用例：
1. pytest.mark.filterwarnings， 给测试用例添加filterwarnings标记，可以忽略警告信息。
2. pytest.mark.skip，给测试用例添加skip标记，可以跳过测试用例。
3. pytest.mark.skipif, 给测试用例添加skipif标记，可以根据条件跳过测试用例。
4. pytest.mark.xfail, 在某些条件下（比如运行在某个os上），用例本应该失败，此时就应使用此标记，以便在测试报告中标记出来。
5. pytest.mark.parametrize, 给测试用例添加参数化标记，可以根据参数化的参数执行多次测试用例。

这些标记可以用pytest --markers命令查看。
### pytest 断言
pytest中的断言巧妙地拦截并复用了python内置的函数assert，从而在这一部分的学习成本变得非常低。

```python {class='line-numbers'}
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
```
上面的代码分别演示了如何判断内置类型、列表、集合、字典、浮点数和浮点数组是否相等。这部分语法跟标准python语法并无二致。pytest与unittest一样，都没有提供如何判断两个浮点数数组是否相等的断言，如果有这个需求，我们可以求助于numpy.testing，正如例子中第25~30行所示。

有时候我们需要测试错误处理，看函数是否正确地抛出了异常，代码32~37演示了异常断言的使用。注意这里我们不应该这么写：
```python {class='line-numbers'}
    try:
        # call some_func will raise ValueError
    except ValueError as e:
        assert str(e) == "some error":
    else:
        assert False
```
上述代码看上去逻辑正确，但它混淆了异常处理和断言，使得他人一时难以分清这段代码究竟是在处理测试代码中的异常呢，还是在测试被调用函数能否正确抛出异常，明显不如异常断言那样清晰。
### pytest fixture
一般而言，我们的测试用例很可能需要依赖于一些外部资源，比如数据库、缓存、第三方微服务等。这些外部资源的初始化和销毁，我们希望能够在测试用例执行前后自动完成，即自动完成setup和teardown的操作。这时候，我们就需要用到pytest的fixture。

!!! Info
    在单元测试中是否需要使用外部资源是一个见仁见智的问题。有的看法认为，一旦引入外部资源，测试用例就不再是单元测试，而是集成测试。时代总在发展，特别是进入容器化时代后，在测试中快速创建一个专属的数据库服务器变得十分快捷和容易，这可能要比我们通过大量的mock来进行外部资源隔离更容易，因此我们也没必要于拘泥于这些看法。

假定我们有一个测试用例，它需要连接数据库，代码如下(参见code/chap07/sample/app.py)

```python {class='line-numbers'}
import asyncpg
import datetime

async def add_user(conn: asyncpg.Connection, name: str, date_of_birth: datetime.date)->int:
    # Insert a record into the created table.
    await conn.execute('''
        INSERT INTO users(name, dob) VALUES($1, $2)
    ''', name, date_of_birth)

    # Select a row from the table.
    row: asyncpg.Record = await conn.fetchrow(
        'SELECT * FROM users WHERE name = $1', 'Bob')
    # *row* now contains
    # asyncpg.Record(id=1, name='Bob', dob=datetime.date(1984, 3, 1))
    return row["id"]
```
我们展示测试代码(参见code/chap07/sample/test_app.py)，再结合代码讲解fixture的使用：

```python {class='line-numbers'}
import pytest
from sample.app import add_user
import pytest_asyncio
import asyncio

# pytest-asyncio已经提供了一个event_loop的fixture,但它是function级别的
# 这里我们需要一个session级别的fixture，所以我们需要自己实现
@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope='session')
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
```
我们的功能代码很简单，就是往users表里插入一条记录，并返回它在表中的id。测试代码调用add_user这个函数，然后检测返回值是否为1（如果每次测试前都新建数据库或者清空表的话，那么返回的ID就应该是1）。

这个测试显然需要连接数据库，因此我们需要在测试前创建一个数据库连接，然后在测试结束后关闭连接。并且，我们还会有多个测试用例需要连接数据库，因此我们希望数据库连接是一个全局的资源，可以在多个测试用例中共享。这就是fixture的用武之地。

fixture是一些函数，pytest会在执行测试函数之前（或之后）加载运行它们。但与unitest中的setup和teardown不同，pytest中的fixture依赖是显式声明的。比如，在上面的test_add_user显式依赖了db这个fixture(通过在函数声明中传入db作为参数)，而db则又显示依赖event_loop这个fixture。即使文件中还存在其它fixture, test_add_user也不会依赖到这些fixture，因为依赖必须显式声明。

上面的代码中，我们演示的是对异步函数add_user的测试。显然，异步函数必须在某个event loop中执行，并且相关的初始化(setup)和退出操作(teardown)也必须在同一个loop中执行。这里是分别通过pytest.mark.asyncio, pytest_asyncio等要件来实现的。

首先，我们需要将测试用例标注为异步执行，即上面的代码第21行。其次，test_add_user需要一个数据库连接，该连接由fixture `db`来提供。这个连接的获得也是异步的，因此，我们不能使用pytest.fixutre来声明该函数，而必须使用@pytest_asyncio.fixture来声明该函数。

最后，我们还必须提供一个event_loop的fixture，它是一切的关键。当某个函数被pytest.mark.asyncio装饰时，该函数将在event_loop提供的event loop中执行。

我们还要介绍一下出现在第6行和第13行中的scope='session'。这个参数表示fixture的作用域，它有四个可选值：function, class, module和session。默认值是function，表示fixture只在当前测试函数中有效。在上面的示例中，我们希望这个event loop在一次测试中都有效，所以将scope设置为session。

上面的例子是关于异步模式下的测试的。对普通函数的测试更简单一些。我们不需要pytest.mark.asynio这个装饰器，也不需要event_loop这个fixture。所有的pytest_asyncio.fixture都换成pytest.fixture即可（显然，它必须、也只能装饰普通函数，而非由async定义的函数）。

!!! Info
    如果我们使用unittest来对异步代码进行测试，要注意首先测试类要从unittest.IsolatedAsyncioTestCase继承，然后测试函数要以async def定义。并且setup和teardown都要换成它们的异步版本asyncSetup、asyncTeardown。
    
    注意只有从python 3.8开始，unittest才直接支持异步测试。在python 3.7及之前的版本中，我们需要使用第三方库aiounittest。

我们通过上面的例子演示了fixture。与markers类似，我们可以通过pytest --fixtures来显示当前环境中所有的fixture。
```bash
pytest --fixtures

------------- fixtures defined from faker.contrib.pytest.plugin --------------
faker -- .../faker/contrib/pytest/plugin.py:24
    Fixture that returns a seeded and suitable ``Faker`` instance.

------------- fixtures defined from pytest_asyncio.plugin -----------------
event_loop -- .../pytest_asyncio/plugin.py:511
    Create an instance of the default event loop for each test case.

...

------------- fixtures defined from tests.test_app ----------------
event_loop [session scope] -- tests/test_app.py:45

db [session scope] -- tests/test_app.py:52
```

这里我们看到faker.contrib提供了一个名为faker的fixture, 我们之前安装的、支持异步测试的pytest_asyncio也提供了名为event_loop的fixture(为节省篇幅，其它几个省略了)，以及我们自己测试代码中定义的event_loop和db这两个fixture。

为了后面讲解方便，我们现在来安装pytest-mock这个插件，看看它提供的fixture。
```bash
pip install pytest-mock
pytest --fixture

------- fixtures defined from pytest_mock.plugin --------
class_mocker [class scope] -- .../pytest_mock/plugin.py:419
    Return an object that has the same interface to the `mock` module, but
    takes care of automatically undoing all patches after each test method.

mocker -- .../pytest_mock/plugin.py:419
    Return an object that has the same interface to the `mock` module, but
    takes care of automatically undoing all patches after each test method.

module_mocker [module scope] -- .../pytest_mock/plugin.py:419
    Return an object that has the same interface to the `mock` module, but
    takes care of automatically undoing all patches after each test method.

package_mocker [package scope] -- .../pytest_mock/plugin.py:419
    Return an object that has the same interface to the `mock` module, but
    takes care of automatically undoing all patches after each test method.

session_mocker [session scope] -- .../pytest_mock/plugin.py:419
    Return an object that has the same interface to the `mock` module, but
    takes care of automatically undoing all patches after each test method.
```
可以看到pytest-mock提供了5个fixture。后面我们会较多地介绍其中的mocker这个fixture。
## Mock
在单元测试时，我们希望测试环境尽可能单纯、可控。因此我们不希望依赖于用户输入，不希望连接数据库或者真实的第三方微服务等。这时候，我们需要通mock来模拟这些外部接口。mock可能是单元测试中最核心的技术。

!!! Readmore
    感谢容器技术！现在单元测试中，越来越多地连接数据库、缓存和第三方微服务了。因为对有一些接口进行mock的代价，已经超过了launch一个容器，初始化数据库再开始测试了。

前面已经提到，无论是unittest还是pytest，都是直接或者间接使用了unittest中的mock模块。所以，当你遇到mock相关的问题，请参阅[mock](https://docs.python.org/3/library/unittest.mock.html)。

!!! info
    python从3.8起，才对async模式下的mock有比较完备的支持。幸好，在本书发布之前，python 3.7就应该已经走到生命的尽头了。

最常用的mock对象有Mock, MagicMock和patch。MagicMock是Mock的子类。如果你之前接触过其它mock框架的话，可能需要注意，python中的mock是’action -> assertion‘模式，而不是其它语言中常见的'record -> replay’模式。

在unittest中要使用mock, 我们需要手动导入mock模块。在pytest中，我们可以直接使用mocker这个fixture。
```python
# unittest example
import unittest
from unittest import mock

class Test(unittest.TestCase):
    def test_mock(self):
        # 在unittest中，我们通过mock模块来调用patch方法
        with mock.patch('builtins.input', return_value = 'Y') as m:
            self.assertEqual('Y', input('continure or not? [Y]/n'))

# pytest example
def test_mock(mocker):
    # 在pytest中，我们通过mocker这个fixture来调用patch方法
    mocker.patch('builtins.input', return_value = 'Y')
    assert 'Y' == input('continure or not? [Y]/n')
```
上面的例子清楚地演示了两个框架中应该如何调用patch方法。如果我们要使用Mock或者MagicMock这两个类，也是一样，只不过在pytest中，我们需要通过mocker这个对象来引用它们。

现在我们来介绍一下patch方法。patch是一个context manager（也可以当装饰器用），它可以用来mock一个对象。上面的例子已经演示了如何mock一个内置函数。内置函数是指象open、print、input这样的方法，我们可以在程序中无须导入即可直接使用，但是在mock它们时，我们必须通过'builtins'这个名字空间来引用它们，这也是我们在这里特别举例的原因。另一个需要特别说明的内置库是datetime，当你需要mock这个库时，我们的建议是使用freezegun这个库，而不是使用patch。
```python {class = 'line-numbers'}
@freeze_time("2021-01-01")
def test_freezegun():
    now = datetime.datetime(2021, 1, 1)
    assert now == datetime.datetime.now()
```

mock自己代码中的方法，或者第三方库中的方法一般来讲是比较容易的，关键是要找到正确的引用方法。在第7章的示例代码中，有这样一小段程序：

```python {class='line-numbers'}
# from sample\core\foo.py
def is_windows():
    return True


def get_operating_system():
    return "Windows" if is_windows() else "Linux"


class Foo:
    def bark(self):
        return "bark"

# from sample\tests\core\test_foo.py
def test_get_operating_system(mocker):
    mocker.patch("sample.core.foo.is_windows", return_value=False)
    assert get_operating_system() == "Linux"
```
第16行中的"sample.core.foo.is_windows"被称作target，return_value则是我们调用target方法时，所期望返回的值。

上面的例子中，我们mock了一个普通方法，如果我们要mock一个类的方法呢？此时target的写法应该是'package.package.module.Class.method'。以第10~12行定义的Foo对象的bark方法为例，target的写法应该是'sample.core.foo.Foo.bark'。

这里我们要指出一个初学者很容易掉进去的坑，就是明明target正确，但是却无法mock成功。在unittest的文档中有这样一句话

!!! quote
    The basic principle is that you patch where an object is looked up, which is not necessarily the same place as where it is defined. 

也就是，patch应用于哪个target对象，取决于被mock对象是在哪里被引用的，而不是在哪里被定义的。

我们通过一个例子来详细说明这个问题。假设在前面的foo.py之外，还有一个sample\bar.py文件，定义如下：
```python {class='line-numbers'}
# sample\bar.py
from sample.core.foo import Foo, is_windows

def my_bark() -> str:
    foo = Foo()
    return foo.bark()

def get_operating_system() -> str:
    return "Windows" if is_windows() else "Linux"
```

对应的测试文件tests\test_bar.py定义如下：
```python {class='line-numbers'}
from sample.bar import get_operating_system, my_bark

def test_my_bark(mocker):
    with mocker.patch("sample.core.foo.Foo.bark", return_value="mock_bark"):
        assert my_bark() == "mock_bark"

def test_get_operation_system(mocker):
    target_will_fail = "sample.core.foo.is_windows"
    target_will_succeed = "sample.bar.is_windows"
    with mocker.patch(target_will_fail, return_value=False):
        assert get_operating_system() == "Linux"
```
运行测试，发现test_my_bark测试通过，而test_get_operation_system测试失败。说明其中一个mock成功，另一个mock失败。这是为什么呢？

在test_get_operation_system中，导致测试失败的target是target_will_fail，即sample.core.foo.is_windows，被测试函数get_operating_system来自由bar.py，在它调用is_windows之前，这个is_windows已经被导入到sample.bar这个名字空间里，sample.bar持有了这个引用（应该是以传值的方式），因此当patch方法对sample.core.foo.is_windows进行修改时，这个改动并不会传递给sample.bar中的is_windows。这就是unittest文档中所说的，patch应用于哪个target对象，取决于被mock对象是在哪里被引用的（sample.bar)，而不是在哪里被定义的(sample.core.foo)。

但上面的理论无法解释为什么test_my_bark测试通过。原因可能还是传值引用的原因。在my_bark中，当调用foo.bark()时，foo对象并没有自己的bark方法，因此它还是会去寻找sample.core.foo.Foo中的bark方法，而这个方法已经被patch了，因此test_my_bark测试通过。

前面我们讨论了patch的一个用法，即patch一个函数的返回值。有时候我们不关心函数的返回值，而是希望函数在被调用时，能够无条件地抛出某个异常，这时就需要用到`side_effect`参数。

```python {class='line-numbers'}
# tests\test_bar.py
import pytest
def test_mock_side_effect(mocker):
    with mocker.patch('builtins.input', side_effect = ValueError):
        with pytest.raises(ValueError) as e:
            input()
```
上述代码不仅模拟出了一个ValueError，还检测这个异常是否抛出。通过这种方式，异常处理代码现在也可以轻松覆盖到了。

side_effect不仅可以用来模拟异常，还可以用来模拟多次调用的返回值。比如，我们希望某个函数在第一次调用时返回1，第二次调用时返回2，第三次调用时返回3，以此类推。这时可以这样写：
```python {class='line-numbers'}
# tests\test_bar.py
def def test_mock_multiple_return(mocker):
    with mocker.patch('builtins.input', side_effect = [1, 2, 3]):
        assert input() == 1
        assert input() == 2
        assert input() == 3
```
我们一共调用了input三次，每次mock都按期望返回了不同的数值。

上面的例子中，我们给patch传入的target是一个字符串，显然，在patch作用域内，所有的新生成的对象都会被patch。如果在patch之前，对象已经生成了，我们则需要使用`patch.object`来完成patch。

```python {class='line-numbers'}
# sample\core\foo.py

def bar():
    logger = logging.getLogger(__name__)
    logger.info("please check if I was called")

    root_logger = logging.getLogger()
    root_logger.info("this is not intercepted")

# test_foo.py
from sample.core.foo import bar

logger = logging.getLogger('sample.core.foo')
with mock.patch.object(logger, 'info') as m:
    bar()
    m.assert_called_once_with("please check if I was called")
```

两个logger(root_logger和'sample.core.foo'对应的logger)都被调用，但我们只拦截了后一个logger的`info`方法，结果验证它被调用，且仅被调用一次。

这里要提及pytest中mocker.patch与unitest.mock.patch的一个细微差别。后者进行patch时，可以返回mock对象，我们可以通过它进行更多的检查（见上面示例代码中的第14，16行）；但mocker.patch的返回值是None。

## 衡量测试的覆盖率
### 配置Pycoverage
### 发布覆盖率报告
### 案例：提高测试覆盖率
## Tox环境矩阵加速测试
### 什么是Tox？
### Tox的工作原理
### 如何配置Tox
