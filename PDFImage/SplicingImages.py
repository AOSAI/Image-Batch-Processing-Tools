from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer, QSize
from PyQt5.QtGui import QIcon, QFont, QIntValidator
from PyQt5.QtWidgets import (QFileDialog, QLabel, QLineEdit, QPushButton,
                             QFormLayout, QWidget, QHBoxLayout, QVBoxLayout,
                             QFileDialog, QButtonGroup, QMessageBox,
                             QVBoxLayout, QRadioButton, QApplication, QListWidgetItem)
import os
from PIL import Image

class ToSplicingImages(QWidget):
    def __init__(self):
        super().__init__()
        self.imageList = []
        self.dirList = ""
        self.fontText = QFont()
        self.fontText.setPixelSize(16)
        self.contentLayout()

    def contentLayout(self):
        layout = QVBoxLayout()
        # layout.addLayout(self.layout1)
        # layout.setContentsMargins(0, 0, 0, 20)  # 设置外边距
        
        contentLayout = QWidget()
        contentLayout.setFixedSize(480, 600)
        contentLayout.setLayout(layout)

        layout1 = QHBoxLayout()
        layout1.addWidget(contentLayout)
        self.setLayout(layout1)