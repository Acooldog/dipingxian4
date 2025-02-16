import sys
import time

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from view.zaxiangOBJ import *
from view.log_maker import *

# from zaxiangOBJ import *
# from log_maker import *

# 实例化函数
zaxiang = Zaxiang()
# 初始化日志
log = log_maker()

# 计数器
class SharedData:
    def __init__(self):

        '''

        完全禁用目前已知与地平线服务冲突专属计数器

        变量:
            self.counter: 计数器
            self.openBan: 完全禁用目前已知与地平线服务冲突计数器
            self.openXbox: 完全禁用Xbox游戏联机计数器

        '''

        # 完全禁用目前已知与地平线服务冲突专属计数器
        self.counter = 0
        self.openBan = 0
        self.openXbox = 0

# == 多线程 ==
# 检测Teredo参数 多线程
class check_Teredo_thread(QThread):
    result_info = Signal(str)
    check_finished = Signal(bool)
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent

    def run(self):
        result = zaxiang.seach_tendo()

        # 发送检测的信息
        self.result_info.emit(result)
        print("====1====")
        # 记录到日志
        log.info(f"用户的Teredo参数检测结果: {result}")

        if "enterpriseclient" in result and "错误" not in result:

            self.check_finished.emit(1)

        elif "错误" in result:

            self.check_finished.emit(-1)
        
        else:
            
            self.check_finished.emit(-2)

# 修复hosts文件 多线程
class hosts_thread(QThread):
    hosts_finished = Signal(bool)
    def __init__(self):
        super().__init__()
        
    def run(self):
        # 修复hosts文件
        result = zaxiang.host_file()
        if result:
            log.info("hosts文件修复成功")
        else:
            log.error("hosts文件修复失败")

        self.hosts_finished.emit(result)

# 重置网络 多线程
class reset_network_thread(QThread):
    reset_network_finished = Signal(bool)
    def __init__(self):
        super().__init__()

    def run(self):
        # 重置网络
        result = zaxiang.reset_winsock()
        if result:
            log.info("重置网络成功")
        else:
            log.error("重置网络失败")

        self.reset_network_finished.emit(result)

# 完全禁用目前已知与地平线服务冲突  多线程
class ShutdownWorker(QThread):
    set_values = Signal(int)
    shutdown_finished = Signal()
    def __init__(self, parent=None):
        super().__init__()
        self.main_window = parent

    def run(self):
        all_count = len(Diconfig.disName)
        self.set_values.emit(0)
        self.main_window.tishi_label.setText("完全禁用目前已知与地平线服务冲突")
        for index, i in enumerate(Diconfig.disName):
            zaxiang.stop_service_by_display_name(i)
            shard_data = SharedData()
            shard_data.counter += 1
            self.set_values.emit(index + 1)
        self.shutdown_finished.emit()

# 启用禁用掉的冲突服务  多线程
class StratServersWorker(QThread):
    open_finished = Signal()
    progress_signal = Signal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.main_window = parent

    def run(self):

        # all_count = len(Diconfig.disName)
        self.main_window.tishi_label.setText("启用被禁用掉的服务中")
        self.progress_signal.emit(0)  # 初始进度为 0
        # 启用被禁用的服务
        for index, i in enumerate(Diconfig.disName):
            zaxiang.stat_service_by_display_name(i)
            zaxiang.start_and_set_auto_service_by_display_name(i)
            shard_data = SharedData()
            # 计数器
            shard_data.openBan += 1
            self.progress_signal.emit(index + 1)  # 发射当前进度
        self.open_finished.emit()

