import sys, os

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from view.log_maker import *

log = log_maker()

class message(QWidget):
    def __init__(self):
        super().__init__()
        self.init_message()
    def init_message(self):
        # 显示信息框
        msg_box = QMessageBox()
        msg_box.setWindowTitle("注意")
        msg_box.setText("本软件为完全免费软件，并且不存在任何收费，\n\n若你从其他渠道购买到了本免费软件，请立即退款，或者联系作者处理\n\n软件Q群: ")
        # 设置颜色为红色
        msg_box.setStyleSheet("color: red;font-size: 18px;")
        msg_box.exec()

class HomeInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent
        self.setObjectName("home")

        self.path = os.getcwd()

        # 显示警告信息
        QMessageBox.information(self.main_window, "注意", "本软件为完全免费软件，并且不存在任何收费，\n若你从其他渠道购买到了本免费软件，请立即退款，或者联系作者处理\n软件Q群: 897194027")
        # 初始化界面
        self.resize(500, 500)
        self.init_ui()

    def init_ui(self):
        container = QVBoxLayout()

        h1_layout = QHBoxLayout()
        top_label = QLabel("本软件为完全免费软件，并且不存在任何收费，\n若你从其他渠道购买到了本免费软件，请立即退款，或者联系作者处理\n软件Q群: 897194027\n\n")
        top_label.setStyleSheet("color: red;font-size: 18px;")
        
        h2_layout = QHBoxLayout()
        shuo_label = QLabel("本软件实现原理均为之前公开的技术原理，只是把它们程序化了\n不会修改任何游戏文件，也不会修改任何游戏数据\n\n再次强调：使用本软件既视为同意软件安装包内的免责条款\n\n")
        shuo_label.setStyleSheet("color: green; font-size: 18px;")

        h3_layout = QHBoxLayout()
        btn = QPushButton("重新阅读免责条款")
        btn.setFixedHeight(30)

        h1_layout.addWidget(top_label)
        h2_layout.addWidget(shuo_label)
        h3_layout.addWidget(btn)

        container.addLayout(h1_layout)
        container.addLayout(h2_layout)
        container.addLayout(h3_layout)

        self.setLayout(container)

        # 信号
        btn.clicked.connect(self.btn_clicked)
    
    @Slot()
    def btn_clicked(self):
        self.open_rtf_file_windows(f"{self.path}\\plugins\\m.rtf")

    def open_rtf_file_windows(self, file_path):
        """
        在Windows系统下使用默认应用打开rtf文档
        """
        try:
            os.startfile(file_path)
        except FileNotFoundError:
            print(f"文件 {file_path} 不存在，请检查文件路径是否正确。")
            # 写入日志
            log.error(f"文件 {file_path} 不存在，请检查文件路径是否正确。")
        except OSError as e:
            print(f"打开文件出现错误: {e}")
            # 写入日志
            log.error(f"打开文件出现错误: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomeInterface()
    window.show()
    sys.exit(app.exec())