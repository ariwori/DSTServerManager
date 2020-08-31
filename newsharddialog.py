# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QDialog, QFrame, QLabel, QLineEdit, QPushButton,
                             QHBoxLayout, QVBoxLayout, QComboBox,
                             QStyledItemDelegate, QButtonGroup, QRadioButton)
from PyQt5.QtCore import pyqtSignal


class NewShardDialog(QDialog):

    # 自定义信号
    serverSignal = pyqtSignal(list)

    def __init__(self, parent=None):
        super(NewShardDialog, self).__init__(parent)
        self.setFixedSize(250, 150)

        frame = QFrame(self)
        frame_layout = QVBoxLayout()

        name_layout = QHBoxLayout()
        name_label = QLabel()
        name_label.setText("世界别名:")
        name_label.setFixedWidth(70)
        self.name_lineEdit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_lineEdit)

        ip_layout = QHBoxLayout()
        ip_label = QLabel()
        ip_label.setText("服务器:")
        ip_label.setFixedWidth(70)
        self.server = QComboBox()
        self.server.setStyleSheet(
            "QComboBox QAbstractItemView::item { min-height: 25px; min-width: 100px; }"
        )
        self.server.setItemDelegate(QStyledItemDelegate())
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.server)

        serverlaber1layout = QHBoxLayout()
        serverlaber1 = QLabel()
        serverlaber1.setText("世界属性:")
        serverlaber1.setFixedWidth(70)
        ismasterGroup = QButtonGroup()
        self.ismasterR = QRadioButton()
        self.notmasterR = QRadioButton()
        self.ismasterR.setText("主世界")
        self.ismasterR.setFixedWidth(80)
        self.notmasterR.setText("附从世界")
        self.notmasterR.setChecked(True)
        ismasterGroup.addButton(self.ismasterR)
        ismasterGroup.addButton(self.notmasterR)
        serverlaber1layout.addWidget(serverlaber1)
        serverlaber1layout.addWidget(self.ismasterR)
        serverlaber1layout.addWidget(self.notmasterR)

        type_layout = QHBoxLayout()
        type_label = QLabel()
        type_label.setText("世界类型:")
        type_label.setFixedWidth(70)
        self.type = QComboBox()
        self.type.setStyleSheet(
            "QComboBox QAbstractItemView::item { min-height: 25px; min-width: 100px; }"
        )
        self.type.setItemDelegate(QStyledItemDelegate())
        self.type.addItems(["地面", "洞穴", "挂机", "熔炉", "暴食"])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type)

        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton()
        self.cancel_btn.setText("取消")
        self.save_btn = QPushButton()
        self.save_btn.setText("确定")
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)

        frame_layout.addLayout(name_layout)
        frame_layout.addLayout(ip_layout)
        frame_layout.addLayout(serverlaber1layout)
        frame_layout.addLayout(type_layout)
        frame_layout.addLayout(btn_layout)
        frame.setLayout(frame_layout)

        self.cancel_btn.clicked.connect(self.hide)
        self.save_btn.clicked.connect(self.save)

    def initServerList(self, slist):
        self.serverlist = slist
        for sl in slist:
            if sl[0] != "":
                self.server.addItem(sl[0] + "@" + sl[1])
            else:
                self.server.addItem(sl[1])

    # 保存
    def save(self):
        name = self.name_lineEdit.text() + self.type.currentText()
        ipindex = self.server.currentIndex()
        if len(self.serverlist) > 1:
            ip = self.serverlist[ipindex][1]
        else:
            ip = "127.0.0.1"
        if self.ismasterR.isChecked():
            ismaster = True
        else:
            ismaster = False
        typevalue = ["forest", "caves", "aog", "lavaarena", "quagmire"]
        wtype = typevalue[self.type.currentIndex()]
        self.serverSignal.emit([name, ip, ismaster, wtype])