# 启用必要的xbox服务 多线程
class openXboxServersWorker(QThread):
    xboxfinished = Signal()
    progress_signal = Signal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.main_window = parent

        # pythoncom.CoInitialize()  # 添加这行初始化 COM 库

    def run(self):
        self.progress_signal.emit(0)  # 初始进度为 0
        self.main_window.tishi_label.setText("启用必要的xbox服务中")
        # 手动
        for self.index, i in enumerate(Diconfig.man_safe):
            xboxServers().stat_xbox_service_by_display_name(i)
            xboxServers().start_and_set_manual_service_by_display_name(i)
            shard_data = SharedData()
            # 计数器
            shard_data.openBan += 1
            print(f'手动 {self.index + 1}')
            self.progress_signal.emit(self.index + 1)  # 发射当前进度

        # 继承数值
        self.index_auto = self.index
        # 自动
        for i in Diconfig.auto_safe:
            xboxServers().start_and_set_auto_service_by_display_name(i)
            shard_data = SharedData()
            # 计数器
            shard_data.openBan += 1
            self.index_auto += 1
            print(f'自动 {self.index_auto + 1}')
            self.progress_signal.emit(self.index_auto + 1)  # 发射当前进度

        self.xboxfinished.emit()

# 启用防火墙
class OpenFirewallWorker(QThread):
    open_fire_finished = Signal(bool)
    def __init__(self):
        super().__init__()
        
    def run(self):
        result = zaxiang.check_and_enable_windows_firewall()
        self.open_fire_finished.emit(result)

# 关闭防火墙
class CloseFirewallWorker(QThread):
    close_fire_finished = Signal(bool)
    def __init__(self):
        super().__init__()
    
    def run(self):
        result = zaxiang.disable_firewall()
        self.close_fire_finished.emit(result)

# 持续检测防火墙状态
class CheckFirewallStatusThread(QThread):
    def __init__(self, parent=None):
        super().__init__()
        self.main_window = parent

    def run(self):
        while True:
            firewall_status = self.check_firewall_status()
            if firewall_status:
                self.main_window.check_firewall_label.setText("当前防火墙状态: 已开启")
                self.main_window.check_firewall_label.setStyleSheet("color: #8aa0e0;")
            else:
                self.main_window.check_firewall_label.setText("当前防火墙状态: 已关闭")
                self.main_window.check_firewall_label.setStyleSheet("color: red;")
            time.sleep(1)  # 每隔1秒检查一次防火墙状态

    def check_firewall_status(self):
        try:
            # 打开注册表键，这里是针对Windows系统中与防火墙相关的注册表位置
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile")
            value, _ = winreg.QueryValueEx(key, "EnableFirewall")
            winreg.CloseKey(key)
            if value == 1:
                return True
            else:
                return False
        except FileNotFoundError:
            return False



# == 卡片组件 ==
# 模板
class obj_Card(QFrame):
    def __init__(self, title, content):
        super().__init__()

        self.title = title
        self.content = content

        self.init_card()

    def init_card(self):
        container = QVBoxLayout()
        container.setContentsMargins(10, 10, 10, 10)
        # 设置卡片的框架形状和阴影效果
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

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
        h1_layout = QHBoxLayout()
        content_label = QLabel(self.content)
        content_label.setStyleSheet("font-size: 15px;")

        h1_layout.addWidget(content_label)

        container.addWidget(titile_label)
        container.addWidget(horizontal_line)
        container.addWidget(content_label)

        container.addLayout(h1_layout)

        # 将布局应用到卡片部件上

        # 将布局应用到卡片部件上
        self.setLayout(container)

        # 设置卡片的背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

