#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/6/23 9:24
# @Author  : xgy
# @Site    :
# @File    : standard2doccano.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import json
import os
import sys 

from csp.common.utils import read_jsonl


def standard2doccno(standard_folder, output):

    doccno_data = []

    for item in st_data:
        id = item["id"]
        text = item["text"]
        spo_list = item["spo_list"]
        doccno_item = {"id": id, "text": text, "entities": [], "relations": []}





def write_json(data, output, file_name,indent=4):
    output_item = os.path.join(output, file_name)  
    with open(output_item, "w", encoding="utf-8") as f: 
        f.write(json.dumps(data, ensure_ascii=False, indent=indent))
     


def check_input_file(file_path_arr):
    for file_path in file_path_arr:
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            print_error_msg(("指定的文件路径不存在: %s" % file_path), 1001)
            return False
    return True

  
if __name__ == '__main__':
    print("SUCCESS")
    

