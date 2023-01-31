<!-- # 持续集成——基于Github Actions
## 持续集成的意义
## 常见的在线CI服务
## Github Actions
### Github Actions概述
### 配置文件语法概览
### 连接其他服务
### 常用的GithubActions
### 案例：使用外部服务的Github CI高级配置实例 
-->

当一组开发者共同开发一个项目时，各种冲突似乎不可避免。我们在第8章介绍了分支和gitflow工作流模型，从而解决了代码冲突的问题。但是，代码合并只能达到表面上的和谐。不同的人开发的代码能否协同工作，最终还得通过测试来检验。

在已经介绍过的开发流程中，开发者在签入代码并推送到远程服务器之前，应该通过tox执行的单元测试和代码检查。但是，如果开发者有意忽略这些步骤，不良代码仍然能溜进仓库。此外，尽管我们虚拟化了测试环境，但仍然有可能在一名开发者机器上通过的测试，不能在另一个环境里运行。比如，可能引入了新的配置项，这些配置项存在于本地环境，但其它人并不知道；或者更改了本地数据库，但相应的变更脚本并没有集成进来，等等。如果只要有新的代码签入，就能在一台公共机器上自动执行所有测试以确保代码正确性，显然可以更早地发现问题，降低后期维护成本。这就是持续集成的意义所在。

持续集成是一种 DevOps 软件开发实践。采用持续集成时，开发人员会定期将代码变更合并到一个中央存储库中，之后系统会自动运行构建和测试操作。持续集成通常是指软件发布流程的构建或集成阶段，需要用到自动化组件（例如 CI 或构建服务）和文化组件（指组织的流程和规范等，例如学习频繁地集成）。持续集成的主要目标是更快发现并解决缺陷，提高软件质量，并减少验证和发布新软件更新所需的时间。

# 常见的在线CI服务
我们先来认识一下持续集成领域的头部玩家。Jekins是持续集成领域的老大哥，Jenkins自诞生之日起，至今已发展了近20年，社区、生态最为完善。Gitlab最初是基于Git的代码托管平台，自版本8.0起，开始提供持续集成功能。其优点是与代码仓库无缝集成，原生地支持代码仓库各类事件触发流水线。不足之处是，无论Jekins还是Gitlab，都需要自己搭建服务器，这对于开源项目和个人开发者来说，成本太高了。

构建CI服务器的成本是昂贵的。在虚拟机没有广泛应用之前，这个成本就更为昂贵。你需要为你的应用将要部署到的每一种操作系统至少准备一台机器。如果你的应用需要部署到从windows到Linux到Macos上的各个版本，你可能就需要准备至少十台以上的机器硬件。虚拟化的出现大大降低了CI的成本，随后是容器化的出现，进一步降低了CI的成本。但是，即便是这样，对开源项目，自行搭建和维护CI服务器的成本仍然是昂贵的。比如，如果你的应用需要部署到MacOs上，你必须至少有一到多台苹果的服务器，因为其它机器上都无法虚拟化出来macos的容器。

这就是为什么我们推荐使用在线CI服务的原因。好消息是，对开源项目，有相当多的在线CI服务是免费的。这里我们仅仅介绍Travis CI和Github Actions。

Travis CI是一个基于云的持续集成服务，它可以帮助开发者在Github上构建和测试代码，从而减少发布软件的时间。Travis CI为开源项目提供了一定量的服务时间，对于私有项目，则需要付费--计划起价是每月69美元。这个定价本身也说明了持续集成的价值，以及要实现持续集成，所需要消耗的资源。

Github Actions是Github在2020年前后推出的持续集成服务，它的优点同gitlab CI一样，也在于与代码托管服务无缝集成，不需要自己搭建服务器。在价格方面，Github Actions对开源项目也是免费使用的，与Travis CI相比，给出的免费quota更多，足堪使用。因此，我们本章就略过Travis CI，直接介绍Github Actions。
# Github Actions
Github Actions是一个持续集成与交付的平台，它使得我们可以将构建、测试和部署像流水线一样自动化。您可以创建工作流程来构建和测试存储库的每个拉取请求，或将合并的拉取请求部署到生产环境。

