import sys
import time
import os

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from view.zaxiangOBJ import *
from view.new_xiufu_scripts import *

# from zaxiangOBJ import *
# from new_xiufu_scripts import *

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
# 自动修复开启/关闭防火墙版本多线程
class ZidongWorker(QThread):
    finish = Signal()
    progress_signal = Signal(int)

    def __init__(self, open_and_close, parent=None):

        '''
        True 为开启防火墙
        False 为关闭防火墙
        
        '''
        super().__init__()
        self.open_and_close = open_and_close

        self.main_window = parent

        # pythoncom.CoInitialize()  # 添加这行初始化 COM 库

    def run(self):
        print("===========进入")
        if self.open_and_close:
            self.main_window.tishi_label.setText("自动修复(开启防火墙)")
            self.main_window.tishi_label.setStyleSheet("color: green; font-size: 13px;")
        else:
            self.main_window.tishi_label.setText("自动修复(关闭防火墙)")
            self.main_window.tishi_label.setStyleSheet("color: red; font-size: 13px;")
        self.main_window.thread_lock = 1
        self.progress_signal.emit(0)  # 初始进度为 0
        self.hostsIndex = 0
        # 1. 重置hosts文件
        Zaxiang().host_file()
        self.progress_signal.emit(self.hostsIndex + 1)

        # 2. 把xbox服务启用
        # 继承数值
        self.index = self.hostsIndex
        # 手动
        for i in Diconfig.man_safe:
            xboxServers().stat_xbox_service_by_display_name(i)
            xboxServers().start_and_set_manual_service_by_display_name(i)
            shard_data = SharedData()
            # 计数器
            shard_data.openBan += 1
            self.index += 1
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

        # 3. 修改注册表并赋值
        # 继承数值
        self.paraIndex = self.index_auto
        for i in Diconfig.para:
            Zaxiang().set_or_create_dword(Diconfig.path, i, 0)
        self.progress_signal.emit(self.paraIndex + 1)

        # 4.是否关闭防火墙
        if self.open_and_close:
            Zaxiang().check_and_enable_windows_firewall()
        else:
            Zaxiang().disable_firewall()
        self.progress_signal.emit(self.paraIndex + 1)

        # 5. 禁用所有仿真电路软件(禁用冲突服务)
        # 继承数值
        self.xboxIndex = self.paraIndex

        for i in Diconfig.disName:
            Zaxiang().stop_service_by_display_name(i)
            shard_data = SharedData()
            # 计数器
            shard_data.openBan += 1
            self.xboxIndex += 1
            print(f'禁用 {self.xboxIndex + 1}')
            self.progress_signal.emit(self.xboxIndex + 1)  # 发射当前进度

        # 命令更改注册表
        self.send_index = self.xboxIndex
        Zaxiang().send_reg_command()
        self.progress_signal.emit(self.send_index)  # 发射当前进度

        # 结束
        self.finish.emit()

# 新版本自动修复 多线程
class new_zidong(QThread):
    send_max_num = Signal(int)
    send_num = Signal(int)
    send_finish = Signal()

    def __init__(self, parent=None):
        super().__init__()    

        self.new = new_xiufu(parent)

    def run(self):
        # 设置最大值
        self.send_max_num.emit(self.new.max_num)
        # 开始修复
        for i in range(1, self.new.max_num):
            self.send_num.emit(5)
            result = self.new.main()
            # 实时更新进度条
            self.send_num.emit(self.new.num)

            if result:
                break
            # time.sleep(0.1)
        # 完成
        self.send_finish.emit()

# 恢复 多线程    
class huifu(QThread):
    send_finish = Signal()
    
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent

    def run(self):
        new = new_xiufu(self.main_window)
        result_list = new.print_network_adapter_aliases()
        for i in result_list:
            new.enable_disable_ipv6_by_name(i, True)

        self.send_finish.emit()




