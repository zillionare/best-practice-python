# 撰写技术文档
所有好的产品都应该有一份简洁易读的使用说明书，除了苹果。苹果用户天生就知道如何使用他们的产品，因此完全不需要文档。这是真的，几乎所有的苹果产品，都没有用户说明书。

但是对于软件来说，其复杂性往往要求必须有与之配套的详尽的技术文档，使用者才好上手。即使是开源产品，人们通常也是首先借助产品的技术文档快速上手。在一个速食时代，如果不是逼不得已，谁有时间去一行一行地看代码呢？

既然技术文档如此重要，那么，如何写好技术文档，有哪些工具可以帮助我们进行文档创作，好的技术文档有哪些评价标准，其评价标准能否象软件一样进行量化？

作者认为，除了要求技术作者本身有较好的文笔之外，一个好的技术文档常常还包括以下技术要求：

1. 规范的文档结构，简洁优美的格式
2. 内容准确无误：包括文档版本与代码实现始终保持一致（多版本）
3. 提供必要的导航和交叉引用，帮助读者进一步阅读，并且无死链
4. 文档在线托管，随时可阅读和可搜索
5. 在必要时能够生成各种格式，比如html, PDF, epub等。

这篇文章将探索常见的文档构建技术栈。作者的重点不在于提供一份大而全的操作指南，而在于探索各种可能的方案，并对它们进行比较，从而帮助您选择自己最适合的方案。至于如何一步步地应用这些方案，文章也提供了丰富的链接供参考。

通过阅读这篇文章，您将了解到：

1. 文档结构的最佳实践
2. 文档构建的两大门派
3. 如何自动生成API文档
4. 如何使用git pages进行文档托管
## 技术文档的组成
一份技术文档通常有两个来源：一是我们在写代码的过程中按照一定风格提供的注释，通过工具将其提取出来形成的所谓API文档，这部分文档深入到细节之中；二是在此之外，我们特别撰写的帮助文档，相比API文档，它们更加宏观概要，涵盖了API文档中不适合提及的部分，比如整个软件的安装指南、设计理念与原则、License信息、版本历史、涵盖全局的示例等等。

