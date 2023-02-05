我们的探索之旅，就要接近Python开发流水线的终点了。终点站的主题是如何打包和发布应用。

Python开发项目的成果，可能是一个Python库(package)，也可能是一个独立运行的应用程序（桌面应用程序或者后台服务）。

Python库主要是供程序员之间复用代码（库）来使用的。PyPA（PyPA是Python软件基金会 -- Python Software Foundation，简称PSF资助的一个核心项目）通过PyPI和一系列工具，为Python库的分发提供了事实上的标准和基础设施。

分发应用程序则要复杂不少。取决于我们使用的框架、技术和用户的使用方式，我们的应用程序可能需要分发到服务平台（Serivce platforms）-- 这一般适用于构建托管的SaaS服务，比如那些部署在Heroku， Google App Engine平台上的服务；也可能是部署在云上（无论是公有云还是私有云）的单个或者一组相互合作的容器 -- 这些都是适合于服务的模式；也有可能这是个面向消费级用户的App，可能需要通过App store, Android市场，或者Windows商店来分发 -- 这就还涉及到向导式安装程序的制作，以及如何运行Python程序的问题。

Python项目应该使用哪种方式进行分发，取决于用户的使用方式，以及是否涉及到安装定制化。一些Python库可以通过console script的方式，在命令行下运行。如果一个Python库以`pip`的方式安装后无须配置即可运行，并且用户自己知道如何安装Python（及可能会创建虚拟环境），这样来分发应用也是允许的。但对多数消费级应用的用户而言，他们恐怕并不懂得如何通过`pip`来安装应用，并在命令行下启动应用。此外，通过`pip`安装时，安装过程中接受用户输入是不被允许的，因此，安装过程无法定制（比如，用户可以需要选择安装目的地、或者需要用户输入账户信息等）。
# 1. 以Python库的方式打包和分发

在程序库的分发上，很多语言都建立了中央存储库和包管理器生态，比如Java的Maven，Ruby的RubyGems，Node.js的npm，Rust的Cargo，甚至C/C++的Conan。与其它语言类似，Python库的分发也是通过一个中央索引库(The Python Package Index)来实现的，简称PyPI，启用于2003年。PyPI的启用是Python得以加速发展的重要因素，因为Python广受欢迎的原因之一就是它的生态系统非常丰富，PyPI则正是构建这个生态系统的核心。

让我们把时间拉回到2000年。当Python 1.6发布时，它添加了一个有意思的功能，distutils，奠定了Python的打包工具的开端。彼时它的功能还很简单，只提供了简单的打包功能，没有声明依赖和自动安装依赖的功能。

2004年， distutils演化成为setuptools，引入了新的打包格式 -- egg。把包格式命为egg是一种程序员式的浪漫和幽默，因为蟒蛇是通过下蛋来实现繁殖的，而Python库正是Python开枝散叶的一个重要载体。同样的类比在其它语言中也存在，比如Ruby语言与gems的关系。 egg文件实际上就是一个zip包，只不过名字不同而已。这一阶段的setuptools还提供了一个新的命令，easy_install，用来安装python eggs，不过这个命令在2.7之后就被移除了。

2008年，PyPA发布pip，替换掉了easy_install，随后将打包工具的行为标准化为PEP 438。

在2012年时，随着PEP 427的通过，一种新的打包格式，即Wheel格式取代了egg格式，成为构建和打包（二进制）Python库的标准格式。今天你仍然能看到Python库安装后，会留下.egg-info文件，这个名字只是巨蟒经过后，留下的岁月痕迹，由pip在安装时临时生成，而与egg无关。

尽管在《zen of Python》中写道，"永远都应该只有一种显而易见的解决之道"，但是，理想照进现实的过程总要经过曲折的投影。我们一路讲述下来，读者已经发现，Python在虚拟环境、依赖解析和打包构建等领域都先后出现了好多个方案来解决相似的问题，出现了让人莫衷一是的”百花齐放“，如果没有经过系统的梳理，很多人会难免感到困惑，不知道哪一个方案能够通向未来，自己掌握的技术与资讯，是否已经被社区抛弃。好在Python社区现在已经通过一系列的PEP回答了标准问题，相关的工具和生态逐渐在遵循标准的基础上建立起来了，今后的这样的”百花齐放“，可能会少一些。是否遵循最新的PEP，也正是`ppw`工具和本书选择某项技术的标尺。