# 检测Teredo参数 卡片组件
class check_Teredo_Card(QFrame):
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent

        self.init_card()

    def init_card(self):
        container = QVBoxLayout()
        container.setContentsMargins(10, 10, 10, 10)
        # 设置卡片的框架形状和阴影效果
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        # 标题
        title_layout = QHBoxLayout()
        titile_label = QLabel("检测Teredo参数")
        # 加粗
        titile_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        # 设置标题在垂直方向可拉伸，水平方向根据内容自适应大小
        # titile_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        hor_layout = QHBoxLayout()
        # 创建一个水平分割线
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)

        # 内容
        h1_layout = QHBoxLayout()
        content_label = QLabel("本修复选项可以检测Teredo参数，\n"
                               "检测后会检测当前Teredo参数是否正常\n\n")
        content_label.setStyleSheet("font-size: 13px;")

        h3_layout = QHBoxLayout()
        sta_btn = QPushButton("开始检测")
        sta_btn.setFixedHeight(50)

        bar_layout = QHBoxLayout()
        # 创建进度条
        self.progress_bar = QProgressBar(self)
        # 设置范围为0 - 0，使其成为不确定进度条
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)

        title_layout.addWidget(titile_label)
        hor_layout.addWidget(horizontal_line)
        h1_layout.addWidget(content_label)
        h3_layout.addWidget(sta_btn)
        bar_layout.addWidget(self.progress_bar)

        container.addLayout(title_layout)
        container.addLayout(hor_layout)
        container.addLayout(h1_layout)
        container.addLayout(h3_layout)
        container.addLayout(bar_layout)

        # 将布局应用到卡片部件上
        self.setLayout(container)

        # 设置卡片的背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # 信号
        sta_btn.clicked.connect(self.sta_btn_clicked)

    # == 普通槽函数 ==
    # 开始检测按钮
    @Slot()
    def sta_btn_clicked(self):
        log.info("用户点击了 检测Teredo参数 里的 开始检测 按钮")
        self.progress_bar.setVisible(True)
        # 检测Teredo参数 多线程
        self.check_Teredo_th = check_Teredo_thread(self.main_window)
        # 连接信号和槽
        self.check_Teredo_th.result_info.connect(self.result_info)
        self.check_Teredo_th.check_finished.connect(self.check_Teredo_finished)
        self.check_Teredo_th.start()

    # == 多线程连接槽函数 ==
    # 检测Teredo参数 多线程 检测消息信号
    def result_info(self, result):
        QMessageBox.information(self.main_window, "检测到的参数: ", result)
    # 检测Teredo参数 多线程 完成信号
    @Slot()
    def check_Teredo_finished(self, result):
        self.progress_bar.setVisible(False)
        if result:
            # 记录到日志
            log.info("Teredo参数检测结果: Teredo参数正常")
            QMessageBox.information(self.main_window, "Teredo参数检测结果:", "Teredo参数正常")

        elif result == -1:
            # 记录到日志
            log.error("Teredo参数检测结果: Teredo参数异常第一分支")
            QMessageBox.critical('Teredo参数检测结果', 'Teredo参数异常: 无法连接UDP\n'
                         "请检查你的“更改直连服务器”功能\n是否跟“XboxLive hosts文件修改功能”混用\n"
                         "\n"
                         "这两个功能不可以使用，否则会导致无法通过UDP连接服务器\n")
        
        else:
            log.error("Teredo参数检测结果: Teredo参数异常第二分支")
            QMessageBox.critical('Teredo参数检测结果', 'Teredo参数异常: 无法连接Teredo服务器\n'
                         "请先自动修复一遍，再去“更改直连服务器”选项中更改一个新的服务器\n"
                         "如果你的网络不适合直连服务器， 请点击“连接xbox中介服务器”, 进行连接"
                         "\n"
                         "\n")

