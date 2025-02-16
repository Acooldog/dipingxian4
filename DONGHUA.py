import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import QPropertyAnimation, QEasingCurve


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.button = QPushButton('点击我')
        self.button.clicked.connect(self.start_animation)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def start_animation(self):
        # 创建一个属性动画，目标对象是按钮，属性是“geometry”（位置和大小）
        animation = QPropertyAnimation(self.button, b'geometry')
        # 设置动画的持续时间，单位为毫秒
        animation.setDuration(300)
        # 设置动画的起始值，即按钮当前的位置和大小
        animation.setStartValue(self.button.geometry())
        # 计算按钮放大后的位置和大小
        new_geometry = self.button.geometry()
        new_geometry.setWidth(new_geometry.width() * 5)
        new_geometry.setHeight(new_geometry.height() * 5)
        # 设置动画的结束值，即按钮放大后的位置和大小
        animation.setEndValue(new_geometry)
        # 设置动画的缓动曲线，让动画效果更自然
        animation.setEasingCurve(QEasingCurve.OutBounce)
        # 设置动画完成后恢复到初始状态
        animation.finished.connect(lambda: self.reset_button(animation))
        # 启动动画
        animation.start()

    def reset_button(self, animation):
        # 动画完成后，将按钮恢复到初始状态
        self.button.setGeometry(animation.startValue())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