在`ppw`中，我们的发布是在Github Actions中完成的。这部分我们已经在[持续集成](chap09.md)那一章讲过了。万一你存在手工发布的需求，那么请回顾[基于Poetry进行发行包的构建](chap05.md#基于Poetry进行发行包的构建)那一节。

这里简要地提及一下，在Poetry出现之前，我们是如何发布Python库的，以防读者偶尔还会遇到需要维护老旧的Python项目的情况。我们需要通过`twine`这个命令来发布Python库。这个命令可以通过`pip`来安装：
```
pip install twine
```

尽管`ppw`生成的项目中，我们使用了别的技术来发布Python库，但这个命令也保留了下来。用在`poetry build`之后，检查构建物是否合乎PyPI的规定，以提前预防发布失败。

## 1.1. 打包和分发流程

打包和发布是一个从开发者的源代码起，到用户可以安装并使用的Python库的过程。这个过程中，我们需要经历以下几个步骤：
1. 准备一个包含将要打包的库的源代码树。这通常是从版本控制系统检出。

2. 准备一个描述包元数据（名称、版本等）以及如何创建构建工件的配置文件。对于大多数库，这将是一个 pyproject.toml 文件，在源代码树中手动维护。

3. 创建要发送到库分发服务（通常是 PyPI）的构建结果；生成工作的格式是"sdist"和（或）"wheel"。这些是由构建工具使用上一步中的配置文件创建的。

4. 将构建的结果上传到包分发服务。

此时，Python库就出现在了分发服务器上（通常是PyPI)。要使用这个库，最终用户必须下载和安装它。通常我们使用`pip`来完成这个过程。

### 1.1.1. 库格式：sdist和wheel
sdist和wheel是两种不同的打包格式，虽然本质上，它们都是zip格式，打包的内容仍然是Python源代码。不同的是，在sdist中会包含一个setup.py文件，如果该项目还包含一些c语言的扩展，那么这些文件也将包含在内。在安装时，setup.py及必要的编译过程将在用户环境下执行，因此，sdist格式的安全性较低。一个恶意的库可能在setup.py中引入任意的代码。但它的好处也是显然易见，如果有一些原生代码需要在目标机器上进行构建，我们必须要有一个机制去触发这个构建。

wheel则完全相反。wheel中不包含任何可执行的安装脚本。如果项目中包含c扩展，这些扩展将被事先编译后，再将其结果包含在wheel中。Pip在安装wheel时，只是简单的文件拷贝。

在Poetry构建的项目中，一般会同时生成sdist和wheel格式的安装包，如果是sdist格式，poetry会生成一个简单的setup.py文件。在安装上，如果没有特别指定，pip总是优先选择wheel格式。

需要注意的是，无论是sdist还是wheel，它们的安装都不是传统意义上的应用程序安装，即在安装过程中，都不能接受用户输入，实现定制。尽管sdist当中存在setup.py的脚本可以执行任意代码，但该脚本仍然无法接入用户来自于控制台的输入。这可能是不太为人所知的一个冷知识。总之，sdist和wheel是用来打包程序库(package)的，**它们不能用来打包应用程序**。

### 1.1.2. 分发包的源数据

在创建的分发布中，包含了一个名为METADATA的文件。这个文件的内容如下所示：
```
Metadata-Version: 2.1
Name: sample
Version: 0.1.0
Summary: Skeleton project created by Python Project Wizard (ppw).
License: MIT
Requires-Python: >=3.8,<3.9
Classifier: Development Status :: 2 - Pre-Alpha
...
Classifier: Programming Language :: Python :: 3.9
Provides-Extra: dev
...
Requires-Dist: black (>=22.3.0,<23.0.0) ; extra == "test"
...
Requires-Dist: virtualenv (>=20.13.1,<21.0.0) ; extra == "dev"
Description-Content-Type: text/markdown

# sample

this is hotfix 533
...

* TODO

## Credits

This package was created with the [ppw](https://zillionare.github.io/python-project-wizard) tool...
```
文件内容进行了适当的删节。

这个文件中的一些字段我们需要简单介绍一下。