# hosts修复 卡片组件
class hosts_Card(QFrame):
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent

        self.init_card()

    def init_card(self):
        container = QVBoxLayout()
        container.setContentsMargins(10, 10, 10, 10)
        # 设置卡片的框架形状和阴影效果
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        # 标题
        title_layout = QHBoxLayout()
        titile_label = QLabel("hosts文件修复")
        # 加粗
        titile_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        # 设置标题在垂直方向可拉伸，水平方向根据内容自适应大小
        # titile_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        hor_layout = QHBoxLayout()
        # 创建一个水平分割线
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)

        # 内容
        h1_layout = QHBoxLayout()
        content_label = QLabel("本修复选项可以hosts状态，\n"
                               "如果hosts文件受损可以使用此选项\n\n")
        content_label.setStyleSheet("font-size: 13px;")

        bao_layout = QHBoxLayout()
        bao_label = QLabel("此选项已包含于“自动修复(关闭防火墙)”、“自动修复(开启防火墙)”中")
        bao_label.setStyleSheet("font-size: 13px; color: green;")

        h3_layout = QHBoxLayout()
        sta_btn = QPushButton("开始修复")
        sta_btn.setFixedHeight(50)

        bar_layout = QHBoxLayout()
        # 创建进度条
        self.progress_bar = QProgressBar(self)
        # 设置范围为0 - 0，使其成为不确定进度条
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)

        title_layout.addWidget(titile_label)
        hor_layout.addWidget(horizontal_line)
        h1_layout.addWidget(content_label)
        bao_layout.addWidget(bao_label)
        h3_layout.addWidget(sta_btn)
        bar_layout.addWidget(self.progress_bar)

        container.addLayout(title_layout)
        container.addLayout(hor_layout)
        container.addLayout(h1_layout)
        container.addLayout(bao_layout)
        container.addLayout(h3_layout)
        container.addLayout(bar_layout)

        # 将布局应用到卡片部件上
        self.setLayout(container)

        # 设置卡片的背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # 信号
        sta_btn.clicked.connect(self.sta_btn_clicked)

    # == 普通槽函数 ==
    # 开始修复按钮
    @Slot()
    def sta_btn_clicked(self):
        log.info("用户点击了 hosts修复 里的 开始修复 按钮")
        self.progress_bar.setVisible(True)
        # hosts修复 多线程
        self.hosts_th = hosts_thread()
        # 连接信号和槽
        self.hosts_th.hosts_finished.connect(self.hosts_finished)
        self.hosts_th.start()

    # == 多线程连接槽函数 == 
    # hosts修复 多线程 完成信号
    @Slot()
    def hosts_finished(self, result):
        if result:
            self.progress_bar.setVisible(False)
            # 显示信息框
            QMessageBox.information(self.main_window, "成功", "修复成功")
        
        else:
            self.progress_bar.setVisible(False)
            # 显示信息框
            QMessageBox.information(self.main_window, "失败", "修复失败")

