# -*- coding: utf-8 -*-
import os
import sys
import json
import paramiko
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QGroupBox, QLabel, QLineEdit, QHBoxLayout, QCheckBox, QTableWidget, QAbstractItemView, QTableWidgetItem, QMessageBox, QHeaderView, QFileDialog
from PyQt5.QtCore import Qt
from serverdialog import ServerDialog
from globalvar import USER_HOME, CLUSTER_DIR, CONFIG_DIR


class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)

        # 软件设置面板
        path_settings_groupbox = QGroupBox()
        path_settings_groupbox.setTitle("本地设置")
        path_settings_groupbox.setFixedHeight(160)
        path_settings_groupbox_layout = QVBoxLayout()
        # 本地客户端路径
        path_widget1_layout = QHBoxLayout()
        local_client_path_label = QLabel()
        local_client_path_label.setText("本地客户端路径:")
        # local_client_path_label.setFixedWidth(105)
        self.local_client_path_lineEdit = QLineEdit()
        self.local_client_path_btn = QPushButton()
        self.local_client_path_btn.setText("浏览")
        path_widget1_layout.addWidget(local_client_path_label)
        path_widget1_layout.addWidget(self.local_client_path_lineEdit)
        path_widget1_layout.addWidget(self.local_client_path_btn)
        # 本地服务端路径
        path_widget2_layout = QHBoxLayout()
        local_server_path_label = QLabel()
        local_server_path_label.setText("本地服务端路径:")
        # local_server_path_label.setFixedWidth(105)
        self.local_server_path_lineEdit = QLineEdit()
        self.local_server_path_btn = QPushButton()
        self.local_server_path_btn.setText("浏览")
        path_widget2_layout.addWidget(local_server_path_label)
        path_widget2_layout.addWidget(self.local_server_path_lineEdit)
        path_widget2_layout.addWidget(self.local_server_path_btn)
        # 本地存档路径
        path_widget3_layout = QHBoxLayout()
        local_cluster_path_label = QLabel()
        local_cluster_path_label.setText("本地存档路径:")
        # local_cluster_path_label.setFixedWidth(105)
        self.local_cluster_path_lineEdit = QLineEdit()
        self.local_cluster_path_lineEdit.setDisabled(True)
        self.local_cluster_path_btn = QPushButton()
        # self.local_cluster_path_btn.setText("浏览")
        self.local_cluster_path_btn.setText("打开")
        path_widget3_layout.addWidget(local_cluster_path_label)
        path_widget3_layout.addWidget(self.local_cluster_path_lineEdit)
        path_widget3_layout.addWidget(self.local_cluster_path_btn)

        path_settings_groupbox_layout.addLayout(path_widget1_layout)
        path_settings_groupbox_layout.addLayout(path_widget2_layout)
        path_settings_groupbox_layout.addLayout(path_widget3_layout)
        path_settings_groupbox.setLayout(path_settings_groupbox_layout)

        sc_settings_groupbox = QGroupBox()
        sc_settings_groupbox.setFixedHeight(75)
        sc_settings_groupbox.setTitle("消息通知设置")
        sc_settings_groupbox_layout = QHBoxLayout()
        self.sc_enable_checkBox = QCheckBox()
        self.sc_enable_checkBox.setText("开启Server酱消息通知")
        sc_key_label = QLabel()
        sc_key_label.setText("Server酱密钥:")
        self.sc_key_lineEdit = QLineEdit()
        sc_settings_groupbox_layout.addWidget(self.sc_enable_checkBox)
        sc_settings_groupbox_layout.addWidget(sc_key_label)
        sc_settings_groupbox_layout.addWidget(self.sc_key_lineEdit)
        sc_settings_groupbox.setLayout(sc_settings_groupbox_layout)

        server_settings_groupbox = QGroupBox()
        server_settings_groupbox.setTitle("云主机设置(截图请注意隐藏IP和密码)")
        server_settings_groupbox_layout = QVBoxLayout()

        token_layout = QHBoxLayout()
        server_token_label = QLabel()
        server_token_label.setText("服务器令牌:")
        self.server_token_lineEdit = QLineEdit()
        token_layout.addWidget(server_token_label)
        token_layout.addWidget(self.server_token_lineEdit)

        server_frame_layout = QHBoxLayout()

        self.server_table = QTableWidget()
        self.server_table.setColumnCount(5)
        # 禁止编辑
        self.server_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置标题
        self.server_table.setHorizontalHeaderLabels(['名称', 'IP或域名', '用户名', '密码', '备注'])
        # 设置选择整行
        self.server_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 只选中单行
        self.server_table.setSelectionMode(QAbstractItemView.SingleSelection)
        # 自动列宽，随内容
        self.server_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.server_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        server_edit_btn_layout = QVBoxLayout()
        self.add_new_server_btn = QPushButton()
        self.add_new_server_btn.setText("添加新的")
        self.edit_server_btn = QPushButton()
        self.edit_server_btn.setText("修改选中")
        self.delete_server_btn = QPushButton()
        self.delete_server_btn.setText("删除选中")
        self.test_server_btn = QPushButton()
        self.test_server_btn.setText("连接测试")
        server_edit_btn_layout.addWidget(self.add_new_server_btn)
        server_edit_btn_layout.addWidget(self.edit_server_btn)
        server_edit_btn_layout.addWidget(self.delete_server_btn)
        server_edit_btn_layout.addWidget(self.test_server_btn)

        server_frame_layout.addWidget(self.server_table)
        server_frame_layout.addLayout(server_edit_btn_layout)

        server_settings_groupbox_layout.addLayout(token_layout)
        server_settings_groupbox_layout.addLayout(server_frame_layout)
        server_settings_groupbox.setLayout(server_settings_groupbox_layout)

        self.save_settings_btn = QPushButton()
        self.save_settings_btn.setText("保存设置(修改完记得保存)")

        settings_layout = QVBoxLayout()
        settings_layout.addWidget(path_settings_groupbox)
        settings_layout.addWidget(sc_settings_groupbox)
        settings_layout.addWidget(server_settings_groupbox)
        settings_layout.addWidget(self.save_settings_btn)
        self.setLayout(settings_layout)

        # 按钮函数绑定
        self.add_new_server_btn.clicked.connect(self.add_new_server)
        self.delete_server_btn.clicked.connect(self.delete_server)
        self.edit_server_btn.clicked.connect(self.edit_server)
        self.test_server_btn.clicked.connect(self.test_server)
        self.save_settings_btn.clicked.connect(self.save_settings_data)
        self.local_server_path_btn.clicked.connect(self.select_server_dir)
        # self.local_cluster_path_btn.clicked.connect(self.select_cluster_dir)
        self.local_cluster_path_btn.clicked.connect(self.open_cluster)
        self.local_client_path_btn.clicked.connect(self.select_client_dir)

        self.init_settings_data()

    # 添加新服务器
    def add_new_server(self):
        self.server_table.clearSelection()
        self.serverDialog = ServerDialog(self)
        self.serverDialog.setWindowTitle("添加服务器")
        self.serverDialog.serverSignal.connect(self.add_server)
        self.serverDialog.exec()

    def is_server_not_exist(self, ip):
        serverlist = self.get_server_list()
        for server in serverlist:
            if ip == server[1]:
                return False
        return True

    def add_server(self, server):
        flag = True
        server_row_num = self.server_table.currentRow()
        print(server_row_num)
        if server_row_num == -1:
            if self.is_server_not_exist(server[1]):
                server_row_num = self.server_table.rowCount()
                self.server_table.setRowCount(server_row_num + 1)
            else:
                QMessageBox.warning(self, "警告", "服务器已存在！", QMessageBox.Yes)
                flag = False
        if flag:
            self.serverDialog.hide()
            for col in range(5):
                self.server_table.setItem(server_row_num, col, QTableWidgetItem(server[col]))
                self.server_table.item(server_row_num, col).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def edit_server(self):
        row = self.server_table.currentRow()
        if row > -1:
            serverDialog = ServerDialog(self)
            serverDialog.setWindowTitle("修改服务器")
            serverDialog.name_lineEdit.setText(self.server_table.item(row, 0).text())
            serverDialog.ip_lineEdit.setText(self.server_table.item(row, 1).text())
            serverDialog.user_lineEdit.setText(self.server_table.item(row, 2).text())
            serverDialog.passwd_lineEdit.setText(self.server_table.item(row, 3).text())
            serverDialog.tips_lineEdit.setText(self.server_table.item(row, 4).text())
            serverDialog.serverSignal.connect(self.add_server)
            serverDialog.exec()
        else:
            QMessageBox.warning(self, "警告", "你没有选中服务器！", QMessageBox.Yes)

    def delete_server(self):
        row = self.server_table.currentRow()
        if row > -1:
            self.server_table.removeRow(row)
        else:
            QMessageBox.warning(self, "警告", "你没有选中服务器！", QMessageBox.Yes)

    def test_server(self):
        row = self.server_table.currentRow()
        if row > -1:
            ip = self.server_table.item(row, 1).text()
            if ip == "127.0.0.1":
                QMessageBox.information(self, "无需测试", "本地服请确保本地已安装服务端且已配好路径！", QMessageBox.Yes)
            else:
                username = self.server_table.item(row, 2).text()
                passwd = self.server_table.item(row, 3).text()
                try:
                    # 创建一个SSH客户端对象
                    ssh = paramiko.SSHClient()
                    # 设置访问策略
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    # 与远程主机进行连接
                    ssh.connect(hostname=ip, port=22, username=username, password=passwd)
                    QMessageBox.information(self, "连接正确", "服务器连接测试通过!", QMessageBox.Yes)
                except Exception as e:
                    QMessageBox.critical(self, "连接错误", str(e), QMessageBox.Yes)
                finally:
                    ssh.close()
        else:
            QMessageBox.warning(self, "警告", "你没有选中服务器！", QMessageBox.Yes)

    def read_json_data(self, filename):
        jsonfile = os.path.join(CONFIG_DIR, "settings.json")
        if os.path.exists(jsonfile):
            with open(jsonfile, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        return data

    def write_json_data(self, filename, data):
        config_dir = os.path.join(CONFIG_DIR)
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)
        jsonfile = os.path.join(config_dir, filename)
        with open(jsonfile, 'w') as f:
            json.dump(data, f)

    # 初始化设置
    def init_settings_data(self):
        settings = self.read_json_data('settings.json')
        if settings:
            self.local_client_path_lineEdit.setText(settings['localclientpath'])
            self.local_server_path_lineEdit.setText(settings['localserverpath'])
            self.local_cluster_path_lineEdit.setText(settings['localclusterpath'])
            self.sc_key_lineEdit.setText(settings['sckey'])
            self.sc_enable_checkBox.setChecked(settings['scenable'])
            self.server_token_lineEdit.setText(settings['servertoken'])
            self.set_server_list(settings['servers'])
        else:
            self.local_cluster_path_lineEdit.setText(CLUSTER_DIR)

    def get_server_list(self):
        slist = []
        rowCount = self.server_table.rowCount()
        for row in range(rowCount):
            slist.append([self.server_table.item(row, 0).text(),
                         self.server_table.item(row, 1).text(),
                         self.server_table.item(row, 2).text(),
                         self.server_table.item(row, 3).text(),
                         self.server_table.item(row, 4).text()])
        return slist

    def set_server_list(self, serverlist):
        row = self.server_table.rowCount()
        flag = False
        for list in serverlist:
            if list[1] == "127.0.0.1":
                flag = True
            self.server_table.setRowCount(row + 1)
            self.server_table.setItem(row, 0, QTableWidgetItem(list[0]))
            self.server_table.setItem(row, 1, QTableWidgetItem(list[1]))
            self.server_table.setItem(row, 2, QTableWidgetItem(list[2]))
            self.server_table.setItem(row, 3, QTableWidgetItem(list[3]))
            self.server_table.setItem(row, 4, QTableWidgetItem(list[4]))
            self.server_table.item(row, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.server_table.item(row, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.server_table.item(row, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.server_table.item(row, 3).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.server_table.item(row, 4).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            row += 1
            if not flag:
                self.set_server_list([["本地服务器", "127.0.0.1", "如无必要", "请勿删除", "这个选项"]])
        if 0 == len(serverlist):
            self.set_server_list([["本地服务器", "127.0.0.1", "如无必要", "请勿删除", "这个选项"]])

    # 保存设置
    def save_settings_data(self):
        settings = {}
        settings['localclientpath'] = self.local_client_path_lineEdit.text()
        settings['localserverpath'] = self.local_server_path_lineEdit.text()
        settings['localclusterpath'] = self.local_cluster_path_lineEdit.text()
        settings['sckey'] = self.sc_key_lineEdit.text()
        settings['scenable'] = self.sc_enable_checkBox.isChecked()
        settings['servertoken'] = self.server_token_lineEdit.text()
        settings['servers'] = self.get_server_list()
        self.write_json_data('settings.json', settings)

    def getClientPath(self):
        return self.local_client_path_lineEdit.text()

    def select_client_dir(self):
        client_dir = ""
        if sys.platform == "darwin":
            fileName, _ = QFileDialog.getOpenFileName(self, "选择本地客户端路径", USER_HOME, "Mac Applications (*.app);;All Files (*)")
            if fileName:
                client_dir = fileName
        else:
            client_dir = QFileDialog.getExistingDirectory(self, "选择本地服务端路径", USER_HOME)
        # self.local_server_path_lineEdit.setText(str(server_dir))

        # client_dir = QFileDialog.getExistingDirectory(self, "选择本地客户端路径", USER_HOME)
        self.local_client_path_lineEdit.setText(str(client_dir))

    def select_cluster_dir(self):
        cluster_dir = QFileDialog.getExistingDirectory(self, "选择本地存档路径", USER_HOME)
        # 官方存档路径
        cluster = os.path.join(USER_HOME, 'Documents', 'Klei', 'DoNotStarveTogether')
        if cluster_dir != cluster:
            self.local_cluster_path_lineEdit.setText(str(cluster_dir))
        else:
            QMessageBox.warning(self, "警告", "不可选择和官方相同的路径", QMessageBox.Yes)

    def open_cluster(self):
        cluster_path = self.local_cluster_path_lineEdit.text()
        if cluster_path == "":
            cluster_path = CLUSTER_DIR
            self.local_cluster_path_lineEdit.setText(CLUSTER_DIR)
            self.save_settings_data()
        if os.path.exists(cluster_path):
            if sys.platform == "darwin":
                os.system("open %s" % cluster_path)
            elif sys.platform == "win32":
                os.system("start explorer %s" % cluster_path)
            else:
                QMessageBox.warning(self, "警告", "当前系统不支持该操作", QMessageBox.Yes)
        else:
            QMessageBox.warning(self, "警告", "存档文件夹不存在", QMessageBox.Yes)

    def select_server_dir(self):
        server_dir = ""
        if sys.platform == "darwin":
            fileName, _ = QFileDialog.getOpenFileName(self, "选择本地服务端路径", USER_HOME, "All Files (*);;Mac Applications (*.app)")
            if fileName:
                server_dir = fileName
        else:
            server_dir = QFileDialog.getExistingDirectory(self, "选择本地服务端路径", USER_HOME)
        self.local_server_path_lineEdit.setText(str(server_dir))
