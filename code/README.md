# 示例代码使用说明

## 运行环境

请在Ubuntu 20.04及以上系统下运行。Python版本为3.8。建议通过以下命令创建虚拟环境：

```bash
conda create -n pbp python=3.8
conda activate pbp
```

然后安装poetry:

```bash
pip install poetry
```

再安装依赖：

```bash
# 进入code所在的目录。该目录下应该存在pyproject.toml文件
poetry install
```

此外，您还需要在本机安装docker。以及安装postgres数据库。推荐使用docker启动postgres数据库。

```bash
sudo docker run -d --name pbp-postgres -p5432:5432 -e POSTGRES_PASSWORD=123456 -e POSTGRES_USER=zillionare -e POSTGRES_DB=pbp postgres
```

这将创建一个名为pbp-postgres的容器。数据库名为pbp，用户名为zillionare，密码为123456，监听在端口5432，可以从宿主机本机访问这个端口。

在运行每章的示例前，请重建该数据库容器。删除容器的命令是：

```bash
sudo docker rm -f pbp-postgres
```

然后再执行命令：

```bash
sudo docker run -d --name pbp-postgres -p5432:5432 -e POSTGRES_PASSWORD=123456 -e POSTGRES_USER=zillionare -e POSTGRES_DB=pbp postgres
```

来重建数据库容器。

## 示例代码目录

示例代码按章节组织，比如第5章示例代码在`chap05`目录下。各个目录中又有README.md文件提供帮助。在运行这些示例前，都需要切换到新建的bpp环境下：

```bash
conda activate pbp
```

然后请进入`code`所在的目录，按各章节的README.md的说明运行程序（或者单元测试）。

## 错误报告及修订
示例代码错误报告及修订请见：

https://github.com/zillionare/best-practice-python
