#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 14:56
# @Author  : zbc@mail.ustc.edu.cn
# @File    : setup.py
# @Software: PyCharm

from setuptools import setup

with open('README.md', 'r', encoding='utf-8')as f:
    long_description = f.read()

setup(
    name='zeo_utils',
    version='0.0.1',
    author='zhang',
    author_email='zhangbc0315@outlook.com',
    url='https://github.com/zbc0315/zeo_utils',
    description=u'Utilities for ZEO++',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['zeo_utils'],
    install_requires=[],
    include_package_data=True,
    entry_points={
        'console_scripts': [
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='==3.7'
)


if __name__ == "__main__":
    pass
