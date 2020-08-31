# -*- coding: utf-8 -*-
# import qdarkstyle
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
                             QLabel, QLineEdit, QRadioButton, QCheckBox,
                             QComboBox, QStyledItemDelegate, QButtonGroup)
from globalvar import CONFIG_DIR
import os
from config import GlobalConfig
from settingswindow import SettingsWidget


class ClusterWidget(QWidget):
    def __init__(self, parent=None):
        super(ClusterWidget, self).__init__(parent)

        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        self.cluster_name = QLineEdit()
        name_label = QLabel()
        name_label.setText('房间名称:')
        description_label = QLabel()
        description_label.setText('房间简介:')
        self.cluster_description = QLineEdit()
        self.cluster_name.setText("南风颂的饥荒世界")
        self.cluster_description.setText("由饥荒联机版服务器管理工具开设！")
        layout1.addWidget(name_label)
        layout1.addWidget(self.cluster_name)
        layout2.addWidget(description_label)
        layout2.addWidget(self.cluster_description)
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()
        layout5 = QHBoxLayout()
        self.cluster_intention = QComboBox()
        self.cluster_intention.setItemDelegate(QStyledItemDelegate())
        self.cluster_intention.setStyleSheet(
            "QComboBox QAbstractItemView::item { min-height: 30px; min-width: 60px; }"
        )
        self.cluster_intention_cn = ['休闲', '合作', '竞赛', '疯狂']
        self.cluster_intention_value = [
            'social', 'cooperative', 'competitive', 'madness'
        ]
        self.cluster_intention.addItems(self.cluster_intention_cn)
        self.game_mode = QComboBox()
        self.game_mode.setStyleSheet(
            "QComboBox QAbstractItemView::item { min-height: 30px; min-width: 60px; }"
        )
        self.game_mode.setItemDelegate(QStyledItemDelegate())
        self.game_mode_cn = ['无尽', '生存', '荒野', '熔炉', '暴食']
        self.game_mode_value = [
            'endless', 'survival', 'wilderness', 'lavaarena', 'quagmire'
        ]
        self.game_mode.addItems(self.game_mode_cn)
        label3 = QLabel()
        label3.setText('游戏风格:')
        label3.setFixedWidth(70)
        label4 = QLabel()
        label4.setFixedWidth(70)
        label4.setText('游戏模式:')
        layout3.addWidget(label3)
        layout3.addWidget(self.cluster_intention)
        layout4.addWidget(label4)
        layout4.addWidget(self.game_mode)

        layout6 = QHBoxLayout()
        label5 = QLabel()
        label5.setText("游戏语言:")
        label5.setFixedWidth(70)
        self.game_language = QButtonGroup()
        self.en_rbtn = QRadioButton('英语')
        self.en_rbtn.setFixedWidth(70)
        self.zh_rbtn = QRadioButton('简体中文')
        self.game_language.addButton(self.en_rbtn, 1)
        self.game_language.addButton(self.zh_rbtn, 2)
        self.zh_rbtn.setChecked(True)
        layout6.addWidget(label5)
        layout6.addWidget(self.en_rbtn)
        layout6.addWidget(self.zh_rbtn)

        layout7 = QHBoxLayout()
        label6 = QLabel()
        label6.setText("Steam群组ID:")
        self.steam_group_id = QLineEdit()
        self.steam_group_admin = QCheckBox('群组官员设为管理员')
        self.steam_group_only = QCheckBox('仅群组成员可进')
        layout7.addWidget(label6)
        layout7.addWidget(self.steam_group_id)
        layout7.addWidget(self.steam_group_admin)
        layout7.addWidget(self.steam_group_only)

        layout8 = QHBoxLayout()
        self.pvp = QCheckBox("开启PVP竞技")
        self.pause_when_empty = QCheckBox("开启无人暂停")
        self.pause_when_empty.setChecked(True)
        self.vote = QCheckBox('开启玩家投票')
        self.vote.setChecked(True)
        layout8.addWidget(self.pvp)
        layout8.addWidget(self.pause_when_empty)
        layout8.addWidget(self.vote)

        layout9 = QHBoxLayout()
        label7 = QLabel()
        label7.setText('最大玩家人数:')
        self.max_players = QLineEdit()
        self.max_players.setText("0")
        label8 = QLabel()
        label8.setText('房间预留位置个数:')
        self.white_players = QLineEdit()
        self.white_players.setText("0")
        layout9.addWidget(label7)
        layout9.addWidget(self.max_players)
        layout9.addWidget(label8)
        layout9.addWidget(self.white_players)

        layout10 = QHBoxLayout()
        label9 = QLabel()
        label9.setText("房间密码:")
        self.password = QLineEdit()
        layout10.addWidget(label9)
        layout10.addWidget(self.password)

        layout11 = QHBoxLayout()
        label10 = QLabel()
        label10.setText("主世界服务器:")
        label10.setFixedWidth(100)
        self.masterip = QComboBox()
        self.masterip.setStyleSheet(
            "QComboBox QAbstractItemView::item { min-height: 25px; min-width: 100px; }"
        )
        self.masterip.setItemDelegate(QStyledItemDelegate())
        layout11.addWidget(label10)
        layout11.addWidget(self.masterip)

        layout12 = QHBoxLayout()
        self.load_default_cluster_settings = QPushButton()
        self.load_default_cluster_settings.setText("载入默认设置")
        self.set_default_cluster_settings = QPushButton()
        self.set_default_cluster_settings.setText("保存为默认设置")
        self.save_cluster_setttings = QPushButton()
        self.save_cluster_setttings.setText("保存房间设置")
        layout12.addWidget(self.load_default_cluster_settings)
        layout12.addWidget(self.set_default_cluster_settings)
        layout12.addWidget(self.save_cluster_setttings)

        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout5.addLayout(layout3)
        layout5.addLayout(layout4)
        layout.addLayout(layout5)
        layout.addLayout(layout6)
        layout.addLayout(layout7)
        layout.addLayout(layout8)
        layout.addLayout(layout9)
        layout.addLayout(layout10)
        layout.addLayout(layout11)
        layout.addLayout(layout12)

        self.setLayout(layout)

        self.load_default_cluster_settings.clicked.connect(
            self.read_default_cluster_data)
        self.set_default_cluster_settings.clicked.connect(
            self.write_to_default_cluster_data)
        self.save_cluster_setttings.clicked.connect(
            self.write_curret_cluster_data)

        self.setServerIP(self.masterip, ip="127.0.0.1")

    def setServerIP(self, combox, ip):
        if ip == "":
            oldvalue = self.getServerIP()
        else:
            oldvalue = ip
        combox.clear()
        self.serverlist = SettingsWidget().get_server_list()
        oldindex = 0
        index = 0
        for slist in self.serverlist:
            if slist[0] != "":
                combox.addItem(slist[0] + "@" + slist[1])
            else:
                combox.addItem(slist[1])
            if slist[1] == oldvalue:
                oldindex = index
            index += 1
        combox.setCurrentIndex(oldindex)

    def getServerIP(self):
        iparr = self.masterip.currentText().split('@')
        if len(iparr) > 1:
            ip = iparr[1]
        else:
            ip = iparr[0]
        if ip == "":
            ip = "127.0.0.1"
        return ip

    def read_default_cluster_data(self):
        file = os.path.join(CONFIG_DIR, "cluster.ini")
        self.read_cluster_data(file)

    def write_to_default_cluster_data(self):
        file = os.path.join(CONFIG_DIR, "cluster.ini")
        self.write_cluster_data(file)

    def write_curret_cluster_data(self):
        self.write_cluster_data(self.current_cluster_file)

    def write_cluster_data(self, file):
        self.cluster_config.set("STEAM", "steam_group_id",
                                self.steam_group_id.text())
        self.cluster_config.setboolean("STEAM", "steam_group_only",
                                       self.steam_group_only.isChecked())
        self.cluster_config.setboolean("STEAM", "steam_group_admins",
                                       self.steam_group_admin.isChecked())

        self.cluster_config.setboolean("GAMEPLAY", "pvp", self.pvp.isChecked())
        self.cluster_config.set(
            "GAMEPLAY", "game_mode",
            self.game_mode_value[self.game_mode.currentIndex()])
        self.cluster_config.setboolean("GAMEPLAY", "pause_when_empty",
                                       self.pause_when_empty.isChecked())
        self.cluster_config.setboolean("GAMEPLAY", "vote_enabled",
                                       self.vote.isChecked())
        self.cluster_config.set("GAMEPLAY", "max_players",
                                self.max_players.text())

        self.cluster_config.set("NETWORK", "cluster_name",
                                self.cluster_name.text())
        self.cluster_config.set("NETWORK", "cluster_description",
                                self.cluster_description.text())
        self.cluster_config.set(
            "NETWORK", "cluster_intention", self.cluster_intention_value[
                self.cluster_intention.currentIndex()])
        if self.zh_rbtn.isChecked():
            lang = "zh"
        else:
            lang = "en"
        self.cluster_config.set("NETWORK", "cluster_language", lang)
        self.cluster_config.set("NETWORK", "whitelist_slots",
                                self.white_players.text())
        self.cluster_config.set("NETWORK", "cluster_password",
                                self.password.text())

        self.cluster_config.set("SHARD", "master_ip", self.getServerIP())

        self.cluster_config.save(file)

    def read_current_cluster_data(self):
        self.read_cluster_data(self.current_cluster_file)

    def read_cluster_data(self, file):
        if not os.path.exists(file):
            file = os.path.join(CONFIG_DIR, "cluster.ini")

        self.cluster_config = GlobalConfig(file)
        self.steam_group_id.setText(
            self.cluster_config.get("STEAM", "steam_group_id"))
        self.steam_group_only.setChecked(
            self.cluster_config.getboolean("STEAM", "steam_group_only"))
        self.steam_group_admin.setChecked(
            self.cluster_config.getboolean("STEAM", "steam_group_admins"))

        self.pvp.setChecked(self.cluster_config.getboolean("GAMEPLAY", "pvp"))
        self.game_mode.setCurrentIndex(
            self.game_mode_value.index(
                self.cluster_config.get("GAMEPLAY", "game_mode")))
        self.pause_when_empty.setChecked(
            self.cluster_config.getboolean("GAMEPLAY", "pause_when_empty"))
        self.vote.setChecked(
            self.cluster_config.getboolean("GAMEPLAY", "vote_enabled"))
        self.max_players.setText(
            self.cluster_config.get("GAMEPLAY", "max_players"))

        self.cluster_name.setText(
            self.cluster_config.get("NETWORK", "cluster_name"))
        self.cluster_description.setText(
            self.cluster_config.get("NETWORK", "cluster_description"))
        self.cluster_intention.setCurrentIndex(
            self.cluster_intention_value.index(
                self.cluster_config.get("NETWORK", "cluster_intention")))
        if self.cluster_config.get("NETWORK", "cluster_language") == "zh":
            self.zh_rbtn.setChecked(True)
        else:
            self.en_rbtn.setChecked(True)
        self.white_players.setText(
            self.cluster_config.get("NETWORK", "whitelist_slots"))
        self.password.setText(
            self.cluster_config.get("NETWORK", "cluster_password"))

        self.setServerIP(self.masterip,
                         self.cluster_config.get("SHARD", "master_ip"))
