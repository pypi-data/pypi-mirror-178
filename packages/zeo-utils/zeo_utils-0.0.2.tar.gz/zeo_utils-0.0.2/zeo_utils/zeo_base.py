#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 11/24/2022 10:50 AM
# @Author  : zhangbc0315@outlook.com
# @File    : zeo_base.py
# @Software: PyCharm

import os
import logging


class ZeoBase:

    def __init__(self):
        pass

    @classmethod
    def _get_abs_path(cls, fp: str) -> str:
        """ 获得文件fp的绝对路径
        如果fp不存在，会报错FileNotFoundError
        """
        if not os.path.exists(fp):
            raise FileNotFoundError(f"there is not file: {fp}")
        return os.path.abspath(fp)

    @classmethod
    def _get_command_res(cls, command: str) -> str:
        """ 获得执行终端命令后的输出值
        """
        logging.info(f"Command: {command}\n")
        res = os.popen(command)
        res_text = res.read()
        res.close()
        return res_text


if __name__ == "__main__":
    pass
