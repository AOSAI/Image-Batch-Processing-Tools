from PIL import Image
import os
import sys
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QIcon, QFont, QIntValidator
from PyQt5.QtWidgets import (QSizePolicy, QLabel, QLineEdit, QPushButton,
                             QFormLayout, QWidget, QHBoxLayout, QFileDialog,
                             QGridLayout, QMessageBox, QVBoxLayout,
                             QApplication)
import imageProcessing.ImageCompress as compress
import imageProcessing.ResolutionAdjust as resolution
import imageProcessing.ShapeChange as shape


class signalandslot(QObject):
    new_progress = pyqtSignal(int, int)
    image_list = pyqtSignal(list)


class BatchProcessing(QWidget):
    def __init__(self):
        super().__init__()
        self.imageNum = 0
        self.imageList = []
        self.signal = signalandslot()
        self.compress = compress.imageCompress()
        self.shape = shape.shapeChange()
        self.resolution = resolution.resolutionAdjust()
        self.contentLayout()

    def selectImages(self):
        iamgePath, imageType = QFileDialog.getOpenFileNames(
            self, "选择图像", "C:\\", "*.jpg;*.jpeg")
        self.imageList = iamgePath
        self.imageNum = len(iamgePath)
        self.signal.image_list.connect(self.compress.getImagesSignal)
        self.signal.image_list.connect(self.shape.getImagesSignal)
        self.signal.image_list.connect(self.resolution.getImagesSignal)
        self.signal.image_list.emit(self.imageList)
        self.label1.setText(f"您一共选择了：{self.imageNum} 张图像")

    def reset(self):
        self.imageList = []
        self.imageNum = 0
        self.signal.image_list.emit(self.imageList)
        self.label1.setText(f"您一共选择了：{self.imageNum} 张图像")

    def leftLayout(self):
        leftArea = QWidget()
        leftArea.setFixedSize(320, 640)
        # leftArea.setStyleSheet("background:#f5f6fa;")

        fontTitle = QFont()
        fontTitle.setPixelSize(24)
        fontTitle.setBold(700)

        title = QLabel("批量图像处理工具")
        title.setFont(fontTitle)
        title.setAlignment(Qt.AlignCenter)

        fontText = QFont()
        fontText.setPixelSize(16)

        chooseBtn = QPushButton("选择图像")
        chooseBtn.setFont(fontText)
        chooseBtn.setFixedHeight(40)
        chooseBtn.clicked.connect(self.selectImages)

        tips1 = QLabel("目前支持格式：JPG/JPEG")
        tips1.setFont(fontText)
        tips1.setAlignment(Qt.AlignCenter)

        self.label1 = QLabel(f"您一共选择了：{self.imageNum} 张图像")
        self.label1.setFont(fontText)
        self.label1.setAlignment(Qt.AlignCenter)

        resetBtn = QPushButton("清空重置")
        resetBtn.setFont(fontText)
        resetBtn.setFixedHeight(40)
        resetBtn.clicked.connect(self.reset)

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(title, 0, 0, 3, 1)
        layout.addWidget(chooseBtn, 4, 0, 1, 1)
        layout.addWidget(tips1, 5, 0, 1, 1)
        layout.addWidget(self.label1, 5, 0, 2, 1)
        layout.addWidget(resetBtn, 8, 0, 4, 1)

        leftArea.setLayout(layout)

        return leftArea

    def rightLayout(self):
        rightArea = QWidget()
        rightArea.setFixedSize(640, 640)
        rightArea.setStyleSheet("background:#f5f6fa;")

        layout1 = QHBoxLayout()
        layout1.addWidget(self.compress)
        layout1.addWidget(self.resolution)

        layout2 = QVBoxLayout()
        layout2.addLayout(layout1)
        layout2.addWidget(self.shape)

        rightArea.setLayout(layout2)

        return rightArea

    def contentLayout(self):
        contentLayout = QHBoxLayout()
        contentLayout.addWidget(self.leftLayout(), Qt.AlignCenter)
        contentLayout.addWidget(self.rightLayout(), Qt.AlignCenter)

        self.setLayout(contentLayout)
