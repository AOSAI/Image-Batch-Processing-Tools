from PyQt5.QtWidgets import QVBoxLayout, QProgressBar, QDialog, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QPoint


class ProgressDialog(QDialog):
    progress_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("任务进度")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)  # 去掉标题栏，置顶
        self.setStyleSheet("background-color: #2c3e50; color: white; padding: 10px; border-radius: 10px;")
        self.drag_position = QPoint()  # 记录鼠标按下时的位置
        
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # 仅处理左键拖动
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def update_progress(self, value):
        """更新进度条和标签的文本"""
        self.progress_bar.setValue(value)
        self.label.setText(f"正在进行: {value}%")
        if value == 100:
            self.accept()  # 完成后自动关闭窗口