GitHub Actions 不仅仅是 DevOps，还允许您在存储库中发生其他事件时运行工作流程。 例如，您可以运行工作流程，以便在有人在您的存储库中创建新问题时自动添加相应的标签。

GitHub 提供 Linux、Windows 和 macOS 虚拟机来运行工作流程，您也可以在自己的数据中心或云基础架构中托管自己的自托管运行器。

## Github Actions的架构和概念

Github Actions由工作流(workflow)、事件(Event)、作业(job)、操作(Action)和执行者(runner)等组件构成。

工作流通过在项目根目录的.github/workflows目录下面的yaml文件来定义，我们也可以简单地将其当成脚本来理解。工作流中定义了哪些事件可以触发工作流，工作流中应该包含哪些作业，以及作业应该在什么样的执行者（容器）中运行。一个存储库中可以有多个工作流，分别执行不同的任务集。

事件是能引发工作流运行的特定事件，比如当有人创建拉取请求、或者将提交(commit)推送到存储库时，这就是一个能触发工作流的事件。

作业(job)是工作流中在同一运行器上执行的一组步骤（steps)。 每个步骤(step)要么是一个将要执行的 shell 脚本，要么是一个将要运行的操作(Action）。 步骤按顺序执行，并且相互依赖。 由于每个步骤都在同一运行器上执行，因此您可以将数据从一个步骤共享到另一个步骤。 例如，可以有一个生成应用程序的步骤，后跟一个测试已生成应用程序的步骤。

一个工作流中可以有多个作业。作业之间默认没有依赖关系，并且彼此并行运行。 但我们也可以配置一个作业依赖于另一个作业，此时，它将等待从属作业完成，然后才能运行。 例如，对于没有依赖关系的不同体系结构，您可能有多个构建作业，以及一个依赖于这些作业的打包作业。 构建作业将并行运行，当它们全部成功完成后，打包作业将运行。

操作(Action)是用于 GitHub Actions 平台的自定义应用程序，它执行复杂但经常重复的任务。 使用操作可帮助减少在工作流程文件中编写的重复代码量。 操作可以从 GitHub 拉取 git 存储库，为您的构建环境设置正确的工具链，或设置对云提供商的身份验证。

您可以编写自己的操作，也可以在 GitHub Marketplace 中找到要在工作流程中使用的操作。

执行者(runner)是运行工作流的服务器。每个执行者一次可以运行一个作业。 GitHub 提供 Ubuntu Linux、Microsoft Windows 和 macOS 运行器来运行您的工作流程；每个工作流程运行都在新预配的全新虚拟机（或者容器）中执行。

下面的图展示了Github Actions的架构：

![](assets/img/chap09/overview-actions.png)
## 工作流语法概述
在了解了Github Actions的架构之后，我们通过一个例子，来讲解如何定义工作流。

我们先看ppw生成的一个工作流文件：

```yaml
name: dev build CI

# 定义哪些事件可以触发工作流，以及筛选条件
on:
  # 当存储库有push或者pull_request事件时触发
  push:
    branches:
      - '*'
  pull_request:
    branches:
      - '*'

# 定义作业集
jobs:
  # 工作流包含三个作业，分别是test, publish_dev_build, notification
  test:
    # 定义作业的运行环境，这里使用了矩阵式定义
    strategy:
      matrix:
        python-versions: ['3.8', '3.9', '3.10']
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    # 将步骤的输出提升为作业的输出，以便它们可以在作业之间共享
    outputs:
      package_version: ${{ steps.variables_step.outputs.package_version }}
      package_name: ${{ steps.variables_step.outputs.package_name }}
      repo_name: ${{ steps.variables_step.outputs.repo_name }}
      repo_owner: ${{ steps.variables_step.outputs.repo_owner }}

    # 这是启用外部服务的一个示例
    # services:
    #   redis:
    #     image: redis
    #     options: >-
    #       --health-cmd "redis-cli ping"
    #       --health-interval 10s
    #       --health-timeout 5s
    #       --health-retries 5
    #     ports:
    #       - 6379:6379

    # 步骤集代表了一系列的任务，这些任务将作为作业的一部分执行
    steps:
      # 作业是在容器里执行的，我们需要先将代码检出到这个干净的容器里
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-versions }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install tox tox-gh-actions poetry

      # 这一步里，我们设置了一些变量，将其输出到控制台，从而可以在第85行提升为job的输出
      - name: Declare variables for convenient use
        id: variables_step
        run: |
          echo "::set-output name=repo_owner::${GITHUB_REPOSITORY%/*}"
          echo "::set-output name=repo_name::${GITHUB_REPOSITORY#*/}"
          echo "::set-output name=package_name::`poetry version | awk '{print $1}'`"
          echo "::set-output name=package_version::`poetry version --short`"
        shell: bash

      # 执行单元测试和代码检查。
      - name: test with tox
        run: tox

      # 通过codecov上传测试覆盖率。
      - uses: codecov/codecov-action@v3
        with:
          fail_ci_if_error: true

  publish_dev_build:
    # 只有test作业完成，我们才开始本作业
    needs: test
    # 指定本作业运行的操作系统环境。
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          # 这一步只需要在任意一个python版本上运行
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry tox tox-gh-actions

      - name: build documentation
        run: |
          poetry install -E doc
          poetry run mkdocs build
          git config --global user.name Docs deploy
          git config --global user.email docs@dummy.bot.com
          poetry run mike deploy -p -f --ignore "`poetry version --short`.dev"
          poetry run mike set-default -p "`poetry version --short`.dev"

      - name: Build wheels and source tarball
        run: |
          poetry version $(poetry version --short)-dev.$GITHUB_RUN_NUMBER
          poetry lock
          poetry build

      - name: publish to Test PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          user: __token__
          password: ${{ secrets.TEST_PYPI_API_TOKEN}}
          repository_url: https://test.pypi.org/legacy/
          skip_existing: true

  notification:
    needs: [test,publish_dev_build]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - uses: martialonline/workflow-status@v2
        id: check

      - name: build success notification via email
        if: ${{ steps.check.outputs.status == 'success' }}
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: ${{ secrets.BUILD_NOTIFY_MAIL_SERVER }}
          server_port: ${{ secrets.BUILD_NOTIFY_MAIL_PORT }}
          username: ${{ secrets.BUILD_NOTIFY_MAIL_FROM }}
          password: ${{ secrets.BUILD_NOTIFY_MAIL_PASSWORD }}
          from: build-bot
          to: ${{ secrets.BUILD_NOTIFY_MAIL_RCPT }}
          subject: ${{ needs.test.outputs.package_name }}.${{ needs.test.outputs.package_version}} build successfully
          convert_markdown: true
          html_body: |
            ## Build Success
            ${{ needs.test.outputs.package_name }}.${{ needs.test.outputs.package_version }} is built and published to test pypi

            ## Change Details
            ${{ github.event.head_commit.message }}

            For more information, please check change history at https://${{ needs.test.outputs.repo_owner }}.github.io/${{ needs.test.outputs.repo_name }}/${{ needs.test.outputs.package_version }}/history

            ## Package Download
            The pacakge is available at: https://test.pypi.org/project/${{ needs.test.outputs.package_name }}/

      - name: build failure notification via email
        if: ${{ steps.check.outputs.status == 'failure' }}
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: ${{ secrets.BUILD_NOTIFY_MAIL_SERVER }}
          server_port: ${{ secrets.BUILD_NOTIFY_MAIL_PORT }}
          username: ${{ secrets.BUILD_NOTIFY_MAIL_FROM }}
          password: ${{ secrets.BUILD_NOTIFY_MAIL_PASSWORD }}
          from: build-bot
          to: ${{ secrets.BUILD_NOTIFY_MAIL_RCPT }}
          subject: ${{ needs.test.outputs.package_name }}.${{ needs.test.outputs.package_version}} build failure
          convert_markdown: true
          html_body: |
            ## Change Details
            ${{ github.event.head_commit.message }}

            ## View Log
            https://github.com/${{ needs.test.outputs.repo_owner }}/${{ needs.test.outputs.repo_name }}/actions
```

这是一个名为dev build CI的作业，它将在任一分支发生提交和pull request时触发。它包含三个作业，即test(执行单元测试)、publish_dev_build(构建并发布开发版本到test_pypi)和notification(在构建成功或失败时发送邮件通知)。三者之间有依赖关系，如果test作业失败，publish_dev_build会取消；但是无论test/publish_dev_build作业是否成功，notification作业都会执行，并根据前两个作业的状态发送邮件通知。

这是一个比较简单的作业，也涉及了我们在CI中需要做的几乎所有事情。在代码中我们加入了较多的注释，建议读者结合下面的讲解，仔细阅读代码。
### 定义触发条件
第4行到第14行配置了工作流的触发条件。触发条件一节由关键字**'on'**引起。在它的下一层，我们可以定义多个触发事件，并为每个触发事件，指定类型和过滤器。一个完整的触发条件配置如下：

```yaml
on:
    push:
        branches: 
          - '*'
        tags:
          - v*
    label:
        branches:
            - main
        types:
            - created
    schedule:
        - cron: '30 5 * * 1,3'
```
在上面的示例中，'push', 'label', 'tags'和'schedule'都是事件关键字。可用的事件关键字可参见[触发工作流的事件](https://docs.github.com/zh/actions/using-workflows/events-that-trigger-workflows)。

在事件的下一级，是定义活动类型和筛选器的地方。不是所有的事件都有活动类型，即使有，它们的活动类型也很可能不一样。比如，`push`事件就没有活动类型，而`label`事件有`created`, `edited`和`deleted`三种活动类型，而`issues`事件的活动类型则是`opened`和`labeled`等。要想知道事件有哪些活动类型，可以参考[触发工作流的事件](https://docs.github.com/zh/actions/using-workflows/events-that-trigger-workflows)。

筛选器有branches和tags两种，分别用于指定分支和标签。从上面的示例可以看出，筛选器的值支持glob模式，即你可以使用*,**, +, ?和!等通配符。除了示例中的正向匹配外，还可以使用branches-ignore或者tags-ignore来反向匹配。

上面的示例还展示了一种特殊的事件，即 'schedule' 事件。这将导致工作流周期性地运行。这可以用来运行一些安全性扫描、依赖升级扫描等工作。

### 定义作业集
接下来工作流声明了三个作业，即test, publish_dev_build和notification。作业定义一节由关键字**'jobs'**引起。在它的下一层，我们可以定义多个作业，并为每个作业，指定运行环境和运行步骤。

每个作业都有自己的id和名字。在上述例子中，test, publish_dev_build和notification都是作业id。作业id是必须的，但是作业名字是可选的。如果没有指定作业名字，那么作业名字将默认为作业id。作业名字可以用来在GitHub Actions的界面上显示作业的名称。

在作业publish_dev_build中，我们通过关键字`needs`来定义了它对作业`test`的依赖。我们在第114行还看到，作业还可以依赖到一组作业。当我们指定作业依赖时，要注意只能使用作业的id，而不是作业的名字。

接下来我们为作业定义执行环境。执行环境是通过关键字 'runs-on' 来定义的。有些任务只需要在一台机器上执行就可以了，比如构建和发布；有些任务则需要在所有的机器上、并以多个python运行时来运行。

比如，publish_dev_build作业只在ubuntu_latest和python 3.9这个组合上运行。我们是通过第78行和第83行来指定的。但对测试任务，我们希望它在所有机器上都运行，并且还要运行在不同的python版本上。为了表达简洁起见，github actions引入了矩阵的概念。

我们通过strategy.matrix来定义测试矩阵。在示例第20~23行定义的矩阵中，我们定义了python版本和操作系统列表。这个定义随后就被使用了，在第24行，我们通过{{matrix.os}}来引用了其中的操作系统定义。第22行的python-versions是一个特殊的关键字，它用来指示我们要使用的python版本。如果我们的开发语言不是python，这里的指定将没有意义。

接下来我们需要为作业定义具体执行哪些任务，它们被归类在步骤集(steps)中。步骤集是一个包含多个步骤的列表。而每一个步骤，要么是一个shell命令（或者一组shell命令），要么是一个action。如果要运行shell命令，我们使用下面的语法：
```yaml
- name: <step name>
  run: <shell command>
```
如果要运行一组shell命令，我们使用:
```yaml
- name: <step name>
  run: |
    <shell command 1>
    <shell command 2>
    ...
```
注意上述两组语法的不同之处，不能混淆。

至于action，我们前面已经讲过了，它是用于 GitHub Actions 平台的自定义应用程序。您可以自己编写action，也可以在Github的应用市场上查找他人开发的应用。

每一个步骤都可以指定python运行时。我们在第48行看到，这里`{{ matrix.python-versions }}`使用的是矩阵中定义的python版本。而在第84行，我们则直接指定了一个python的版本。这里还要注意，版本号是一个字符串，q我们可以使用`'3.10'`，但不能使用`3.10`，后者将会被yaml解析为`3.1`，从而出现找不到python版本的问题。

最后，我们介绍一下job运行时的条件控制。我们已经介绍过了job之间的依赖关系，这可以算作是一种条件。还有一种情况，比如示例中的notification作业，我们要求它只能在前两个作业都完成后才运行，但无论成功与否，都要运行，但会根据前面作业的状态，发出不同内容的通知邮件，此时，我们就需要引入`if`条件控制。

`if`条件控制可以作用于作业作用域（如第116行所示），也可以作用于步骤作用域（如第123行所示）。在作业作用域中，我们可以使用`success()`、`failure()`、`cancelled()`、`always()`等函数来指定在何种情况下才运行本作业。在步骤作用域中，我们则可以进行简单的条件判断，来指标本步骤是否运行。

在进行条件判断时，我们必然需要使用变量。现在，我们需要全面地介绍一下在工作流中变量的使用。通过变量，结合各种控制条件，我们才能实现一些高级的技巧。
Github中的变量分为两种，一种是系统变量，一种是作业变量。系统变量是Github平台提供的，作业变量是我们自己定义的。无论那一种变量，我们都通过`${{ }}`来引用。

系统变量按级别可以定义在组织、存储库或者环境上。比如`secrets`就定义在存储库级别上，我们可以通过`${{ secrets.BUILD_NOTIFY_MAIL_RCPT }}`来访问它的值，这需要我们在存储库里事先定义`BUILD_NOTIFY_MAIL_RCPT`这个变量。Github提供了一些默认变量，比如`GITHUB_REPOSITORY`（你在第59行，声明变量那一节可以看到它的使用）等。

作业变量的使用比较特殊，我们看看下面的例子：
```yaml
  notification:
    needs: [test,publish_dev_build]
    steps:
      - name: build success notification via email
        if: ${{ steps.check.outputs.status == 'success' }}
        uses: dawidd6/action-send-mail@v3
        with:
          subject: ${{ needs.test.outputs.package_name }}.
```
例子中，我们通过${{ needs.test.outputs.package_name }}来引用在第24行声明的`package_name`变量。变量是通过`{job_id}.outputs.{variable}`来引用的，这并没有什么奇怪的地方。但是要注意它还有一个`needs`作用域。这表明，如果我们使用变量的地方，其所属的作业如果没有声明依赖到`test`作业，那么这个变量是无法被引用的。

示例中没有展示环境变量的用法，这里我们给一个示例，请读者结合注释自行研究：
```
env:
  # 声明了一个全局上下文的环境变量
  DAY_OF_WEEK: Monday

jobs:
  greeting_job:
    runs-on: ubuntu-latest
    env:
      # 声明了一个作业上下文的环境变量
      Greeting: Hello
    steps:
      - name: "Say Hello Mona it's Monday"
        # 使用时我们在变量前加一个`env.`的约束
        if: ${{ env.DAY_OF_WEEK == 'Monday' }}
        # 当使用的环境变量是在作业内声明时，我们可以省略`env.`的约束
        run: echo "$Greeting $First_Name. Today is $DAY_OF_WEEK!"
        env:
          # 声明了步骤上下文的环境变量
          First_Name: Mona
```
### 连接其它服务
