#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/11/16 11:28
# @Author  : xgy
# @Site    : 
# @File    : login_server.py
# @Software: PyCharm
# @python version: 3.7.13
"""
import os
import time

import yaml
from csp.common.config import Configure
from csp.aip.common.http_client import HttpClient
import requests

"""
登录操作支持单用户
"""


parent_path = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
user_file = os.path.join(parent_path, "common/config", "user_config.yaml")


def user_login(username, passwd):
    # 调用后端注册服服务
    infer_dict = Configure().data
    get_token_url = infer_dict["user"]["token"]
    client_id = infer_dict["user"]["clientId"]
    client_secret = infer_dict["user"]["clientSecret"]

    params = {"clientId": client_id, "clientSecret": client_secret, "username": username, "password": passwd}
    http_client = HttpClient()
    # res = http_client.get(get_token_url, **params)
    res = http_client.post(get_token_url, arg_type="data", **params)

    # create_time = time.time()
    # expire_time = create_time + 2592000
    # user_data = {"username": username, "passwd": passwd, "token": res,
    #              create_time: create_time, "expire_time": expire_time}
    user_data = {"username": username, "passwd": passwd, "access_token": res['data']['access_token']}

    with open(user_file, "w", encoding="utf-8") as fw:
        yaml.dump(user_data, fw)


def check_user():
    if not os.path.exists(user_file):
        raise NameError("请先登录 csp login")
    else:
        user_data = Configure(user_file).data
        return user_data
    # else:
    #     # 本栋验证token过期时间
    #     user_data = Configure(user_file).data
    #     current_time = time.time()
    #     if user_data["expire_time"] < current_time:
    #         print("token 过期，请重新登录")
    #         raise ConnectionError("token 过期")


if __name__ == '__main__':
    print("start")