Name，Author，Author-email，License， Homepage, Keywords, Download-URL等字段的含义不言自明，无须解释。在旧式的项目（即通过setuptools来打包）中，这些字段都要指定在setup.py文件中，并传递给一个名为`setup`的可以接受非常多参数的函数。在使用了Poetry的项目中，Poetry会从pyproject.toml文件中提取。

**Platform字段**用来指定特殊的操作系统要求。
**Supported-Platform字段**，用来指定更详细的操作系统和CPU架构支持，比如指定Linux为RedHat，或者cpu架构为arm等。
**Summary字段**来用简要地描述包的功能。在使用了Poetry的项目中，它提取自description字段。在PyPI上，它将显示在这里：

![](assets/img/chap11/meta_summary.png){width="50%"}

**Description和Description-Content-Type字段：**Description字段用来详细描述包的一些信息，通常开发者会把项目的README.md及Change History的文件内容复制到这里。Description-Content-Type字段用来指定Description字段的内容类型，支持的类型有Markdown和reStructuredText两种。在使用了Poetry的项目中，Poetry将自动把README的内容复制进来。在PyPI上，它将显示在下图中的右下侧（方框中）：

![](assets/img/chap11/meta_description.png){width="50%"}

**Classifier字段：**分类器描述了这个项目的一些分类属性。这些属性会在PyPI上显示，并且可以作为筛选条件来进行查找和过滤，请参见下图：

![](assets/img/chap11/meta_classifier.png)

PyPI的分类系统是一个树形结构。最顶层的分类是框架（Framework)， 主题（Topic），开发状态（Development Status），操作系统（Operating System）等10个大类别。其实，PyPi上的第三方库可谓浩如烟海，人工查询这些分类意义并不大。这些分类符有助于PyPI组织和管理所有的库，但并不是强制的，对包的安装也没有帮助。但是，PyPA仍然推荐在任何项目中，都至少声明该库工作的Python版本、license, 操作系统等。

此外，新加入的'Typing'分类符比较有意思。它的作用是告诉PyPI这个项目是一个类型注解的项目。如果我们的项目是一个类型注解的项目，那么我们应该在项目的源代码目录下加入py.typed文件，并在pyproject.toml中加入这个分类符：
```toml
classifiers=[
    'Typing :: Typed',
]
```

**Requires-Dist字段：**这个字段用来描述项目的依赖关系。`pip`在安装时，需要读取这个字段以发现哪些依赖需要安装。
**Requires-Python字段：**表明这个项目需要的Python版本。

遗憾的是，尽管每一个包都包含了这些信息，但是对于一些重要的信息，特别是象requires-dist这样的信息，PyPI并没有将其提取出来单独管理。其它语言的库管理器，比如maven，在这一点上做得更好。为什么这是一个遗憾，我们将在很快讲到。

## 1.2. TestPyPI和PyPI
在`ppw`生成的项目中，`dev`工作流中的`publish`任务会将构建物发布到TestPyPI。这是一个供测试用的PyPI。这么做的目的有两个，一来我们希望CI总是覆盖到开发全过程，因此构建和发布这两步也不应该缺失。二来，在一个大型应用中，我们可能同时开发着多个相互依赖的项目，此时我们就需要借助testpypi，使得当某个项目有了更新的版本、但又不到正式发布阶段之前，其它依赖于它的项目也能够使用到这个项目的最新的版本。在这种情况下，我们可以在pyproject中添加第二个源，指向testpypi，这样当我们指定该项目的最新开发版本时，poetry就会从查找testpypi。

我们来举例说明如何通过testpypi向项目添加一个非正式发布版本。

我们以大富翁量化框架为例。这是一个包含了多个模块的大型应用。其中，`zillionare-omicron`是数据读写的sdk， `zillionare-omega`是行情数据服务器，它依赖于`zillionare-omicron`。还有许多其它模块，不过要理解我们这里的示例，只需要知道这两个模块就够了。实际上，你可以完全不知道什么是大富翁量化框架，只需要知道几个模块之间的依赖关系就可以了。

假设`zillionare-omicron`当前最新的开发版本是1.2.3a1。`zillionare-omicron`使用了基于语义的版本管理方案，因此从版本号上我们得知，这不是正式版本，只会发布到testpypi上去。如果要在项目中使用这个版本，我们需要先将testpypi添加为一个源，然后在`pyproject.toml`中指定`zillionare-omicron`的版本为`1.2.3a1`。这样，当我们执行`poetry install`时，poetry就会从testpypi中查找`zillionare-omicron`的1.2.3a1版本，然后安装到本地。

