# 项目布局和项目生成向导
## 标准项目布局
### 文档
### 工程构建配置文件
### 代码目录
### 单元测试文件目录
### 持续集成配置文件
## 项目生成向导——Python Project Wizard
### 安装Python Project Wizard
### 创建虚拟环境
### 安装开发依赖
### 创建Github Repo
### 运行发布测试
### 设置Github CI
### 设置Codecov

# 项目布局和项目生成向导

通过前三章的学习，我们了解了如何构建开发环境，并且也完成了一个最简单的python程序 -- Hello World。

您可能已经意识到，即使撇开其简陋的功能不说，在很多其它方面，它也有明显的不足：
1. 一般而言，程序的使用者会需要帮助文档，也需要了解关于版权、作者等信息，这些信息应该如何提供？
2. 没有任何程序能够避免bug。您可能已经听说，要减少bug，程序就必须经过系统和详尽的测试。我们应该如何编写和组织测试代码？
   
   !!! Info
    在github上有一个高达50k stars的项目，名为[nocode](https://github.com/kelseyhightower/nocode)。它确实做到了不产生任何bug：
    _No code is the best way to write secure and reliable applications. Write nothing; deploy nowhere.
    不写代码，就不会产生bug,这真是极高的佛家智慧：菩提本无树，明镜亦非台，本来无一物，何处惹尘埃？不过，就是这样一个项目，还是被人提交了超过3k的issues(如果你认为项目中存在bug，或者有新的功能需求，或者其它需要解决的问题，就可以提出一个issue)，这算是程序员的幽默吧？

3. 程序应该以可安装包的形式发布出去，而不是以源代码的方式交付。Hello World小程序显然也没有涉及到这一部分。

还有很多很多。一个完整的项目，除了提供最核心的程序功能之外，还必然涉及到产品质量控制（包括单元测试、代码风格控制等）、版权、发布历史、制作分发包等杂务，从而也就在实现功能的源代码之外，引入了许多其它文件。这些文件应该如何组织？有没有基本的命名规范？是否有工程模板可以套用，或者可以通过工具来生成？这一章将为您解答这些问题。

这一章将介绍规范的项目布局应该具有什么样的目录视图，并在最后介绍了一个遵循社区最新规范的、生成Python工程框架的向导工具。

项目文件布局必须遵循一定的规范。这有两方面的考虑，一是项目文件布局是项目给人的第一印象，一个布局混乱的项目，会吓跑潜在的用户和贡献者；遵循规范的项目文件布局，可以让他人更容易上手；二来，构建工具、测试工具等工具也依赖于一定的文件结构。如果文件结构没有一定的规范，则必然要对每个工具进行一定的配置，才能使其工作。过多的配置项往往会引起错误，加重学习成本。

!!! Readmore
    以依赖管理和构建工具Poetry为例，它会默认把构建生成的包放在dist目录下，tox在构建测试环境时，则会在这个目录下寻找安装包。这是一种约定。

在工程构建过程中，使用约定俗成的项目文件结构和规范的文件、文件夹名字，而不是通过繁琐的配置项目以允许过度自定义，这种原则被称为惯例优于配置(convention over configuration)，这不仅仅是Python,也是许多其它语言遵循的原则。

## 标准项目布局
首先，我们介绍一个经典的Python项目布局，由[Kenneth Reitz](https://kennethreitz.org/)推荐。Kenneth Reitz是著名的Python http库[requests](https://github.com/psf/requests)和[pipenv](https://github.com/pypa/pipenv)的作者。

这个布局如下面所示：
```text
├── sample
│   ├── AUTHORS.rst
│   ├── docs
|   |   ├── conf.py
│   │   └── index.rst
│   ├── HISTORY.rst
│   ├── LICENSE
│   ├── makefile
│   ├── MANIFEST.in
│   ├── README.rst
│   ├── requirements.txt
│   ├── sample
|   |   ├── app.py
│   │   └── helper.py
|   ├── setup.cfg
|   ├── setup.py
│   └── tests
```
下面我们来逐一解释。
### 文档
#### 项目说明文档
一般使用README作为文件名，大写。用来向本项目的使用者概括性地介绍这个项目的基本情况，比如主要功能、优势、版本计划等。这里文件的后缀是.rst，这是一种扩展标记文本格式，通过文档构建工具，可以生成富文本格式的文件。现在更流行的格式可能是markdown，以.md作为文件名后缀。我们会在文档构建那一章再详细介绍两者的区别。
#### 许可证文档
一般使用LICENSE作为文件名，大写。开源项目必须配置此文档。此文件一般为纯文本格式，不支持扩展标记。
#### 版本历史文档
一般使用HISTORY作为文件名，大写。

每一个版本发布，都可能引入新的功能、修复了一些bug和安全性问题，也可能带来一些行为变更，导致使用者必须也要做相应的修改才能使用。

如果没有一个清晰的版本说明，程序库的用户就不知道应该选用哪一个版本，或者是否应该升级到最新版本上。使用新的版本可能会有益处，但也带来很多测试的工作。因此，我们在使用其它人开发的程序库时，并不一定要选择最新的，有时候甚至升级到最新的版本会导致程序无法运行。比如SQLAlchemy是一个应用十分广泛的Python ORM框架，它的1.4版本与前面的版本有较多不兼容的问题。如果您的程序不加修改就直接升级到1.4，那么大概率程序会崩溃。

同README一样，可以使用.rst的文件格式，也可以使用.md的文件格式，后面我们不再特别提示。
#### 开发者介绍文档
一般使用AUTHORS作为文件名，大写。其目的是向他人介绍项目的开发者团队。

### 帮助文档
一个优秀的项目，还往往会有比较详尽的帮助文档，来告诉使用者如何安装、配置和使用，甚至还会配有一些教程。这些文档在命名上就没有那么严格，最终，它们将通过文档生成工具转换成格式更加美观的在线文档，供使用者阅读。一般地，这些文档都放在docs目录下，由一个主控文档(index.rst)来串联。当然，具体如何做，取决于文档构建工具。

#### API文档
还有一类比较特殊的文档，它们不直接出现在上述目录中，而是散落在源代码的各个部分，通过专用工具生成，与帮助文档一起使用。关于帮助文档和API文档，我们将在第10章，撰写技术文档中详细介绍。
### 工程构建配置文件
不同的构建工具需要不同的配置文件。在Python工程中，主要有两种主流的构建工具，一是Python setup tools,另一种是符合PEP517，PEP518规范的新型构建工具，如Poetry等。

在上述目录示例中，使用的是基于python setup tools的构建工具，它需要的配置文件有setup.py, MANIFEST.IN等文件，还可能会有requirements.txt和makefile；这也是为什么您会看到setup.py等文件的原因。如果是使用Poetry,则配置文件会简单许多，只需要一个pyproject.toml就够了。

当您开始新的项目时，应该只使用Poetry，而不使用python setup tools。Poetry的依赖管理可以锁定程序的运行时，避免很多问题。但是，您可能依然要能看懂基于setup tools的老式工程配置，它们将可能在未来的一两年里还继续存在。
### 代码目录
在其它开发语言，特别是编译型语言中，代码目录常常被称为源文件目录。由于Python是非编译型语言，代码源文件本身就是可执行文件，所以一般我们不把代码文件称作源文件。我们通常把发行的目标物称之为一个"包(package)"。因此，在下面的叙述中，我们将会把代码目录称之为包目录，或者package目录。

因此，如果您正在开发一个名为sample的package，那么您的代码就应该放在一个名为sample的目录下，正如上面的目录视图所示。

有一个小地方需要说明，这里顶层的sample是项目名字，内层的sample是包名字。两级目录共用一个名字，这是会让初学者多多少少有一些困惑的地方。但是，在Python中,我们不能象其它语言那样，直接把package目录改为src目录，因为这样会导致生成的package名字也会叫src。

!!! Info
    更有基者，一些项目（或者项目生成工具）会将程序的主入口文件也命名为与项目同名的文件。即，如果项目名字为sample，则主入口程序文件也命名为sample.py。在上面的示例中，我们推荐的主入口程序文件名为app.py。这个文件应该是您的程序入口，管理应用程序的生命期，比如初始化、进入事件循环并响应退出信号等。

按照上面的目录视图制作出来的发行包，包名字会是sample。当我们要使用sample中模块的功能时，可以这样导入：

```python
# 注意， `import *`一般来说是一种不好的语法，这里这样使用，是为了方便示例。
from sample.helper import *
```

!!! readmore
    Pypa在[sampleproject](https://github.com/pypa/sampleproject)中给出了另一种文件结构，在这里`sample`放在src目录下。

    我们在上一章中提到过，pypa就是pypi的开发者，python分发包事实上的标准。因此他们的趣向也会影响到其它开发者。

    可以肯定的是，无论如何，代码目录名必须是package名字，而不能为其它。至于要不要在其上再加一层src/目录，目前还存在一些争议。但是，一旦您的工程确定了目录结构，此后就不要修改，否则，会涉及到大量文件需要修改，因为这跟导入密切相关。

    这个例子中我们使用了老式的构建工具。注意除了构建工具之外，其它部分仍然是一样的。

### 单元测试文件目录
单元测试文件的目录名一般为tests。这也是许多测试框架和工具默认的文件夹位置。

### Makefile
对Python程序员来说，可能并不太喜欢Makefile。在其它语言中，makefile和工具make的主要作用是定义依赖关系，编译生成构建物。Python程序一般而言无须编译，它只需要进行打包。所以在最新的基于Poetry的项目模板中，是没有Makefile的。但是有一些工具，比如sphinx文档构建中还需要Makefile；此外，Makefile的多target命令模式，也还有它的用处，因此，是否使用Makefile，可以取决于您项目的需要。

在Kenneth Reitz推荐的项目布局中，还缺少一些重要的文件（或者目录）。这些是确保项目质量不可或缺的。主要是lint工具的配置文件，tox配置文件，codecoverage配置文件，CI配置文件等。
### lint相关工具配置文件
项目可能使用工具如flake8来进行语法检查，使用black来进行格式化。这些工具都会引入配置文件。此外，为了保证签入服务器的代码的风格和质量，可能会配置pre-commit hooks。

### tox
如果一个项目同时支持多个Python版本，那么在发布之前，往往需要在各个Python环境下都运行单元测试。为单元测试自动化地构建虚拟运行环境并执行单元测试，这就是tox要做的工作。这也是上一章讲的虚拟运行环境的一个实际使用案例。

配置了tox的项目，会在根目录下引入tox.ini文件。

### CI
在项目中使用CI是尽早暴露问题，避免更大的损失的有效方法。通过使用CI，可以确保程序员签入的代码在并入主分支之前，是能够通过单元测试的。

有一些在线的CI服务，比如appVeyor, travis和后起之秀github actions. 作者没有使用过AppVeyor。如果使用travis的话，需要在根目录下放置travis.yml这个文件。如果使用github actions，则需要在根目录下的.github/workflows/中放置配置文件，github对配置文件的名字没有要求。

### codecoverage

我们需要通过code coverage来度量单元测试的强度。一些优秀的开源项目，其code coverage甚至可以做到100%（当然允许合理地排除一些代码）。在Python项目中，我们一般使用[coverage.py](https://coverage.readthedocs.io/en/coverage-5.5/)来进行代码覆盖测试。测试框架比如pytest都会集成它，无须单独调用，但一般需要在根目录下配置.coveragerc。

作为开源项目，我们希望能够发布单元测试覆盖报告，以便给使用者更强的信心。[Codecov]就是这样一个平台。一般我们在CI中配置它。所以这部分配置会体现在CI的配置文档中。

一个有经验的开发者会发现，一个成熟的项目，往往还包括更多配置文件，远远不止Kenneth Reitz推荐的这些。比如，lint工具的配置文件，tox配置文件，codecoverage配置文件，CI配置文件等等。实际上，要手动生成一个规范的项目框架并不容易。要理解每种工具的作用，并且配置好它们使之能协同工作，需要一定的经验，在许多开发组里，搭架子的工作一般由dev lead来进行，这也是有其依据的。因此我们推荐使用项目生成向导来生成项目布局并完成配置。

!!! Readmore
    一些工具的默认配置可能会相互冲突，这也是很常见的现象。因为大家对什么是最优的技术路线都有自己的理解。比如flak8与black之间，对什么是正确的代码，有一些地方看法就不一致，从而导致black格式化的代码，总是通不过flak8的检查。因此，如何使得工具之间相互协调，也是新建项目时比较费时费力的事。

下面，我们就结合项目生成向导，来介绍更多的配置文件。
## 项目生成向导 - Python Project Wizard

如果您有其它语言的开发经验，您会发现象visual studio， 或者IntelliJ这样的开发工具有较好的向导，您只需要点击一些按钮，填写一些信息，就能立刻生成一个能编译的项目。在Python世界中，很遗憾没有任何一个开发工具（无论是vscode还是pycharm)提供这样的功能。

### cookiecutter

幸运的是，有一个开源的项目，[cookiecutter](https://cookiecutter.readthedocs.io)，可以帮我们生成各种项目的架子。

!!! Readmore
    现在的趋势是，除了IDE之外，一些框架和工具本身也在提供生成向导。比如js中的vue。本文中多次提到的Poetry也有生成框架程序的功能，不过，它并不能提供上文介绍的所有这些文件的模板，更不要提自定义它们。

cookiecutter一词的本意是饼干制造机。在这里，cookiecutter是一个生产项目模板的基础框架，理论上可用以生成任何开发语言的项目框架。通过cookiecutter,结合各种事先定义好的工程模板，就可以快速定制出自己想要的项目框架。

cookiecutter-pypackage是遵循cookiecutter规范开发的一个生成Python项目的模板，它在github上有超过3k的stars。

在`cookiecutter-pypackage`生成项目的过程中，会询问开发者的名字、电邮、项目名称，许可证类型（会让你在MIT，BSD等好几种知名的许可证模式中选择，并提供标准的LICENSE文本），是否集成click这个命令行接口，是否生成console script等。回答完成这些问题之后，您就能得到一个框架程序，您可以立刻编译并发布它，包括文档。

### python project wizard
cookiecutter-pypackage所使用的技术并不完全符合现在的社区规范，所以本书作者基于这个repo，开发了一个全新的模板，它具有这些功能：

1. 提供README，AUTHORS, LICENSE, HISTORY等文件的模块，并根据您提供的相关信息进行定制化。
2. 管理项目的版本和依赖，进行构建和发布。这主要是通过[poetry]这个工具来完成的。
3. 允许您使用简便的Markdown语法来撰写帮助文档，并自动从代码中提取注释生成API文档，这主要是通过[Mkdocs]和[Mkdocstrings]来实现的。
4. 本地单元测试的多Python版本的矩阵式覆盖。这主要是通过[Tox]和[Pytest]来完成的。同时，这一阶段还进行代码格式化、语法检查、构建物格式测试，确保代码风格完全符合项目约定，代码质量符合要求。
5. 在代码风格强化方面，通过[Black]来格式化代码，使用[Isort]来格式化import代码段，使用[Flake8]和[Flake8-docstrings]来检查语法和文档格式。
6. 通过[Pre-commit hooks](https://pre-commit.com/)在代码签入时，强制进行语法检查和格式化。
7.  使用[Python Fire](https://github.com/google/python-fire)来生成命令行接口（console script)。[Python Fire]要比[Click]更简单易用。您基本上无须进行学习即可上手。
8.  使用[Github Actions]来进行CI，实现在多个操作系统、多个python版本下的矩阵式测试覆盖，自动发布文档和构建物，生成codecoverage report，并自动上传到[Codecov]
9.  使用[Git Pages]来托管您的文档

!!! Readmore
    这里提到了很多概念，很可能您还是第一次接触。我们先介绍一小部分。

    什么是构建物(artifact)测试？当您发布构建好的程序库到PyPI时，有可能因为格式问题被拒绝。Twine工具可以对artifact进行检查，提前发现这种错误。

    console script是Python的分发包的一种功能，允许在安装过程中，将指定的python脚本安装到用户可执行程序路径下,直接从命令行调用，就象原生的shell命令一样。

    为什么要通过CI来进行版本发布？从开发机器上进行发布有很大的随意性，难以确保发布包的质量。当您的代码签入到main/master分支，通过测试后，您给分支打上tag，这时就会触发自动发布。这样发布的包可以确保质量。

从上面的功能介绍可以看出，Python Project Wizard不仅仅帮助我们生成项目的初始布局，它还是一系列规范和流程的倡导者，并通过工具配置和自动化使这些规范和流程在开发过程中被严格遵循。如果您不遵循这些规范，那么，您的代码将不会被签入代码仓库，也永远不能自动发布到pypi上面。

这个向导工具的文档在[这里](https://zillionare.github.io/python-project-wizard/)。

## 如何使用项目生成向导

### 1. 安装python project wizard (ppw)
首先，为我们的新工程创建一个虚拟环境，就叫sample好了：
```bash
conda create -n sample python=3.10
```
然后，在sample虚拟环境下，运行下面的命令：
```
pip install ppw
```
### 2. 生成项目
现在，我们可以使用`ppw`来创建一个项目。

```
ppw
```
这里会提示输入一些信息。
![](https://images.jieyu.ai/images/202211/20221224180300.png)

注意project_slug是github repo的名字，默认也是您的程序库的名字。不能有空格和"-"。

最后，ppw提示你，是否要创建开发环境，默认是'yes'。它将为您安装pre-commit hooks, 安装poetry和项目依赖。如果您不清楚这意味着什么，我们将在稍后的章节中进行讲解。

### 安装pre-commit hooks
如果您在ppw生成命令时，选择了init_dev_env的话，那么这一步已经自动运行过了。不过，我们正好借此机会来介绍一下init_dev_env具体做了什么。

pre-commit hooks是git的一个功能，它允许通过配置一些检查钩子，使得您的代码在上传到仓库之前，可以进行一些基础的语法和风格检查，避免将不合格的代码混入到仓库中。

一般情况下，我们通过运行命令`pre-commit install`来安装钩子。当`ppw`被安装时，这个命令也就随之安装到您的虚拟环境中了，因此，如果您在ppw命令生成时，没有选择init_dev_env的话，现在也可以手动运行这个命令。
### 安装开发依赖
如果您在ppw生成命令时，选择了init_dev_env的话，同pre-commit hooks一样，这一步也自动运行过了。

模板使用Poetry来进行项目管理，并将项目的开发依赖分成dev, test, doc等三个组，这样依赖的粒度更小一些。作为开发者，应该同时安装这三组依赖。

```
pip install poetry
poetry install -E doc -E test -E dev
tox
```
在安装好开发依赖之后，我们立即运行了`tox`命令，对新生成的框架程序进行测试。命令最后会给出一个测试报告和lint report。不出意外，这里不应该有任何错误（但可能会有重新格式化的警告)。

### 创建Github Repo
现在，我们已经有了一个结构良好的框架程序，您可以立刻基于它进行功能开发。但是，一个完整的开发流程，还至少包括代码管理、CI和发布。我们接下来看看应该如何处理这一部分。

我们使用github作为代码仓库。您也可以使用gitlab或者其它的代码仓库。但是，github是一个免费的服务，人人都能使用，也无须安装设置。因此，在本书中，我们都尽可能地使用这些免费服务。

登录到github,创建一个名为sample的repo（sample即为project_slug)。然后在本机进入sample目录，执行以下操作：

```
cd sample

# git init
git add .
git commit -m "Initial skeleton."
git branch -M main
git remote add origin git@github.com:myusername/sample.git
git push -u origin main
```

### 进行发布测试

您可以通过向testpypi进行发布来测试构建过程，您也可以忽略这一步。

关于这一步，请参见[文档](https://zillionare.github.io/python-project-wizard/tutorial/)

### 设置Github CI

您也可以暂时忽略这一步，但是强烈建议您完成它。

向导生成的项目中已经包括了必要的CI步骤，如调用tox进行测试，发布文档和发行包。但是需要您配置一些账户。您需要生成github的personal token，并在repo > settings > secrets中，新增一个名为``PESONAL_TOKEN``的环境变量，其值设置为您的token。

您需要在[test pypi](https://test.pypi.org/manage/account/)和[pypi](https://pypi.org/manage/account/)上申请部署用token，并象刚刚设置github token一样，新增``TEST_PYPI_API_TOKEN``和``PYPI_API_TOKEN``这两个变量。

当您完成上述设置后，以后每次将代码推送到github上的任何分支，都会触发CI，并在测试通过后，自动向testpypi进行发布；当main分支签入代码，并且打了tag时，则在测试通过后，自动向pypi进行发布。

### 设置Codecov

CI已设置为自动发布codecoverage report，但需要您在[codecov]上导入您的repo并授权。

### 设置git pages
CI已设置为自动发布文档到git pages。但您需要在您的项目中启用它。启用的方法是，在 repo > settings > pages中，选中以下两项：

![](https://images.jieyu.ai/images/202211/20221225094224.png)

### 自动化脚本
对初次使用github的人来说，从创建git仓库开始的一些操作可能会比较困难；即使是对熟练使用github的人，这些步骤也会比较繁琐易错。因此，在python project wizard创建的项目中，都会存在一个github.sh脚本:

```bash
#!/bin/bash

# !!!NOTICE!!
# Personal token with full access rights is required to run this scripts
# Once you got persona token, set enviroment variable GH_TOKEN with it

# uncomment the following to create repo and push code to github
# gh repo create sample --public
# git remote add origin git@github.com:zillionare/sample.git
# git add .
# pre-commit run --all-files
# git add .
# git commit -m "Initial commit by ppw"
# git branch -M main

# Uncomment the following to config github secret used by github workflow. 
# gh secret set PERSONAL_TOKEN --body $GH_TOKEN
# gh secret set PYPI_API_TOKEN --body $PYPI_API_TOKEN
# gh secret set TEST_PYPI_API_TOKEN --body $TEST_PYPI_API_TOKEN

# uncomment the following if you need to setup email notification
# gh secret set BUILD_NOTIFY_MAIL_SERVER --body $BUILD_NOTIFY_MAIL_SERVER
# gh secret set BUILD_NOTIFY_MAIL_PORT --body $BUILD_NOTIFY_MAIL_PORT
# gh secret set BUILD_NOTIFY_MAIL_FROM --body $BUILD_NOTIFY_MAIL_FROM
# gh secret set BUILD_NOTIFY_MAIL_PASSWORD --body $BUILD_NOTIFY_MAIL_PASSWORD
# gh secret set BUILD_NOTIFY_MAIL_RCPT --body $BUILD_NOTIFY_MAIL_RCPT
```

这个脚本帮助我们完成这些任务：
1. 创建github仓库，并将代码推送到github
2. 向github仓库添加个人token（PERSONAL_TOKEN），pypi发布的API token，test pypi发布的API token。
3. 注册邮件通知。当Github CI执行完成后，无论是成功还是失败，都会向您注册的邮箱里发送一封通知邮件。

要运行上述脚本，您需要完成两件事：
1. 安装github cli工具。请参考[安装指南](https://github.com/cli/cli#installation)
2. 申请一个GitHub的个人token（全部权限），然后将这个token通过环境变量GH_TOKEN暴露给脚本。只有这样，脚本才能创建github仓库，并设置其它token。

### ppw生成的文件列表
现在，一个规范的新项目就已经创建好，您已经拥有了很多酷炫的功能，比如CI，codecov, git pages，poetry，基于markdown的文档等等。您新生成的项目，应该看起来象这样：
```text
.
├── .coveragerc
├── .docstring.tpl
├── .editorconfig
├── .flake8
├── .git
│   ├── hooks
│   │   ├── pre-commit
│   │   └── ...
├── .github
│   ├── ISSUE_TEMPLATE.md
│   └── workflows
│       ├── dev.yml
│       └── release.yml
├── .gitignore
├── .isort.cfg
├── .pre-commit-config.yaml
├── AUTHORS.md
├── CONTRIBUTING.md
├── HISTORY.md
├── LICENSE
├── README.md
├── docs
│   ├── api.md
│   ├── authors.md
│   ├── contributing.md
│   ├── history.md
│   ├── index.md
│   ├── installation.md
│   └── usage.md
├── mkdocs.yml
├── poetry.lock
├── pyproject.toml
├── pyrightconfig.json
├── repo.sh
├── sample
│   ├── __init__.py
│   ├── app.py
│   ├── py.typed
│   └── cli.py
├── tests
│   ├── __init__.py
│   └── test_app.py
└── tox.ini
```
接下来，我们将带领您深入这些工具，了解为什么在众多工具中，选择了这一种，应该如何配置，如何使用等等。
