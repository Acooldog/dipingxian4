import sys

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from view.HomeInterface import *
from view.Zaxiang import *
from view.xiufu import *
from view.kaiyuan import *

from check_up import *
from send_email import *
from update import *
from remove_old_exe import *


# === 多线程 ===
# 检查是否被作者关闭，版本是否被作者关闭 检查更新
class check_ban_and_version(QThread):
    check_finished = Signal(int)
    def __init__(self, parent=None):
        super().__init__()
        self.main_window = parent

    def run(self):
        self.start = check_update()
        result = self.start.main()

        # 需要更新
        if result == -1:
            # 没用管理员方式启动
            self.check_finished.emit(-1)
        elif result == 0:
            # 作者关闭版本
            self.check_finished.emit(0)
        elif result == 66:
            # 作者关闭版本，并且启动自毁程序
            self.check_finished.emit(66)
        elif result == 11:
            # 版本号不一致且需要强制更新
            self.check_finished.emit(11)
        elif result == 1:
            # 需要更新
            self.check_finished.emit(1)

# 发送邮件
class EmailWork(QThread):

    def run(self):

        # 发送邮件
        login_send_email()

# 检测并删除老版本exe
class check_and_del_exe(QThread):

    check_finished = Signal()
    
    def __init__(self, parent=None):
        super().__init__()
        self.main_window = parent

    def run(self):
        while True:
            self.sta = remove_old_exe()
            result = self.sta.main()

            if result:
                self.check_finished.emit()
                break
        


# 自定义消息框
class CustomMessageBox:
    def __init__(self, parent=None):

        self.main_window = parent
        # 创建消息框
        self.msg_box = QMessageBox()
        self.msg_box.setText("有新版本更新，是否更新？")
        self.msg_box.setWindowTitle("需要更新")

        # 创建按钮并添加到消息框
        self.button1 = self.msg_box.addButton("这就更新", QMessageBox.ButtonRole.AcceptRole)
        self.button1.setFixedHeight(30)
        self.button2 = self.msg_box.addButton("下次一定", QMessageBox.ButtonRole.RejectRole)
        self.button2.setFixedHeight(30)

        # 连接按钮点击信号到对应的槽函数
        self.button1.clicked.connect(self.button1_clicked)
        self.button2.clicked.connect(self.button2_clicked)

    # == 槽函数 ==
    # 点击更新
    @Slot(int)
    def button1_clicked(self, button_role):
        # QMessageBox.information(self.msg_box, "提示", "请前往Q群获取更新\n在线更新功能暂未开发")
        self.update = updateInterface(self.main_window)
        self.update.show()
        # self.main_window.close()
        # 在这里添加按钮1点击后的具体逻辑

    # 点击下次一定
    @Slot(int)
    def button2_clicked(self, button_role):
        # 在这里添加按钮2点击后的具体逻辑
        # 写入到日志
        log.info("用户选择下次一定")

    def show(self):
        self.msg_box.exec()
    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小等属性
        self.setWindowTitle(f"地平线修复工具 {Diconfig.Version}")
        # self.setGeometry(300, 300, 300, 200)
        self.resize(650, 650)

        self.path = os.getcwd()
        # 创建多线程
        self.check_thread = check_ban_and_version(self)
        self.check_thread.check_finished.connect(self.check_finished)
        # 开始检查
        self.check_thread.start()
        # 发送邮件
        self.send_email = EmailWork()
        self.send_email.start()

        self.setWindowIcon(QIcon(f"{self.path}\\plugins\\ke.ico"))

        self.window_ui()

    def window_ui(self):

        # 创建中央部件和布局（用于放置其他内容）
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 创建工具栏（导航栏）
        toolbar = QToolBar("导航栏")
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # 创建堆叠式窗口部件来管理页面
        self.stacked_widget = QStackedWidget()
        self.page1 = HomeInterface(self)
        self.page2 = zaxiangInterface(self)
        self.page3 = xiufiuInterface(self)
        self.kaiuan = kaiyuanInterface(self)
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)
        self.stacked_widget.addWidget(self.kaiuan)
        layout.addWidget(self.stacked_widget)

        # 创建导航按钮并添加到工具栏
        button1 = QPushButton("主页")
        button1.clicked.connect(self.show_page1)
        toolbar.addWidget(button1)

        button2 = QPushButton("分步修复")
        button2.clicked.connect(self.show_page2)
        toolbar.addWidget(button2)

        button3 = QPushButton("修复")
        button3.clicked.connect(self.show_page3)
        toolbar.addWidget(button3)

        kaiyuan_btn = QPushButton("开源协议")
        kaiyuan_btn.clicked.connect(self.show_kaiyuan)
        toolbar.addWidget(kaiyuan_btn)

        # 按钮样式表
        kaiyuan_btn.setStyleSheet("color: red;")

        # 多线程
        # self.start_check_exe()
    
    # == 槽函数 == 
    # 开源协议
    @Slot()
    def show_kaiyuan(self):
        self.stacked_widget.setCurrentWidget(self.kaiuan)

    # 主页
    @Slot()
    def show_page1(self):
        self.stacked_widget.setCurrentWidget(self.page1)

    # 分步修复
    @Slot()
    def show_page2(self):
        self.stacked_widget.setCurrentWidget(self.page2)

    # 修复
    @Slot()
    def show_page3(self):
        self.stacked_widget.setCurrentWidget(self.page3)

    # == 多线程函数 ==
    # 检测老版本
    def start_check_exe(self):
        self.sta_check_old = check_and_del_exe(self)
        self.sta_check_old.check_finished.connect(self.check_exe_finished)
        self.sta_check_old.start()

    # == 多线程返回函数 == 
    @Slot(int)
    def check_finished(self, result):
        if result == -1:
            QMessageBox.critical(self, "错误", "此程序需要以管理员身份运行。请重新以管理员身份启动程序。")
            sys.exit()
        elif result == 0:
            # 作者关闭版本
            QMessageBox.critical(self, "错误", "版本被作者关闭")
            sys.exit()
        elif result == 66:
            # 作者关闭版本，并且启动自毁程序
            QMessageBox.critical(self, "错误", "版本被作者关闭")
            sys.exit()
        elif result == 11:
            # 版本号不一致且需要强制更新
            must_box = QMessageBox.critical(self, "错误", "版本号不一致且\n\n此次版本为强制更新版本\n\n点击 ok 开始更新", QMessageBox.Ok)
            if must_box == QMessageBox.Ok:
                self.update = updateInterface(self)
                self.update.show()

        elif result == 1:
            # 需要更新
            self.mes = CustomMessageBox(self)
            self.mes.show()
            # self.close()

    @Slot()
    def check_exe_finished(self):
        time.sleep(1)
        # 删除完成
        QMessageBox.information(self, "提示", "更新完成")
        print("========================= 已经删除老版本 =========================")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
