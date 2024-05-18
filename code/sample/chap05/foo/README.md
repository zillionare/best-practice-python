本项目对应《Python高效编程实践指南》第5章。

## 运行环境准备

本程序在Ubuntu 20.04及Python 3.11上运行通过。

要运行本程序，需要先安装postgresql数据库，并创建用户zillionare，密码为123456，以及名为bpp的数据库。

推荐使用docker容器：

```
sudo docker run -d --name ppw-postgres -p5432:5432 -e POSTGRES_PASSWORD=123456 -e POSTGRES_USER=zillionare -e POSTGRES_DB=bpp postgres
```

你需要为运行本项目创建专门的虚拟环境（以免破坏其它项目的运行环境），再执行以下命令安装gino:

```
pip install gino==1.0.1
```

## 运行和结果

执行以下命令：

```bash
python code/sample/chap05/foo/foo/bar/data.py
```

输出结果为：

```
zillionare 2024-01-01
```
