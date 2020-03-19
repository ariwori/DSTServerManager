# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QPushButton, QSizePolicy
from PyQt5.QtCore import QCoreApplication
from ui_design.ui_mainwindow import Ui_MainWindow


class MainCode(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.pushButtons = {}
        _translate = QCoreApplication.translate
        for i in range(0, 10):
            self.pushButtons[i] = QPushButton(self.verticalLayoutWidget)
            sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(5)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.pushButtons[i].sizePolicy().hasHeightForWidth())
            self.pushButtons[i].setSizePolicy(sizePolicy)
            self.pushButtons[i].setObjectName("pushButton_"+str(i))
            self.pushButtons[i].setText(_translate("MainWindow", "存档槽"+str(i+1)))
            self.verticalLayout.addWidget(self.pushButtons[i])
