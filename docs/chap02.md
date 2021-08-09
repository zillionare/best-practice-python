尽管条条道路通罗马，但毕竟有的路走得更平稳更快捷，更不要说有的人甚至就住在罗马。构建一个好用的开发环境，你的开发之路当然会走得更平稳快捷。因此，我们的旅程从这里开始。

本章首先介绍Python开发的操作系统环境，然后介绍一些流行的集成IDE，并对他们的特点进行了比较，供读者选择。
# 选择哪一种操作系统？
看上去操作系统是一个与编程语言无关的话题，特别是象Python这样的开发语言，它编写的程序几乎可以运行在任何一种操作系统上。但是，仍然有一些微妙的差异我们需要考虑。首先，Python更适合于数据分析、人工智能和后台开发，而不是用于开发桌面和移动端应用。这些应用，无论是大数据分析和人工智能，还是后台开发，往往都部署在Linux服务器环境下。此外，这些应用所依赖的生态，也往往构建在Linux下（比如大数据平台和分布式计算平台）。一些重要的的程序库，尽管往往最终都会兼容多个操作系统，但由于操作系统之间的差异，它们在不同操作系统下的新版本发布计划往往是不一样的。一些开源的程序和类库往往会优先考虑Linux操作系统，它们在Linux上的测试似乎也更充分。

我们可以举出很多这样的例子，这里我们仅以容器为例。尽管你可以在Windows机器上安装桌面版的Docker，然后运行一些容器，Windows下Docker对资源的利用远不如在Linux下来得充分 -- 它们是在Docker服务启动时就从系统中划走的，无论当下是否有容器在运行，这此资源都无法被其它Windows程序使用。从根本上讲，这种差异是Windows不能提供容器级别的资源隔离造成的。

在本书的后面，我们将讲到CI/CD，这些都需要使用容器技术。那时，您将深切体会到使用Linux的种种方便。

基于上述原因，我们推荐使用Linux作为您的Python开发环境。本书中提到的工具和示例，也都默认地使用Linux作为运行环境。

但是，您很可能并不会喜欢这个建议，因为您的电脑很可能是MacOS或者Windows。

好消息是，MacOS和Linux都是所谓的"类Unix"操作系统，它们之间有极高的相似度。所以，如果您的电脑是MacOS操作系统，您大可不必安装另一个Linux。如果您的电脑是Windows操作系统，我们在下面也提供了三种方案，可以让您的机器也能运行一个虚拟的Linux操作系统用于开发。

# Windows下的虚拟Linux环境
在Windows下有三种构建Linux虚拟环境的方式。其中之一是Windows的原生方案，即使用Windows Subsystem for Linux(以下简称WSL)，其它两种方案则分别是Docker和虚拟机方案。
## WSL方案
WSL是Windows 10的一个新功能。通过WSL，在Windows之上，运行了一个GNU/Linux环境。在这个环境里，绝大多数Linux命令行工具和应用都可以运行，而不需要设置双系统，或者承担虚拟机带来的额外代价。

当前有两个版本可用，wsl v1和wsl v2, 我个人更推荐使用wsl v1。WSL v2的体验更象虚拟机，因此与windows集成性反而更差一些。

### 安装WSL
首先要启用“适用于Linux的Windows子系统”功能：