# 启用/禁用防火墙 卡片组件
class open_and_close_firewall_Card(QFrame):
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent

        self.init_card()

    def init_card(self):
        container = QVBoxLayout()
        container.setContentsMargins(10, 10, 10, 10)
        # 设置卡片的框架形状和阴影效果
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        # 标题
        title_layout = QHBoxLayout()
        titile_label = QLabel("禁用/启用防火墙")
        # 加粗
        titile_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        # 设置标题在垂直方向可拉伸，水平方向根据内容自适应大小
        # titile_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        hor_layout = QHBoxLayout()
        # 创建一个水平分割线
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)

        # 内容
        h1_layout = QHBoxLayout()
        content_label = QLabel("本选项可以一键关闭或者开启防火墙\n\n"
                               "有些人开防火墙才能进去，有些人关闭防火墙才能进去，所以自行测试\n\n"
                               "\n")
        content_label.setStyleSheet("font-size: 13px;")

        check_fire_wall_layout = QHBoxLayout()
        self.check_firewall_label = QLabel("当前防火墙状态: 未检测")

        bao_layout = QHBoxLayout()
        bao_label = QLabel("\n此选项已分别已包含于“自动修复(关闭防火墙)”、“自动修复(开启防火墙)”中")
        bao_label.setStyleSheet("font-size: 13px; color: green;")

        h3_layout = QHBoxLayout()
        sta_btn = QPushButton("禁用")
        sta_btn.setFixedHeight(50)
        open_btn = QPushButton("启用")
        open_btn.setFixedHeight(50)

        tishi_layout = QHBoxLayout()
        self.tishi_label = QLabel("")
        self.tishi_label.setStyleSheet("font-size: 13px; color: green;")
        self.tishi_label.setVisible(False)

        bar_layout = QHBoxLayout()
        # 创建进度条
        self.progress_bar = QProgressBar(self)
        # 设置范围为0 - 0，使其成为不确定进度条
        self.progress_bar.setRange(0, len(Diconfig.disName))
        self.progress_bar.setVisible(False)

        title_layout.addWidget(titile_label)
        hor_layout.addWidget(horizontal_line)
        h1_layout.addWidget(content_label)
        check_fire_wall_layout.addWidget(self.check_firewall_label)
        bao_layout.addWidget(bao_label)
        h3_layout.addWidget(sta_btn)
        h3_layout.addWidget(open_btn)
        tishi_layout.addStretch(1)
        tishi_layout.addWidget(self.tishi_label)
        tishi_layout.addStretch(1)
        bar_layout.addWidget(self.progress_bar)

        container.addLayout(title_layout)
        container.addLayout(hor_layout)
        container.addLayout(h1_layout)
        container.addLayout(check_fire_wall_layout)
        container.addLayout(bao_layout)
        container.addLayout(h3_layout)
        container.addLayout(tishi_layout)
        container.addLayout(bar_layout)

        # 将布局应用到卡片部件上
        self.setLayout(container)

        # 设置卡片的背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # 多线程
        # 持续检测防火墙开启状态
        self.open_and_close_firewall_th = CheckFirewallStatusThread(self)
        self.open_and_close_firewall_th.start()
        # 信号
        sta_btn.clicked.connect(self.sta_btn_clicked)
        open_btn.clicked.connect(self.open_btn_clicked)

    # == 普通槽函数 ==
    # 禁用 按钮
    @Slot()
    def sta_btn_clicked(self):
        log.info("用户点击了 禁用/启用防火墙 里的 禁用 按钮")
        self.progress_bar.setVisible(True)
        # 禁用防火墙 多线程
        self.open_and_close_firewall_th = CloseFirewallWorker()
        # 连接信号和槽
        self.open_and_close_firewall_th.close_fire_finished.connect(self.close_firewall_finished)
        self.open_and_close_firewall_th.start()

    # 启用 按钮
    @Slot()
    def open_btn_clicked(self):
        log.info("用户点击了 禁用/启用防火墙 里的 启用 按钮")
        self.progress_bar.setVisible(True)
        # 启用防火墙 多线程
        self.open_and_close_firewall_th = OpenFirewallWorker()
        # 连接信号和槽
        self.open_and_close_firewall_th.open_fire_finished.connect(self.open_fire_wall_finished)
        self.open_and_close_firewall_th.start()

    # == 多线程连接槽函数 ==
    # 启用防火墙 多线程 完成信号
    @Slot()
    def open_fire_wall_finished(self, result):
        if result:
            self.progress_bar.setVisible(False)
            # 显示信息框
            QMessageBox.information(self.main_window, "成功", "防火墙已开启")
            # 记录到日志
            log.info("防火墙已开启")

        else:
            self.progress_bar.setVisible(False)
            # 显示信息框
            QMessageBox.information(self.main_window, "失败", "防火墙开启失败")
            # 记录到日志
            log.error("防火墙开启失败")
    
    # 禁用防火墙 多线程 完成信号
    @Slot()
    def close_firewall_finished(self, result):
        if result:
            self.progress_bar.setVisible(False)
            # 显示信息框
            QMessageBox.information(self.main_window, "成功", "防火墙已关闭")
            # 记录到日志
            log.info("防火墙已关闭")

        else:
            self.progress_bar.setVisible(False)
            # 显示信息框
            QMessageBox.information(self.main_window, "失败", "防火墙关闭失败")
            # 记录到日志
            log.error("防火墙关闭失败")