# == 卡片组件 == 
# 老版本修复 卡片组件
class old_xiu_Card(QFrame):
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent
        self.thread_lock = 0

        self.init_card()

    def init_card(self):
        container = QVBoxLayout()
        container.setContentsMargins(10, 10, 10, 10)
        # 设置卡片的框架形状和阴影效果
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        # 标题
        title_layout = QHBoxLayout()
        titile_label = QLabel("老版本自动修复")
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
        content_label = QLabel("本自动修复选项为公开技术原理，网络上完全可以搜索到\n"
                               "此卡片组有概率修复进入不到线上的状况\n\n")
        content_label.setStyleSheet("font-size: 13px;")

        bao_layout = QHBoxLayout()
        bao_label = QLabel("“自动修复(关闭防火墙)”、“自动修复(开启防火墙)”这两个不同的点就是\n"
                           "前者是关闭防火墙，后者是开启防火墙\n\n")
        bao_label.setStyleSheet("font-size: 13px; color: green;")

        h3_layout = QHBoxLayout()
        sta_btn = QPushButton("自动修复(关闭防火墙)")
        sta_btn.setFixedHeight(50)
        sta_2_btn = QPushButton("自动修复(开启防火墙)")
        sta_2_btn.setFixedHeight(50)

        tishi_layout = QHBoxLayout()
        self.tishi_label = QLabel("")
        self.tishi_label.setVisible(False)

        bar_layout = QHBoxLayout()
        # 创建进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)

        title_layout.addWidget(titile_label)
        hor_layout.addWidget(horizontal_line)
        h1_layout.addWidget(content_label)
        bao_layout.addWidget(bao_label)
        h3_layout.addWidget(sta_btn)
        h3_layout.addWidget(sta_2_btn)
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
        # 自动修复(关闭防火墙)
        sta_btn.clicked.connect(self.sta_btn_clicked)
        # 自动修复(开启防火墙)
        sta_2_btn.clicked.connect(self.sta_2_btn_clicked)

    # == 槽函数 ==
    # 自动修复(关闭防火墙)
    @Slot()
    def sta_btn_clicked(self):
        if self.thread_lock == 1:
            # 弹出警告对话框
            QMessageBox.warning(self.main_window, "警告", "已经有一个任务正在运行")
            return
        restul_len = 1 + len(Diconfig.man_safe) + len(Diconfig.auto_safe) + 1 + 1 + len(Diconfig.disName)
        self.tishi_label.setVisible(True)
        # 进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, restul_len)
        
        # 开启多线程
        self.close_worker = ZidongWorker(open_and_close=False, parent=self)
        # 连接信号和槽
        self.close_worker.progress_signal.connect(self.progress_bar.setValue)
        self.close_worker.finish.connect(self.close_worker_finish)
        self.close_worker.start()

    # 自动修复(开启防火墙)
    @Slot()
    def sta_2_btn_clicked(self):
        if self.thread_lock == 1:
            # 弹出警告对话框
            QMessageBox.warning(self.main_window, "警告", "已经有一个任务正在运行")
            return
        restul_len = 1 + len(Diconfig.man_safe) + len(Diconfig.auto_safe) + 1 + 1 + len(Diconfig.disName)
        self.tishi_label.setVisible(True)
        # 进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, restul_len)
        # 开启多线程
        self.open_worker = ZidongWorker(open_and_close=True, parent=self)
        # 连接信号和槽
        self.open_worker.progress_signal.connect(self.progress_bar.setValue)
        self.open_worker.finish.connect(self.open_worker_finish)
        self.open_worker.start()
    
    # === 多线程返回函数 == 
    @Slot()
    def close_worker_finish(self):
        # 进度条
        self.progress_bar.setVisible(False)
        self.tishi_label.setVisible(False)
        # 弹窗
        QMessageBox.information(self, "提示", "自动修复(关闭防火墙)完成")
        self.thread_lock = 0

    @Slot()
    def open_worker_finish(self):
        # 进度条
        self.progress_bar.setVisible(False)
        self.tishi_label.setVisible(False)
        # 弹窗
        QMessageBox.information(self, "提示", "自动修复(开启防火墙)完成")
        self.thread_lock = 0
    
