#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 11/24/2022 10:18 AM
# @Author  : zhangbc0315@outlook.com
# @File    : prop_parser.py
# @Software: PyCharm


class PropParser:

    @classmethod
    def _parse_tuple(cls, data, line):
        key, values = line.split(': ')
        # keys = keys.split(',')
        values = values.split(',')
        if data is None:
            data = {key: []}
        data[key].append(values)
        return data

    @classmethod
    def parse(cls, pdm_str: str):
        props = {}
        logs = []
        data = None
        for line in pdm_str.split('\n'):
            line = line.strip()
            if len(line) == 0:
                continue
            logs.append(line)
            if line.startswith('@@'):
                line = line[2:]
                if line.startswith('TUPLE='):
                    data = cls._parse_tuple(data, line[6:])
                else:
                    key, value = line.split(': ')
                    props[key] = value
        if data is not None:
            for k, v in data.items():
                props[k] = v
        props['logs'] = logs
        return props


if __name__ == "__main__":
    pass
