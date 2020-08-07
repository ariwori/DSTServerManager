# -*- coding: utf-8 -*-
import os
import qdarkstyle
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QGridLayout, QFrame, QVBoxLayout, QPushButton, QWidget, QStackedLayout, QSplitter, QSpacerItem, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt
from maintab import MainTab
from settingswindow import SettingsWidget
from globalvar import ROOT_DIR, CLUSTER_DIR, CONFIG_DIR, TEMP_FILE
from config import GlobalConfig
import shutil
import sys
import distutils


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi()
        self.initData()

    def setupUi(self):
        # 设置窗体无边框
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口名称
        self.setWindowTitle("饥荒联机版服务器管理工具")
        # 设置状态栏
        self.status = self.statusBar()
        self.status.showMessage("我是状态栏，用于显示程序运行信息！")
        # 设置初始化的窗口大小
        self.setMinimumWidth(800)
        self.resize(1100, 700)
        # 最开始窗口要居中显示
        self.center()
        # 设置窗口透明度
        # self.setWindowOpacity(0.9)
        # 设置窗口样式
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        # 设置整体布局 左右显示
        pagelayout = QGridLayout()
        '''
        开始左上侧布局
        '''
        # 创建左上侧部件
        top_left_frame = QFrame(self)
        top_left_frame.setFrameShape(QFrame.StyledPanel)
        # 按钮垂直布局
        top_button_layout = QVBoxLayout(top_left_frame)
        # 五个存档槽按钮
        self.cluster_btns = {}
        for b_index in range(5):
            self.cluster_btns[b_index] = QPushButton(top_left_frame)
            self.cluster_btns[b_index].setFixedSize(180, 30)
            self.cluster_btns[b_index].setText("存档槽 " + str(b_index + 1))
            # cluster_btns[b_index].setEnabled(False)
            self.cluster_btns[b_index].index = b_index + 1
            self.cluster_btns[b_index].clicked.connect(self.set_cluster)
            top_button_layout.addWidget(self.cluster_btns[b_index])
        # 删除存档按钮
        delete_cluster_btn = QPushButton(top_left_frame)
        delete_cluster_btn.setFixedSize(180, 30)
        delete_cluster_btn.setText("删除存档")
        top_button_layout.addWidget(delete_cluster_btn)
        delete_cluster_btn.clicked.connect(self.deleteCluster)
        # 导出远程存档按钮
        export_remote_cluster_btn = QPushButton(top_left_frame)
        export_remote_cluster_btn.setText("导出远程存档")
        export_remote_cluster_btn.setFixedSize(180, 30)
        top_button_layout.addWidget(export_remote_cluster_btn)
        # 导入本地存档按钮
        import_local_cluster_btn = QPushButton(top_left_frame)
        import_local_cluster_btn.setText("导入本地存档")
        import_local_cluster_btn.setFixedSize(180, 30)
        top_button_layout.addWidget(import_local_cluster_btn)
        '''
        开始左下侧布局
        '''
        # 创建左下侧部件
        bottom_left_frame = QFrame(self)
        bottom_left_frame.setFrameShape(QFrame.StyledPanel)
        # 按钮垂直布局
        bottom_button_layout = QVBoxLayout(bottom_left_frame)
        # 控制台按钮
        console_btn = QPushButton(bottom_left_frame)
        console_btn.setText("控制台")
        console_btn.setFixedSize(180, 30)
        bottom_button_layout.addWidget(console_btn)
        # 软件设置按钮
        settings_btn = QPushButton(bottom_left_frame)
        settings_btn.setText("软件设置")
        settings_btn.setFixedSize(180, 30)
        settings_btn.clicked.connect(self.soft_settings)
        bottom_button_layout.addWidget(settings_btn)
        # 导出远程存档按钮
        browser_online_server_btn = QPushButton(bottom_left_frame)
        browser_online_server_btn.setText("浏览在线服务器")
        browser_online_server_btn.setFixedSize(180, 30)
        bottom_button_layout.addWidget(browser_online_server_btn)
        # 导出远程存档按钮
        help_and_about_btn = QPushButton(bottom_left_frame)
        help_and_about_btn.setText("使用帮助和关于")
        help_and_about_btn.setFixedSize(180, 30)
        bottom_button_layout.addWidget(help_and_about_btn)
        # 弹簧控件
        spacerItem = QSpacerItem(20, 20, QSizePolicy.Minimum,
                                 QSizePolicy.Expanding)
        bottom_button_layout.addItem(spacerItem)
        '''
        开始右侧布局
        '''
        # 右侧开始布局 对应按钮布局
        right_frame = QFrame(self)
        right_frame.setFrameShape(QFrame.StyledPanel)
        # 右边显示为stack布局
        self.right_layout = QStackedLayout(right_frame)

        self.settings_widget = SettingsWidget()
        self.cluster_tab = MainTab()
        self.right_layout.addWidget(self.cluster_tab)
        self.right_layout.addWidget(self.settings_widget)

        # 划分界面
        splitterV = QSplitter(Qt.Vertical)
        splitterV.addWidget(top_left_frame)
        splitterV.addWidget(bottom_left_frame)
        # 固定左上高度
        top_left_frame.setFixedHeight(330)
        splitterH = QSplitter(Qt.Horizontal)
        splitterH.addWidget(splitterV)
        splitterH.addWidget(right_frame)
        # 固定左侧宽度
        top_left_frame.setFixedWidth(200)
        # bottom_left_frame.setFixedWidth(200)

        # 窗口部件添加布局
        widget = QWidget()
        pagelayout.addWidget(splitterH)
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        # 按钮函数绑定

    def soft_settings(self):
        self.right_layout.setCurrentIndex(1)

    # 存档按钮状态刷新
    def refresh_cluster_btn_state(self, index):
        for i in self.cluster_btns:
            if index == self.cluster_btns[i].index:
                self.cluster_btns[i].setStyleSheet("")
            else:
                self.cluster_btns[i].setStyleSheet("color:gray")

    # 存档设置
    def set_cluster(self):
        self.current_cluster_index = self.sender().index
        self.tempconfig.set("TEMP", "cluster_index", str(self.current_cluster_index))
        self.tempconfig.save(TEMP_FILE)
        self.refresh_cluster_btn_state(self.current_cluster_index)
        self.right_layout.setCurrentIndex(0)
        self.mk_cluster_dir()
        self.cluster_tab.cluster_settings_tab.current_cluster_file = os.path.join(self.current_cluster_folder, "cluster.ini")
        self.cluster_tab.cluster_settings_tab.read_cluster_data(self.cluster_tab.cluster_settings_tab.current_cluster_file)
        self.cluster_tab.cluster_settings_tab.setServerIP(self.cluster_tab.cluster_settings_tab.masterip, self.cluster_tab.cluster_settings_tab.getServerIP())
        self.cluster_tab.shard_settings_tab.initShardTab()

    def deleteCluster(self):
        cindex = self.current_cluster_index
        delm = QMessageBox.warning(self, "删除警告", "你确定要删除存档槽" + str(cindex) + "?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if delm == QMessageBox.Yes:
            sdir = os.path.join(CLUSTER_DIR, "Cluster_" + str(cindex))
            if os.path.exists(sdir):
                shutil.rmtree(sdir)
            self.right_layout.setCurrentIndex(0)
            self.mk_cluster_dir()
            self.cluster_tab.setCurrentIndex(0)
            self.cluster_tab.cluster_settings_tab.current_cluster_file = os.path.join(self.current_cluster_folder, "cluster.ini")
            self.cluster_tab.cluster_settings_tab.read_cluster_data(self.cluster_tab.cluster_settings_tab.current_cluster_file)
            self.cluster_tab.cluster_settings_tab.setServerIP(self.cluster_tab.cluster_settings_tab.masterip, self.cluster_tab.cluster_settings_tab.getServerIP())
            self.cluster_tab.shard_settings_tab.initShardTab()
            QMessageBox.information(self, "删除完毕", "存档槽" + str(cindex) + "已删除并重置！", QMessageBox.Yes)

    def mk_cluster_dir(self):
        self.current_cluster_folder = os.path.join(CLUSTER_DIR, "Cluster_" + str(self.current_cluster_index))
        if not os.path.exists(self.current_cluster_folder):
            os.mkdir(self.current_cluster_folder)

    def init_cluster_data(self, index):
        self.mk_cluster_dir()
        self.right_layout.setCurrentIndex(0)
        self.refresh_cluster_btn_state(self.current_cluster_index)
        self.cluster_tab.cluster_settings_tab.current_cluster_file = os.path.join(self.current_cluster_folder, "cluster.ini")
        self.cluster_tab.cluster_settings_tab.read_cluster_data(self.cluster_tab.cluster_settings_tab.current_cluster_file)

    def resource_path(self, relative_path):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def initDir(self):
        if not os.path.exists(ROOT_DIR):
            os.mkdir(ROOT_DIR)
        if not os.path.exists(CLUSTER_DIR):
            os.mkdir(CLUSTER_DIR)
        if not os.path.exists(CONFIG_DIR):
            print(self.resource_path("Configs"))
            distutils.dir_util.copy_tree(self.resource_path("Configs"), CONFIG_DIR)

    def initData(self):
        self.initDir()
        self.tempconfig = GlobalConfig(TEMP_FILE)
        if os.path.exists(TEMP_FILE):
            self.current_cluster_index = int(self.tempconfig.get("TEMP", "cluster_index"))
        else:
            self.current_cluster_index = 1
        self.init_cluster_data(self.current_cluster_index)

    # 设置窗口居中
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
