# -*- coding: utf-8 -*-
import qdarkstyle
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QLineEdit, QTabWidget, QFormLayout, QRadioButton, QCheckBox


class ClusterTab(QTabWidget):

    def __init__(self, parent=None):
        super(ClusterTab, self).__init__(parent)
        # 设置窗口透明度
        self.setWindowOpacity(0.9)
        # 设置窗口样式
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # 创建3个选项卡小控件窗口
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # 将三个选项卡添加到顶层窗口中
        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")
        self.addTab(self.tab3, "Tab 3")

        # 每个选项卡自定义的内容
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

    def tab1UI(self):
        # 表单布局
        layout = QFormLayout()
        # 添加姓名，地址的单行文本输入框
        layout.addRow('姓名', QLineEdit())
        layout.addRow('地址', QLineEdit())
        # 设置选项卡的小标题与布局方式
        self.setTabText(0, '联系方式')
        self.tab1.setLayout(layout)

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
        self.setTabText(1, '个人详细信息')
        self.tab2.setLayout(layout)

    def tab3UI(self):
        # 水平布局
        layout = QHBoxLayout()

        # 添加控件到布局中
        layout.addWidget(QLabel('科目'))
        layout.addWidget(QCheckBox('物理'))
        layout.addWidget(QCheckBox('高数'))

        # 设置小标题与布局方式
        self.setTabText(2, '教育程度')
        self.tab3.setLayout(layout)
