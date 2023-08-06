#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 11/24/2022 10:18 AM
# @Author  : zhangbc0315@outlook.com
# @File    : prop_parser.py
# @Software: PyCharm


class PropParser:

    @classmethod
    def parse(cls, pdm_str: str):
        props = {}
        logs = []
        for line in pdm_str.split('\n'):
            line = line.strip()
            logs.append(line)
            if line.startswith('@@'):
                line = line[2:]
                if line.startswith('TUPLE='):
                    pass
                else:
                    key, value = line.split(': ')
                    props[key] = value
        props['logs'] = logs
        return props


if __name__ == "__main__":
    pass