# 新版本修复 卡片组件
class new_xiu_Card(QFrame):
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent
        self.thread_lock = 0

        self.init_card()

    def init_card(self):
        container = QVBoxLayout()
        container.setContentsMargins(10, 10, 10, 10)
        # 设置卡片的框架形状和阴影效果
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        # 标题
        title_layout = QHBoxLayout()
        titile_label = QLabel("新版本自动修复(功能不和老版本重合)")
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
        content_label = QLabel("本自动修复选项为公开技术原理，网络上完全可以搜索到\n"
                               "此卡片组有概率修复进入不到线上的状况\n\n")
        content_label.setStyleSheet("font-size: 13px;")

        bao_layout = QHBoxLayout()
        bao_label = QLabel("如果修复了还是进不去，则点击“恢复”按钮\n"
                           "恢复一些必要的组件至正常\n\n")
        bao_label.setStyleSheet("font-size: 13px; color: green;")

        tips_layout = QHBoxLayout()
        tips_label = QLabel("最后会给你打开'凭据管理器'，\n把Xbl|开头的选项，举例：Xbl|Devicekey，全部统统删除，随后重启电脑")

        h3_layout = QHBoxLayout()
        sta_btn = QPushButton("开始修复")
        sta_btn.setFixedHeight(50)
        sta_2_btn = QPushButton("恢复")
        sta_2_btn.setFixedHeight(50)

        tishi_layout = QHBoxLayout()
        self.tishi_label = QLabel("")
        self.tishi_label.setVisible(False)

        bar_layout = QHBoxLayout()
        # 创建进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)

        title_layout.addWidget(titile_label)
        hor_layout.addWidget(horizontal_line)
        h1_layout.addWidget(content_label)
        bao_layout.addWidget(bao_label)
        tips_layout.addWidget(tips_label)
        h3_layout.addWidget(sta_btn)
        h3_layout.addWidget(sta_2_btn)
        tishi_layout.addStretch(1)
        tishi_layout.addWidget(self.tishi_label)
        tishi_layout.addStretch(1)
        bar_layout.addWidget(self.progress_bar)

        container.addLayout(title_layout)
        container.addLayout(hor_layout)
        container.addLayout(h1_layout)
        container.addLayout(bao_layout)
        container.addLayout(tips_layout)
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
        # 开始修复
        sta_btn.clicked.connect(self.sta_btn_clicked)
        # 恢复
        sta_2_btn.clicked.connect(self.sta_2_btn_clicked)
    # === 控件信号槽函数 ===
    @Slot()
    def sta_btn_clicked(self):
        self.progress_bar.setVisible(True)
        self.sta_new = new_zidong(self.main_window)
        self.sta_new.send_num.connect(self.progress_bar.setValue)
        self.sta_new.send_max_num.connect(self.progress_bar.setMaximum)
        self.sta_new.send_finish.connect(self.sta_new_finish)
        self.sta_new.start()

    @Slot()
    def sta_2_btn_clicked(self):
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.sta_2_t = huifu(self.main_window)
        self.sta_2_t.send_finish.connect(self.sta_2_t_finish)
        self.sta_2_t.start()

    # === 多线程返回函数 ===
    @Slot()
    def sta_new_finish(self):
        self.progress_bar.setVisible(False)
        QMessageBox.information(self.main_window, "修复完成", "在给你打开的凭据管理器当中，\n把Xbl|开头的选项，举例：Xbl|Devicekey，全部统统删除, 随后重启电脑\n如果忘记删除那就再修复一遍")
        log.info("新版自动修复完成")

    @Slot()
    def sta_2_t_finish(self):
        self.progress_bar.setVisible(False)
        # 弹窗
        QMessageBox.information(self.main_window, "提示", "恢复完成")
        # QMessageBox.information(self.main_window, "提示", "在给你打开的凭据管理器当中，\n把Xbl|开头的选项，举例：Xbl|Devicekey，全部统统删除, 随后重启电脑")
        log.info("新版恢复完成")

# == 主窗口 ==
class xiufiuInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent

        self.setObjectName("xiufu_interface")
        self.resize(650, 650)
        self.init_ui()
    
    def init_ui(self):
        # 创建滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # 设置滚动区域内的部件可自适应大小

        # 创建一个容器部件，用来放置其他需要滚动展示的部件
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)

        # 老版本修复
        old_xiu_card = old_xiu_Card(self.main_window)
        # 新版本修复
        new_xiu_card = new_xiu_Card(self.main_window)

        # 设置边距
        old_xiu_card.setContentsMargins(50, 25, 50, 0)
        new_xiu_card.setContentsMargins(50, 25, 50, 0)

        container_layout.addWidget(old_xiu_card)
        container_layout.addWidget(new_xiu_card)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = xiufiuInterface()
    window.show()
    sys.exit(app.exec())