import sys, os
import time

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# from view.log_maker import *

from log_maker import *

log = log_maker()

# === 卡片组件 ===
# 版权声明 卡片
class banquanshengming_Card(QFrame):
    def __init__(self):
        super().__init__()
        # self.resize(500, 650)

        self.init_card()

    def init_card(self):
        container = QVBoxLayout()
        container.setContentsMargins(10, 10, 10, 10)
        # 设置卡片的框架形状和阴影效果
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        # 标题
        title_layout = QHBoxLayout()
        titile_label = QLabel("开源软件使用声明")
        # 加粗
        titile_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        # 设置标题在垂直方向可拉伸，水平方向根据内容自适应大小
        # titile_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # 创建一个水平分割线
        hou_layout = QHBoxLayout()
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)

        # 内容
        h1_layout = QHBoxLayout()
        content_label = QLabel("本产品使用了 Pyside6 软件，\nPyside6 是遵循 GNU Lesser General Public License v3（LGPLv3）\n开源协议的软件 。\n\n")
        content_label.setStyleSheet("font-size: 15px;")

        h2_layout = QHBoxLayout()
        c_2_label = QLabel("Pyside6 版权归属于 The Qt Company Ltd. 及其贡献者。保留所有权利。")
        c_2_label.setStyleSheet("font-size: 13px;")

        title_layout.addWidget(titile_label)
        hou_layout.addWidget(horizontal_line)
        h1_layout.addWidget(content_label)
        h2_layout.addWidget(c_2_label)

        container.addLayout(title_layout)
        container.addLayout(hou_layout)
        container.addLayout(h1_layout)
        container.addLayout(h2_layout)

        # 将布局应用到卡片部件上

        # 将布局应用到卡片部件上
        self.setLayout(container)

        # 设置卡片的背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

# LGPLv3许可证 卡片
class xuke_Card(QFrame):
    def __init__(self):
        super().__init__()
        # self.resize(500, 650)

        self.path = os.getcwd()

        self.init_card()

    def init_card(self):
        container = QVBoxLayout()
        container.setContentsMargins(10, 10, 10, 10)
        # 设置卡片的框架形状和阴影效果
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        # 标题
        title_layout = QHBoxLayout()
        titile_label = QLabel("LGPLv3 许可证")
        # 加粗
        titile_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        # 设置标题在垂直方向可拉伸，水平方向根据内容自适应大小
        # titile_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # 创建一个水平分割线
        hou_layout = QHBoxLayout()
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)

        # 内容
        h1_layout = QHBoxLayout()
        content_label = QLabel("欲查看许可证，请点击按钮，或者点击链接进入网站查看许可证\n\n")
        content_label.setStyleSheet("font-size: 15px;")
        
        link_layout = QHBoxLayout()
        # 检测是否被封禁
        ban_yon = QLabel('<a href="https://www.gnu.org/licenses/lgpl-3.0.html">LGPLv3 许可证 官方链接</a>')
        ban_yon.setOpenExternalLinks(True)
        ban_yon.setStyleSheet("font-size: 13px;")

        h2_layout = QHBoxLayout()
        btn = QPushButton("打开本地许可证副本")
        btn.setFixedHeight(30)

        title_layout.addWidget(titile_label)
        hou_layout.addWidget(horizontal_line)
        h1_layout.addWidget(content_label)
        link_layout.addWidget(ban_yon)
        h2_layout.addWidget(btn)

        container.addLayout(title_layout)
        container.addLayout(hou_layout)
        container.addLayout(h1_layout)
        container.addLayout(link_layout)
        container.addLayout(h2_layout)

        # 将布局应用到卡片部件上

        # 将布局应用到卡片部件上
        self.setLayout(container)

        # 设置卡片的背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # 信号槽
        btn.clicked.connect(self.click_btn)

    # === 信号槽函数 ===
    @Slot()
    def click_btn(self):
        
        path = f"{self.path}\\plugins\\LGPLv3.rtf"
        self.open_rtf_file_windows(path)

        log.info("用户打开了本地许可证副本")
    
    # === 非信号槽函数 ===
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

# 获取源代码 卡片
class huoqu_Card(QFrame):
    def __init__(self):
        super().__init__()
        # self.resize(500, 650)

        self.path = os.getcwd()

        self.init_card()

    def init_card(self):
        container = QVBoxLayout()
        container.setContentsMargins(10, 10, 10, 10)
        # 设置卡片的框架形状和阴影效果
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        # 标题
        title_layout = QHBoxLayout()
        # 图标
        icon = QPixmap(f"{self.path}\\plugins\\img\\Github.png")
        icon_label = QLabel()
        icon_label.setPixmap(icon)
        # 将它等比例缩小到18px
        icon_label.setFixedSize(30, 30)
        icon_label.setScaledContents(True)
        # 标题
        titile_label = QLabel("获取PySide6源代码")
        # 加粗
        titile_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        # 设置标题在垂直方向可拉伸，水平方向根据内容自适应大小
        # titile_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # 创建一个水平分割线
        hou_layout = QHBoxLayout()
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)

        # 内容
        h1_layout = QHBoxLayout()
        content_label = QLabel("用户可通过下面的官网链接进入官网获取源码\n\n")
        content_label.setStyleSheet("font-size: 15px;")

        h2_layout = QHBoxLayout()
        c_2_label = QLabel('<a href="https://pypi.org/project/PySide6/">PySide6 官方网站</a>')
        c_2_label.setStyleSheet("font-size: 13px;")
        # 设置超链接
        c_2_label.setOpenExternalLinks(True)

        title_layout.addWidget(icon_label)
        title_layout.addWidget(titile_label)
        hou_layout.addWidget(horizontal_line)
        h1_layout.addWidget(content_label)
        h2_layout.addWidget(c_2_label)

        container.addLayout(title_layout)
        container.addLayout(hou_layout)
        container.addLayout(h1_layout)
        container.addLayout(h2_layout)

        # 将布局应用到卡片部件上

        # 将布局应用到卡片部件上
        self.setLayout(container)

        # 设置卡片的背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

# === 主窗口 ===
class kaiyuanInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        
        self.main_window = parent
        
        self.setObjectName("kaiyuanInterface")
        self.resize(650, 650)
        self.init_ui()

    def init_ui(self):

        # 创建滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # 设置滚动区域内的部件可自适应大小

        # 创建一个容器部件，用来放置其他需要滚动展示的部件
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)

        banquan = banquanshengming_Card()
        xuke = xuke_Card()
        huoqu = huoqu_Card()

        # 设置边距
        banquan.setContentsMargins(50, 25, 50, 0)
        xuke.setContentsMargins(50, 25, 50, 0)
        huoqu.setContentsMargins(50, 25, 50, 0)
        
        container_layout.addWidget(banquan)
        container_layout.addWidget(xuke)
        container_layout.addWidget(huoqu)
        
        container_layout.addStretch(1)

        # 将包含所有部件的容器部件设置为滚动区域的子部件
        scroll_area.setWidget(container_widget)

        # 创建主布局，将滚动区域添加到主布局中
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

        # 样式表
        scroll_area.setStyleSheet("QScrollArea{background: transparent; border: none}"
                                  "QScrollBar:vertical { background: #404040; }")

        # 必须给内部的视图也加上透明背景样式
        container_widget.setStyleSheet("QWidget{background: transparent}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = kaiyuanInterface()
    window.show()
    sys.exit(app.exec())
        
