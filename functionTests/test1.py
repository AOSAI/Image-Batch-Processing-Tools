import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QPushButton, QDialog, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import time


class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("任务进度")
        self.setWindowFlag(Qt.FramelessWindowHint)  # 去掉标题栏
        self.setStyleSheet("background-color: #2c3e50; color: white; padding: 10px; border-radius: 10px;")
        
        # 创建布局
        layout = QVBoxLayout()

        # 添加进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("QProgressBar {"
                                        "border: 2px solid #bbb;"
                                        "border-radius: 5px;"
                                        "background-color: #ecf0f1;"
                                        "text-align: center;"
                                        "color: #34495e;"
                                        "font-size: 14px;"
                                        "}"
                                        "QProgressBar::chunk {"
                                        "background-color: #1abc9c;"
                                        "border-radius: 5px;"
                                        "}")
        layout.addWidget(self.progress_bar)

        # 进度文字标签
        self.label = QLabel("任务进行中...")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.label)

        # 设置布局
        self.setLayout(layout)
        self.setFixedSize(400, 100)

    def update_progress(self, value):
        """更新进度条和标签的文本"""
        self.progress_bar.setValue(value)
        self.label.setText(f"正在进行: {value}%")
        if value == 100:
            self.accept()  # 完成后自动关闭窗口


class Worker(QThread):
    progress_signal = pyqtSignal(int)

    def run(self):
        """模拟一个长时间运行的任务"""
        for i in range(101):
            time.sleep(0.1)  # 模拟任务
            self.progress_signal.emit(i)  # 发射进度信号


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("进度条示例")
        self.setGeometry(100, 100, 300, 200)

        # 创建按钮
        self.start_button = QPushButton("开始任务", self)
        self.start_button.clicked.connect(self.start_task)

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        self.setLayout(layout)

    def start_task(self):
        """启动任务并显示进度条弹窗"""
        self.progress_dialog = ProgressDialog(self)
        self.progress_dialog.show()  # 显示进度条弹窗

        self.worker = Worker()
        self.worker.progress_signal.connect(self.progress_dialog.update_progress)
        self.worker.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