![](http://images.jieyu.ai/images/2020-05/20200503185200[1].png)

设置后，需要重启一次电脑。接下来从Windows应用商店搜索安装一个Linux发行版，这里的示例中我们使用ubuntu:
![](http://images.jieyu.ai/images/2020-05/20200503191417[1].png)


现在，在搜索栏输入ubuntu，就会打开ubuntu shell。由于是第一次运行，此时会提示我们输入用户名和口令。这样WSL就安装成功了。此后，也可以从搜索框输入`wsl`来启动这个系统。

### 定制WSL
下面我们对WSL 1.0进行一些定制，使之更象一台常驻运行的Linux虚拟机。比如，我们可能希望这个WSL虚拟机随windows自动启动。当WSL启动后，它能自动运行一个ssh服务，这样我们就可以随时连接使用这台WSL虚拟机。注意WSL 1.0虚拟机跟真正的虚拟机有细微的差别，主要就是它没有自己的init.d系统，因此没法运行系统服务（即开机自动运行的后台程序）。但是，我们可以通过一些简单的定制来实现这一场景。

我们需要写三个脚本，一个start.vbs，一个control.bat和一个commands.txt，并且增加一个开机自动执行的计划任务。当Windows开机后，这个计划任务自动执行，调用start.vbs来执行control.bat, 而control.bat则会启动WSL（及其依赖的Windows服务）,并在WSL环境下执行定义在commands.txt中的那些命令--即要在WSL中运行的服务，比如ssh server。

首先，我们在commands.txt文件定义要在WSL中运行的后台服务：
```text
/etc/init.d/cron
/etc/init.d/ssh
```
然后，我们编写一个批处理脚本（即control.bat)，用以启动WSL,并执行上述命令：
```bat
REM 脚本来源于https://github.com/troytse/wsl-autostart/
@echo off
REM Goto the detect section.
goto lxssDetect

:lxssRestart
    REM ReStart the LxssManager service
    net stop LxssManager

:lxssStart
    REM Start the LxssManager service
    net start LxssManager

:lxssDetect
    REM Detect the LxssManager service status
    for /f "skip=3 tokens=4" %%i in ('sc query LxssManager') do set "state=%%i" &goto lxssStatus

:lxssStatus
    REM If the LxssManager service is stopped, start it.
    if /i "%state%"=="STOPPED" (goto lxssStart)
    REM If the LxssManager service is starting, wait for it to finish start.
    if /i "%state%"=="STARTING" (goto lxssDetect)
    REM If the LxssManager service is running, start the linux service.
    if /i "%state%"=="RUNNING" (goto next)
    REM If the LxssManager service is stopping, nothing to do.
    if /i "%state%"=="STOPPING" (goto end)

:next
    REM Check the LxssManager service is started correctly.
    wsl echo OK >nul 2>nul
    if not %errorlevel% == 0 (goto lxssRestart)

    REM Start services in the WSL
    REM Define the service commands in commands.txt.
    for /f %%i in (%~dp0commands.txt) do (wsl sudo %%i %*)

:end
```
然后我们编写一个start.vbs脚本，来执行control.bat：
``` vb
' 脚本来源于 https://github.com/troytse/wsl-autostart/
' Start services
Set UAC = CreateObject("Shell.Application")
command = "/c """ + CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) + "\control.bat"" start"
UAC.ShellExecute "C:\Windows\System32\cmd.exe", command, "", "runas", 0
Set UAC = Nothing
```

最后，我们向计划任务程序中添加一个新的开机启动任务：

![](http://images.jieyu.ai/images/202106/20210616215338.png)

![](http://images.jieyu.ai/images/202106/20210616215237.png)

需要说明的是，通过Windows应用商店安装的ubuntu子系统，它应该已经安装好了ssh-server，我们上述操作中所做的事，只不过是让它随WSL一起启动而已。但是，如果您发现您的WSL中并没有安装ssh-server，您也可以自行安装。毕竟，这就是一台Linux服务器，您可以在上面安装几乎所有的可以运行在标准Linux上的任何软件。

通过应用上述方案，您就在Windows启动之后，在一台机器上拥有了同时运行的两个操作系统。关键在于，如果您当前并不使用WSL的话，它只占用很少的CPU和内存资源（仅限WSL 1.0）。这是其它虚拟化方案所无法比拟的。

在本书写作时，WSL已经有了支持图形化界面的预览版，称之为[wslg](https://github.com/microsoft/wslg)。未来这个版本将合并到WSL中，随Windows一起发行的正式版发行。下图是wslg图形化界面的一个效果图：

![](http://images.jieyu.ai/images/202108WSLg_IntegratedDesktop.png)


## Docker方案
WSL的出现要比Docker晚。因此，可能您的Windows不支持安装WSL，这种情况下，您可以尝试安装桌面版的Docker,然后通过Docker来运行一个Linux虚拟机。

安装Docker可以从其[官方网站](https://desktop.docker.com/win/stable/amd64/Docker%20Desktop%20Installer.exe)下载，安装完成后，首次运行手动启动。可以从搜索框中搜索"Docker"，然后选择"Docker Desktop"来启动，见下图：

![](http://images.jieyu.ai/images/202108docker-app-search.png)

当Docker启动后，就会在系统托盘区显示一个通知图标：

![](http://images.jieyu.ai/images/202108whale-icon-systray.png)

上图中第三个，鲸鱼图标，即是Docker正在运行的标志。点击它可以进入管理界面。首次运行时需要做一些设置，可以参考官方文档。

在Windows上运行Docker，由于操作系统异构的原因，首先需要启用Hyper-V虚拟机，然后将Docker安装到这个虚拟机中。这就是为什么在Windows下安装运行Docker，无论当前是否有容器在运行，系统资源也被静态分配切割的原因。但是大概从2020年3月起，Docker开始支持运行基于WSL2的桌面版。基于WSL2的桌面版Docker，Docker后台服务启动更快，资源也仅在需要时才进行分配，因此在资源调度上更加灵活高效。

## 虚拟机方案

也有可能您的机器既不支持安装WSL，也不支持安装Docker。这种情况下，您可以通过安装VirtualBox等虚拟机来运行Linux。

## 小结
我们介绍了三种在Windows上构建Linux虚拟环境的方案。只要有可能，您首先应该安装的是WSL。WSL可以在运行在几乎所有的Windows发行版上，包括Win10 Home。

如果您的机器不支持安装WSL，也可以考虑安装Docker。即使您的机器支持WSL，出于练习CI/CD的考虑，也可以安装Docker，以便体验容器化构建和部署。当然，这需要您的机器有更强劲的CPU和内存。

对于较早的机型，无法升级到较新版本的Windows时，可以考虑使用虚拟机，比如免费版的VirtualBox。
# 集成开发环境（IDE）
作为一种脚本语言，Python可以无须编译即可运行，因此，几乎所有的文本编辑器都可以作为Python开发工具。然而，要进行真正严肃的开发，要在开发进度、开发质量之间取得最佳平衡，就需要一个更专业的工具。

集成开发环境（IDE）是一种提高开发效率的工具，它可以让开发者在编写代码时，得到各种代码提示，更早发现语法错误，还可以直接在编辑器中进行调试，而不需要在命令行中运行调试命令。

Pycharm和Vscode是进行Python应用程序开发的两个首选工具。对于从事数据分析和人工智能领域的开发者，还可以考虑Jupyter Notebook和Anaconda的Spyder。

## VSCode vs Pycharm:使用哪一个IDE？
Pycharm是老牌的Python开发IDE，Visual Studio Code(以下简称VSCode)则是近两年的后起之秀。VSCode完全免费，Pycharm则提供了社区版和专业版两个版本，专业版本功能更强大，但需要付费。下表简要说明了两个IDE的最重要的差异：

| 特性      | Pycharm  | VSCode        | 说明                                                                           |
| ------- | -------- | ------------- | ---------------------------------------------------------------------------- |
| 远程开发    | 仅专业版支持   | 支持            | Pycharm文件编辑在本地，调试前将文件同步到远程机器上进行调试；VSCode通过文件共享协议，直接在远程机器上编辑和调试               |
| 代码冲突归并  | 支持三路归并   | 不支持，目前也没有插件支持 |                                                                              |
| 数据查看    | 支持       | 不支持           | PyCharm中可以图形化界面查看数据库和来自DataFrame的数据；VSCode需要插件支持，但功能较弱。一般通过第三方数据库工具查行数据查看和管理 |
| 启动速度    | 慢        | 很快            | VSCode启动速度十分优异，这也使得它除了用作开发外，还可以用作文档撰写、记事等功能。                                 |
| 多开发语言支持 | Python为主 | 支持多种开发语言      | VSCode可以支持很多种语言的开发，因此特别适合专业开发者                                               |

还有一些小的差异，比如VSCode很多功能是通过插件实现的，每个插件都有自己的日志输出窗口。在你使用VSCode时，当某个功能出错时，有可能只是某个插件的错误。这个错误可能只会静悄悄地在插件的日志窗口中输出，而不是输出在你熟悉的那些界面窗口中。这可能会让初学者感到困惑。而在Pycharm中，这些窗口、提示界面的安排似乎更容易理解。

总之，Pycharm是一个开箱即用的IDE，而VSCode安装之后，在正式开发之前，还得安装一系列插件，这可能要花费你一定的时间去选择比较、配置和学习。当然，如果你打算长期从事开发工作，那么在VSCode上投入一些时间则是值得的。VSCode是一个免费产品，它的许可证允许您使用VSCode来进行任何商业开发。因此，无论您是个人开发者，还是受雇于某个组织，您都可以使用它。

由于这样的原因，也由于Pycharm简单易上手，所以我们这里略过对Pycharm的使用说明，重点讲述如何配置VSCode开发环境。

## VSCode及扩展
VSCode是一个支持多语言编辑开发的平台，它本身只提供了编辑器、代码管理（Git）、扩展管理等基础功能。具体到某个语言的开发，则是通过加载该语言的扩展来完成的。因此，安装VSCode之后，往往还需要配置一系列的扩展。

安装好VSCode之后，在侧边栏上就会出现如下图所示工具栏：

![](http://images.jieyu.ai/images/20210820210809145433.png)

被圆形框框住的图标对应着扩展管理。上部的矩形框可以用来搜索某个扩展，找到对应的扩展并点击，就可以在右边的窗口中看到该扩展的详细信息，如下图所示：

![](http://images.jieyu.ai/images/20210820210809145930.png)

在这个详细信息页，提供了安装按钮。

VSCode扩展管理除了搜索之外，还提供了过滤、排序等功能，读者可以自行探索。如果读者要在多个开发环境下使用VSCode，可能希望这些扩展在不同的环境下都能使用，针对这个需求，VSCode还提供了扩展同步机制。在上图中，在扩展详情页的"Uninstall"按键右侧，有一个同步图标，点击后，VSCode会自动将该扩展同步到其他环境。

下面，我们将讨论一些最常用、最重要的VSCode扩展。在使用这些扩展武装VSCode之后，您的开发效率将大大提高。
### Python扩展

要在VSCode中开发Python应用程序，就需要安装Python扩展。该扩展如前图所示。

Python扩展由微软开发，目前有超过3900万次下载。它提供了IntelliSense、代码检查、调试、导航、格式化、重构和单元测试功能。此外，它还提供了Jupyter Notebook集成环境。

随Python扩展一起安装的，还有Pylane, Python Test Explorer for Visual Studio Code, Jupyter等扩展

Pylance是微软基于自身收购的Pyright静态检查工具，开发的具有IntelliSense的Languange Server。它提供语法高亮、代码自动完成、语法检查、参数建议等功能。

尽管Pylance提供了这些功能，但在使用中，我们更多地把Pylance看成是一个language server，上述功能中的语法检查、代码提示和自动完成等功能，还是应该通过更专业的专门扩展（或者第三方服务）来完成。在这里，Pylance可以作为这些功能的一个扩展平台。

Test Explorer的主要作用是发现和搜集项目中定义的单元测试用例，构建TestSuite，提供测试执行入口，并在测试完成之后，报告测试执行情况。

Jupyter是一个允许你在VSCode中阅读、开发notebook的扩展。与单独安装的Jupyter notebook相比，它能提供更强大的代码提示、变量查看和数据查看。此外，调试notebook一直是个比较麻烦的事。在VSCode中，你可以通过将notebook导出为.py文件的方式来对其进行调试，待调试完成，还可以再将文件导回为notebook。可以说，较好地解决了notebook的调试问题。

在Python扩展安装完成之后，就可以进行Python开发了。在开发之前，需要为工程选择Python解释器。可以从命令面板中输入Python: Select Interpreter来完成，也可以点击状态栏中的选择图标，如下图所示：

![](http://images.jieyu.ai/images/20210820210806163607.png)

### Remote - SSH

这是一个非常有用的扩展，是微软官方开发的扩展之一。它可以让你在VSCode中直接打开远程机上的文件夹，编辑并调试运行。如果您使用过Pycharm等IDE，就会知道，尽管这些IDE也支持远程开发，但它们是在本地创建文件，调试运行前先要上传同步到远程机器上。频繁同步不仅降低了效率，而且也常常出现未能同步，导致行为与预期不一致，浪费时间查找问题的情况。这也是也是VSCode优于Pycharm的一个重要特性。

![](http://images.jieyu.ai/images/20210820210809145039.png)

安装好这个扩展之后，在侧边栏会出现一个远程连接图标。同时，如果当前已经连接到远程机器，则在状态栏最左侧，会出现该连接的概要信息。

### 代码管理类扩展

VSCode只提供了简单的Git功能，在实际使用中，我们常常还需要更多的功能。这些功能包括：
1. 代码分支管理、提交历史等
2. 代码提交时，遵照指定的格式规范编辑commit message
3. gitignore管理

![](http://images.jieyu.ai/images/20210820210809155757.png)

Gitlens的功能十分强大，是团队开发中常用的一个扩展。它的功能包括：
1. 在文件修改历史中快速导航
2. 在代码行中提示blame信息，如下图所示：
![](http://images.jieyu.ai/images/202108hovers-current-line.png)
3. gutter change，如下图所示：
![](http://images.jieyu.ai/images/20210820210809160826.png)
gutter change是指如上图所示，在编辑区行号指示右侧，通过一个线条来指示当前区域存在变更，当你点击这个线条时，会弹出一个窗口，显示当前区域的变更历史，并且允许你回滚变更、或者提交变更。

如果你在编辑文件之前没有做好规划，引入了本应该隶属于多个提交的修改，gutter change是最好的补救方案。它允许你逐块、而不是按文件提交修改。因此，你可以将一个文件里的不同块分几次进行提交。
4. 在侧边栏提供了丰富的工具条，如下图所示：
![](http://images.jieyu.ai/images/202108views-layout-gitlens.png)
通过这些工具条，你不再需要记忆大量的git命令，并且这些命令的结果也以可视化的方式展示，更加高效。在这些工具栏里，提供了提交视图、仓库视图、分支视图、文件历史视图、标签视图等。

编辑提交信息的扩展




# 其他开发环境
## Jupyter Notebook
## Spyder
