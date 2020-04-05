# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTabWidget, QLabel
from clustertab import ClusterWidget
from shardtab import ShardWidget


class MainTab(QTabWidget):

    def __init__(self, parent=None):
        super(MainTab, self).__init__(parent)

        self.cluster_settings_tab = ClusterWidget()
        self.shard_settings_tab = ShardWidget()
        s = QLabel()
        s.setText("MOD")

        self.addTab(self.cluster_settings_tab, "房间设置")
        self.addTab(self.shard_settings_tab, "世界设置")
        self.addTab(s, "MOD设置")
