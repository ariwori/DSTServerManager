# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QStatusBar, QProgressBar, QLabel


class StatusProgressBar(QStatusBar):

    def __init__(self, parent=None):
        super(StatusProgressBar, self).__init__(parent)
        # 设置状态栏
        self.setStyleSheet('QStatusBar::item {border: none;}')
        self.progressBar = QProgressBar()
        self.label = QLabel()
        self.label2 = QLabel()
        self.label.setText("状态栏")
        self.label2.setText("进度:")
        self.addPermanentWidget(self.label, stretch=2)
        self.addPermanentWidget(self.label2, stretch=0)
        self.addPermanentWidget(self.progressBar, stretch=4)
        self.progressBar.setRange(0, 500)  # 设置进度条的范围
        self.progressBar.setValue(200)
