上一章里，我们通过ppw生成了一个规范的python项目，对初学者来说，许多闻所未闻、见所未见的概念和名词扑面而来，不免让人一时眼花缭乱，目不睱接。然而，如果我们不从头讲起，可能读者也无从理解，ppw为何需要运用这些技术，又倒底解决了哪些问题。

在2021年3月的某个孤独的夜晚，我决定创建一个创建一个python项目以打发时间，这个项目有以下文件：

```
├── foo
│   ├── foo
│   │   ├── bar
│   │   │   └── data.py
│   └── README.md
```

当然，作为一个有经验的开发人员，我的机器上已经有了好多个其它的python项目，这些项目往往使用不同的Python版本，彼此相互冲突。所以，从一开始，我就决定通过虚拟开发环境来隔离这些不同的工程。这一次也不例外：我通过conda创建了一个名为foo的虚拟环境，并且始终在这个环境下工作。

我们的程序将会访问postgres数据库里的users表。一般来说，我们都会使用sqlalchemy来访问数据库，而避免直接使用特定的数据库驱动。这样做的好处是，万一将来我们需要更换数据库，那么这种迁移带来的工作量将轻松不少。

在2021年，python的异步io已经大放异彩。而sqlalchemy依然不支持这一最新特性，不免让人有些失望 -- 这会导致在进行数据库查询时，python进程会死等数据库返回结果，而无法有效利用CPU时间。好在有一个名为Gino的项目弥补了这一缺陷：

```
pip install gino
```

!!! Warning
    在那个孤独的夜晚，上述命令将安装gino 1.0版本。如果读者想运行这里的程序，请将gino的版本改为1.0.1，即运行 pip install gino==1.0.1

做完这一切准备工作，开始编写代码，其中data.py的内容如下：
```python
# 运行以下代码前，请确保本地已安装postgres数据库，并且创建了名为gino的数据库。

import asyncio
from gino import Gino

db = Gino()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    nickname = db.Column(db.Unicode(), default='noname')


async def main():
    # 请根据实际情况，添加用户名和密码
    # 示例：postgresql://zillionare:123456@localhost/gino
    # 并在本地postgres数据库中，创建gino数据库。
    await db.set_bind('postgresql://localhost/gino')
    await db.gino.create_all()

    # further code goes here

    await db.pop_bind().close()


asyncio.get_event_loop().run_until_complete(main())
```

作为一个对代码有洁癖的人，我坚持始终使用`black`来格式化代码：
```bash
pip install black
black .
```

现在一切ok，运行一下:
```bash
python foo/bar/data.py
```
检查数据库，发现users表已经创建。一切正常。

我希望这个程序在macos, windows和linux等操作系统上都能运行，并且可以运行在从python 3.6到3.9的所有版本上。

这里出现第一个问题。你需要准备12个环境: 三个操作系统，每个操作系统上4个python版本，而且还要考虑如何进行"可复现的部署"的问题。在通过ppw创建的项目中，这些仅仅是通过修改tox.ini和.github\dev.yaml中相关配置就可以做到了。但在没有使用ppw之前，我只能这么做：

在三台分别安装有macos， windows和ubuntu的机器上，分别创建python 3.8到python 3.11的虚拟环境，然后安装相同的依赖。首先，我通过`pip freeze`把开发机器上的依赖抓取出来:

```bash
pip freeze > requirements.txt
```

然后在另一台机器准备好的虚拟环境中，运行安装命令：
```bash
pip install -r requirements.txt
```

这里又出现了第二个问题。`black`纯粹是只用于开发目的，为什么也需要在测试/部署环境上安装呢？因此，在制作`requirements.txt`之前，我决定将`black`卸载掉：

```bash
pip uninstall -y black && pip freeze > requirements.txt
```
然而，仔细检查requirements.txt之后发现，`black`是被移除了，但仅仅是它自己。它的一些依赖，比如`click`， `tomli`等等，仍然出现在这个文件中。

于是，我不得不抛弃`pip freeze`这种作法，只在requirements.txt中加上直接依赖，并且，将这个文件一分为二，将`black`放在requirements_dev.txt中。
```text
# requirements.txt
gino==1.0
```
```text
# requirements_dev.txt
black==18.0
```

现在，在测试环境下，将只安装requirements.txt中的那些依赖。不出所料，项目运行得很流畅，目标达成，放心地去睡觉了。但是，gino还依赖于sqlalchemy和asyncpg。后二者被称为传递依赖。我们锁定了gino的版本，但是gino是否正确锁定了sqlalchemy和asyncpg的版本呢？这一切仍然不得而知。

