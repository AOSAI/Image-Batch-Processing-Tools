from PIL import Image
import os
import sys
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QFont, QIntValidator
from PyQt5.QtWidgets import (QSizePolicy, QLabel, QLineEdit, QPushButton,
                             QFormLayout, QWidget, QHBoxLayout, QFileDialog,
                             QGridLayout, QMessageBox, QVBoxLayout,
                             QRadioButton, QButtonGroup)
import imageProcessing.BatchProcessing as batch


class imageCompress(QWidget):
    def __init__(self):
        super().__init__()
        self.contentLayout()
        self.imageList = []
        self.radioValue1 = 1
        self.radioValue2 = True
        self.signal = batch.signalandslot()

    def getImagesSignal(self, imgs):
        self.imageList = imgs

    def startCompress(self):
        expect_folder = ""
        expect_size = 200

        if self.radioValue1 == 2:
            if self.input1.text() == "":
                QMessageBox.warning(self, "警告", "压缩预期大小不能为空（单位KB）")
                return 0
            else:
                expect_size = int(self.input1.text())

        if self.imageList == []:
            QMessageBox.warning(self, "警告", "您还未选择需要压缩的图片\n无法执行压缩操作")
            return 0

        if self.input2.text() == "":
            base_path = os.path.dirname(self.imageList[0])
            expect_folder = base_path + "/Compressed"
            if not os.path.exists(expect_folder):
                os.mkdir(expect_folder)
        else:
            if os.path.isdir(self.input2.text()):
                expect_folder = self.input2.text()
            else:
                QMessageBox(self, "警告", "您输入的目标文件夹路径有误\n请重新修正！")
                return 0
        # print(self.imageList[0].split("/"))

        self.signal.new_progress.emit(0, len(self.imageList))
        step = 0
        for index, item in enumerate(self.imageList):
            new_photo = (expect_folder + "/" + str(index) +
                         ".jpeg" if self.radioValue2 == 2 else expect_folder +
                         "/" + item.split("/")[-1])
            self.CompressByPillow(item, new_photo, expect_size,
                                  self.radioValue1)
            step += 1
            self.signal.new_progress.emit(1, step)
            # time.sleep(0.05)
        os.startfile(expect_folder)
        # self.reset()

    def CompressByPillow(self, input, output, expect_size, flag):
        if flag == 1:
            img = Image.open(input)
            img.save(output)
        else:
            photo_size = os.path.getsize(input) / 1024
            left = 0
            right = 100
            while True:
                mid = int((left + right) / 2)
                img = Image.open(input)
                img.save(output, quality=mid)
                photo_size = os.path.getsize(output) / 1024
                if right - left <= 1:
                    break
                if photo_size >= expect_size:
                    right = mid
                else:
                    left = mid

    def radioChecked1(self, e):
        self.input1.setEnabled(True) if e == 2 else self.input1.setEnabled(
            False)
        self.radioValue1 = e

    def radioChecked2(self, e):
        self.radioValue2 = e

    def contentLayout(self):
        contentArea = QWidget()
        contentArea.setFixedSize(320, 360)
        contentArea.setStyleSheet("background:#F0F0F0;")
        contentArea.setContentsMargins(0, 0, 0, 0)

        fontTitle = QFont()
        fontTitle.setPixelSize(22)
        fontTitle.setBold(700)
        title = QLabel("图像压缩")
        title.setFont(fontTitle)

        fontText1 = QFont()
        fontText1.setPixelSize(14)

        label1 = QLabel("压缩目标大小（KB）：")
        label1.setFont(fontText1)
        self.input1 = QLineEdit()
        self.input1.setFixedHeight(24)
        self.input1.setEnabled(False)
        intFilter = QIntValidator()
        intFilter.setRange(1, 10240)
        self.input1.setValidator(intFilter)

        fontText = QFont()
        fontText.setPixelSize(16)

        label4 = QLabel("1.图片大小是否最优化处理：")
        label4.setFont(fontText)
        radio3 = QRadioButton("最优化")
        radio3.toggled.connect(lambda: self.radioChecked1(1))
        radio3.setChecked(True)
        radio4 = QRadioButton("指定大小")
        radio4.toggled.connect(lambda: self.radioChecked1(2))

        radioGroup1 = QButtonGroup(contentArea)
        radioGroup1.addButton(radio3)
        radioGroup1.addButton(radio4)

        label2 = QLabel("2.自定义存放路径：")
        label2.setFont(fontText)
        self.input2 = QLineEdit()
        self.input2.setFixedHeight(28)

        label3 = QLabel("3.是否保留文件原名称：")
        label3.setFont(fontText)
        radio1 = QRadioButton("保留")
        radio1.toggled.connect(lambda: self.radioChecked2(True))
        radio1.setChecked(True)
        radio2 = QRadioButton("不保留")
        radio2.toggled.connect(lambda: self.radioChecked2(False))

        radioGroup2 = QButtonGroup(contentArea)
        radioGroup2.addButton(radio1)
        radioGroup2.addButton(radio2)

        btn1 = QPushButton("开始压缩")
        btn1.setFont(fontText)
        btn1.setFixedSize(112, 32)
        btn1.clicked.connect(self.startCompress)

        tips1 = QLabel(
            "说明：\n1.单位转换：1MB=1024KB，2MB=2048KB\n2.存放路径为空时，默认选择第一张图像的路径")
        # tips1.setFont(fontText)

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(title, 0, 0, 2, 4)
        layout.addWidget(btn1, 0, 6, 2, 4)
        layout.addWidget(label4, 3, 0, 1, 9)
        layout.addWidget(radio3, 4, 0, 1, 3)
        layout.addWidget(radio4, 4, 3, 1, 3)
        layout.addWidget(label1, 5, 0, 1, 6)
        layout.addWidget(self.input1, 5, 5, 1, 6)
        layout.addWidget(label2, 6, 0, 1, 6)
        layout.addWidget(self.input2, 7, 0, 1, 11)
        layout.addWidget(label3, 8, 0, 1, 6)
        layout.addWidget(radio1, 9, 0, 1, 3)
        layout.addWidget(radio2, 9, 3, 1, 3)
        layout.addWidget(tips1, 10, 0, 3, 13)
        # layout.setAlignment(Qt.AlignTop)

        contentArea.setLayout(layout)
        contentLayout = QHBoxLayout()
        contentLayout.addWidget(contentArea)
        self.setLayout(contentLayout)