时至今日，在Python世界里，大致有两种流行的技术文档构建技术栈，即sphinx和mkdocs。下面的基于sphinx技术栈构建文档的一份文件清单：
```
.
├── AUTHORS.rst
├── CONTRIBUTING.rst
├── HISTORY.rst
├── LICENSE
├── README.rst
├── docs
│   ├── conf.py
│   ├── Makefile
│   ├── make.bat
│   └── index.rst
└── Makefile
```
这个布局是《[Python最佳实践指南](https://docs.python-guide.org/writing/structure/)》一书中推荐的，它的最初出处是[Knnedth Reitz](https://kennethreitz.org/essays/repository-structure-and-python)在2013年推荐的一个Python项目布局的最佳实践，为适应开源项目的需要，我在这里增加了CONTRIBUTING.rst和AUTHORS.rst两个文件。我们看到其特点是，文档的类型是rst文件，在文档目录下包含了一个conf.py的python文件，还有Makefile。

如果你使用[Cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)来生成项目的框架，你会发现它生成的项目正好就包括了这些文件。

另一条技术路线则是mkdocs。这也是ppw所采用的技术路线。为了叙述方便起见，我们在这里也给出一个ppw生成的、仅与文档构建相关的文件清单：

```txt
.
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
└── mkdocs.yml
```
可以看出，这条技术路线使用markdown的文件格式，由mkdocs.yml提供主控文档和配置，除此之外，并不需要别的配置。
## 两种主要的文档格式
技术文档一般使用纯文本格式的超集来书写。常见的格式有[reStructuredText](https://docutils.sourceforge.io/rst.html)(以下称为rst)和[Markdown](https://zh.wikipedia.org/zh-hans/Markdown)。前者历史更为久远，语法复杂，但功能强大；后者比较新颖，语法十分简洁，在一些第三方插件的支持下，功能上也已逐渐追赶上来。
### reStructured Text
这一节我们简要地介绍reStructured Text的常用语法。
#### 章节标题(section)
在rst中，章节标题是文本加上下缀标点(限#=-~:'"^_*+<>`)。

```rst
一级标题
####

restructured text example

1.二级标题
=====

1.1三级标题
-------

1.1.1四级标题
^^^^^^^^^

1.1.2四级标题
^^^^^^^^^
1.1.1.2.1五级标题
+++++++++++++

1.1.1.2.1.1六级标题
***************
1.2三级标题
-------
```
上述文本将渲染为以下格式：
![](https://images.jieyu.ai/images/202301/20230126213304.png)

这种语法的繁琐和难用之外在于，首先标题字符数与下面的标点符号数必须匹配。如果使用了非等宽字符，或者使用了中文标题，匹配将十分困难，您可以试下上面的例子。

除了在输入上不够简洁，易出错（主要是指数量匹配）外，标题的级别与符号无关，只与符号出现的顺序有关，也是容易出错的地方。使用者必须记住每个符号与标题级别的对应关系，否则生成的文档就会出现标题级别错误。
#### 列表(list)
在rst中，使用*,-,+做项目符号构成无序列表；有序列表则以数字、字母、罗马数字加上'.'或者括号来构成。请见以下示例：
```
*   无序 1
-   无序 2
+   无序 3
1.  有序 1
2)  有序 2)
(3) 有序 (3)
i.  有序 一
II.  有序 贰
c.  有序 three
```
示例中，有序列表可以使用右括号，或者完全包围的括号，但不能只使用左括号。

#### 表格
rst中的表格功能比较强大，支持网格表格、简单表格、csv表格和list表格。网格表格就是使用一些符号来构成表格，如下所示：
```txt
+------------------------+------------+----------+----------+
| Header row, column 1   | Header 2   | Header 3 | Header 4 |
| (header rows optional) |            |          |          |
+========================+============+==========+==========+
| body row 1, column 1   | column 2   | column 3 | column 4 |
+------------------------+------------+----------+----------+
| body row 2             | Cells may span columns.          |
+------------------------+------------+---------------------+
| body row 3             | Cells may  | - Table cells       |
+------------------------+ span rows. | - contain           |
| body row 4             |            | - body elements.    |
+------------------------+------------+---------------------+
```
这样制表显然十分繁琐，不易维护。我们也可以用指令语法来从csv数据制作表格，比如：
```rst {class='line-numbers'}
.. csv-table:: Frozen Delights!
    :header: "Treat", "Quantity", "Description"
    :widths: 15, 10, 30

    "Albatross", 2.99, "On a stick!"
    "Crunchy Frog", 1.49, "If we took the bones out, it wouldn't be
    crunchy, now would it?"
    "Gannet Ripple", 1.99, "On a stick!"
```
上面的示例中，1~3是指令，5~8是csv数据，最终我们会得到如下表格：
![](https://images.jieyu.ai/images/202301/20230126224448.png)

#### 图片
在文档中插入图片要使用指令语法，例如：
```
.. image:: img/p0.jpg
    :height: 400px
    :width: 600px
    :scale: 50%
    :align: center
    :target: https://docutils.sourceforge.io/docs/ref/rst/directives.html#image
```
示例在文档中插入了img目录下的p0.jpg图片，并且显示为400px高，600px宽，缩放比例为50%，图片居中对齐，点击图片会跳转到指定的链接。

#### 代码块
在文档中插入代码块要使用指令语法，例如：
```
.. code:: python

  def my_function():
      "just a test"
      print 8/2
```

#### 警示文本
警示文本通常用于强调一些重要的信息，比如提示错误(error)、重要(important)、小贴士(tip)、警告(warning)、注释(note)等。

同样我们用指令语法来显示警示文本，例如:

```
.. DANGER::
   Beware killer rabbits!
```
显示如下：
![](https://images.jieyu.ai/images/202301/20230126230014.png)

此外还有一些常用的语法，比如对字体加粗、斜体显示，显示数学公式、上下标、脚注、引用和超链接等。要介绍完全部rst的语法，已经远远超出了本书的范围，感兴趣的读者可以参考[官方文档](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html)。关于rst，我们要记住的是，它提供了非常强大的排版功能，不仅可以用来写在线文档，还可以直接付印成书。

### Markdown
Markdown的起源受到html的影响。HTML是一种具有强大表现力的markup语言，但是过于复杂，不利于文档的维护。Markdown的作者John Gruber希望能够用一种精减语法来书写文档，这种语法可以转换成HTML，但是简单易用，因此取名为Markdown。

Markdown的语法非常简单，只有几十个规则，但也支持我们在rst里介绍的那些基础功能，比如多级标题、列表、图片、表格、代码块、超链接、脚注、数学公式等。

#### 章节标题
Markdown的章节标题使用#来表示，有多少个‘#’就表示多少级标题，例如：
```txt
# 1. 这是一级标题
## 1.1 这是二级标题
### 1.1.1 这是三级标题
### 1.1.2 另一个三级标题
## 1.2 另一个二级标题
```
可以看出，这比rst要容易不少。在示例中，我们给标题进行了手工编号，不过这并不是必须的，markdown的编辑工具和渲染工具往往都能自动帮我们补齐（或者渲染出来）。

#### 列表
Markdown的列表与rst差不多，无序列表使用'-'或者'*'引起，有序列表使用数字加'.'引起，例如：
```markdown {class='line-numbers'}
- 无序列表1
- 无序列表2

1. 有序列表1
3. 有序列表2
```
在上面的示例中，我们给有序列表的序号并不是连续的，这是允许的，markdown的渲染工具会自动帮我们调整

#### 插入链接
在markdown中插入链接更简单，语法如下：
```
[链接名](https://example.com)
```
即由符号[]()定义了一个链接，其中[]中是链接的显示文字，()中则是链接的target。
#### 插入图片
插入图片的语法与插入链接类似，只是在前面多了一个'!'，例如：
```
![](https://images.jieyu.ai/images/202301/20230126230014.png)
```
此时'[]'中是不需要有文字的。

#### 代码块
我们使用三个反引号('`')来定义代码块，例如：
```txt {class='line-numbers'}
    ```python
        def foo():
            print('hello world')
    ```
```
起头的反引号之后，可以加上语言定义。如此以来，代码块就可以获得语法高亮了。上面的代码块，我们使用了'python'作为语言定义，这样代码块就会获得python的语法高亮，如下所示：
```python
    def foo() -> None:
        print('hello world')
```
#### 警示文本
markdown本身不支持警示文本，但一些常用的工具已经对此进行了扩展。在markdown中，我们可以用三个感叹号来引起警示文本，其类型则由感叹号后面的文字来决定，比如：
```
    !!! quote
        这里引用名人名言
```
其效果如下：

!!! quote
    这里引用名人名言

#### 其它语法
两个'\*\*'之间的文本将显示为加粗，两个'\_'之间的文本将显示为 _斜体_（也可以使用两个'\*'包含文本）。如果文本被包含在两个'\*\*\*'，则文本显示 ***既加粗，也显示为斜体***。

行内数字公式使用一对'\$'包含，例如：\$x\^2\$，效果如下：$x^2$。这里我们还演示了上标，即使用'^'。如果是要生成下标，则可以用'_'，例如：\$x\_2\$，效果如下：$x_2$。

## 两种主要的文档构建工具
### Sphinx
### Mkdocs
## 使用Sphinx构建文档
### 文档结构与主控文档
### 工具链
### 混合使用Markdown
### 使用Mkdocs构建文档
### 文档结构
### API文档
## 文档在线托管服务
### Read the Docs
### Github Pages
## 案例：基于Mkdocs的文档构建及发布



## 1.2. 文档格式



我们推荐使用Markdown来作为主要的文档格式，原因是使用Markdown可以节省较多的时间；在Markdown标准语法无法涵盖的一些特殊情况上，可以使用插件或者其它变通方法来补救。

这里我们通过几个例子来比较一下两种格式上的区别。
在Markdown中，标题使用 `#`来引起，有几个`#`，就意味着是几级标题，非常简明，完全没有上述烦恼。

当然rst也有Markdown力有不逮的地方。它强大的指令(directive)语法使之很容易扩展。Sphinx利用这一特性扩展出很多高效的指令，比如csv-table：

```
.. csv-table:: 物理内存需求表
    :header: "行情数据","记录数（每品种）","时长（年）","物理内存（GB)"
    :widths: 12, 15, 10, 15

    日线,1000,4,0.75

```
上面的语法将生成下面的表格:

![](http://images.jieyu.ai/images/12/20201207190429.png)

如果你使用过Markdown的表格（实际上Markdown标准语法并不支持表格，表格已经是扩展的语法，但已成为事实上的标准，几乎所有的Markdown viewer都会支持），你就会了解在Markdown中画表格是多么繁琐的一件事！不过，如果你使用vscode，那么也可以用扩展可以将csv数据转换成为Markdown支持的表格格式。下面这个表格，就是先输入csv数据，再转换成Markdown表格的：

下表列出了两种语法各自的能力特征。对rst来说，一些通过Sphinx支持的功能基本上已成事实标准，多数能渲染rst的工具也支持

![](http://images.jieyu.ai/images/12/20201207190709.png)

## 1.3. Sphinx vs Mkdocs, 两种主要的构建工具

rst和Markdown为我们提供了可靠的（即无须任何工具也可阅读）、但是降了级的阅读体验。所以，我们需要文档构建工具，将以这些文档格式写成的文件，转换成富文本格式的文件，比如html，pdf等。此外，在一个较大的工程中，我们的文档也必然是分成多个文档来组织，而决不会是一个单一文档。如何将多个文档统合起来，使之呈现一定的结构，文档各部分能够相互链接，也需要构建工具来实现。

Sphinx和Mkdocs就是两种比较重要的文档构建工具。

[Sphinx](https://www.sphinx-doc.org/en/master/)是始于2008年5月的一种文档构建工具，当前版本3.3。其主要功能是通过主控文档来统合各个子文档，生成文档结构(toctree)，自动生成API文档，实现文档内及跨文、跨项目的引用，以及界面主题功能。

在早期的版本中，Sphinx并没有生成API文档的功能，我们通过第三方工具，sphinx-apidoc来实现这一功能。大约是从2018年起，Sphinx通过autodoc这一扩展来实现了生成API文档的功能。现在的项目中，已经没有必要再使用sphinx-apidoc这一工具了(注：如果你使用cookiecutter-pypackage来生成项目，它仍然在使用这一工具)。

[intersphinx](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html)是其特色功能，它允许你在两个不同的文档中相互链接。比如，你在自己的项目中重载了Python标准库中的某个实现，自己提供了新增实现的这部分文档，但对于未做改变的那部分功能，你并不希望将它的帮助文档重写一遍，这样就有了链接到Python标准库文档的需求。比如，通过intersphinx，你可以使用 _*:py:class:\`zipfile.ZipFile\`*_ 来跳转到Python标准库的`ZipFile`类的文档上。虽然也可以直接使用一个外部链接来实现这样的跳转，但毫无疑问，intersphinx的语法更为简洁。

[Mkdocs](https://www.mkdocs.or)出现于2014年，当前版本1.1。其主要功能除了构建项目文档外，还可以用来构建静态站点。在构建项目文档方面，它主要提供文档统合功能（包括 toctree）和界面主题，其它功能（比如API文档）要依靠插件来实现。与Sphinx相比，它提供了**更好的实时预览能力**。Sphinx自身没有提供这一能力，有一些第三方工具（比如vscode中的rst插件，提供了单篇文章的预览功能。很显然Mkdocs无法提供intersphinx的功能，但在项目内的相互引用是完全满足要求的。

这两种文档构建工具都得到了[readthedocs](https://readthedocs.org/)的支持。在多数情况下，我们更推荐使用mkdocs及Markdown语法。

# 3. 使用Sphinx构建文档

## 3.1. 初始化文档结构

您可以使用前面提到的cookiecutter-pypackage来生成项目的框架。它生成的项目框架就包含了Sphinx构建工具及相关配置。

如果您没有使用框架代码生成工具，也可以在安装sphinx之后，运行下面的代码来初始化文档:

``` bash
pip install sphinx 

# exec this in your project root folder!!!
shpinx-quickstart
```
Sphinx会提示你输入项目名称、作者、版本等信息，最终生成docs目录及以下文件：
```
docs/
docs/conf.py
docs/index.rst
docs/Makefile
docs/make.bat
docs/_build
docs/_static
docs/_templates
```
如果文档中使用了图像文件，应该放在_static目录下。

现在运行 ``make html``就可以生成一份文档。你可以通过浏览器打开``_build/index.html``来阅读，也可以通过``python -m http.server -d _build/index``,然后再通过浏览器来访问阅读。

按照Python的最佳实践，我们一般把README.rst, AUTHOR.rst, HISTORY.rst放在项目的根目录下，即与Sphinx的文档根目录同级。而按Sphinx的要求，文档又必须放置在docs目录下。我们当然不想同样的文件，在两个目录下各放置一份拷贝。为解决这个问题，我们一般使用``include``语法，来将父目录中的同名文件包含进来。比如上述index.rst中的history文件：
```
# content of docs/history.rst

.. include:: ../HISTORY.rst
``` 
这样就避免了同一份文件，出现多个拷贝的情况。

## 3.2. 主控文档和工具链

如果您是通过Sphinx-quickstart来进行初始化的，它的向导会引您进行一些工具链的配置，比如象autodoc(用于生成API文档)。为了完备起见，我们还是再提一下这个话题。

Sphinx在构建文档时，需要一个主控文档，一般是index.rst:

```

文档Title
==========

.. toctree::
   :maxdepth: 2

   deployment
   usage
   api
   contributing
   authors
   history

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

Sphinx通过主控文档，把单个文档串联起来。 上面的toctree中的每一个入口（比如deployment)，都对应到一篇文档（比如deployment.rst)。此外，还包含了索引和搜索入口。

### 3.2.1. 生成API文档

要自动生成API文档，我们需要配置autodoc扩展。Sphinx的配置文档是docs/conf.py：

```python
# from conf.py

# 要实现autodoc的功能，你的模块必须能够导入，因此先声明导入路径
sys.path.insert(0, os.path.abspath('../src'))

# 声明autodoc扩展
extensions = [
  'sphinx.ext.intersphinx',
  'sphinx.ext.autodoc',
  'sphinx.ext.doctest'
]
```
注意到在``index.rst``中我们声明了对``api``文档的引用。这个文档用作autodoc的文档入口，其语法入下：

```
Crawler Python API
==================

Getting started with Crawler is easy.
The main class you need to care about is :class:`~crawler.main.Crawler`

crawler.main
------------

.. automodule:: crawler.main
   :members:

crawler.utils
-------------

.. testsetup:: *

   from crawler.utils import should_ignore, log

.. automethod:: crawler.utils.should_ignore

.. doctest::

	>>> should_ignore(['blog/$'], 'http://ericholscher.com/blog/')
	True
```
这里假设了一个名为Crawler的程序，它共有``main``和``util``两个模块。我们通过``.. automodule:: crawler.main``将``main``模块引入，并使用``..doctest::``来进行测试。

在Sphinx进行文档构建时，就会生成这两个模块对应的API文档，并将上述入口绑定到正确的链接上。

Sphinx的功能比较强大，因而其学习曲线也比较陡峭。在学习时，可以将其[渲染好的教程](https://sphinx-tutorial.readthedocs.io/)与[教程的源码](https://github.com/ericholscher/sphinx-tutorial/)对照起来看，这样更容易理解。

使用Autodoc生成的API文档，需要我们逐个手动添加入口，就象上面的``.. automodules:: cralwer.main``那样。对比较大的工程，这样无疑会引入一定的工作量。Sphinx的官方推荐使用[sphinx.ext.autosummary](https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html)扩展来自动化这一任务。前面已经提到，在较早的时候，Sphinx还有一个cli工具，叫sphinx-apidoc可以用来完成这一任务。但根据[这篇文章](https://romanvm.pythonanywhere.com/post/autodocumenting-your-python-code-sphinx-part-ii-6/)，我们应该转而使用``sphinx-ext.autosummary``这个扩展。

除此之外，readthedocs官方还开发了一个名为[sphinx-autoapi](https://sphinx-autoapi.readthedocs.io/en/latest/tutorials.html)的扩展。与autosummary不同，它在构建API文档时，并不需要导入我们的项目。目前看，除了不需要导入项目之外，没有人特别提到这个扩展与autosummary相比有何优势，这里也就简单提一下，大家可以持续跟踪这个项目的进展。

### 3.2.2. docstring的样式

如果不做任何配置，Sphinx会使用rst的docstring样式。为简洁起见，我们一般使用google style(最简)，或者numpy style(适用于较长的docstring)。

要在文档中使用这两种样式的docstring，你需要启用[Napolen](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)扩展。关于这两种样式的示例，我觉得最好的例子来自于[MkApi的文档](https://mkapi.daizutabi.net/examples/google_style/)，这里不再赘述。

注意在Sphinx 3.0以后，如果你使用了Type Hint，则在书写docstring时，不必在参数和返回值上声明类型。扩展将自动为你加上类型声明。

### 3.2.3. 混合使用Markdown

多数人会觉得rst的语法过于繁琐，因此很自然地，我们希望部分文档使用Markdown来书写（如果不能全部使用Markdown的话）。大约从2018年起，readthedocs开发了一个名为[recommonmark](https://recommonmark.readthedocs.io/en/latest/)的扩展，以支持在Sphinx构建过程中部分使用Markdown。

在这种场景下要注意的一个问题是，Markdown文件必须都在docs目录及其下级目录中，而不能出现在项目的根目录下。这样一来，象README，HISTORY这样的文档，就必须仍然使用rst来写（以利用``include``语法来包含来自上一级的README)。如果要使用Markdown的话，就必须使用符号连接将父目录中的README.md连接到docs目录下（recommenmark自己的文档采用这种方式）；或者通过Makefile等第三方工具，在sphinx build之前，将这些文档拷贝到docs目录。

在github上还有一个m2r的项目，及其fork m2r2，可以解决这些问题，不过开发者怠于维护，随着Sphinx版本升级，基本上不可用了。

如果您的项目必须使用rst，那么可以在项目中启用recommonmark，实现两种方式的混用。通过在recommonmark中启用一个名为autostructify的子组件，可以将Markdown文件事前编译成rst文件，再传给Sphinx处理；更妙的是，autostructify组件支持在Markdown中嵌入rst语法，所以即使一些功能Markdown不支持，也可以通过局部使用rst来补救。

如果您对使用Markdown来撰写文档更感兴趣的话，请接着往下看。

# 4. 使用Mkdocs构建文档

Mkdocs支持完全使用Markdown来撰写文档，并且通过社区提供的插件来支持将生成的API文档与手工文档融合。

[mkdocs](https://www.mkdocs.org)自身提供的功能非常简单，粗粗看一眼的话，你会觉得它只能用来构建静态网站，而无法用来撰写项目文档。但社区提供了很多插件，加上本身提供的扩展一起，使得简单快捷地构建项目文档成为可能。

安装mkdocs之后，可以看一下它的基本命令：

![](http://images.jieyu.ai/images/12/20201207190824.png)

Mkdocs提供了两种theme，readthedocs和mkdocs。你也可以在社区里寻找更  多的[Theme](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Themes)。有些主题很适合构建静态网站。[这篇文章](https://www.mkdocs.org/user-guide/writing-your-docs/)给出了一个不错的教程。


我们来简单地看一下使用：

```
pip install --upgrade pip
pip install mkdocs
pip install mkdocs-material # 安装material主题，可忽略。技术文档一般使用自带的readthedocs主题

# 创建文档结构，在项目根目录下执行
mkdocs new PROJECT_NAME
cd PROJECT_NAME
```

现在，在项目根目录下应该多了一个docs目录，和一个名为mkdocs.yaml的文件。docs目录下还有一个名为index.md的文件。如果此时运行``mkdocs serve -a 0.0.0.0:8000``,在浏览器中打开，你会看到如下图所示界面：

![](http://images.jieyu.ai/images/12/mkdocs_new.png)

***Note：***
  请注意，Mkdocs提供的是实时预览文档，而且有很快的响应速度。

现在来看一看mkdocs.yaml的内容:

```
site_name: An amazing site!

nav: 
  - Home: index.md
  - 安装: installation.md
  - History: history.md

theme: readthedocs
```

这里mkdocs.yaml充当了主控文档。nav下面的每一项列表，都成为一级菜单。列表项可以用":"来分割，左边的是显示的文字，右边则是连接的文档。


接下来， 我们主要对照文章最初提出的那些要求，看看如何在Mkdocs中通过插件和扩展来实现。

***Note***
  在Mkdocs中既有扩展，又有插件。

## 4.1. 链接到父目录中的文件

前面提到，我们应该把READEME, HISTORY, AUTHORS, LICENSE等几个文件放在项目根目录下，但又不希望在docs目录中重复它们的拷贝。mkdocs也不能支持这种结构，不过好在有一个好用的插件，[mkdocs-include-mkdown-plugin](https://github.com/mondeja/mkdocs-include-markdown-plugin)，在安装好之后，修改index.md文件，使之指向父目录的README:

```
{%
  include-markdown "../README.md"
%}
```
修改mkdocs.yaml,加载include-markdown插件：
```
site_name: Omicron

nav: 
  - Home: index.md
  - 安装: installation.md
  - History: history.md

theme: readthedocs

plugins:
  - include-markdown
```

## 4.2. API文档

前面已经提到过这个插件， [MkApi](https://mkapi.daizutabi.net/)。但在我们试用中，可能[Mkdocstrings](https://github.com/pawamoy/mkdocstrings)的稳定性更好，社区活跃度也更高一些。

这两个插件的配置都不复杂。Mkdocs只支持google style的docstring, 在样式上支持了Material样式。对readthedocs的支持还在测试中，但也将在下一版发布。

## 4.3. 警示标注

在rst中你可以用这样的警示语:

```

.. Note:: title of notice

   PLEASE DONT

```
这样的警示语还有tip, important, warnings等好几种。Markdown不支持警示语语法，不过你可以使用[Admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)扩展来增强。

这个扩展支持了info, todo, tip,hint,important, suceess, check, done, warnings, error, example等语法：

![](http://images.jieyu.ai/images/12/mkdocs_tip.jpg)

## 4.4. 其它

链接到文档、文档中的节标题都很容易。在使用了Mkdocstrings这一类的API文档插件之后，也能够直接链接到模块中的函数。如何链接到其它项目（比如Python标准库）中的对象，没有看到文档说明。

# 5. 使用Readthedocs托管文档

最好的文档分发方式是使用在线托管，并且一旦有新版本发布，文档能立即得到更新；并且，旧的版本对应的文档也能得到保留。这两个功能，都在read the docs网站上得到完美支持。此外，您也可以使用gitpages。如果您使用Mkdocs来构建的话，似乎也支持多个版本同时在线。

[Readethedocs](https://readthedocs.org/)（以下称RTD）是Python文档最重要的托管网站，也是事实上的标准。关于如何使用RTD，请参考它的[帮助文档](https://docs.readthedocs.io/en/stable/index.html)。

这里要注意的几个核心概念：

1. 目前RTD支持Sphinx和MkDocs两种构建工具。
2. RTD上面文档来源于在线代码托管库，比如github。RTD上面的文档与你本地构建的文档没有任何关系。你在本地构建的文档，都不要上传到github上。如果你将github账号与RTD账号进行了绑定，此后每次更新代码，RTD都会自动为你编译文档并发布（也可以登录到RTD上手动触发build）。
3. 如果设置了RTD自动同步代码并build，那么每次往github上push代码时，都会触发一次build，并导致文档更新。所以正确的做法是将RTD绑定到特定的分支上（比如release），只有重要的版本发布时，才往这个分支上push代码，从而触发文档编译。RTD目前并不支持tags。
4. RTD编译文档时，可能会遇到各种依赖问题。首先应该绑定构建工具(Sphinx和Mkdocs)的版本。RTD提供了readthedocs.yml以供配置（放在项目根目录下）。根据你使用的API文档生成工具，可能还需要导入你的package，这种情况下，可能还需要为你的构建工具指定依赖。[在这里](https://docs.readthedocs.io/en/stable/config-file/v2.html)有这个配置文件的模板。
5. 在文档构建中可能出现各种问题，为了帮助调试，RTD发布了官方docker image，供大家在本地使用。

# 6. 结论

Sphinx + RST是构建技术文档的事实标准，整个技术栈比较成熟稳定，但学习曲线比较陡峭，RST的一些语法过于繁琐。随着Markdown的应用越来越成熟，Mkdocs正在成为构建静态站点和技术文档的新工具，并得到的Read the docs的支持。在使用Mkdocs进行技术文档构建时，要注意选用的插件在支持的Python版本、docstring样式及主题方面的限制。下面是两种方式的一个比较：

![](http://images.jieyu.ai/images/12/20201207190913.png)

两种方式一般配置的插件（扩展）见以下清单：

Sphinx:
```
autodoc
autosummary
recommonmark
```
mkdocs:
```
mkdocs-include-markdown-plugin
Admonitions
mkdocstrings
```




