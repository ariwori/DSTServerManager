# -*- coding: utf-8 -*-
import qdarkstyle
import paramiko
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QGridLayout, QFrame, QVBoxLayout, QPushButton, QWidget, QStackedLayout, QSplitter, QGroupBox, QLabel, QLineEdit, QHBoxLayout, QCheckBox, QSpacerItem, QSizePolicy, QTableWidget, QAbstractItemView, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt
from serverdialog import ServerDialog


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # 设置窗体无边框
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口名称
        self.setWindowTitle("饥荒联机版服务器管理工具")
        # 设置状态栏
        self.status = self.statusBar()
        self.status.showMessage("我是状态栏，用于显示程序运行信息！")
        # 设置初始化的窗口大小
        self.setMinimumWidth(800)
        self.resize(1000, 600)
        # 最开始窗口要居中显示
        self.center()
        # 设置窗口透明度
        self.setWindowOpacity(0.9)
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
        cluster_btns = {}
        for b_index in range(5):
            cluster_btns[b_index] = QPushButton(top_left_frame)
            cluster_btns[b_index].setFixedSize(180, 30)
            cluster_btns[b_index].setText("存档槽 " + str(b_index + 1))
            # cluster_btns[b_index].setEnabled(False)
            top_button_layout.addWidget(cluster_btns[b_index])
        # 删除存档按钮
        delete_cluster_btn = QPushButton(top_left_frame)
        delete_cluster_btn.setFixedSize(180, 30)
        delete_cluster_btn.setText("删除存档")
        top_button_layout.addWidget(delete_cluster_btn)
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

        # 软件设置面板
        path_settings_groupbox = QGroupBox(right_frame)
        path_settings_groupbox.setTitle("本地设置")
        path_settings_groupbox.setFixedHeight(160)
        path_settings_groupbox_layout = QVBoxLayout()
        # 本地客户端路径
        path_widget1_layout = QHBoxLayout()
        local_client_path_label = QLabel()
        local_client_path_label.setText("本地客户端路径:")
        local_client_path_label.setFixedWidth(105)
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
        local_server_path_label.setFixedWidth(105)
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
        local_cluster_path_label.setFixedWidth(105)
        self.local_cluster_path_lineEdit = QLineEdit()
        self.local_cluster_path_btn = QPushButton()
        self.local_cluster_path_btn.setText("浏览")
        path_widget3_layout.addWidget(local_cluster_path_label)
        path_widget3_layout.addWidget(self.local_cluster_path_lineEdit)
        path_widget3_layout.addWidget(self.local_cluster_path_btn)

        path_settings_groupbox_layout.addLayout(path_widget1_layout)
        path_settings_groupbox_layout.addLayout(path_widget2_layout)
        path_settings_groupbox_layout.addLayout(path_widget3_layout)
        path_settings_groupbox.setLayout(path_settings_groupbox_layout)

        sc_settings_groupbox = QGroupBox(right_frame)
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

        server_settings_groupbox = QGroupBox(right_frame)
        server_settings_groupbox.setTitle("云主机设置")
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
        settings_widget = QWidget(right_frame)
        settings_layout.addWidget(path_settings_groupbox)
        settings_layout.addWidget(sc_settings_groupbox)
        settings_layout.addWidget(server_settings_groupbox)
        settings_layout.addWidget(self.save_settings_btn)
        settings_widget.setLayout(settings_layout)
        self.right_layout.addWidget(settings_widget)

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
        self.add_new_server_btn.clicked.connect(self.add_new_server)
        self.delete_server_btn.clicked.connect(self.delete_server)
        self.edit_server_btn.clicked.connect(self.edit_server)
        self.test_server_btn.clicked.connect(self.test_server)

    # 添加新服务器
    def add_new_server(self):
        self.server_table.clearSelection()
        serverDialog = ServerDialog(self)
        serverDialog.setWindowTitle("添加服务器")
        serverDialog.serverSignal.connect(self.add_server)
        serverDialog.exec()

    def add_server(self, server):
        server_row_num = self.server_table.currentRow()
        if server_row_num == -1:
            server_row_num = self.server_table.rowCount()
            self.server_table.setRowCount(server_row_num + 1)
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

    # 设置窗口居中
    def center(self):
        '''
        获取桌面长宽
        获取窗口长宽
        移动
        '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