第二天早晨醒来，sqlalchemy 1.4版本发布了。突然地，当我再安装新的测试环境并进行测试时，程序报出了以下错误：
```
Traceback (most recent call last):
  File "/Users/aaronyang/workspace/best-practice-python/code/05/foo/foo/bar/data.py", line 3, in <module>
    from gino import Gino
  File "/Users/aaronyang/miniforge3/envs/bpp/lib/python3.9/site-packages/gino/__init__.py", line 2, in <module>
    from .engine import GinoEngine, GinoConnection  # NOQA
  File "/Users/aaronyang/miniforge3/envs/bpp/lib/python3.9/site-packages/gino/engine.py", line 181, in <module>
    class GinoConnection:
  File "/Users/aaronyang/miniforge3/envs/bpp/lib/python3.9/site-packages/gino/engine.py", line 211, in GinoConnection
    schema_for_object = schema._schema_getter(None)
AttributeError: module 'sqlalchemy.sql.schema' has no attribute '_schema_getter'
```

我差不多花了整整两天才弄明白发生了什么。我的程序依赖于gino,而gino又依赖于著名的SQLAlchemy。gino 1.0是这样锁定SQLAlchemy的版本的：
```bash
pip install gino==1.0
Looking in indexes: https://pypi.jieyu.ai/simple, https://pypi.org/simple
Collecting gino==1.0
  Downloading gino-1.0.0-py3-none-any.whl (48 kB)
     |████████████████████████████████| 48 kB 129 kB/s 
Collecting SQLAlchemy<2.0,>=1.2
  Downloading SQLAlchemy-1.4.0.tar.gz (8.5 MB)
     |████████████████████████████████| 8.5 MB 2.3 MB/s 
```
!!!Info
    上述文本是在2021年3月安装gino 1.0时的输出。如果您现在运行``pip install gino==1.0``，会安装SQLAlchemy 1.4.46版本，这是它在1.x下的最后一个版本。

从pip的安装日志可以看到，gino声明能接受的SQLAlchemy的最小版本是1.2，最大版本则不到2.0。因此，当我们安装gino 1.0时，只要SQLAlchemy有超过1.2，且于于2.0的最新版本，它就一定会选择安装这个最新版本，最终，SQLAlchemy 1.4.0被安装到环境中。

SQLAlchemy在2020年也意识到了asyncio的重要性，并且从1.4开始使用了异步IO。然而，这样一来，调用接口就必须发生改变 -- 也就是，之前依赖于SQLAlchemy的那些程序，不进行修改是无法直接使用SQLAlchemy 1.4的。1.4.0这个版本发布于2021年3月16日。

原因找到了，最终问题也解决了。最终，我把这个错误报告给了gino，gino的开发者承担了责任，发布了1.0.1,将SQLAlchemy的版本锁定在">1.2,<1.4"这个范围内。

```bash
pip install gino==1.0.1
Looking in indexes: https://pypi.jieyu.ai/simple, https://pypi.org/simple
Collecting gino==1.0.1
  Using cached gino-1.0.1-py3-none-any.whl (49 kB)
Collecting SQLAlchemy<1.4,>=1.2.16
  Using cached SQLAlchemy-1.3.24-cp39-cp39-macosx_11_0_arm64.whl
```

在这个案例中，最终用户并没有要求升级并使用SQLAlchemy的新功能，因此，新的安装本不应该去升级这样一个破坏性的版本；但是如果SQLAlchemy出了新的安全更新，或者bug修复，显然，我们也希望我们的程序在不进行更新发布的情况下，就能对依赖进行更新（否则，如果任何一个依赖发布安全更新，都将导致主程序不得不发布更新的话，这种耦合也是很难接受的）。因此，是否存在一种机制，使得我们的应用在指定直接依赖时，也可以恰当地锁定传递依赖的版本，并且允许传递依赖进行合理的更新？这是我们这个案例提出来的第三个问题。

现在，似乎是我们将产品发布的时候了。我们看到其它人开发的开源项目发布在pypi上，这很酷。我也希望我的程序能被千百万人使用。这就需要编写MANINFEST.in, setup.cfg, setup.py等文件。

MANIFEST.in用来告诉setup tools哪些额外的文件应该被包含在发行包里，以及哪些文件则应该被排除掉。当然在我们这个简单的例子中，这个文件是可以被忽略的。

setup.py中需要指明依赖项、版本号等等信息。由于我们已经使用了requirements.txt和requirements_dev.txt来管理依赖，所以，我们并不希望在setup.py中重复指定 -- 我们希望只更新requirements.txt，就可以自动更新setup.py：

