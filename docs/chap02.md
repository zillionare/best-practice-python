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
WSL的出现要比Docker晚。因此，可能您的Windows不支持安装WSL，这种情况下，您可以尝试安装
## 虚拟机方案
# 集成开发环境（IDE）
## VSCodevsPycharm:使用哪一个IDE？
## VSCode及扩展
# 其他开发环境
## Jupyter Notebook
## Spyder
