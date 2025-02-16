import sys, os
import requests, subprocess

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from update_zip import *

# === 多线程 ===
class down_load(QThread):

    send_max = Signal(int)
    send_value = Signal(int)
    down_finished = Signal(bool, str)
    
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent
        self.path = os.getcwd()

    def run(self):
        # 下载
        self.start_download()
        # 安装
        self.anzhuang()
        # 结束
        self.down_finished.emit(self.result, self.exe_path)
    
    # 下载压缩包
    def start_download(self):
        self.main_window.tishi_label.setText("下载更新内容中...")
        url = "压缩包地址"  # 替换为你要下载的文件的 URL
        local_filename = f"{self.path}/up.zip"  # 替换为本地保存的文件名
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            # self.progress_bar.setMaximum(total_size)
            self.send_max.emit(total_size)
            downloaded_size = 0
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    # self.progress_bar.setValue(downloaded_size)
                    self.send_value.emit(downloaded_size)

    # 安装
    def anzhuang(self):
        self.main_window.tishi_label.setText("安装更新内容中...")
        # 设置为不确定进度条
        self.send_max.emit(0)
        self.sta = find_file_and_move_file()
        self.result, self.exe_path = self.sta.main()

# 自动升级
class updateInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.path = os.getcwd()
        self.main_window = parent
        # self.main_window.close()
        # 不允许关闭窗口
        self.Yon_close = 0

        self.initUI()
        self.window_ui()
    
    def initUI(self):
        self.setWindowTitle("在线更新")
        self.setWindowIcon(QIcon(f"{self.path}/plugins/ke.ico"))
        self.setFixedSize(300, 100)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    def window_ui(self):
        container = QVBoxLayout()

        self.tishi_label = QLabel("等待")

        self.progress_bar = QProgressBar()
        # self.progress_bar.setMaximum(0)
        
        container.addWidget(self.tishi_label)
        container.addWidget(self.progress_bar)

        self.setLayout(container)

        # 多线程开始
        self.start_download()

    # === 多线程函数 ===
    def start_download(self):
        # 多线程
        self.down_load = down_load(self)
        # 信号
        self.down_load.send_max.connect(self.progress_bar.setMaximum)
        self.down_load.send_value.connect(self.progress_bar.setValue)
        self.down_load.down_finished.connect(self.down_finished)
        self.down_load.start()


    # === 多线程返回槽函数 ===
    @Slot(bool, str)
    def down_finished(self, result, exe_path):

        if result:
            self.tishi_label.setText("更新完成")
            self.progress_bar.setVisible(False)

            # QMessageBox.information(self, "提示", "更新完成, 点击ok继续")

            # 打开exe
            # print(f"=============== exe 路径为 {exe_path}")
            # 如果打不开 不是exe路径
            if "exe" not in exe_path:
                # exe路径需要放在最后一位
                QMessageBox.critical(self, "错误", "请联系作者, 看他是否更新清单填写错误")
                return
            
            ok_click = QMessageBox.information(self, "提示", "更新完成, 点击ok继续\n\n点击ok后本窗口卡住， 属于正常现象\n\n更新完成后请手动删除旧启用文件",
                                    QMessageBox.Ok)
            
            if ok_click == QMessageBox.Ok:
                # 允许关闭窗口
                self.Yon_close = 1

                open_result = self.open_exe(exe_path)
                if open_result == False:
                    QMessageBox.critical(self, "错误", "发生未知错误, 但是貌似更新文件已经安装完毕, 手动打开并删除旧文件即可")
                    return
                    # 关闭窗口
                sys.exit()
        else:
            self.tishi_label.setText("更新失败")
            self.progress_bar.setVisible(False)

            QMessageBox.critical(self, "错误", "更新失败, 文件清点失败, 请检查日志提交给作者或者联系作者处理")
    
    # === 非槽函数 ===
    # 打开exe
    def open_exe(self, file_path):
        try:
            subprocess.Popen(file_path)
            # print(f"已打开文件: {file_path}")
            return True
        except FileNotFoundError:
            # print(f"未找到文件: {file_path}")
            return False
        except Exception as e:
            # print(f"发生错误: {e}")
            return False
        
    # === 重写函数 ===
    # 无法关闭窗口
    def closeEvent(self, event):
        if self.Yon_close == 0:
            # 当 Yon_close 为 0 时，忽略关闭事件，从而阻止用户关闭窗口
            event.ignore()
        else:
            # 当 Yon_close 为 1 时，允许关闭窗口
            event.accept()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = updateInterface()
    window.show()
    sys.exit(app.exec())