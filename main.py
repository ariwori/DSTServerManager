# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, Qt
from mainwindow import MainWindow

if __name__ == '__main__':
    # 高分屏自动适配
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
