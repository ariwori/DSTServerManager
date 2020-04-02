# -*- coding: utf-8 -*-
# import qdarkstyle
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QRadioButton, QCheckBox, QComboBox, QStyledItemDelegate, QButtonGroup, QTabWidget, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from globalvar import CONFIG_DIR, CLUSTER_DIR, TEMP_FILE
import os
import json
import random
from LuaTableParser import LuaTableParser
from config import GlobalConfig


class ShardWidget(QWidget):

    def __init__(self, parent=None):
        super(ShardWidget, self).__init__(parent)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.add_shard_btn = QPushButton()
        self.add_shard_btn.setText("添加世界")
        self.del_shard_btn = QPushButton()
        self.del_shard_btn.setText("删除世界")
        self.save_shard_btn = QPushButton()
        self.save_shard_btn.setText("保存世界设置")
        self.save_as_btn = QPushButton()
        self.save_as_btn.setText("另存为预设")
        self.load_default_btn = QPushButton()
        self.load_default_btn.setText("载入预设")
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_shard_btn)
        btn_layout.addWidget(self.del_shard_btn)
        btn_layout.addWidget(self.load_default_btn)
        btn_layout.addWidget(self.save_as_btn)
        btn_layout.addWidget(self.save_shard_btn)
        self.layout.addLayout(btn_layout)
        self.topFiller = QWidget()
        self.topFiller.setMinimumSize(865, 925)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.topFiller)
        # self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.shardtab = QTabWidget(self.topFiller)
        self.shardtab.setTabPosition(QTabWidget.West)
        self.shardtabs = []
        self.shardlayouts = []
        self.scrolls = []
        self.topFillers = []
        self.scrolls = []
        self.addShardTab("forest")
        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)

    def getCurrentCluster(self):
        tc = GlobalConfig(TEMP_FILE)
        return tc.get("TEMP", "cluster_index")

    def loadShaedValue(self, wtype, wid, combos):
        levelfname = os.path.join(CLUSTER_DIR, "Cluster_" + self.getCurrentCluster(), wtype + str(wid), "leveldataoverride.lua")
        if not os.path.exists(levelfname):
            levelfname = os.path.join(CONFIG_DIR, wtype + ".lua")
        f = open(levelfname, 'r', encoding='utf-8')
        data = f.read()
        f.close()
        data = data.replace("return", "")
        p1 = LuaTableParser()
        p1.load(data)
        shardValueDict = p1.dumpDict()
        for comk, comv in combos.items():
            value = shardValueDict["overrides"][comk]
            comindex = 0
            for v in comv.valuearr:
                if v == value:
                    break
                else:
                    comindex += 1
            comv.setCurrentIndex(comindex)

    def addShardTab(self, world):
        if world == "forest":
            name_prefix = "地面"
        else:
            name_prefix = "洞穴"
        sindex = len(self.shardtabs)
        self.shardtabs.append(QWidget())
        self.shardtabs[sindex].type = world
        self.shardtabs[sindex].id = str(random.randint(100, 999))
        self.shardtab.addTab(self.shardtabs[sindex], name_prefix + " " + str(sindex + 1))
        self.optionsCombobox = {}
        self.shardlayouts.append(QVBoxLayout())
        optionsDict = self.readShardOptions(world)
        self.labels = []
        self.ollabels = []
        self.ollayouts = []
        typedict = {"environment": "世界环境", "source": "资源", "food": "食物", "animal": "动物", "monster": "怪物"}
        for tk, tv in typedict.items():
            self.labels.append(QPushButton())
            lindex = len(self.labels) - 1
            self.labels[lindex].setText(tv)

            self.shardlayouts[sindex].addWidget(self.labels[lindex])
            oindex = 0
            ooindex = 0
            for olist in optionsDict[tk]:
                if oindex + 4 < 5:
                    self.ollayouts.append(QHBoxLayout())
                    olindex = len(self.ollayouts) - 1
                    self.shardlayouts[sindex].addLayout(self.ollayouts[olindex])
                olindex = len(self.ollayouts) - 1
                self.ollabels.append(QLabel())
                ollindex = len(self.ollabels) - 1
                self.ollabels[ollindex].setText(olist["name"])
                self.ollabels[ollindex].setFixedWidth(60)
                self.optionsCombobox[olist["key"]] = QComboBox()
                self.optionsCombobox[olist["key"]].setFixedWidth(120)
                self.optionsCombobox[olist["key"]].setStyleSheet("QComboBox QAbstractItemView::item { min-height: 25px; min-width: 80px; }")
                self.optionsCombobox[olist["key"]].setItemDelegate(QStyledItemDelegate())
                self.optionsCombobox[olist["key"]].addItems(olist["options"]["label"])
                self.optionsCombobox[olist["key"]].valuearr = olist["options"]["value"]
                self.ollayouts[olindex].addWidget(self.ollabels[ollindex])
                self.ollayouts[olindex].addWidget(self.optionsCombobox[olist["key"]])
                if oindex < 3:
                    oindex += 1
                else:
                    oindex = 0
                if len(optionsDict[tk])-1 == ooindex and oindex != 0 and ooindex != 0:
                    self.ollayouts[olindex].addWidget(QLabel())
                ooindex += 1
        self.shardtabs[sindex].setLayout(self.shardlayouts[sindex])

        self.loadShaedValue(world, self.shardtabs[sindex].id, self.optionsCombobox)

    def readShardOptions(self, filename):
        file = os.path.join(CONFIG_DIR, filename + ".json")
        if os.path.exists(file):
            with open(file, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        return data
