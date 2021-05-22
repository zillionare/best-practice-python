# black

Black的维护者是 Łukasz Langa和Carol willing， Łukasz Langa也是Python 3.8和3.9的release manager。 Carole Willing是Python指导委员会成员， Python Software Foundation fellow， Frank Willison奖获得者（
编辑，Python enthusiast），他也是Jupyter的贡献者之一。

Dusty Phillips, writer:

    Black is opinionated so you don't have to be.

Hynek Schlawack, creator of attrs, core developer of Twisted and CPython:

    An auto-formatter that doesn't suck is all I want for Xmas!

Carl Meyer, Django core developer:

    At least the name is good.

Kenneth Reitz, creator of requests and pipenv:

    This vastly improves the formatting of our code. Thanks a ton!

The following notable open-source projects trust Black with enforcing a consistent code style: pytest, tox, Pyramid, Django Channels, Hypothesis, attrs, SQLAlchemy, Poetry, PyPA applications (Warehouse, Bandersnatch, Pipenv, virtualenv), pandas, Pillow, every Datadog Agent Integration, Home Assistant, Zulip.

The following organizations use Black: Facebook, Dropbox, Mozilla, Quora.

# About Python

1. why Python is so popular?

Carol willing: 可读性和perfomance（从原型到部署，quickly, efficiently, reliably)

2. Python project相关的治理实体？
Python Software Foundation是人们成为Python社区一员时最先接触到的组织，该组织维护着http://python.org. 主要负责维护Python的知识产权，推广。

Python Steering Council(指导委员会)主要是从技术层面，对语言的核心开发负责。2018年Guido退休，成为终生仁慈独裁者之后，根据他的提议成立。工作方式主要是通过PEP（Python Enhancement Proposal). 两个组织每周开一次会。Ewa Jodlowska， PSF的执行总裁，参与PSC的周会。

# Type annotation

future import annotations: So if you are declaring a type of argument, and that type’s class is only defined later, that’s fine with Python now. There’s another PEP—PEP 585—which makes it easier to use static typing with Python and which is now part of Python 3.9.

## mypy

# performance

[Python performance: past, present, future](https://raw.githubusercontent.com/vstinner/talks/main/2019-EuroPython/python_performance.pdf)
[Pyjion](https://github.com/tonybaloney/Pyjion)
[Faster Python]()