我们在[第5章 poetry依赖解析的工作原理](chap05.md#poetry依赖解析的工作原理)那一节介绍过如何增加第二个源。我们这里用同样的方法来增加testpypi源：
```bash
$ poetry source add -s testpypi https://test.pypi.org/simple
```
然后我们的pyproject.toml文件中将会多这样一项：
```toml
[[tool.poetry.source]]
name = "testpypi"
url = "https://test.pypi.org/simple"
default = false
secondary = true
```
现在我们就可以把对zillionare-omicron的开发中版本的依赖加进来：
```bash
$ poetry add -v zillionare-omicron^1.2.3a1
```
命令将成功执行，你可以从更新后的pyproject.toml中看到对`zillionare-omicron`的引用。如果我们没有添加这个源，则上述命令在执行时会报出以下错误：
```
Using virtualenv: /home/aaron/miniconda3/envs/sample

  ValueError

  Could not find a matching version of package zillionare-omicron

  at ~/miniconda3/envs/sample/lib/python3.8/site-packages/poetry/console/commands/init.py:414 in _find_best_version_for_package
      410│         )
      411│ 
      412│         if not package:
      413│             # TODO: find similar
    → 414│             raise ValueError(f"Could not find a matching version of package {name}")
      415│ 
      416│         return package.pretty_name, selector.find_recommended_require_version(package)
      417│ 
      418│     def _parse_requirements(self, requirements: list[str]) -> list[dict[str, Any]]:
```


## 1.3. Pip: Python包管理工具
你可能感到好奇，`pip`几乎是所有学习Python的人最早接触的几个命令之一，也是本书最早使用的那些命令之一，为什么我们却安排到了最后来介绍？原因是，因为大家非常熟悉`pip`了，所以对`pip`的一般性介绍已经不太有必要。值得一提的是，`pip`同样面临着依赖解析的问题，最适合讨论这个问题的地方，则是在了解了构建和分发系统的全貌之后。

依赖解析。这是我们又一次接触到这个词。上一次还是在讲Poetry的那一章。是的，Poetry只解决了开发阶段的依赖问题，并为安装阶段的依赖解析打下了良好基础，但是，`pip`仍然要独自面临依赖解析问题。

下面的示例来自于`pip`的文档：

```
pip install tea
Collecting tea
  Downloading tea-1.9.8-py2.py3-none-any.whl (346 kB)
     |████████████████████████████████| 346 kB 10.4 MB/s
Collecting spoon==2.27.0
  Downloading spoon-2.27.0-py2.py3-none-any.whl (312 kB)
     |████████████████████████████████| 312 kB 19.2 MB/s
Collecting cup>=1.6.0
  Downloading cup-3.22.0-py2.py3-none-any.whl (397 kB)
     |████████████████████████████████| 397 kB 28.2 MB/s
INFO: pip is looking at multiple versions of this package to determine
which version is compatible with other requirements.
This could take a while.
  Downloading cup-3.21.0-py2.py3-none-any.whl (395 kB)
     |████████████████████████████████| 395 kB 27.0 MB/s
  Downloading cup-3.20.0-py2.py3-none-any.whl (394 kB)
     |████████████████████████████████| 394 kB 24.4 MB/s
  Downloading cup-3.19.1-py2.py3-none-any.whl (394 kB)
     |████████████████████████████████| 394 kB 21.3 MB/s
  Downloading cup-3.19.0-py2.py3-none-any.whl (394 kB)
     |████████████████████████████████| 394 kB 26.2 MB/s
  Downloading cup-3.18.0-py2.py3-none-any.whl (393 kB)
     |████████████████████████████████| 393 kB 22.1 MB/s
  Downloading cup-3.17.0-py2.py3-none-any.whl (382 kB)
     |████████████████████████████████| 382 kB 23.8 MB/s
  Downloading cup-3.16.0-py2.py3-none-any.whl (376 kB)
     |████████████████████████████████| 376 kB 27.5 MB/s
  Downloading cup-3.15.1-py2.py3-none-any.whl (385 kB)
     |████████████████████████████████| 385 kB 30.4 MB/s
INFO: pip is looking at multiple versions of this package to determine
which version is compatible with other requirements.
This could take a while.
  Downloading cup-3.15.0-py2.py3-none-any.whl (378 kB)
     |████████████████████████████████| 378 kB 21.4 MB/s
  Downloading cup-3.14.0-py2.py3-none-any.whl (372 kB)
     |████████████████████████████████| 372 kB 21.1 MB/s
```
在这里，`tea`依赖于`hot-water`, `spoon`, `cup`。当安装`tea`时，`pip`下载了最新的`spoon`和`cup`，发现两者不兼容，于是它不得不向前搜索兼容的版本，这个功能被称之为回溯，是从20.3起才有的功能。由于依赖信息不能通过查询PyPI得到，所以它不得不一次又一次的下载早前版本的包，从这些包中提取依赖信息，看是否与`spoon`兼容，不断重复这个过程直到找到一个兼容的版本。

这个过程我们在Poetry进行依赖解析时也看到过。我们在[第5章 poetry依赖解析的工作原理](chap05.md#poetry依赖解析的工作原理)中解释过，PyPI上并没有某个库的依赖树，所以，Poetry要知道某个库的依赖项，就必须先把它下载下来。这个说法其实只是部分正确。在读过[分发包的源数据](chap11.md#分发包的源数据)那一节之后，我们已经知道，这些信息已经上传到了PyPI，只是由于某些历史原因，PyPI并没有把它们单独提取出来以供使用而已。

人们花了这么多功夫来解决依赖问题，看来”依赖地狱“一说，并非虚妄。

问题是，既然Poetry在添加依赖时，已经进行过了依赖解析，又生成了lock文件，为何`pip`不能直接使用些信息，还要重新进行一次依赖解析呢？现在请你打开`sample`工程构建出来的wheel文件。我们说过，它是`zip`格式的压缩文件。打开后，其内容如下：
```
.
├── sample
│   ├── __init__.py
│   ├── app.py
│   └── cli.py
└── sample-0.1.0.dist-info
    ├── LICENSE
    ├── METADATA
    ├── RECORD
    ├── WHEEL
    └── entry_points.txt
```
我们在这里找不到任何跟poetry有关的东西。这并不奇怪，毕竟，`poetry`与`pip`不属于同一个开发者，而`poetry`还不是标准库的一部分，所以`pip`没有理由去理解任何`poetry`直接相关的东西。所有的依赖信息都在METADATA这个文件里，特别是`Requires-Deps`:
```
Requires-Dist: black (>=22.3.0,<23.0.0) ; extra == "test"
Requires-Dist: fire (==0.4.0)
Requires-Dist: flake8 (==4.0.1) ; extra == "test"
Requires-Dist: flake8-docstrings (>=1.6.0,<2.0.0) ; extra == "test"
Requires-Dist: isort (==5.10.1) ; extra == "test"
```
我们看到，有一些依赖指定了精确的版本，有的则只指定了版本范围，这里使用的是不等式语法（请见[Poetry进行依赖管理的相关命令](chap05.md#Poetry进行依赖管理的相关命令))。所以，尽管Poetry通过lock文件锁定了精确的版本，但lock文件只会在开发者之间共享，以加快他们的开发环境构建速度，而不会发布给终端用户。发布给终端用户的依赖信息，是Poetry按照pyproject.toml文件的内容生成的，两者语义完全一致，只不过Poetry允许开发者使用包括通配符、插字符、波浪符、不等式等多种语法来指定版本号，而在生成METADATA时，都被转换成不等式语法而已。我们再来回忆一下sample项目中的pyproject.toml文件的相关部分:
```
fire = "0.4.0"

black  = { version = "^22.3.0", optional = true}
isort  = { version = "5.10.1", optional = true}
flake8  = { version = "4.0.1", optional = true}
flake8-docstrings = { version = "^1.6.0", optional = true }
```

Poetry为何不将`lock`文件中锁定的版本号写入到METADATA文件中呢？这是因为，lock文件完全锁死了依赖的版本号，这样虽然安装速度变快，但也会导致任何更新，就连安全更新也不可用。

现在我们明白了，在Poetry向项目中增加一个依赖时，如果发生了回溯，那么极有可能在`pip`安装时也发生同样的回溯。要加快`pip`安装的速度，我们应该查看`poetry.lock`文件，找出其锁定的版本，以它为基点，重新指定一个恰当的版本范围，这样可以极大程度上避免在`pip`安装时发生回溯。

一个好消息是，根据`pip`的文档，致力于不下载Python package就能得到其依赖信息的方案正在工作当中。让我们期待它的到来吧。
# 2. 应用程序分发
应用程序的打包分发，按它最终分的的目标，又可大致分为桌面应用程序和移动应用程序[^1]。前者一般只需要借助一些打包工具；后者往往要在一开始，就要从框架入手进行支持。
## 2.1. 桌面应用程序
Python打包桌面应用程序的选项非常之多，包括跨平台的如[pyInstaller](https://pyinstaller.readthedocs.io/en/stable/), [cx_Freeze](https://marcelotduarte.github.io/cx_Freeze/)，[briefcase](briefcase.readthedocs.io/)，专用于Windows的[py2exe](http://www.py2exe.org/)和专用于Mac的[py2app](https://py2app.readthedocs.io/en/latest/)等。此外，还有Nuitka, makeself等。这里我们只介绍makeself, PyInstaller和Nuikta。
### 2.1.1. makeself的多平台安装包（内含案例）
makeself[^2]是一个可用以Unix/Linux和MacOs下的自解压工具。在安装了cygwin的前提下，也可用以Windows。它不仅可以用来打包Python应用程序，也可以用来打包其它脚本应用。makeself本身是一个小型 shell 脚本，可从指定目录生成可自解压的压缩文档。生成的文件显示为 shell 脚本（其中许多具有.run后缀），并且可以在shell下启动执行，执行后，这个压缩文档将自行解压缩到一个临时目录，并执行可选的任意命令（例如安装脚本）。这与在 Windows 世界中使用 WinZip Self-Extractor 生成的档案非常相似。Makeself 档案还包括用于完整性自我验证的校验和（CRC 和/或 MD5/SHA256 校验和）。

我们介绍这个工具，是因为在运维领域它应用非常广泛，在Github上也有过千stars。它的使用方法也非常简单，几乎没有学习成本。在Ubuntu下，它可以通过以下命令安装:
```
sudo apt-get install makeself
```
在其它操作系统上，您可能需要从其官网[^2]下载安装。

它的用法如下：

```
$ makeself.sh [args] archive_dir file_name label startup_script [script_args]
```
args是Makeself的可选参数。参数比较多，涵盖了如何压缩、是否加密、解压缩行为等，这里就不一一详述。请读者在需要时参考官方文档[^2]。
archive_dir是包含归档文件的目录名，比如项目下的dist文件夹；file_name是要创建的归档文件名，比如install_sample.sh；label是归档文件的描述，比如“Install sample”;startup_script是归档文件解压后执行的脚本，比如install.sh；script_args是startup_script的参数。

仍以`sample`项目为例，我们可以使用以下脚本来完成打包：
```
#!/bin/bash
  
poetry build
rm -rf /tmp/sample
mkdir /tmp/sample

version=`poetry version | awk '{print $2}'`

echo "version is $version"
# prepare archive
cp dist/sample-$version-py3-none-any.whl /tmp/sample/

# prepare install script
echo "#! /bin/bash" > /tmp/sample/install.sh
echo "pip install ./sample-$version-py3-none-any.whl" >> /tmp/sample/install.sh
chmod +x /tmp/sample/install.sh

# packaging with makeself
makeself /tmp/sample install_sample.sh "sample package made by makeself" ./install.sh
```
非常轻巧和干净，这正是我们介绍它的目的。我们这里使用了一个名为`install.sh`的脚本作为启动脚本。在这个脚本里，我们仅仅执行了安装命令，您也可以在此与用户交互，并在安装后，根据用户的输入进行初始化设置。

### 2.1.2. 基于PyInstaller的多平台安装包
### 2.1.3. Nuitka
## 2.2. 移动应用程序

# 3. 基于云的应用部署
code to implement a simple REST API in GO

[^1]: 在[Python官方文档](https://packaging.python.org/en/latest/overview/#packaging-python-applications)(https://packaging.python.org/en/latest/overview/#packaging-python-applications)中，还提到了其它几种打包。
[^2]: [Makeself](https://makeself.io/)的官网地址是：https://makeself.io/

