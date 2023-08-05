#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 11/24/2022 10:08 AM
# @Author  : zhangbc0315@outlook.com
# @File    : network.py
# @Software: PyCharm

from zeo_utils.zeo_base import ZeoBase


class Network(ZeoBase):

    def __init__(self, network_exec_fp: str):
        """ 初始化 zeo++ 软件路径
        """
        super(Network, self).__init__()
        self._network_exec_fp = self._get_abs_path(network_exec_fp)

    def test(self):
        """ 测试 zeo++ 软件是否可以正常使用
        """
        print(self._get_command_res(self._network_exec_fp))

    def calc_pore_diameter(self, cif_fp: str) -> str:
        """ 计算孔径

        原理是调用命令   ./network.exe -ha -res ***.cif

        :param cif_fp: cif文件的路径，相对路径或绝对路径都行
        """
        cif_fp = self._get_abs_path(cif_fp)
        return self._get_command_res(f"{self._network_exec_fp} -ha -res {cif_fp}")

    def calc_specific_surface_area(self, cif_fp: str, chan_radius: float, probe_radius: float, num_samples: int) -> str:
        """ 计算比表面积

        原理是调用命令  ./network.exe -ha -sa chen_radius probe_radius num_sample ***.cif

        :param cif_fp: cif文件的路径，相对路径或绝对路径都行
        :param chan_radius: 用于探测材料内孔道空间可及性情况的探针分子半径（Å）
        :param probe_radius: 用于计算比表面积的探针分子半径（Å）
        :param num_samples: 在每个材料原子周围进行Monte Carlo抽样探测的次数
        """
        cif_fp = self._get_abs_path(cif_fp)
        return self._get_command_res(
            f"{self._network_exec_fp} -ha -sa {chan_radius} {probe_radius} {num_samples} {cif_fp}")

    def calc_accessible_volume(self, cif_fp: str, chan_radius: float, probe_radius: float,
                               num_samples: int):
        """ 计算可及孔体积

               原理是调用命令  ./network.exe -ha -vol chen_radius probe_radius num_sample ***.cif

               :param cif_fp: cif文件的路径，相对路径或绝对路径都行
               :param chan_radius: 用于探测材料内孔道空间可及性情况的探针分子半径（Å）
               :param probe_radius: 用于计算比表面积的探针分子半径（Å）
               :param num_samples: 在每个材料原子周围进行Monte Carlo抽样探测的次数
               """
        cif_fp = self._get_abs_path(cif_fp)
        return self._get_command_res(f"{self._network_exec_fp} -ha -vol {chan_radius} {probe_radius} {num_samples} "
                                     f"{cif_fp}")

    def calc_pore_size_distribution(self, cif_fp: str, chan_radius: float, probe_radius: float, num_samples: int):
        """ 计算孔径分布

        原理是调用命令  ./network.exe -ha -psd chen_radius probe_radius num_sample ***.cif

        :param cif_fp: cif文件的路径，相对路径或绝对路径都行
        :param chan_radius: 用于探测材料内孔道空间可及性情况的探针分子半径（Å）
        :param probe_radius: 用于计算比表面积的探针分子半径（Å）
        :param num_samples: 在每个材料原子周围进行Monte Carlo抽样探测的次数
        """
        cif_fp = self._get_abs_path(cif_fp)
        return self._get_command_res(
            f"{self._network_exec_fp} -ha -psd {chan_radius} {probe_radius} {num_samples} {cif_fp}")


if __name__ == "__main__":
    pass
