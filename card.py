import sys

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# 通用卡片组件
class obj_Card(QFrame):
    def __init__(self, title, content):
        super().__init__()

        self.title = title
        self.content = content

        self.init_card()

    def init_card(self):
        container = QVBoxLayout()
        # 设置卡片的框架形状和阴影效果
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        # 创建一个垂直布局用于放置卡片内容
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # 标题
        titile_label = QLabel(self.title)
        # 加粗
        titile_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        # 设置标题在垂直方向可拉伸，水平方向根据内容自适应大小
        # titile_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # 创建一个水平分割线
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)

        # 内容
        content_label = QLabel(self.content)
        content_label.setStyleSheet("font-size: 15px;")

        layout.addWidget(titile_label)
        layout.addWidget(horizontal_line)
        layout.addWidget(content_label)

        # 将布局应用到卡片部件上
        container.addLayout(layout)
        # 将布局应用到卡片部件上
        self.setLayout(container)

        # 设置卡片的背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建主窗口布局
        layout = QVBoxLayout()

        # 创建卡片部件实例
        card = obj_Card(
            title="这是标题",
            content="这是内容"
        )
        layout.addWidget(card)
        layout.addStretch(1)

        # 将布局应用到主窗口上
        self.setLayout(layout)

        # 设置主窗口标题和大小等属性
        self.setWindowTitle("卡片组件示例")
        self.setGeometry(300, 300, 300, 200)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())