```python
from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()
with open('requirements_dev.txt') as f:
    extras_dev_requires = f.read().splitlines()

setup(
    name='foo',
    version='0.0.1',
    author='Aaron',
    author_email='aaron_yang@jieyu.ai',
    install_requires=install_requires,
    extras_require={'dev': extras_dev_requires},
    packages=['foo'],
)
```
看上去还算完美。但实际上，我们每一次发布时，还会涉及到修改版本号等问题，这都是容易出错的地方。而且，它还不涉及打包和发布。通常，我们还需要编写一个makefile，通过makefile命令来实现打包和发布。

这些看上去都是很常规的操作，为什么不将它自动化呢？这是第四个问题，即如何简化打包和发布。

这就是我们这一章要讨论的主题。我们将以Poetry为主要工具，结合semantic versioning来串起这一话题的讨论。
# Poetry： 简洁清晰的项目管理工具
  
![](http://images.jieyu.ai/images/202104/1-BUUIee-t1I2eqTm0RtDNHQ.jpeg)

[Poetry]是一个依赖管理和打包工具。Poetry的作者解释开发Poetry的初衷时说：

!!! Quote
    Packaging systems and dependency management in Python are rather convoluted and hard to understand for newcomers. Even for seasoned developers it might be cumbersome at times to create all files needed in a Python project: setup.py, requirements.txt, setup.cfg, MANIFEST.in and the newly added Pipfile. So I wanted a tool that would limit everything to a single configuration file to do: dependency management, packaging and publishing.

    翻译：Python的打包系统和依赖管理相当复杂，对新人来讲尤其费解。要正确地创建Python项目所需要的文件:setup.py, requirements.txt, setup.cfg, MANIFEST.in和新加入的pipfile，有时候即使对一个有经验的老手，也是有一些困难的。因此，我希望创建一种工具，只用一个文件就实现依赖管理、打包和发布。

依赖是指我们的应用程序中使用到的第三方库。比如，当你写一个网络爬虫时，很可能会使用requests, lxml等第三方库。因此，您的程序是依赖到这些第三方库的。

我们在上一章中已经介绍过，打包一个Python程序库，需要有setup.py, setup.cfg, MANIFEST.in, requirements.txt等文件，这个流程和规范是[Pypa](https://www.pypa.io)定义的，也成为Python标准库的一部分。但是，在那一章里，我们没有详细介绍这些文件的作用和配置，因为我们已经决定使用Poetry来取代它。

现在，我们来简单地看一下，标准流程有哪些不足？

需求依赖散布于requirements.txt和setup.py之中；当您将依赖加入到工程时，没有人帮你确定它是否与既存的依赖能够和平共处；所以一般的做法是，先将它们加进来，完成开发和测试，在打包之前，运行``pip freeze > requirements.txt``来锁定依赖库的版本。但这也将一些你的工程中并不直接依赖的包加入进来--你可能甚至并不清楚它是做什么的。

项目的版本管理也是一个问题。在老旧的Python项目中，一般我们使用bumpversion来管理版本，它需要使用三个文件。在我的日常使用时，它常常会出现各种问题，最常见的是单双引号导致把``__version__=0.1``当成一个版本号，而不是``0.1``。这样打出来的包名也会奇怪地多一个无意义的version字样。单双引号则是因为你的format工具对字符串常量应该使用什么样的引号规则有自己的意见。

Poetry解决了所有这些问题。它提供了版本管理、依赖解析、构建和发布的一站式服务，并将所有的配置，集中到一个文件中，即pyproject.toml。此外，Poetry还提供了一个简单的工程创建向导。不过这个向导的功能比较简单，我们的推荐是使用上一章介绍的python project wizard。

!!! Readmore
    实际上Poetry还会用到另一个文件，即poetry.lock。这个文件并非独立文件，而是Poetry根据pyproject.toml生成的、锁定了依赖版本的最终文件。

现在，让我们看一眼sample项目中的pyproject.toml文件:
```toml
[tool]
[tool.poetry]
name = "sample"
version = "0.1.0"
homepage = "https://github.com/zillionare/sample"
description = "Skeleton project created by Python Project Wizard (ppw)."
authors = ["aaron yang <aaron_yang@jieyu.ai>"]
readme = "README.md"
license =  "MIT"
classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
]
packages = [
    { include = "sample" },
    { include = "tests", format = "sdist" },
]

[tool.poetry.dependencies]
python = ">=3.7.1,<4.0"
fire = "0.4.0"

black  = { version = "^22.3.0", optional = true}
isort  = { version = "5.10.1", optional = true}
flake8  = { version = "4.0.1", optional = true}
flake8-docstrings = { version = "^1.6.0", optional = true }
pytest  = { version = "^7.0.1", optional = true}
pytest-cov  = { version = "^3.0.0", optional = true}
tox  = { version = "^3.24.5", optional = true}
virtualenv  = { version = "^20.13.1", optional = true}
pip  = { version = "^22.0.3", optional = true}
mkdocs  = { version = "^1.2.3", optional = true}
mkdocs-include-markdown-plugin  = { version = "^3.2.3", optional = true}
mkdocs-material  = { version = "^8.1.11", optional = true}
mkdocstrings  = { version = "^0.18.0", optional = true}
mkdocs-material-extensions  = { version = "^1.0.3", optional = true}
twine  = { version = "^3.8.0", optional = true}
mkdocs-autorefs = {version = "^0.3.1", optional = true}
pre-commit = {version = "^2.17.0", optional = true}
toml = {version = "^0.10.2", optional = true}
livereload = {version = "^2.6.3", optional = true}
pyreadline = {version = "^2.1", optional = true}
mike = { version="^1.1.2", optional=true}

[tool.poetry.extras]
test = [
    "pytest",
    "black",
    "isort",
    "flake8",
    "flake8-docstrings",
    "pytest-cov"
    ]

dev = ["tox", "pre-commit", "virtualenv", "pip", "twine", "toml"]

doc = [
    "mkdocs",
    "mkdocs-include-markdown-plugin",
    "mkdocs-material",
    "mkdocstrings",
    "mkdocs-material-extension",
    "mkdocs-autorefs",
    "mike"
    ]

[tool.poetry.scripts]
sample = 'sample.cli:main'

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88
include = '\.pyi?$'
exclude = '''
/(
    \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
[tool.isort]
profile = "black"
```
我们简单地解读一下这个文件：
在[tool.poetry]那一节，定义了包的名字（这里是sample)、版本号(这里是0.1.0)，其它的一些字段，比如classifiers，这是打包和发布时需要的。如果您熟悉python setup tools，那么对这些字段将不会陌生。packages字段指明了打包时需要包含的文件。在示例中，我们要求在以.whl格式发布的包中，将sample目录下的所有文件打包发布；而以sdist格式(即.tar.gz)发布的包中，还要包含tests目录下的文件。

接下来是[tool.poetry.dependencies]一节，这是我们声明工程的依赖的地方。首先是工程要求的python版本声明。这里我们要求必须在3.7.1以上，4.0以下的python环境中运行。因此，python 3.7.1， 3.9， 3.10都是恰当的python版本，但4.0则不允许。

接下来就是工程中需要用到的其它第三方依赖，有运行时的（即当最终用户使用我们的程序时，必须安装的那些第三方依赖），也有开发时的（即只在开发和测试过程中使用到的，比如文档工具类mkdocs， 测试类tox, pytest等）。

我们对运行时和开发时需要的依赖进行了分组。对开发时需要的依赖，我们分成dev, test和doc三组，通过d [tool.poetry.extras]中进行分组声明。对于归入到dev, test和doc分组中的依赖，我们在[tool.poetry.dependencies]中，将其声明为optional的，这样在安装最终分发包时，这些声明为optional的第三方依赖将不会安装到用户环境中。

再接下来，[tool.poetry.scripts]声明了一个console script入口。Console script是一种特殊的Python脚本，它使得您可以象调用普通的shell命令一样来调用这个脚本。在这里：
```toml
[tool.poetry.scripts]
sample = 'sample.cli:main'
```
当sample包被安装后，就往安装环境里注入了一个``sample`` shell命令。它可以接受各种参数，最终将交给sample\cli.py中的main函数来执行。

接下来就是关于如何构建的相关指示，在[build-system]中。如果你的程序中只包含纯粹的Python代码，那么这部分可不做任何修改。如果你的程序包含了一些原生的代码（比如c的），那么就需要自己定义构建脚本。

在示例代码中，还有[tool.black]和[tool.isort]两个小节，分别是black（代码格式化工具）和isort（将导入进行排序的工具）的配置文件。

## 版本管理
poetry为我们的package提供了基于语义(semantic version)的版本管理功能。它通过`poetry version`这个命令，让我们查看package的版本，并且实现版本号的升级。
### Semantic Versioning（基于语义的版本管理）
当我们说起软件的版本号时，我们通常会意识到，软件的版本号一般由主版本号(major)，次版本号(minor)，修订号(patch)和构建编号(build no.)四部分组成。由于Python程序没有其它语言通常意义上的构建，所以，对Python程序而言，一般只用三段，即major.minor.patch来表示。

!!! Info
    实际上，出于内部开发的需要，我们仍然可能给Python程序的版本用上build no，特别是在CI集成中。当我们向仓库推送一个commit时，CI都需要进行一轮构建和自动验证，此时并不会修改正式版本号，因此，一般倾向于使用构建号来区分不同的提交导致的版本上的不同。在python project wizard生成的项目中，其CI就实现了这个逻辑。

上述版本表示法没有反映出任何规则。在什么情况下，你的软件应该定义为0.x，什么时候又应该定义为1.x，什么时候递增主版本号，什么时候则只需要递增修订号呢？如果不同的软件生产商对以这些问题没有共识的话，会产生什么问题吗？

实际上，由于随意定义版本号引起的问题很多。在前面我们提到过SQLAlchemy的升级导致许多Python软件不能正常工作的例子。归根结底，这是由于SQLAlchemy官方错误地定义版本号引起的。

正是看到这一问题，Tom Preston-Werner（Github的共同创始人）提出Semantic versioniong方案，即基于语义的版本管理。Semantic version表示法提出的初衷是：

!!! Quote
    在软件管理的领域里存在着被称作“依赖地狱”的死亡之谷，系统规模越大，加入的包越多，你就越有可能在未来的某一天发现自己已深陷绝望之中。

    在依赖高的系统中发布新版本包可能很快会成为噩梦。如果依赖关系过高，可能面临版本控制被锁死的风险（必须对每一个依赖包改版才能完成某次升级）。而如果依赖关系过于松散，又将无法避免版本的混乱（假设兼容于未来的多个版本已超出了合理数量）。当你专案的进展因为版本依赖被锁死或版本混乱变得不够简便和可靠，就意味着你正处于依赖地狱之中。

Sematic versioning提议用一组简单的规则及条件来约束版本号的配置和增长。首先，你规划好公共API，在此后的新版本发布中，透过修改相应的版本号来向大家说明你的修改的特性。考虑使用这样的版本号格式：X.Y.Z （主版本号.次版本号.修订号）：修复问题但不影响API 时，递增修订号；API 保持向下兼容的新增及修改时，递增次版本号；进行不向下兼容的修改时，递增主版本号。

在前面我们提到过SQLAlchemy从1.x升级到1.4的例子。实际上，这是个不能向下兼容的修改，引入了异步机制，因此，SQLAlchemy本应该启用2.x的全新版本序列号，而把1.4留作1.x的后续修补发布版本号使用。如此以来，SQLAlchemy的使用者就很容易明白，如果要使用最新的SQLAlchemy版本，则必须对他们的应用程序进行完全的适配和测试，而不能象之前的升级一样，简单地把最新版本安装上，仍然期望它能象之前一样工作。不仅如此，一个定义了良好依赖关系的软件，还能自动从升级中排除掉升级到SQLAlchemy 2.x，而始终只在1.x，甚至更小的范围内进行升级。

一个正确地使用semantic versioning的例子是aioredis从1.x升级到2.0。尽管aioredis升级到2.0时，大多数API并没有发生改变--只是在内部进行了性能增强，但它的确改变了初始化aioredis的方式，从而使得你的应用程序，不可能不加修改就直接更新到2.0版本。因此，aioredis在这种情况下，将版本号更新为2.0是非常正确的。

事实上，如果你的程序的API发生了变化（函数签名发生改变），或者会导致旧版的数据无法继续使用，你都应该考虑主版本号的递增。

此外，从0.1到1.0之前的每一个minor版本，都被认为在API上是不稳定的，都可能是破坏性的更新。因此，如果你的程序使用了还未定型到1.0版本的第三方库，你需要谨慎声明其依赖关系。
### 如何使用Poetry进行版本管理
假设您已经使用[python project wizard]生成了一个工程框架，那么应该可以在根目录下找到pyproject.toml文件，其中有一项：

```
version = 0.1
```
如果您现在运行``poetry version``这个命令，就会显示``0.1``这个版本号。

Poetry使用基于语义的版本(semantic version)表示法。 

在Poetry中，当我们需要修改版本号时，并不是直接指定新的版本号，而是通过``poetry version semver``来修改版本。``semver``可以是``patch``, ``minor``, ``major``, ``prepatch``, ``preminor``, ``premajor``和 ``prerelease``中的一个。这些关键字定义在规范[PEP 440](https://peps.python.org/pep-0440/)中。

``semver``结合您当前的版本号，通过运算，就得出了新的版本号：

| rule       | before        | after         |
| ---------- | ------------- | ------------- |
| major      | 1.3.0         | 2.0.0         |
| minor      | 2.1.4         | 2.2.0         |
| patch      | 4.1.1         | 4.1.2         |
| premajor   | 1.0.2         | 2.0.0-alpha.0 |
| preminor   | 1.0.2         | 1.1.0-alpha.0 |
| prepatch   | 1.0.2         | 1.0.3-alpha.0 |
| prerelease | 1.0.2         | 1.0.3-alpha.0 |
| prerelease | 1.0.3-alpha.0 | 1.0.3-alpha.1 |
| prerelease | 1.0.3-beta.0  | 1.0.3-beta.1  |

可以看出，poetry对版本号的管理是完全符合semantic version的要求的。当你完成了一个小的修订（比如修复了一个bug，或者增强了性能，或者修复了安全漏洞)，此时只应该递增package的修订号，即x.y.z中的'z'，这时我们就应该使用命令:
```
poetry version patch
```
如果之前的版本是0.1.0，那么运行上述命令后，版本号将变更为0.1.1。
如果我们的package新增加了一些功能，而之前提供的功能（API）都还能不加修改，继续使用，那么我们应该递增次版本号，即x.y.z中的'y'。这时我们应该使用命令：
```
poetry version minor
```
如果之前的版本是0.1.1，那么运行上述命令后，版本号将变更为0.2.0

如果我们的package进行了大幅的修改，并且之前提供的功能（API）的签名已经变掉，从而使得调用者必须修改他们的程序才能继续使用这些API，又或者新的版本不再能兼容老版本的数据格式，用户必须对数据进行额外的迁移，那么，我们就认为这是一次破坏性的更新，必须升级主版本号：
```
poetry version major
```
如果之前的版本号是0.3.1,那么运行上述命令之后，版本号将变更为1.0.0；如果之前的版本号是1.2.1，那么运行上述命令之后，版本号将变更为2.0.0。

除此之外，poetry还提供了预发布版本号的支持。比如，上一个发布的版本是0.1.0，那么我们在正式发布0.1.1这个修订之前，可以使用0.1.1.a0这个版本号：
```
poetry version prerelease
# output:
Bumping version from 0.1.0 to 0.1.1a0
```
如果需要再出一个alpha版本，则可以再次运行上述命令：
```
poetry version prerelease
# output:
Bumping version from 0.1.1a0 to 0.1.1a1
```
如果alpha版本已经完成，可以正式发布，运行下面的命令：
```
poetry version patch
# output:
Bumping version from 0.1.1a1 to 0.1.1
```
poetry暂时还没有提供从alpha转到beta版本系列的命令。如果有此需要，您需要手工编辑pyproject.toml文件。

除了poetry version prerelease之外，我们还注意到上面列出的premajor, preminor和prepatch选项。它们的作用也是将版本号修改为alpha版本系列，但无论你运行多少次，它们并不会象prerelease选项一样，递增alpha版本号。所以在实际的alpha版本管理中，似乎只使用``poetry version prerelease``就可以了。
## 依赖管理
### 实现依赖管理的意义
Poetry的自我定位就是"Poetry is a tool for dependency management and packaging in Python"。Poetry最重要的功能就是依赖解析和管理，也是迄今为止，依赖解析做得最成功的工具。类似的工具还是pipenv和PDM，但根据[这篇文章](https://frostming.com/2021/03-26/pm-review-2021/)，pipenv在依赖解析的正确性上以及在不同安装环境（比如不同的操作系统或者python版本上）下的一致性不太能得到保证。而Poetry与PDM则正确性上都能得到保证，但PDM还比较新，社区认可度还没有Poetry高。

依赖管理就是要在各方软件都保证正确的版本声明的基础上，通过Poetry正确地声明第三方依赖版本的上下界，并且在Pip安装时，只在声明的上下界之间寻找合适的版本。在前面我们已经看到了，如果第三方库不正确在声明自己的版本号，就会导致升级错误。如果第三方库正确在声明了自己的版本号，那么通过Poetry的依赖管理，我们就可以正确锁定依赖的版本，使之既能无须发布新的版本，就能自动升级依赖的最新的小的更新，同时又永远拒绝破坏性的更新。
### Poetry进行依赖管理的相关命令
在Poetry管理的工程中，当我们向工程中加入（或者更新）依赖时，总是使用``poetry add``命令，比如：``poetry add pytest``

这里可以指定，也可以不指定版本号。命令在执行时，会对``pytest``所依赖的库进行解析，直到找到合适的版本为止。如果您指定了版本号，该版本与工程里已有的其它库不兼容的话，命令将会失败。

我们在添加依赖时，一般要指定较为准确的版本号，界定上下界，从而避免意外升级带来的各种风险。在指定依赖库的版本范围时，有以下各种语法：
```
poetry add SQLAlchemy               # 使用最新的版本
```
使用通配符语法:
```
poetry add SQLAlchemy=*             # 使用>=0.0.0的版本，无法锁定上界，不推荐
poetry add SQLAlchemy=1.*           # 使用>=1.0.0, <2.0.0的版本
```
使用插字符(caret)语法:
```
poetry add SQLAlchemy^1.2.3         # 使用>=1.2.3, <2.0.0的版本
poetry add SQLAlchemy^1.2           # 使用>=1.2.0, <2.0.0的版本
poetry add SQLAlchemy^1             # 使用>=1.0.0, <2.0.0的版本
```
使用波浪符(Tilde)语法:
```
poetry add SQLAlchemy~1.2           # 使用>=1.2.0,<1.3的版本
poetry add SQLAlchemy~1.2.3         # 使用>=1.2.3，<1.3的版本
```
使用不等式语法(及多个不等式):
```
poetry add SQLAlchemy>=1.2,<1.4     # 使用>=1.2,<1.4的版本
```
最后，精确匹配语法：
```
poetry add SQLAlchemy==1.2.3        # 使用1.2.3版本
```

如果有可能，我们推荐总是使用波浪符或者不等式语法。它们有助于在可升级性和可匹配性上取得较好的平衡。比如，如果在增加对SQLAlchemy的依赖时，如果使用了插字符语法，你已经发行出去的安装包，则会在安装时自动采用直到2.0.0之前的SQLAlchemy的最新版本。因此，如果你的安装包是在SQLAlchemy 1.4之前被安装，此后用户不再升级，则它们将可以正常运行；而如果是在SQLAlchemy 1.4发布之后被安装，pip将自动使用1.4及以后最新的SQLAlchemy，于是1.4这个跟之前版本不兼容的版本就被安装上了，导致你的程序崩溃;而你将不会有任何办法（除非发行新的升级包）来解决这一问题。

这也看出来SQLAlchemy的发行并不符合Semantic的标准。一旦出现API不兼容的情况，是需要对主版本升级的。如果SQLAlchemy不是将版本升级到1.4，则是升级到2.0，则不会导致程序出现问题。

始终遵循社区规范进行开发，这是每一个开源程序开发者都应该重视的问题。

但是，指定具体的版本也会有它的问题。在向工程中增加依赖时，如果我们直接指定了具体的版本，有可能因为依赖冲突的原因，无法指定成功。此时可以指定一个较宽泛一点的版本范围，待解析成功和测试通过后，再改为固定版本。另外，如果该依赖发布了一个紧急的安全更新，通常会使用递增修订号的方式来递增版本。使用指定的版本号会导致你的应用无法快速获得此安全更新。

在上一章里，我们已经提到了依赖分组。我们的应用程序会依赖许多第三方库，这些第三方库中，有的是运行时依赖，因此它们必须随我们的程序一同被分发到终端用户那里；有的则只是开发过程中需要，比如象pytest，black，mkdocs等等。因此，我们应该将依赖分组，并且只向终端用户分发必要的依赖。

这样做的益处是显而易见的。一方面，依赖解析并不容易，一个程序同时依赖的第三方库越多，依赖解析就越困难，耗时越长，也越容易失败；另一方面，我们向终端用户的环境里注入的依赖越多，他们的环境中就越容易遇到依赖冲突问题。

最新的Python规范允许你的程序使用发行依赖（在最新的poetry版本中，被归类为main依赖）和extra requirements。在上一章向导创建的工程中，我们把extra reuqirement分为了三个组，即dev, test, doc。

```
[tool.poetry.dependencies]
black  = { version = "20.8b1", optional = true}
isort  = { version = "5.6.4", optional = true}
flake8  = { version = "3.8.4", optional = true}
flake8-docstrings = { version = "^1.6.0", optional = true }
pytest  = { version = "6.1.2", optional = true}
pytest-cov  = { version = "2.10.1", optional = true}
tox  = { version = "^3.20.1", optional = true}
virtualenv  = { version = "^20.2.2", optional = true}
pip  = { version = "^20.3.1", optional = true}
mkdocs  = { version = "^1.1.2", optional = true}
mkdocs-include-markdown-plugin  = { version = "^1.0.0", optional = true}
mkdocs-material  = { version = "^6.1.7", optional = true}
mkdocstrings  = { version = "^0.13.6", optional = true}
mkdocs-material-extensions  = { version = "^1.0.1", optional = true}
twine  = { version = "^3.3.0", optional = true}
mkdocs-autorefs = {version = "0.1.1", optional = true}
pre-commit = {version = "^2.12.0", optional = true}
toml = {version = "^0.10.2", optional = true}

[tool.poetry.extras]
test = [
    "pytest",
    "black",
    "isort",
    "flake8",
    "flake8-docstrings",
    "pytest-cov"，
    "twine"
    ]

dev = ["tox", "pre-commit", "virtualenv", "pip",  "toml"]

doc = [
    "mkdocs",
    "mkdocs-include-markdown-plugin",
    "mkdocs-material",
    "mkdocstrings",
    "mkdocs-material-extension",
    "mkdocs-autorefs"
    ]
```
这里tox， pre-commit等是我们开发过程中使用的工具；pytest等是测试时需要的依赖；而doc则是构建文档时需要的工具。通过这样划分，可以使CI或者文档托管平台只安装必要的依赖；同时也容易让开发者分清每个依赖的具体作用。

当你使用poetry add命令，不加任何选项时，该依赖将被添加为发行依赖（在1.3以上的poetry中，被归为main组），即安装你的包的最终用户，他们也将安装该依赖。但有一些依赖只是开发者需要，比如象mkdocs， pytest等，它们不应该被分发到最终用户那里。

在python proejct wizard开发时，poetry还只支持一个dev分组，这样的粒度当然是不够的，因此，python project wizard借用了extras字段来向项目添加可选依赖分组，其它工具，比如tox也支持这样的语法。

现在最新的poetry已经完全支持分组模式，并且从文档可以看出，它建议至少使用main, docs和test三个分组。后续python project wizard生成的项目框架，也将完全使用最新的语法，但仍然保留四个分组，即main, dev, docs和test。

通过poetry向项目增加分组及依赖，语法是：
```
poetry add pytest --group test
```
这样，生成的pyproject.toml片段如下：
```
[tool.poetry.group.test.dependencies]
pytest = "*"
```

一般地，我们应该将其指定为optional。目前最新版本的poetry仍然不支持通过命令行直接将group指定为optional，您可能需要手工编辑这个文件。

```
[tool.poetry.group.test]
optional = true
```

!!! Info
    注意，通过上述命令生成的toml文件的内容可能与python project wizard当前版本生成的有所不同。但python project wizard的未来版本最终将使用同样的语法。

### poetry依赖解析的工作原理

在上一节，我们简单地介绍了如何使用poetry来向我们的项目中增加依赖。我们强调了依赖解析的困难，但并没有解释poetry是如何进行依赖解析的，它会遇到哪些困难，可能遭遇什么样的失败，以及应该如何排错。对于初学者来说，这往往是配置poetry项目时最困难和最耗时间的部分。




## 虚拟运行时

Poetry自己管理着虚拟运行时环境。当你执行``poetry install``命令时，Poetry就会安装一个基于venv的虚拟环境，然后把项目依赖都安装到这个虚拟的运行环境中去。此后，当你通过poetry来执行其它命令时，比如``poetry pytest``，也会在这个虚拟环境中执行。反之，如果你直接执行``pytest``，则会报告一些模块无法导入，因为你的工程依赖并没有安装在当前的环境下。

我们推荐在开发过程中，使用conda来创建集中式管理的运行时。在调试Python程序时，都要事先给IDE指定解析器，这里使用集中式管理的运行时，可能更方便一点。Poetry也允许这种做法。当Poetry检测到当前是运行在虚拟运行时环境下时，它是不会创建新的虚拟环境的。

但是Poetry的创建虚拟环境的功能也是有用的，主要是在测试时，通过virtualenv/venv创建虚拟环境速度非常快。

## 构建发行包
### Python构建标准和工具的变化
### 基于Poetry进行发行包的构建

我们通过运行``poetry build``来打包，打包的文件约定俗成地放在dist目录下。

poetry支持向pypi进行发布，其命令是`poetry publish`。不过，在运行该命令之前，我们需要对poetry进行一些配置，主要是repo和token。

```
# publish to test pypi
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config testpypi-token.pypi my-token
poetry publish -r testpypi

# publish to pypi
poetry config pypi-token.pypi my-token
poetry publish
```
上面的命令分别对发布到test pypi和pypi进行了演示。由于默认地Poetry支持PyPI发布，所以有些参数就不需要提供了。当然，一般情况下，我们都不应该直接运行`poetry publish`命令来发布版本。版本的发布，都应该通过CI机制来进行。这样的好处时，可以保证每次发布，都经过了完整的测试，并且，构建环境是始终一致的，不会出现因构建环境不一致，导致打出来的包有问题的情况。

## 其它重要的Poetry命令
## 案例： 基于Poetry创建并发布一个项目

1. 为何要使用Semantic Version?
2. 当前版本是``0.1``,执行``poetry version pre-release``，新的版本号是?
3. 为何要尽可能精确地锁定依赖的版本号？锁定版本号后，依赖失去自动升级能力，这样做是好是坏？
4. 如何查看项目安装的依赖库（使用Poetry)?
5. 如果在使用Poetry过程中，依赖解析和安装较慢，如何修改Poetry源？

[semantic version]: https://semver.org/
