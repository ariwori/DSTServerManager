# -*- coding: utf-8 -*-
# import qdarkstyle
from PyQt5.QtWidgets import (QDialog, QLabel, QPushButton, QHBoxLayout,
                             QVBoxLayout, QComboBox, QStyledItemDelegate,
                             QScrollArea, QWidget)
from PyQt5.QtCore import Qt
import os
from globalvar import CLUSTER_DIR, TEMP_FILE, ROOT_DIR
from config import GlobalConfig
from LuaTableParser import LuaTableParser


class ModConfigDialog(QDialog):
    def __init__(self, parent=None):
        super(ModConfigDialog, self).__init__(parent)

        self.savemoddict = {}
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.topFiller = QWidget()
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.topFiller)
        self.layout.addWidget(self.scroll)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.cancel_btn = QPushButton()
        self.cancel_btn.setText("取消")
        self.reset_btn = QPushButton()
        self.reset_btn.setText("重置为默认")
        self.reset_btn.clicked.connect(self.loadDefaultValue)
        self.save_btn = QPushButton()
        self.save_btn.setText("保存")
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addWidget(self.save_btn)
        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.hide)

    def getDictValue(self, d, k):
        if k in d:
            return d[k]
        else:
            return ""

    def initData(self, cdict):
        self.options = cdict
        num = len(cdict)
        self.topFiller.setMinimumSize(400, 40 * num + 50)
        maxh = 40 * num + 50 > 500 and 500 or 40 * num + 50
        self.setFixedHeight(maxh)
        oWidget = QWidget(self.topFiller)
        mm = QVBoxLayout()
        oWidget.setLayout(mm)
        index = 0
        self.opcombox = []
        for op in self.options:
            if self.getDictValue(op, 'default') != "":
                m = QHBoxLayout()
                a = QLabel()
                a.setFixedWidth(200)
                a.setText(op['label'])
                if self.getDictValue(op, "hover"):
                    a.setToolTip(op['hover'])
                m.addWidget(a)
                if self.getDictValue(op, 'options'):
                    b = QComboBox()
                    b.select = True
                    b.index = index
                    b.name = op['name']
                    self.opcombox.append(b)
                    b.setFixedWidth(150)
                    b.setStyleSheet(
                        "QComboBox QAbstractItemView::item { min-height: 25px; min-width: 100px; }"
                    )
                    b.setItemDelegate(QStyledItemDelegate())
                    b.currentIndexChanged.connect(self.selectChange)
                    bd = []
                    for o in op['options']:
                        b.addItem(str(o['description']))
                        bd.append(o['data'])
                    b.data = bd
                    if self.getDictValue(op['options'][b.currentIndex()],
                                         'hover'):
                        b.setToolTip(op['options'][b.currentIndex()]['hover'])
                else:
                    b = QLabel()
                    self.opcombox.append(b)
                    b.select = False
                    b.name = op['name']
                    b.data = op['default']
                    b.setText("请直接修改modinfo.lua")
                m.addWidget(b)
                mm.addLayout(m)
            index += 1
        self.loadExistValue()

    def getCurrentCluster(self):
        tc = GlobalConfig(TEMP_FILE)
        return tc.get("TEMP", "cluster_index")

    def loadExistValue(self):
        rootdir = os.path.join(CLUSTER_DIR,
                               "Cluster_" + self.getCurrentCluster())
        file = os.path.join(rootdir, "modoverrides.lua")
        if os.path.exists(file):
            f = open(file, 'r', encoding='utf-8')
            data = f.read()
            f.close()
            data = data.replace("return", "")
            p1 = LuaTableParser()
            p1.load(data)
            self.savemoddict = p1.dumpDict()

        allfile = os.path.join(ROOT_DIR, "modoverrides.lua")
        af = open(allfile, 'r', encoding='utf-8')
        adata = af.read()
        af.close()
        adata = adata.replace("return", "")
        ap1 = LuaTableParser()
        ap1.load(adata)
        self.allsavemoddict = ap1.dumpDict()

        if self.moddir in self.allsavemoddict:
            if self.moddir in self.savemoddict:
                self.updateComboxsValue(
                    self.savemoddict[self.moddir]["configuration_options"])
            else:
                self.updateComboxsValue(
                    self.allsavemoddict[self.moddir]["configuration_options"])
        else:
            self.loadDefaultValue()

    def loadDefaultValue(self):
        c = {}
        # print(self.options)
        for op in self.options:
            if self.getDictValue(op, 'default'):
                c[op['name']] = op['default']
        self.updateComboxsValue(c)

    def updateComboxsValue(self, cdict):
        for com in self.opcombox:
            index = 0
            for data in com.data:
                if self.getDictValue(cdict,
                                     com.name) and cdict[com.name] == data:
                    com.setCurrentIndex(index)
                    break
                index += 1

    def selectChange(self):
        s = self.sender()
        sdict = self.options[s.index]['options']
        if self.getDictValue(sdict, 'hover'):
            i = s.currentIndex()
            s.setToolTip(sdict[i]['hover'])

    def save(self):
        if len(self.savemoddict) > 0 and self.moddir in self.savemoddict:
            cdict = self.savemoddict[self.moddir]["configuration_options"]
            if len(cdict) < 1:
                cdict = {}
            for com in self.opcombox:
                if com.select:
                    index = com.currentIndex()
                    cdict[com.name] = com.data[index]
                else:
                    cdict[com.name] = com.data
            self.savemoddict[self.moddir]["configuration_options"] = cdict
            rootdir = os.path.join(CLUSTER_DIR,
                                   "Cluster_" + self.getCurrentCluster())

            file = os.path.join(rootdir, "modoverrides.lua")
            p1 = LuaTableParser()
            p1.loadDict(self.savemoddict)
            data = "return" + p1.dump()
            with open(file, 'w', encoding='utf-8') as f:
                f.write(data)
                f.close()
        if len(self.allsavemoddict) > 0 and self.moddir in self.allsavemoddict:
            cdict = self.allsavemoddict[self.moddir]["configuration_options"]
            if len(cdict) < 1:
                cdict = {}
            for com in self.opcombox:
                if com.select:
                    index = com.currentIndex()
                    cdict[com.name] = com.data[index]
                else:
                    cdict[com.name] = com.data
            self.allsavemoddict[self.moddir]["configuration_options"] = cdict
            file = os.path.join(ROOT_DIR, "modoverrides.lua")
            p1 = LuaTableParser()
            p1.loadDict(self.allsavemoddict)
            data = "return" + p1.dump()
            with open(file, 'w', encoding='utf-8') as f:
                f.write(data)
                f.close()
            self.hide()
