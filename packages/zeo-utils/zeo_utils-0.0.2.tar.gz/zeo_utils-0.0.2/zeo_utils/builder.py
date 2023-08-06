#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 11/24/2022 10:51 AM
# @Author  : zhangbc0315@outlook.com
# @File    : builder.py
# @Software: PyCharm

from zeo_utils.zeo_base import ZeoBase


class Builder(ZeoBase):
    
    def __init__(self, builder_exec_fp: str):
        super(Builder, self).__init__()
        self._builder_exec_fp = self._get_abs_path(builder_exec_fp)

    def build(self, cgd_fp: str, mols_fps: [str], out_fn: str, has_2c: bool, distance_between_2d_layers: float = None):
        cgd_fp = self._get_abs_path(cgd_fp)
        mols_fps = [self._get_abs_path(mol_fp) for mol_fp in mols_fps]
        mols_fps_cmd = ' '.join(mols_fps)
        if distance_between_2d_layers is None:
            command = f"{self._builder_exec_fp} {cgd_fp} {1 if has_2c else 0} {out_fn} {mols_fps_cmd}"
        else:
            command = f"{self._builder_exec_fp} {cgd_fp} {1 if has_2c else 0} {out_fn} {mols_fps_cmd} " \
                      f"{distance_between_2d_layers}"
        return self._get_command_res(command)


if __name__ == "__main__":
    pass
