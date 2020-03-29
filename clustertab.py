# -*- coding: utf-8 -*-
# import qdarkstyle
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QTabWidget, QFormLayout, QRadioButton, QCheckBox, QComboBox, QStyledItemDelegate, QButtonGroup
from globalvar import CONFIG_DIR
import os
from config import GlobalConfig


class ClusterTab(QTabWidget):

    def __init__(self, parent=None):
        super(ClusterTab, self).__init__(parent)
        # 设置窗口透明度
        # self.setWindowOpacity(0.9)
        # 设置窗口样式
        # self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # 创建3个选项卡小控件窗口
        self.cluster_settings_tab = QWidget()
        self.shard_settings_tab = QWidget()
        self.mods_settings_tab = QWidget()

        # 将三个选项卡添加到顶层窗口中
        self.addTab(self.cluster_settings_tab, "Tab 1")
        self.addTab(self.shard_settings_tab, "Tab 2")
        self.addTab(self.mods_settings_tab, "Tab 3")

        # 每个选项卡自定义的内容
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

    # 房间设置
    def tab1UI(self):
        # 表单布局
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
        self.cluster_intention.setStyleSheet("QComboBox QAbstractItemView::item { min-height: 30px; min-width: 60px; }")
        self.cluster_intention_cn = ['休闲', '合作', '竞赛', '疯狂']
        self.cluster_intention_value = ['social', 'cooperative', 'competitive', 'madness']
        self.cluster_intention.addItems(self.cluster_intention_cn)
        self.game_mode = QComboBox()
        self.game_mode.setStyleSheet("QComboBox QAbstractItemView::item { min-height: 30px; min-width: 60px; }")
        self.game_mode.setItemDelegate(QStyledItemDelegate())
        self.game_mode_cn = ['无尽', '生存', '荒野', '熔炉', '暴食']
        self.game_mode_value = ['endless', 'survival', 'wilderness', 'lavaarena', 'quagmire']
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
        label10.setText("主世界IP:")
        self.masterip = QLineEdit()
        self.masterip.setText("127.0.0.1")
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
        # # 设置选项卡的小标题与布局方式
        self.setTabText(0, '房间设置')
        self.cluster_settings_tab.setLayout(layout)

        self.load_default_cluster_settings.clicked.connect(self.read_default_cluster_data)
        self.set_default_cluster_settings.clicked.connect(self.write_to_default_cluster_data)
        self.save_cluster_setttings.clicked.connect(self.write_curret_cluster_data)

    def tab2UI(self):
        # zhu表单布局，次水平布局
        layout = QFormLayout()
        sex = QHBoxLayout()

        # 水平布局添加单选按钮
        sex.addWidget(QRadioButton('男'))
        sex.addWidget(QRadioButton('女'))

        # 表单布局添加控件
        layout.addRow(QLabel('性别'), sex)
        layout.addRow('生日', QLineEdit())

        # 设置标题与布局
        self.setTabText(1, '世界设置')
        self.shard_settings_tab.setLayout(layout)

    def tab3UI(self):
        # 水平布局
        layout = QHBoxLayout()

        # 添加控件到布局中
        layout.addWidget(QLabel('科目'))
        layout.addWidget(QCheckBox('物理'))
        layout.addWidget(QCheckBox('高数'))

        # 设置小标题与布局方式
        self.setTabText(2, 'MOD设置')
        self.mods_settings_tab.setLayout(layout)

    def read_default_cluster_data(self):
        file = os.path.join(CONFIG_DIR, "cluster.ini")
        self.read_cluster_data(file)

    def write_to_default_cluster_data(self):
        file = os.path.join(CONFIG_DIR, "cluster.ini")
        self.write_cluster_data(file)

    def write_curret_cluster_data(self):
        self.write_cluster_data(self.current_cluster_file)

    def write_cluster_data(self, file):
        self.cluster_config.set("STEAM", "steam_group_id", self.steam_group_id.text())
        self.cluster_config.setboolen("STEAM", "steam_group_only", self.steam_group_only.isChecked())
        self.cluster_config.setboolen("STEAM", "steam_group_admins", self.steam_group_admin.isChecked())

        self.cluster_config.setboolen("GAMEPLAY", "pvp", self.pvp.isChecked())
        self.cluster_config.set("GAMEPLAY", "game_mode", self.game_mode_value[self.game_mode.currentIndex()])
        self.cluster_config.setboolen("GAMEPLAY", "pause_when_empty", self.pause_when_empty.isChecked())
        self.cluster_config.setboolen("GAMEPLAY", "vote_enabled", self.vote.isChecked())
        self.cluster_config.set("GAMEPLAY", "max_players", self.max_players.text())

        self.cluster_config.set("NETWORK", "cluster_name", self.cluster_name.text())
        self.cluster_config.set("NETWORK", "cluster_description", self.cluster_description.text())
        self.cluster_config.set("NETWORK", "cluster_intention", self.cluster_intention_value[self.cluster_intention.currentIndex()])
        if self.zh_rbtn.isChecked():
            lang = "zh"
        else:
            lang = "en"
        self.cluster_config.set("NETWORK", "cluster_language", lang)
        self.cluster_config.set("NETWORK", "whitelist_slots", self.white_players.text())
        self.cluster_config.set("NETWORK", "cluster_password", self.password.text())

        self.cluster_config.set("SHARD", "master_ip", self.masterip.text())

        self.cluster_config.save(file)

    def read_current_cluster_data(self):
        self.read_cluster_data(self.current_cluster_file)

    def read_cluster_data(self, file):
        if not os.path.exists(file):
            file = os.path.join(CONFIG_DIR, "cluster.ini")
            if not os.path.exists(file):
                data = """[STEAM]
steam_group_id = 0
steam_group_admins = false
steam_group_only = false

[GAMEPLAY]
game_mode = survival
pause_when_empty = true
vote_enabled = true
pvp = false
max_players = 6

[NETWORK]
cluster_name = 由脚本dstserver.sh创建！
cluster_description = 由脚本dstserver.sh创建！
cluster_intention = social
cluster_language = zh
whitelist_slots = 0
idle_timeout = 0
cluster_password =
lan_only_cluster = false
offline_cluster = false
autosaver_enabled = true
tick_rate = 15

[MISC]
max_snapshots = 10
console_enabled = true

[SHARD]
master_ip = 127.0.0.1
shard_enabled = true
bind_ip = 0.0.0.0
master_port = 10888
cluster_key = Tendy2020"""
                try:
                    f = open(file, 'a', encoding='utf-8')
                    f.write(data)
                    f.close()
                except ImportError:
                    pass

        self.cluster_config = GlobalConfig(file)
        self.steam_group_id.setText(self.cluster_config.get("STEAM", "steam_group_id"))
        self.steam_group_only.setChecked(self.cluster_config.getboolean("STEAM", "steam_group_only"))
        self.steam_group_admin.setChecked(self.cluster_config.getboolean("STEAM", "steam_group_admins"))

        self.pvp.setChecked(self.cluster_config.getboolean("GAMEPLAY", "pvp"))
        self.game_mode.setCurrentIndex(self.game_mode_value.index(self.cluster_config.get("GAMEPLAY", "game_mode")))
        self.pause_when_empty.setChecked(self.cluster_config.getboolean("GAMEPLAY", "pause_when_empty"))
        self.vote.setChecked(self.cluster_config.getboolean("GAMEPLAY", "vote_enabled"))
        self.max_players.setText(self.cluster_config.get("GAMEPLAY", "max_players"))

        self.cluster_name.setText(self.cluster_config.get("NETWORK", "cluster_name"))
        self.cluster_description.setText(self.cluster_config.get("NETWORK", "cluster_description"))
        self.cluster_intention.setCurrentIndex(self.cluster_intention_value.index(self.cluster_config.get("NETWORK", "cluster_intention")))
        if self.cluster_config.get("NETWORK", "cluster_language") == "zh":
            self.zh_rbtn.setChecked(True)
        else:
            self.en_rbtn.setChecked(True)
        self.white_players.setText(self.cluster_config.get("NETWORK", "whitelist_slots"))
        self.password.setText(self.cluster_config.get("NETWORK", "cluster_password"))

        self.masterip.setText(self.cluster_config.get("SHARD", "master_ip"))
