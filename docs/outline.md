第1章 高效的软件开发语言——Python
1.1 Python软件开发的优势
1.2 Python软件开发的过程
1.3 Python高质量软件开发的关键点
1.3.1严格执行软件开发流程 
1.3.2重视开发中3个核心步骤 
1.3.3选用高效的开发工具

第2章 Python的编程开发环境
2.1 Python开发环境
2.2Windows下的虚拟Linux环境
2.2.1 WSL方案
2.2.2 Docker方案
2.2.3虚拟机方案
2.3集成开发环境（IDE）
2.3.1VSCodevsPycharm:使用哪一个IDE？
2.3.2VSCode及扩展
2.4其他开发环境
2.4.1Jupyter Notebook
2.4.2Spyder

第3章 构建Python虚拟环境
3.1Python虚拟环境：消灭依赖地狱
3.2 Anaconda：集中式管理的虚拟环境
3.2.1安装Anaconda
3.2.2配置conda
3.2.3创建和管理虚拟环境
3.3轻量的Python包安装工具Pip
3.4配置VSCode中的解释器

第4章 项目布局和项目生成向导
4.1标准项目布局
4.1.1文档
4.1.2工程构建配置文件
4.1.3代码目录
4.1.4单元测试文件目录
4.1.5持续集成配置文件
4.2项目生成向导——Python Project Wizard
4.2.1安装Python Project Wizard
4.2.2创建虚拟环境
4.2.3安装开发依赖
4.2.4创建Github Repo
4.2.5运行发布测试
4.2.6设置Github CI
4.2.7设置Codecov

第5章 管理版本、依赖和构建——基于Poetry
5.1 Poetry：简洁清晰的项目管理工具
5.2版本管理
5.2.1Semantic Versioning
5.2.2如何使用Poetry进行版本管理
5.3依赖管理
5.3.1实现依赖管理的意义
5.3.2Poetry依赖管理相关命令
5.3.3 Poetry 依赖解析的工作原理
5.4构建发行包
5.4.1 Python构建标准和工具的变化
5.4.2 基于Poetry进行发行包的构建
5.5 其他重要的Poetry命令
5.6 案例：基于poetry创建并发布一个项目

第6章 实现高效的Python编码
6.1Kite：AI赋能的自动完成和文档提示
6.2给代码加上类型标注
6.3运用Lint工具
6.3.1 Lint工具的作用
6.3.2 Python Lint工具比较
6.3.3 Flake8的配置和使用
6.3.4 案例：Flake8查错功能演示及错误解析
6.4Formatter工具
6.4.1 什么样的代码，才符合Zen of Python
6.4.2 Python formatter工具比较
6.4.3Black：不妥协的代码格式化工具
6.4.4iSort：导入格式化工具
6.4.5 案例：基于Black和iSort进行代码格式化
6.5代码提交钩子：把不规范的代码挡在门外
6.5.1 为什么要使用代码提交钩子？
6.5.2 安装和配置常用的代码提交钩子
6.5.2 案例：代码钩子阻止不合规范的代码入库

第7章 代码单元测试——基于Unittest、Pytest、Pycoverage和Tox
7.1测试代码的组织结构
7.2Unittest框架
7.2.1测试文件的基本结构
7.2.2如何使用Mock（内含案例）
7.2.3使用断言（内含案例）
7.3Pytest测试库
7.4 衡量测试的覆盖率
7.4.1配置Pycoverage
7.4.2发布覆盖率报告
7.4.3 案例：提高测试覆盖率
7.5 Tox环境矩阵加速测试
  7.5.1什么是Tox？
  7.5.2 Tox的工作原理
  7.5.3如何配置Tox

第8章 代码版本管理——基于Git和Github
8.1代码版本管理的意义
8.2版本管理工具Git
8.2.1Git中的基础操作
8.2.2Git中的高级操作
8.2.3谁引入了错误：如何追踪代码变化（案例）
8.3分支管理
8.4代码在分支之间的流动
8.5Github/Gitlab

第9章 持续集成——基于Github CI和Travis CI
9.1持续集成的意义
9.2常见的在线CI服务
9.3Github CI
9.3.1Github CI概述
9.3.2配置文件语法概览
9.3.3连接其他服务
9.3.4常用的GithubActions
9.3.5 案例：使用外部服务的Github CI高级配置实例
9.4Travis CI

第10章 撰写技术文档
10.1技术文档的组成
10.2两种主要的文档格式
10.2.1reStructured Text
10.2.2Markdown
10.3两种主要的文档构建工具
10.3.1Sphinx
10.3.2Mkdocs
10.4使用Sphinx构建文档
10.4.1文档结构与主控文档
10.4.2工具链
10.4.3混合使用Markdown
10.5使用Mkdocs构建文档
10.5.1文档结构
10.5.2API文档
10.6文档在线托管服务
10.6.1 Read the Docs
10.6.2 Github Pages
10.7 案例：基于Mkdocs的文档构建及发布

第11章 发布应用
11.1通过PyPI发布应用
11.1.1 TestPyPI
11.1.2 PyPI
11.1.3案例：发布一个包到TestPyPI
11.2Whl格式的局限
11.3制作Native的安装包
11.3.1 makeself的多平台安装包（内含案例）
11.3.2 基于PyInstaller的多平台安装包
