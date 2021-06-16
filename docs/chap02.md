尽管条条道路通罗马，但毕竟有的路走得更平稳更快捷，更不要说有的人就住在罗马。构建一个好用的开发环境，你的开发之路当然会走得更平稳快捷。因此，我们的旅程从这里开始。

本章首先介绍Python开发的操作系统环境，然后介绍一些流行的集成IDE，并对他们的特点进行了比较，供读者选择。
# 选择哪一种操作系统？
看上去操作系统是一个与编程语言无关的话题，特别是象Python这样的开发语言，它编写的程序几乎可以运行在任何一种操作系统上。但是，这里也有一些微妙的影响：

1. 尽管Python可以用来开发任何一种应用程序，但用于后台服务程序开发（相对于桌面应用而言）则更为常见。对于后台服务程序，最理想的操作系统当然是Linux。因此，毋庸置疑，在这种情况下，您最好从一开始就在Linux下进行开发，避免出现您使用的库存在兼容性问题。

2. 尽管Python编写的程序几乎可以运行在任何一种操作系统上，但是毕竟操作系统之间是有区别的。尽管一些重要的程序库往往都会兼容多数操作系统，但仍然有可能会有小的区别，或者在版本发布时间上有所不同。在这一点上，很多程序和开源程序库往往都会优先考虑Linux操作系统，它们在这些操作系统上的测试也似乎更为充分。如果您使用了一些小众的开源程序库的话，您更得有它们只能在Linux下运行的准备。

3. 一些命令行工具似乎也更适合Linux。比如可能您的工程中使用了make来进行构建管理（假如您使用著名的文档构建工具Sphinx来撰写文档的话，就会使用make)；或者如果您使用了CI/CD，它们可能依赖一些Linux的shell命令，毕竟Linux的Shell命令要比Windows强大很多。

基于上述原因，我们推荐使用Linux作为您的Python开发环境。但是，您很可能并不会喜欢这个建议，因为您的笔记本很可能是MacOS或者Windows。

好消息是，MacOS和Linux都是所谓的"类Unix"操作系统，它们之间有极高的相似度。所以，如果您的电脑是MacOS操作系统，您大可不必安装另一个Linux。如果您的电脑是Windows操作系统，我们在下面也提供了三种方案，可以让您的机器也能运行一个Linux操作系统用于开发。

当然，如果您并不打算进行服务器开发，那么使用Windows，在绝大多数情况下也是可以的。
# Windows下的虚拟Linux环境
在Windows下有三种启用Linux虚拟机的方式。其中之一是Windows的原生方案，即使用Windows Subsystem for Linux(以下简称WSL)，其它两种方案则分别是Docker和虚拟机方案。
## WSL方案
WSL是Windows 10的一个新功能。通过WSL，在Windows之上，运行了一个GNU/Linux环境。在这个环境里，绝大多数Linux命令行工具和应用都可以运行，而不需要设置双系统，或者承担虚拟机带来的额外代价。

当前有两个版本可用，wsl v1和wsl v2, 我个人更推荐使用wsl v1。WSL v2的体验更象虚拟机，因此与windows集成性反而更差一些。v1用于Python开发是没有任何问题的；如果用于nodejs或者前端开发，可能要担心性能问题（因为wsl v1的文件系统性能不太好，而js开发文件特别多，小文件又多）。

### 安装WSL
首先要启用“适用于Linux的Windows子系统”功能：

![](http://images.jieyu.ai/images/2020-05/20200503185200[1].png)

设置后，需要重启一次电脑。接下来从应用商店搜索安装Ubuntu安装就可以了。
![](http://images.jieyu.ai/images/2020-05/20200503191417[1].png)


现在在搜索栏输入ubuntu，就可以进入一个命令行窗口。由于是第一次运行，这里会提示我们输入用户名和口令。这样WSL就安装成功了。现在，可以在命令行中输入wsl来启动。

下面我们对WSL进行一些定制，使之更象一台常驻运行的Linux虚拟机。

首先，WSL 1.0缺少一些必要的Linux系统文件，因此它不能象普通的Linux那样，拥有自己的开机任务。但是我们可以在Windows下通过`wsl`来运行这些开机任务，比如：
```
wsl sudo /etc/init.d/ssh start
```
这样会提示:
```
 * Starting OpenBSD Secure Shell server sshd                                       [ OK ]
 ```
表明服务启动成功。因此，我们只要写一个脚本，让它在windows启动时自动运行，并且执行上述命令，就能实现wsl的开机自启动，并且启动常用的后台服务。

我们需要写三个脚本，一个start.vbs，一个control.bat和一个commands.txt。启动wsl之后，需要在wsl中运行的后台服务放在commands.txt文件中：
```text
/etc/init.d/cron
/etc/init.d/ssh
```

control.bat则用以启动wsl所依赖的核心服务，以及启动wsl并执行commands.txt中的命令：
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
最后，我们通过start.vbs这个脚本来执行control.bat：
``` vb
' 脚本来源于 https://github.com/troytse/wsl-autostart/
' Start services
Set UAC = CreateObject("Shell.Application")
command = "/c """ + CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) + "\control.bat"" start"
UAC.ShellExecute "C:\Windows\System32\cmd.exe", command, "", "runas", 0
Set UAC = Nothing
```

那么谁在开机时调用start.vbs呢？我们可以使用任务计划程序：

![](http://images.jieyu.ai/images/202106/20210616215338.png)

![](http://images.jieyu.ai/images/202106/20210616215237.png)


首先是要设置ssh服务。我们设置ssh服务的目标是为了开机自启wsl子系统（无窗口模式），这样我们可以随时以ssh方式连接进去，就好象我们有了一台Linux服务器一样。也许你安装的版本已经直接设置好了ssh server，所以这里我们略过。如果没有，具体设置可参考Ubuntu的ssh设置。
## Docker方案
## 虚拟机方案
# 集成开发环境（IDE）
## VSCodevsPycharm:使用哪一个IDE？
## VSCode及扩展
# 其他开发环境
## Jupyter Notebook
## Spyder