# 重置网络 卡片组件
class reset_network_Card(QFrame):
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent

        self.init_card()

    def init_card(self):
        container = QVBoxLayout()
        container.setContentsMargins(10, 10, 10, 10)
        # 设置卡片的框架形状和阴影效果
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        # 标题
        title_layout = QHBoxLayout()
        titile_label = QLabel("重置网络")
        # 加粗
        titile_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        # 设置标题在垂直方向可拉伸，水平方向根据内容自适应大小
        # titile_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        hor_layout = QHBoxLayout()
        # 创建一个水平分割线
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)

        # 内容
        h1_layout = QHBoxLayout()
        content_label = QLabel("本修复选项可以重置电脑状态，\n"
                               "修复之后会造成全部软件都要重新通过防火墙\n\n")
        content_label.setStyleSheet("font-size: 13px;")

        h2_layout = QHBoxLayout()
        content_2_label = QLabel("没有特殊情况最好不要使用本选项!!!")
        content_2_label.setStyleSheet("font-size: 13px; color: red;")

        h3_layout = QHBoxLayout()
        sta_btn = QPushButton("重置网络")
        sta_btn.setFixedHeight(50)

        bar_layout = QHBoxLayout()
        # 创建进度条
        self.progress_bar = QProgressBar(self)
        # 设置范围为0 - 0，使其成为不确定进度条
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)

        title_layout.addWidget(titile_label)
        hor_layout.addWidget(horizontal_line)
        h1_layout.addWidget(content_label)
        h2_layout.addWidget(content_2_label)
        h3_layout.addWidget(sta_btn)
        bar_layout.addWidget(self.progress_bar)

        container.addLayout(title_layout)
        container.addLayout(hor_layout)
        container.addLayout(h1_layout)
        container.addLayout(h2_layout)
        container.addLayout(h3_layout)
        container.addLayout(bar_layout)

        # 将布局应用到卡片部件上
        self.setLayout(container)

        # 设置卡片的背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

    # == 普通槽函数 ==
    # 开始修复按钮
    @Slot()
    def sta_btn_clicked(self):
        # 写入日志
        log.info("用户点击了 重置网络 里的 重置网络 按钮")
        self.progress_bar.setVisible(True)
        # 重置网络 多线程
        self.reset_network_th = reset_network_thread()
        # 连接信号和槽
        self.reset_network_th.reset_network_finished.connect(self.reset_network_finished)
        self.reset_network_th.start()

    # == 多线程连接槽函数 ==
    # 重置网络 多线程 完成信号
    @Slot()
    def reset_network_finished(self, result):
        if result:
            self.progress_bar.setVisible(False)
            # 显示信息框
            QMessageBox.information(self.main_window, "成功", "修复成功\n重启电脑生效")
        else:
            self.progress_bar.setVisible(False)
            # 显示信息框
            QMessageBox.information(self.main_window, "失败", "修复失败\n重启电脑生效")

# 完全禁用/启用目前已知与地平线冲突的服务 卡片组件
class ban_and_open_servers_Card(QFrame):
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent

        self.init_card()

    def init_card(self):
        container = QVBoxLayout()
        container.setContentsMargins(10, 10, 10, 10)
        # 设置卡片的框架形状和阴影效果
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        # 标题
        title_layout = QHBoxLayout()
        titile_label = QLabel("完全禁用/启动目前已知与地平线冲突的服务")
        # 加粗
        titile_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        # 设置标题在垂直方向可拉伸，水平方向根据内容自适应大小
        # titile_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        hor_layout = QHBoxLayout()
        # 创建一个水平分割线
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)

        # 内容
        h1_layout = QHBoxLayout()
        content_label = QLabel("本选项可以完全禁用目前与地平线冲突的服务\n\n"
                               "修复之后会造成某些电路仿真软件无法正常使用\n\n"
                               "如需使用电路仿真软件，请在使用之时点击启用\n")
        content_label.setStyleSheet("font-size: 13px;")

        bao_layout = QHBoxLayout()
        bao_label = QLabel("禁用选项已包含于“自动修复(关闭防火墙)”、“自动修复(开启防火墙)”中")
        bao_label.setStyleSheet("font-size: 13px; color: green;")

        h3_layout = QHBoxLayout()
        sta_btn = QPushButton("禁用")
        sta_btn.setFixedHeight(50)
        open_btn = QPushButton("启用")
        open_btn.setFixedHeight(50)

        tishi_layout = QHBoxLayout()
        self.tishi_label = QLabel("")
        self.tishi_label.setStyleSheet("font-size: 13px; color: green;")
        self.tishi_label.setVisible(False)

        bar_layout = QHBoxLayout()
        # 创建进度条
        self.progress_bar = QProgressBar(self)
        # 设置范围为0 - 0，使其成为不确定进度条
        self.progress_bar.setRange(0, len(Diconfig.disName))
        self.progress_bar.setVisible(False)

        title_layout.addWidget(titile_label)
        hor_layout.addWidget(horizontal_line)
        h1_layout.addWidget(content_label)
        bao_layout.addWidget(bao_label)
        h3_layout.addWidget(sta_btn)
        h3_layout.addWidget(open_btn)
        tishi_layout.addStretch(1)
        tishi_layout.addWidget(self.tishi_label)
        tishi_layout.addStretch(1)
        bar_layout.addWidget(self.progress_bar)

        container.addLayout(title_layout)
        container.addLayout(hor_layout)
        container.addLayout(h1_layout)
        container.addLayout(bao_layout)
        container.addLayout(h3_layout)
        container.addLayout(tishi_layout)
        container.addLayout(bar_layout)

        # 将布局应用到卡片部件上
        self.setLayout(container)

        # 设置卡片的背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # 信号
        # 点击禁用
        sta_btn.clicked.connect(self.sta_btn_clicked)
        # 点击启用
        open_btn.clicked.connect(self.open_btn_clicked)

    # == 普通槽函数 ==
    # 点击禁用
    @Slot()
    def sta_btn_clicked(self):
        # 写入日志
        log.info("用户点击了 完全禁用/启用目前已知与地平线冲突的服务 里的 禁用 按钮")
        self.progress_bar.setVisible(True)
        self.tishi_label.setVisible(True)
        self.sta_ban = ShutdownWorker(self)
        self.sta_ban.set_values.connect(self.progress_bar.setValue)
        self.sta_ban.shutdown_finished.connect(self.sta_ban_finished)
        self.sta_ban.start()

    # 点击启用
    @Slot()
    def open_btn_clicked(self):
        # 写入日志
        log.info("用户点击了 完全禁用/启用目前已知与地平线冲突的服务 里的 启用 按钮")
        self.progress_bar.setVisible(True)
        self.tishi_label.setVisible(True)
        self.progress_bar.setRange(0, len(Diconfig.disName))
        self.open_work = StratServersWorker(self)
        self.open_work.progress_signal.connect(self.progress_bar.setValue)
        self.open_work.open_finished.connect(self.open_servers_finished)
        self.open_work.start()

    # == 多线程连接槽函数 ==
    # 禁用 多线程 完成信号
    @Slot()
    def sta_ban_finished(self):
        self.progress_bar.setVisible(False)
        self.tishi_label.setVisible(False)
        # 信息框
        QMessageBox.information(self.main_window, "成功", "禁用成功")
        # 成功日志
        log.info("禁用成功")

    # 启用服务 多线程 完成信号
    @Slot()
    def open_servers_finished(self):
        self.progress_bar.setVisible(False)
        self.tishi_label.setVisible(False)
        # 信息框
        QMessageBox.information(self.main_window, "成功", "启用成功")
        # 成功日志
        log.info("启用成功")

