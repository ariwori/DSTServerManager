# -*- coding: utf-8 -*-
import qdarkstyle
from PyQt5.QtWidgets import QDialog, QFrame, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal
import paramiko


class ServerDialog(QDialog):

    # 自定义信号
    serverSignal = pyqtSignal(list)

    def __init__(self, parent=None):
        super(ServerDialog, self).__init__(parent)
        # 设置窗口透明度
        self.setWindowOpacity(0.9)
        # 设置窗口样式
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setFixedSize(300, 230)

        frame = QFrame(self)
        frame_layout = QVBoxLayout()

        name_layout = QHBoxLayout()
        name_label = QLabel()
        name_label.setText("主机名称:")
        name_label.setFixedWidth(70)
        self.name_lineEdit = QLineEdit()
        self.name_lineEdit.setFixedWidth(200)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_lineEdit)

        ip_layout = QHBoxLayout()
        ip_label = QLabel()
        ip_label.setText("IP或域名:")
        ip_label.setFixedWidth(70)
        self.ip_lineEdit = QLineEdit()
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.ip_lineEdit)

        user_layout = QHBoxLayout()
        user_label = QLabel()
        user_label.setText("登录名:")
        user_label.setFixedWidth(70)
        self.user_lineEdit = QLineEdit()
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_lineEdit)

        passwd_layout = QHBoxLayout()
        passwd_label = QLabel()
        passwd_label.setText("登录密码:")
        passwd_label.setFixedWidth(70)
        self.passwd_lineEdit = QLineEdit()
        passwd_layout.addWidget(passwd_label)
        passwd_layout.addWidget(self.passwd_lineEdit)

        tips_layout = QHBoxLayout()
        tips_label = QLabel()
        tips_label.setText("备注:")
        tips_label.setFixedWidth(70)
        self.tips_lineEdit = QLineEdit()
        tips_layout.addWidget(tips_label)
        tips_layout.addWidget(self.tips_lineEdit)

        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton()
        self.cancel_btn.setText("取消")
        self.test_then_save_btn = QPushButton()
        self.test_then_save_btn.setText("测试连接后保存")
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.test_then_save_btn)

        frame_layout.addLayout(name_layout)
        frame_layout.addLayout(ip_layout)
        frame_layout.addLayout(user_layout)
        frame_layout.addLayout(passwd_layout)
        frame_layout.addLayout(tips_layout)
        frame_layout.addLayout(btn_layout)
        frame.setLayout(frame_layout)

        self.cancel_btn.clicked.connect(self.hide)
        self.test_then_save_btn.clicked.connect(self.test_then_save)

    # 测试连接通过后保存
    def test_then_save(self):
        tips = self.tips_lineEdit.text()
        name = self.name_lineEdit.text()
        ip = self.ip_lineEdit.text()
        username = self.user_lineEdit.text()
        password = self.passwd_lineEdit.text()
        port = 22
        try:
            # 创建一个SSH客户端对象
            ssh = paramiko.SSHClient()
            # 设置访问策略
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 与远程主机进行连接
            ssh.connect(hostname=ip, port=port, username=username, password=password)
            button = QMessageBox.information(self, "连接正确", "服务器连接测试通过!\n是否保存新的服务器？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if button == QMessageBox.Yes:
                self.serverSignal.emit([name, ip, username, password, tips])
        except Exception as e:
            QMessageBox.critical(self, "连接错误", str(e), QMessageBox.Yes)
        finally:
            ssh.close()
