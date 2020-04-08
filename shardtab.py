# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QRadioButton, QCheckBox, QComboBox, QStyledItemDelegate, QButtonGroup, QTabWidget, QScrollArea
from PyQt5.QtCore import Qt
from globalvar import CONFIG_DIR, CLUSTER_DIR, TEMP_FILE
import os
import json
import random
import shutil
from LuaTableParser import LuaTableParser
from config import GlobalConfig
from newsharddialog import NewShardDialog
from settingswindow import SettingsWidget
from clustertab import ClusterWidget


class ShardWidget(QWidget):

    def __init__(self, parent=None):
        super(ShardWidget, self).__init__(parent)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.add_shard_btn = QPushButton()
        self.add_shard_btn.setText("添加世界")
        self.add_shard_btn.setFixedWidth(100)
        self.del_shard_btn = QPushButton()
        self.del_shard_btn.setText("删除世界")
        self.del_shard_btn.setFixedWidth(100)
        self.save_shard_btn = QPushButton()
        self.save_shard_btn.setText("保存世界设置(修改完一定要保存)")
        self.save_as_btn = QPushButton()
        self.save_as_btn.setText("另存为预设")
        self.save_as_btn.setFixedWidth(100)
        self.load_default_btn = QPushButton()
        self.load_default_btn.setText("载入预设")
        self.load_default_btn.setFixedWidth(100)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_shard_btn)
        btn_layout.addWidget(self.del_shard_btn)
        btn_layout.addWidget(self.load_default_btn)
        btn_layout.addWidget(self.save_as_btn)
        btn_layout.addWidget(self.save_shard_btn)
        self.layout.addLayout(btn_layout)
        self.topFiller = QWidget()
        self.topFiller.setMinimumSize(835, 995)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.topFiller)
        # self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.shardtab = QTabWidget(self.topFiller)
        self.shardtab.setFixedSize(835, 995)
        # self.shardtab.setTabPosition(QTabWidget.West)
        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)
        self.initShardTab()
        self.save_shard_btn.clicked.connect(self.saveShardLevelData)
        self.del_shard_btn.clicked.connect(self.deleteShard)
        self.add_shard_btn.clicked.connect(self.addNewShard)

    def getServerList(self):
        s = SettingsWidget()
        return s.get_server_list()

    def addNewShard(self):
        slist = self.getServerList()
        self.newShardDialog = NewShardDialog(self)
        self.newShardDialog.setWindowTitle("添加服务器")
        self.newShardDialog.initServerList(slist)
        self.newShardDialog.serverSignal.connect(self.add_shard)
        self.newShardDialog.exec()

    # 初始化世界配置从文件加载世界配置并写入UI
    def loadServerIni(self, wtype, wid):
        file = os.path.join(CLUSTER_DIR, "Cluster_" + self.getCurrentCluster(), wtype + "_" + str(wid), "server.ini")
        if not os.path.exists(file):
            file = os.path.join(CONFIG_DIR, "server.ini")
        self.serverconfig[wid] = GlobalConfig(file)
        self.serverconfig[wid].server_port = self.serverconfig[wid].get("NETWORK", "server_port")
        self.serverconfig[wid].is_master = self.serverconfig[wid].getboolean("SHARD", "is_master")
        self.serverconfig[wid].name = self.serverconfig[wid].get("SHARD", "name")
        self.serverconfig[wid].id = self.serverconfig[wid].get("SHARD", "id")
        self.serverconfig[wid].master_server_port = self.serverconfig[wid].get("STEAM", "master_server_port")
        self.serverconfig[wid].authentication_port = self.serverconfig[wid].get("STEAM", "authentication_port")
        if self.serverconfig[wid].has_section("SERVER"):
            self.serverconfig[wid].ip = self.serverconfig[wid].get("SERVER", "ip")
            self.serverconfig[wid].alias = self.serverconfig[wid].get("SERVER", "alias")
        else:
            self.serverconfig[wid].add_section("SERVER")
            self.serverconfig[wid].set("SERVER", "ip", "127.0.0.1")
            self.serverconfig[wid].set("SERVER", "alias", wtype + "_" + str(wid))

        if self.serverconfig[wid].server_port == "":
            self.serverconfig[wid].set("NETWORK", "server_port", str(10998+random.randint(1, 100)))
        if self.serverconfig[wid].name == "":
            self.serverconfig[wid].set("SHARD", "name", wtype + str(wid))
        if self.serverconfig[wid].id == "":
            self.serverconfig[wid].set("SHARD", "id", str(wid))
        if self.serverconfig[wid].master_server_port == "":
            self.serverconfig[wid].set("STEAM", "master_server_port", str(27016+random.randint(1, 100)))
        if self.serverconfig[wid].authentication_port == "":
            self.serverconfig[wid].set("STEAM", "authentication_port", str(8766+random.randint(1, 100)))
        if self.serverconfig[wid].alias == "":
            self.serverconfig[wid].set("SERVER", "alias", wtype + "_" + str(wid))

    def setServerIni(self, wid):
        self.serverconfig[wid].set("SERVER", "ip", self.getShardIP())
        if self.ismasterR.isChecked():
            ismaster = True
        else:
            ismaster = False
        self.serverconfig[wid].setboolean("SHARD", "is_master", ismaster)

    def savaServerIni(self, wtype, wid):
        inidir = os.path.join(CLUSTER_DIR, "Cluster_" + self.getCurrentCluster(), wtype + "_" + str(wid))
        file = os.path.join(inidir, "server.ini")
        if not os.path.exists(inidir):
            os.mkdir(inidir)
        self.serverconfig[wid].save(file)

    def setShardIP(self, combox, ip):
        if ip == "":
            ip = "127.0.0.1"
        ClusterWidget().setServerIP(combox, ip)

    def getShardIP(self):
        iparr = self.serverCombox.currentText().split('@')
        if len(iparr) > 1:
            ip = iparr[1]
        else:
            ip = iparr[0]
        if ip == "":
            ip = "127.0.0.1"
        return ip

    def add_shard(self, shard):
        self.newShardDialog.hide()
        self.addShardTab(shard[3], 0, shard)

    def getCurrentCluster(self):
        tc = GlobalConfig(TEMP_FILE)
        return tc.get("TEMP", "cluster_index")

    def loadShardValue(self, w, combos):
        levelfname = os.path.join(CLUSTER_DIR, "Cluster_" + self.getCurrentCluster(), w.type + "_" + str(w.id), "leveldataoverride.lua")
        saveFlag = False
        if not os.path.exists(levelfname):
            levelfname = os.path.join(CONFIG_DIR, w.type + ".lua")
            saveFlag = True
        f = open(levelfname, 'r', encoding='utf-8')
        data = f.read()
        f.close()
        data = data.replace("return", "")
        p1 = LuaTableParser()
        p1.load(data)
        w.shardValueDict = p1.dumpDict()
        if w.type == "forest" or w.type == "caves":
            for comk, comv in combos.items():
                value = w.shardValueDict["overrides"][comk]
                comindex = 0
                for v in comv.valuearr:
                    if v == value:
                        break
                    else:
                        comindex += 1
                    comv.setCurrentIndex(comindex)
        if saveFlag:
            self.saveShardLevelData()

    def initShardTab(self):
        self.shardtabs = []
        self.shardlayouts = []
        self.optionsCombobox = {}
        self.serverconfig = {}
        self.shardtab.clear()
        cdir = os.path.join(CLUSTER_DIR, "Cluster_" + self.getCurrentCluster())
        shard_type = ["forest", "caves", "aog", "lavaarena", "quagmire"]
        exist_shards = os.listdir(cdir)
        cindex = 0
        for file in exist_shards:
            arr = file.split("_")
            if len(arr) > 1 and arr[0] in shard_type and file != "cluster_token.txt":
                self.addShardTab(arr[0], int(arr[1]), shard=[])
                cindex += 1

    def addShardTab(self, world, wid, shard):
        sindex = len(self.shardtabs)
        self.shardtabs.append(QWidget())
        self.shardtabs[sindex].type = world
        self.shardtabs[sindex].id = wid == 0 and str(random.randint(100, 999)) or wid
        self.loadServerIni(self.shardtabs[sindex].type, self.shardtabs[sindex].id)
        wid = self.shardtabs[sindex].id
        if len(shard) > 0:
            self.serverconfig[wid].set("SERVER", "ip", shard[1])
            self.serverconfig[wid].set("SERVER", "alias", shard[0])
            self.serverconfig[wid].setboolean("SHARD", "is_master", shard[2])
            self.savaServerIni(self.shardtabs[sindex].type, self.shardtabs[sindex].id)

        self.shardtab.addTab(self.shardtabs[sindex], self.serverconfig[wid].get("SERVER", "alias") + " " + str(sindex + 1))

        shardlayout = QVBoxLayout()
        comboboxObject = {}

        # shard ip, ismaster
        shardserverlayout = QHBoxLayout()
        serverlaber = QLabel()
        serverlaber.setText("服务器:")
        serverlaber.setFixedWidth(60)
        self.serverCombox = QComboBox()
        self.serverCombox.setStyleSheet("QComboBox QAbstractItemView::item { min-height: 25px; min-width: 100px; }")
        self.serverCombox.setItemDelegate(QStyledItemDelegate())
        shardserverlayout.addWidget(serverlaber)
        shardserverlayout.addWidget(self.serverCombox)
        serverlaber1 = QLabel()
        serverlaber1.setText("世界属性:")
        serverlaber1.setFixedWidth(70)
        ismasterGroup = QButtonGroup()
        self.ismasterR = QRadioButton()
        self.notmasterR = QRadioButton()
        self.ismasterR.setText("主世界")
        self.ismasterR.setFixedWidth(80)
        self.notmasterR.setText("附从世界")
        ismasterGroup.addButton(self.ismasterR)
        ismasterGroup.addButton(self.notmasterR)
        shardserverlayout.addWidget(serverlaber1)
        shardserverlayout.addWidget(self.ismasterR)
        shardserverlayout.addWidget(self.notmasterR)
        shardlayout.addLayout(shardserverlayout)
        if self.serverconfig[self.shardtabs[sindex].id].getboolean("SHARD", "is_master"):
            self.ismasterR.setChecked(True)
        else:
            self.notmasterR.setChecked(True)
        self.setShardIP(self.serverCombox, self.serverconfig[self.shardtabs[sindex].id].get("SERVER", "ip"))
        if world == "forest" or world == "caves":
            optionsDict = self.readShardOptions(world)
            typedict = {"environment": "世界环境", "source": "资源", "food": "食物", "animal": "动物", "monster": "怪物"}
            for tk, tv in typedict.items():
                tlabel = QPushButton()
                tlabel.setText(tv)
                shardlayout.addWidget(tlabel)
                oindex, ooindex = 0, 0
                for olist in optionsDict[tk]:
                    if oindex + 4 < 5:
                        ollayout = QHBoxLayout()
                        shardlayout.addLayout(ollayout)
                    ollabel = QLabel()
                    ollabel.setText(olist["name"])
                    ollabel.setFixedWidth(60)
                    comboboxObject[olist["key"]] = QComboBox()
                    comboboxObject[olist["key"]].setFixedWidth(120)
                    comboboxObject[olist["key"]].setStyleSheet("QComboBox QAbstractItemView::item { min-height: 25px; min-width: 80px; }")
                    comboboxObject[olist["key"]].setItemDelegate(QStyledItemDelegate())
                    comboboxObject[olist["key"]].addItems(olist["options"]["label"])
                    comboboxObject[olist["key"]].valuearr = olist["options"]["value"]
                    ollayout.addWidget(ollabel)
                    ollayout.addWidget(comboboxObject[olist["key"]])
                    if oindex < 3:
                        oindex += 1
                    else:
                        oindex = 0
                    if len(optionsDict[tk])-1 == ooindex and oindex != 0 and ooindex != 0:
                        ollayout.addWidget(QLabel())
                    ooindex += 1
        else:
            tip = QLabel()
            tip.setText("当前世界类型不支持修改设置！")
            tip.setAlignment(Qt.AlignHCenter)
            shardlayout.addWidget(tip)
        self.shardtabs[sindex].setLayout(shardlayout)

        self.optionsCombobox[self.shardtabs[sindex].id] = comboboxObject
        self.loadShardValue(self.shardtabs[sindex], self.optionsCombobox[self.shardtabs[sindex].id])

    def readShardOptions(self, filename):
        file = os.path.join(CONFIG_DIR, filename + ".json")
        if os.path.exists(file):
            with open(file, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        return data

    def saveShardLevelData(self):
        for w in self.shardtabs:
            # w = self.shardtab.currentWidget()
            sdir = os.path.join(CLUSTER_DIR, "Cluster_" + self.getCurrentCluster(), w.type + "_" + str(w.id))
            levelfname = os.path.join(sdir, "leveldataoverride.lua")
            # print(w.shardValueDict)
            if w.type == "forest" or w.type == "caves":
                for comk, comv in self.optionsCombobox[w.id].items():
                    comindex = comv.currentIndex()
                    w.shardValueDict['overrides'][comk] = comv.valuearr[comindex]
            p1 = LuaTableParser()
            p1.loadDict(w.shardValueDict)
            data = "return" + p1.dump()
            if not os.path.exists(sdir):
                os.mkdir(sdir)
            with open(levelfname, 'w', encoding='utf-8') as f:
                f.write(data)
                f.close()
            self.setServerIni(w.id)
            self.savaServerIni(w.type, w.id)

    def deleteShard(self):
        if len(self.shardtabs) > 0:
            w = self.shardtab.currentWidget()
            sdir = os.path.join(CLUSTER_DIR, "Cluster_" + self.getCurrentCluster(), w.type + "_" + str(w.id))
            if os.path.exists(sdir):
                shutil.rmtree(sdir)
            ci = self.shardtab.currentIndex()
            self.shardtab.removeTab(ci)
            self.shardtabs.remove(w)