# 启用必要的xbox服务 卡片组件
class open_xbox_servers_Card(QFrame):
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent

        self.init_card()

    def init_card(self):
        container = QVBoxLayout()
        container.setContentsMargins(10, 10, 10, 10)
        # 设置卡片的框架形状和阴影效果
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        # 标题
        title_layout = QHBoxLayout()
        titile_label = QLabel("启用必要的xbox服务")
        # 加粗
        titile_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        # 设置标题在垂直方向可拉伸，水平方向根据内容自适应大小
        # titile_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        hor_layout = QHBoxLayout()
        # 创建一个水平分割线
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)

        # 内容
        h1_layout = QHBoxLayout()
        content_label = QLabel("本选项可以修复某些地平线4的问题\n\n"
                               "例如: 账号对了但是搜索不到好友、无法进入到线上、加不了好友等\n\n")
        content_label.setStyleSheet("font-size: 13px;")

        bao_layout = QHBoxLayout()
        bao_label = QLabel("此选项已包含于“自动修复(关闭防火墙)”、“自动修复(开启防火墙)”中")
        bao_label.setStyleSheet("font-size: 13px; color: green;")

        h3_layout = QHBoxLayout()
        open_btn = QPushButton("启用")
        open_btn.setFixedHeight(50)

        tishi_layout = QHBoxLayout()
        self.tishi_label = QLabel("")
        self.tishi_label.setStyleSheet("font-size: 13px; color: green;")
        self.tishi_label.setVisible(False)

        bar_layout = QHBoxLayout()
        # 创建进度条
        self.progress_bar = QProgressBar(self)
        # 设置范围为0 - 0，使其成为不确定进度条
        self.progress_bar.setRange(0, len(Diconfig.disName))
        self.progress_bar.setVisible(False)

        title_layout.addWidget(titile_label)
        hor_layout.addWidget(horizontal_line)
        h1_layout.addWidget(content_label)
        bao_layout.addWidget(bao_label)
        h3_layout.addWidget(open_btn)
        tishi_layout.addStretch(1)
        tishi_layout.addWidget(self.tishi_label)
        tishi_layout.addStretch(1)
        bar_layout.addWidget(self.progress_bar)

        container.addLayout(title_layout)
        container.addLayout(hor_layout)
        container.addLayout(h1_layout)
        container.addLayout(bao_layout)
        container.addLayout(h3_layout)
        container.addLayout(tishi_layout)
        container.addLayout(bar_layout)

        # 将布局应用到卡片部件上
        self.setLayout(container)

        # 设置卡片的背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # 信号
        # 点击启用
        open_btn.clicked.connect(self.open_btn_clicked)

    def open_btn_clicked(self):
        # 写入日志
        log.info("用户点击了 启用必要的xbox服务 里的 启用 按钮")
        self.progress_bar.setVisible(True)
        self.tishi_label.setVisible(True)
        result_len = len(Diconfig.man_safe) + len(Diconfig.auto_safe)
        self.progress_bar.setRange(0, result_len)
        self.open_work = openXboxServersWorker(self)
        self.open_work.progress_signal.connect(self.progress_bar.setValue)
        self.open_work.xboxfinished.connect(self.open_servers_finished)
        self.open_work.start()

    # == 多线程连接槽函数 ==
    # 启用服务 多线程 完成信号
    @Slot()
    def open_servers_finished(self):
        self.progress_bar.setVisible(False)
        self.tishi_label.setVisible(False)
        # 信息框
        QMessageBox.information(self.main_window, "成功", "启用成功")
        # 成功日志
        log.info("启用必要的xbox服务 启用成功")


