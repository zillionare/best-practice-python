## Nuitka打包
在chap11目录下有一个greetings.py的文件，对应第11章210页。

## 基于云的应用部署

在chap11/docker/sample目录下，演示了如何构建基于docker的Python应用分发项目。

与其它项目一样，该项目仍然通过ppw来生成，具有与其它项目基本一样的目录结构。但有所不同的是，在根目录（docker/sample）下，还存在一个名为docker的目录，这里包含了build.sh, dockerfile和一个名为rootfs的目录。

rootfs存放了镜像的根文件系统，这个目录下的内容会被复制到docker容器中。dockerfile用来指导如何构建这个镜像。build.sh则是一个调用docker build的脚本。它主要完成Python项目的构建和打包，为镜像设置版本等工作。

要实现镜像构建，请进入chap11/docker/sample/docker目录，然后运行：

```bash
./build.sh
```

!!! 注意：
    运行此命令要求:
    1. 本机安装有docker，并且可以以sudo命令运行docker命令。
    2. 当前Python运行环境下安装有poetry。
    3. 请使用Ubuntu 20.04 LTS或以上版本。

运行完成之后，你可以通过以下命令检查容器是否正在运行：

```bash
sudo docker ps -a |grep sample
```

此时应该列出一个名为sample的容器，监听在7080端口。在浏览器中输入http://localhost:7080/（可替换成机器的IP），应该能看到一个勇气号的图片。
