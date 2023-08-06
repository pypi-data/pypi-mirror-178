#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/9/27 9:29
# @Author  : xgy
# @Site    : 
# @File    : model_cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import os
import sys

import click
from csp.command.cli import csptools


# 一级命令 CSPtools topic
@csptools.group("topic")
def topic():
    """
    主题命令，包括主题信息列表、主题下载等子命令

    \b
    csp topic 'commands' -h 获取子命令使用帮助
    """


## 模型信息列表展示
@topic.command()
@click.option("-n", "--name", type=click.STRING, help="模型名称:版本", default=None)
@click.option("-c", "--classify", type=click.STRING, help="分类名称，支持模糊查找", default=None, show_default=True)
@click.option("-m", "--more", type=click.BOOL, help="是否以 linux more 命令风格查看结果", default=True, show_default=True)
def list(name, classify, more):
    """
    主题模型镜像列表命令

    \b
    使用示例：csp topic list or csp topic list -c "分类名称" -n "镜像资源库:镜像tag"
    """
    try:
        from csp.topic.topic_server import topic_list
        res = topic_list(name, classify, show=more)
        if more:
            os.makedirs("/tmp", exist_ok=True)
            if sys.platform == "win32":
                code = "GBK"
            else:
                code = "utf-8"

            with open("/tmp/topic_l.txt", "w", encoding=code) as fw:
                fw.write(res)
            txt_abs = os.path.abspath("/tmp/topic_l.txt")

            os.system("more " + txt_abs)

    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


@topic.command()
@click.option("-n", "--name", type=click.STRING, help="模型名称:版本", prompt="模型名称:版本", required=True)
@click.option("-t", "--model_type", type=click.Choice(["0", "1"]), help="镜像类型，0-内部 1-外部", prompt="镜像类型，0-内部 1-外部", required=True)
@click.option("-d", "--dataset", type=click.STRING, help="模型关联数据集名称", prompt="模型关联数据集名称", required=True)
def upload(model_type, name, dataset):
    """
    主题模型镜像上传命令

    \b
    使用示例：csp topic upload -n "镜像资源库:镜像tag" -t 0 -d "关联数据集名称"
    """
    try:
        from csp.topic.topic_server import topic_upload
        topic_upload(int(model_type), name, dataset)
    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


@topic.command()
@click.option("-n", "--name", type=click.STRING, help="模型名称:版本", prompt="模型名称:版本", required=True)
def download(name):
    """
    主题模型镜像下载命令

    \b
    使用示例：csp topic download -n "镜像资源库:镜像tag"
    """
    try:
        from csp.topic.topic_server import topic_download
        topic_download(name)
    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


@topic.command()
@click.option("-n", "--name", type=click.STRING, help="模型名称:版本", prompt="模型名称:版本", required=True)
def info(name):
    """
    主题模型镜像评估详情命令

    \b
    使用示例：csp topic info -n "镜像资源库:镜像tag"
    """
    try:
        from csp.topic.topic_server import topic_info
        topic_info(name)
    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))



# @topic.command()
# @click.option("-n", "--name", type=click.STRING, help="模型名称，支持模糊查找", required=True)
# def start(name):
#     """
#     模型服务启动命令
#
#     \b
#     使用示例：csp topic start
#     """
#     from csp.topic.topic_server import model_start
#     model_start(name)


# @topic.command()
# @click.option("-n", "--name", type=click.STRING, help="模型名称，支持模糊查找", required=True)
# def eva(name):
#     """
#     模型评估命令
#
#     \b
#     使用示例：csp topic eva
#     """
#     from csp.topic.topic_server import model_eva
#     model_eva()


if __name__ == '__main__':
    print("start")
