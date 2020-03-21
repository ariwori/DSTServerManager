#!/bin/bash
import sys, hashlib
import qdarkstyle

from PyQt5.QtWidgets import (QApplication, QSplitter, QGridLayout, QHBoxLayout, QPushButton,
                            QTreeWidget, QFrame, QLabel, QHBoxLayout, QMainWindow,
                            QStackedLayout, QWidget, QVBoxLayout, QLineEdit, QRadioButton,
                            QTreeWidgetItem, QDesktopWidget)
from PyQt5.QtCore import Qt, QUrl, QCoreApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # 设置窗口名称
        self.setWindowTitle("华北理工数学建模协会比赛查询")

        # 设置状态栏
        self.status = self.statusBar()
        self.status.showMessage("我在主页面～")

        # 设置初始化的窗口大小
        self.resize(600, 400)

        # 最开始窗口要居中显示
        self.center()

        # 设置窗口透明度
        self.setWindowOpacity(0.9)

        # 设置窗口样式
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # 设置整体布局 左右显示
        pagelayout = QGridLayout()

        # 左侧开始布局
        # 创建左侧部件
        top_left_frame = QFrame(self)
        top_left_frame.setFrameShape(QFrame.StyledPanel)
        #　左边按钮为垂直布局
        button_layout = QVBoxLayout(top_left_frame)

        # 登录按钮
        verifyid_btn = QPushButton(top_left_frame)
        verifyid_btn.setFixedSize(100, 30), verifyid_btn.setText("确认身份")
        button_layout.addWidget(verifyid_btn)
        # 输入用户名　密码按钮
        user_btn = QPushButton(top_left_frame)
        user_btn.setFixedSize(100, 30), user_btn.setText("登录")
        button_layout.addWidget(user_btn)
        # 申请账号　按钮
        registor_btn = QPushButton(top_left_frame)
        registor_btn.setFixedSize(100, 30), registor_btn.setText("申请帐号")
        button_layout.addWidget(registor_btn)
        # 录入信息按钮
        input_btn = QPushButton(top_left_frame)
        input_btn.setFixedSize(100, 30), input_btn.setText("录入信息")
        button_layout.addWidget(input_btn)
        # 查询按钮
        query_btn = QPushButton(top_left_frame)
        query_btn.setFixedSize(100, 30), query_btn.setText("查询信息")
        button_layout.addWidget(query_btn)
        # 建模之家　按钮
        friend_btn = QPushButton(top_left_frame)
        friend_btn.setFixedSize(100, 30), friend_btn.setText("建模园地")
        button_layout.addWidget(friend_btn)
        # 退出按钮
        quit_btn = QPushButton(top_left_frame)
        quit_btn.setFixedSize(100, 30), quit_btn.setText("退出")
        button_layout.addWidget(quit_btn)

        # 左下角为空白 必须要有布局，才可以显示至内容中
        bottom_left_frame = QFrame(self)
        blank_label = QLabel(bottom_left_frame)
        blank_layout = QVBoxLayout(bottom_left_frame)
        blank_label.setText("建模学子的博客")
        blank_label.setFixedHeight(20)
        blank_layout.addWidget(blank_label)
        self.webEngineView = QWebEngineView(bottom_left_frame)
        self.webEngineView.close()
        blank_layout.addWidget(self.webEngineView)

        # 右侧开始布局 对应按钮布局
        right_frame = QFrame(self)
        right_frame.setFrameShape(QFrame.StyledPanel)
        # 右边显示为stack布局
        self.right_layout = QStackedLayout(right_frame)

        # 确认身份
        # 管理员身份
        radio_btn_admin = QRadioButton(right_frame)
        radio_btn_admin.setText("我是管理员，来输入数据的")
        # 游客身份
        radio_btn_user = QRadioButton(right_frame)
        radio_btn_user.setText("我是游客，就来看看")
        # 以处置布局管理器管理
        radio_btn_layout = QVBoxLayout()  # 这里没必要在传入frame，已经有布局了
        radio_btn_widget = QWidget(right_frame)
        radio_btn_layout.addWidget(radio_btn_admin)
        radio_btn_layout.addWidget(radio_btn_user)
        radio_btn_widget.setLayout(radio_btn_layout)
        self.right_layout.addWidget(radio_btn_widget)

        # 登录界面
        user_line = QLineEdit(right_frame)
        user_line.setPlaceholderText("输入账号：")
        user_line.setFixedWidth(400)
        password_line = QLineEdit(right_frame)
        password_line.setPlaceholderText("请输入密码：")
        password_line.setFixedWidth(400)
        login_layout = QVBoxLayout()
        login_widget = QWidget(right_frame)
        login_widget.setLayout(login_layout)
        login_layout.addWidget(user_line)
        login_layout.addWidget(password_line)
        self.right_layout.addWidget(login_widget)

        # 申请帐号
        registor_id = QLineEdit(right_frame)
        registor_id.setPlaceholderText("请输入新帐号：")
        registor_id.setFixedWidth(400)
        registor_psd = QLineEdit(right_frame)
        registor_psd.setPlaceholderText("请输入密码：")
        registor_psd.setFixedWidth(400)
        registor_confirm = QLineEdit(right_frame)
        registor_confirm.setPlaceholderText("请确认密码：")
        registor_confirm.setFixedWidth(400)
        registor_confirm_btn = QPushButton("确认提交")
        registor_confirm_btn.setFixedSize(100, 30)
        registor_layout = QVBoxLayout()
        register_widget = QWidget(right_frame)
        register_widget.setLayout(registor_layout)
        registor_layout.addWidget(registor_id)
        registor_layout.addWidget(registor_psd)
        registor_layout.addWidget(registor_confirm)
        registor_layout.addWidget(registor_confirm_btn)
        self.right_layout.addWidget(register_widget)

        # 建模园地 使用 TreeView　水平布局　应该读取数据库
        self.friend_tree = QTreeWidget(right_frame)
        self.friend_tree.setColumnCount(3)  # 一列
        self.friend_tree.setHeaderLabels(['年级', '人员', '友情链接']) # 设置标题
        root = QTreeWidgetItem(self.friend_tree) # 设置根节点
        self.friend_tree.setColumnWidth(2, 400) # 设置宽度
        # 设置子节点
        root.setText(0, "年级") # 0 表示位置
        root.setText(1, "姓名")
        root.setText(2, "网址")
        child_16 = QTreeWidgetItem(root)
        child_16.setText(0, "16级")

        child_ljw = QTreeWidgetItem(child_16)
        child_ljw.setText(1, "刘佳玮")
        child_ljw.setText(2, "https://muyuuuu.github.io")

        child_17 = QTreeWidgetItem(root)
        child_17.setText(0, "17级")

        child_lqr = QTreeWidgetItem(child_17)
        child_lqr.setText(1, "李秋然")
        child_lqr.setText(2, "https://dgimoyeran.github.io")

        friend_widget = QWidget(right_frame)
        friend_layout = QVBoxLayout()
        friend_widget.setLayout(friend_layout)
        friend_layout.addWidget(self.friend_tree)
        self.right_layout.addWidget(friend_widget)

        self.url = ''  #　后期会获取要访问的url

        # 三分界面，可拖动
        self.splitter1 = QSplitter(Qt.Vertical)
        top_left_frame.setFixedHeight(250)
        self.splitter1.addWidget(top_left_frame)
        self.splitter1.addWidget(bottom_left_frame)

        self.splitter2 = QSplitter(Qt.Horizontal)
        self.splitter2.addWidget(self.splitter1)
        #　添加右侧的布局
        self.splitter2.addWidget(right_frame)

        # 窗口部件添加布局
        widget = QWidget()
        pagelayout.addWidget(self.splitter2)
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        # 函数功能区
        verifyid_btn.clicked.connect(self.show_verifyid_page)
        user_btn.clicked.connect(self.show_login_page)
        registor_btn.clicked.connect(self.show_register_page)
        friend_btn.clicked.connect(self.show_friend_page)
        self.friend_tree.clicked.connect(self.show_firend_web)
        quit_btn.clicked.connect(self.quit_act)

    def init(self):
        # 刚开始要管理浏览器，否则很丑
        self.webEngineView.close()
        # 注意先后顺序，resize　在前面会使代码无效
        self.splitter1.setMinimumWidth(150)
        self.splitter2.setMinimumWidth(250)
        self.resize(600, 400)

    # TreeView 的点击事件
    def show_firend_web(self):
        item = self.friend_tree.currentItem()
        if item.text(2)[:4] == "http":
            self.url = item.text(2)
            self.resize(1800, 1200)
            self.webEngineView.show()
            self.splitter1.setFixedWidth(1400)
            self.webEngineView.load(QUrl(self.url))

    # 展示树形结构
    def show_friend_page(self):
        self.init()
        self.center()
        self.right_layout.setCurrentIndex(3)

    # 显示注册帐号的页面
    def show_register_page(self):
        self.init()
        self.center()
        self.right_layout.setCurrentIndex(2)

    # 显示登录的页面
    def show_login_page(self):
        self.init()
        self.center()
        self.right_layout.setCurrentIndex(1)

    # stacklayout 布局，显示验证身份的页面
    def show_verifyid_page(self):
        self.init()
        self.center()
        self.right_layout.setCurrentIndex(0)

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

    # 退出按钮 有信息框的提示　询问是否确认退出
    def quit_act(self):
        # sender 是发送信号的对象
        sender = self.sender()
        print(sender.text() + '键被按下')
        qApp = QApplication.instance()
        qApp.quit()


if __name__ == '__main__':
    # 高分屏自动适配
    # QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