# == 主窗口 == 
# 杂项
class zaxiangInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setObjectName("zaxiangInterface")
        # 设置外面的主窗口为父窗口
        self.main_window = parent
        # 初始化界面
        self.resize(500, 500)
        self.init_ui()

    def init_ui(self):
        # 创建滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # 设置滚动区域内的部件可自适应大小

        # 创建一个容器部件，用来放置其他需要滚动展示的部件
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)

        # 检测是否被封禁
        ban_yon = QLabel('<a href="https://forza.net/myforza/banhistory">点我查看是否被封禁-------->请注意，点击前确保登录过一次官网</a>')
        ban_yon.setOpenExternalLinks(True)
        ban_yon.setStyleSheet("font-size: 13px;")
        # ban_yon.linkActivated.connect(link_clicked)
        # 检测Teredo参数
        teredo_card = check_Teredo_Card(self.main_window)
        # hosts修复
        host_card = hosts_Card(self.main_window)
        # 启用/禁用防火墙
        firewall_card = open_and_close_firewall_Card(self.main_window)
        # 重置网络
        reset_network_card = reset_network_Card(self.main_window)
        # 完全禁用目前已知与地平线冲突的服务
        ban_and_open_card = ban_and_open_servers_Card(self.main_window)
        # 启用必要的xbox服务
        open_xbox_card = open_xbox_servers_Card(self.main_window)

        # 设置边距
        teredo_card.setContentsMargins(50, 25, 50, 0)
        host_card.setContentsMargins(50, 25, 50, 0)
        firewall_card.setContentsMargins(50, 25, 50, 0)
        reset_network_card.setContentsMargins(50, 25, 50, 0)
        ban_and_open_card.setContentsMargins(50, 25, 50, 0)
        open_xbox_card.setContentsMargins(50, 25, 50, 0)

        # 将其他部件添加到容器布局中
        container_layout.addWidget(ban_yon)
        container_layout.addWidget(teredo_card)
        container_layout.addWidget(host_card)
        container_layout.addWidget(firewall_card)
        container_layout.addWidget(reset_network_card)
        container_layout.addWidget(ban_and_open_card)
        container_layout.addWidget(open_xbox_card)
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
    window = zaxiangInterface()
    window.show()
    sys.exit(app.exec())