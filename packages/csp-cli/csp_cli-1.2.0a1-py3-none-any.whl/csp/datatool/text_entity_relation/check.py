#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/6/21 15:59
# @Author  : xgy
# @Site    : 
# @File    : check.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import json
import os

from loguru import logger

# from csp.datatool.text_entity.check import EntityCheck
from csp.datatool.utils import Entity


class SpoCheck(Entity):
    
    def __init__(self, folder, output=None):
        super(SpoCheck, self).__init__(folder, output)
        self.get_dataset()

    def check(self):
        """
        公共检查，字段值为空
        :return:
        """
        # connectioncategorys_flg = True

        spo_list_null_l = []
        id_text_error_l = []
        id_error_l = []
        text_error_l = []

        spo_key_error_l = []
        spo_value_error_l = []

        id_l = []

        # 检查字段全为空为空
        for index, item in enumerate(self.data):
            spo_list = item["spo_list"]
            id = item["id"]

            if not spo_list:
                error_item = {"message": "'spo_list' is empty in line {}".format(str(index)), "data": item}
                spo_list_null_l.append(error_item)

            if not item["id"] and not item["text"]:
                error_item = {"message": "'id' and 'text' are empty in line {}".format(str(index)), "data": item}
                id_text_error_l.append(error_item)
            if item["id"] and not item["text"]:
                error_item = {"message": "'text' is empty in line {}".format(str(index)), "data": item}
                text_error_l.append(error_item)
            if not item["id"] and item["text"]:
                error_item = {"message": "'id' is empty in line {}".format(str(index)), "data": item}
                id_error_l.append(error_item)
            if id in id_l:
                error_item = {"message": "'Duplicate' id in line {}".format(str(index)), "data": item}
                id_error_l.append(error_item)

            id_l.append(id)

            # spo_list 内部字段检查
            if spo_list:
                for spo in spo_list:
                    if spo.get("h", None) is None or spo.get("t", None) is None or spo.get("relation", None) is None:
                        error_item = {"message": "SPO should include three fields: h, t, relation id in line {}".format(str(index)), "data": spo}
                        spo_key_error_l.append(error_item)

                    if not spo.get("h", None) and type(spo.get("h", None)) == dict:
                        error_item = {
                            "message": "'h' is empty in line {}".format(
                                str(index)), "data": spo}
                        spo_value_error_l.append(error_item)

                    if not spo.get("t", None) and type(spo.get("t", None)) == dict:
                        error_item = {
                            "message": "'t' is empty in line {}".format(
                                str(index)), "data": spo}
                        spo_value_error_l.append(error_item)

                    if not spo.get("relation", None) and spo.get("relation", None) == '':
                        error_item = {
                            "message": "'relation' is empty in line {}".format(
                                str(index)), "data": spo}
                        spo_value_error_l.append(error_item)

                    if spo.get("h", None):
                        h = spo["h"]

                        if h.get("name", None) is None or h.get("pos", None) is None:
                            error_item = {
                                "message": "'h' should include three fields: name, pos, relation id in line {}".format(
                                    str(index)), "data": spo}
                            spo_key_error_l.append(error_item)

                        if not h.get("name", None) and h.get("name", None) == '':
                            error_item = {
                                "message": "'name' is empty in line {}".format(
                                    str(index)), "data": spo}
                            spo_value_error_l.append(error_item)

                        if not h.get("pos", None) and type(h.get("name", None)) == 'list':
                            error_item = {
                                "message": "'pos' is empty in line {}".format(
                                    str(index)), "data": spo}
                            spo_value_error_l.append(error_item)

                        if h.get("pos", None):
                            pos = h.get("pos", None)
                            start = int(pos[0])
                            end = int(pos[1])
                            try:
                                if start >= end or start < 0 or end < 0:
                                    error_item = {
                                        "message": "'pos[0]' must be less than pos[1] and greater than 0 in line {}".format(str(index)), "data": spo}
                                    spo_value_error_l.append(error_item)
                            except Exception:
                                error_item = {
                                    "message": "The value of 'pos' cannot be converted to integer in line {}".format(
                                        str(index)), "data": spo}
                                spo_value_error_l.append(error_item)

                    if spo.get("t", None):
                        t = spo["t"]

                        if t.get("name", None) is None or t.get("pos", None) is None:
                            error_item = {
                                "message": "'t' should include three fields: name, pos, relation id in line {}".format(
                                    str(index)), "data": spo}
                            spo_key_error_l.append(error_item)

                        if not t.get("name", None) and t.get("name", None) == '':
                            error_item = {
                                "message": "'name' is empty in line {}".format(
                                    str(index)), "data": spo}
                            spo_value_error_l.append(error_item)

                        if not t.get("pos", None) and type(t.get("name", None)) == 'list':
                            error_item = {
                                "message": "'pos' is empty in line {}".format(
                                    str(index)), "data": spo}
                            spo_value_error_l.append(error_item)

                        if t.get("pos", None):
                            pos = t.get("pos", None)
                            start = int(pos[0])
                            end = int(pos[1])
                            try:
                                if start >= end or start < 0 or end < 0:
                                    error_item = {
                                        "message": "'pos[0]' must be less than pos[1] and greater than 0 in line {}".format(str(index)), "data": spo}
                                    spo_value_error_l.append(error_item)
                            except Exception:
                                error_item = {
                                    "message": "The value of 'pos' cannot be converted to integer in line {}".format(
                                        str(index)), "data": spo}
                                spo_value_error_l.append(error_item)

        spo_list_null_path = os.path.join(self.output, "spo_list_null.txt") if self.output else "spo_list_null.txt"
        id_text_error_path = os.path.join(self.output, "id_text_error.txt") if self.output else "id_text_error"
        id_error_path = os.path.join(self.output, "id_error.txt") if self.output else "id_error.txt"
        text_error_path = os.path.join(self.output, "text_error.txt") if self.output else "text_error.txt"
        spo_key_error_path = os.path.join(self.output, "spo_key_error.txt") if self.output else "spo_key_error.txt"
        spo_value_error_path = os.path.join(self.output, "spo_value_error.txt") if self.output else "spo_value_error.txt"

        if spo_list_null_l:
            self.write_error_txt(spo_list_null_path, spo_list_null_l)
        if id_text_error_l:
            self.write_error_txt(id_text_error_path, id_text_error_l)
        if id_error_l:
            self.write_error_txt(id_error_path, id_error_l)
        if text_error_l:
            self.write_error_txt(text_error_path, text_error_l)
        if spo_key_error_l:
            self.write_error_txt(spo_key_error_path, spo_key_error_l)
        if spo_value_error_l:
            self.write_error_txt(spo_value_error_path, spo_value_error_l)

        if not spo_list_null_l and not id_text_error_l and not id_error_l and not text_error_l and not spo_key_error_l and not spo_value_error_l:
            logger.info("未检测出相关错误")

        # return connectioncategorys_flg

    def write_error_txt(self, save_path, data):
        with open(save_path, "w", encoding="utf-8") as fw:
            for item in data:
                fw.write(json.dumps(item, ensure_ascii=False))
                fw.write("\n")
            logger.info("the result has been saved in {}".format(save_path))


def spo_check(folder, output=None):
    check_relation = SpoCheck(folder, output=output)
    check_relation.clean_output()
    check_relation.check()


if __name__ == '__main__':
    print("start")
