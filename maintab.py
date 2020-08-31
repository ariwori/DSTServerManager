# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTabWidget
from clustertab import ClusterWidget
from shardtab import ShardWidget
from modtab import ModWidget


class MainTab(QTabWidget):

    def __init__(self, parent=None):
        super(MainTab, self).__init__(parent)

        self.cluster_settings_tab = ClusterWidget()
        self.shard_settings_tab = ShardWidget()
        self.mod_tab = ModWidget()

        self.addTab(self.cluster_settings_tab, "房间设置")
        self.addTab(self.shard_settings_tab, "世界设置")
        self.addTab(self.mod_tab, "MOD设置")

        self.currentChanged['int'].connect(self.tabfun)   # 绑定标签点击时的信号与槽函数

    #  自定义的槽函数
    def tabfun(self, index):
        if (index == 2):
            self.mod_tab.initData()
