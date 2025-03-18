from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QRadioButton,
                             QPushButton, QGridLayout, QMessageBox,
                             QButtonGroup, QLineEdit)
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import Qt
import imageProcessing.BatchProcessing as batch
from PIL import Image
import os


class resolutionAdjust(QWidget):
    def __init__(self):
        super().__init__()
        self.imageList = []
        self.scaleValue = False
        self.w_h_value = "width"
        self.contentLayout()
        self.signal = batch.signalandslot()

    def getImagesSignal(self, imgs):
        self.imageList = imgs

    def startChange(self):
        if self.imageList == []:
            QMessageBox.warning(self, "警告", "您还未选择图片，无法执行操作")
            return 0

        expect_width = self.input1.text()
        expect_height = self.input2.text()

        if self.scaleValue == False:
            if expect_width == "" or expect_height == "":
                QMessageBox.warning(self, "警告", "您的输入不完整，请修改")
                return 0
        else:
            if self.w_h_value == "width" and expect_width == "":
                QMessageBox.warning(self, "警告", "您还未输入宽度，无法执行操作")
                return 0
            if self.w_h_value == "height" and expect_height == "":
                QMessageBox.warning(self, "警告", "您还未输入高度，无法执行操作")
                return 0

        base_path = os.path.dirname(self.imageList[0])
        expect_folder = base_path + "/Resized"
        if not os.path.exists(expect_folder):
            os.mkdir(expect_folder)

        self.signal.new_progress.emit(0, len(self.imageList))
        step = 0
        for index, item in enumerate(self.imageList):
            new_photo = expect_folder + "/" + item.split("/")[-1]
            if self.scaleValue == False:
                self.resizeImages(item, new_photo, int(expect_width),
                                  int(expect_height))
            else:
                if self.w_h_value == "width":
                    self.resizeImages(item, new_photo, int(expect_width), None)
                if self.w_h_value == "height":
                    self.resizeImages(item, new_photo, None,
                                      int(expect_height))
            step += 1
            self.signal.new_progress.emit(1, step)
            # time.sleep(0.05)
        os.startfile(expect_folder)

    def resizeImages(self, old_path, new_path, width=None, height=None):
        img = Image.open(old_path)
        w, h = img.size
        if width == None:
            ratio = height / h
            width = int(w * ratio)
        if height == None:
            ratio = width / w
            height = int(h * ratio)
        new_img = img.resize((width, height))
        new_img.save(new_path, quality=100)

    def fixedWH(self, value=1):
        if value == "width":
            self.input1.setEnabled(True)
            self.input2.setEnabled(False)
        elif value == "height":
            self.input1.setEnabled(False)
            self.input2.setEnabled(True)
        else:
            self.input1.setEnabled(True)
            self.input2.setEnabled(True)

        if type(value) == str:
            self.w_h_value = value

    def scaleRadio(self, value):
        if value == True:
            for item in self.radioGroup2.buttons():
                item.setEnabled(True)
            self.fixedWH(self.w_h_value)
        else:
            for item in self.radioGroup2.buttons():
                item.setEnabled(False)
            self.fixedWH()
        self.scaleValue = value

    def contentLayout(self):
        contentArea = QWidget()
        contentArea.setFixedSize(320, 360)
        contentArea.setStyleSheet("background:#F0F0F0;")

        fontTitle = QFont()
        fontTitle.setPixelSize(22)
        fontTitle.setBold(700)

        title = QLabel("修改尺寸")
        title.setFont(fontTitle)
        # title.setAlignment(Qt.AlignCenter)

        fontText = QFont()
        fontText.setPixelSize(16)
        fontText1 = QFont()
        fontText1.setPixelSize(14)

        label2 = QLabel("2.设置图像的尺寸：")
        label2.setFont(fontText)
        label3 = QLabel("图像宽度：")
        label3.setFont(fontText1)
        self.input1 = QLineEdit()
        self.input1.setFixedHeight(24)
        intFilter = QIntValidator()
        intFilter.setRange(1, 10000)
        self.input1.setValidator(intFilter)
        label4 = QLabel("图像高度：")
        label4.setFont(fontText1)
        self.input2 = QLineEdit()
        self.input2.setFixedHeight(24)
        intFilter = QIntValidator()
        intFilter.setRange(1, 10000)
        self.input2.setValidator(intFilter)

        radio3 = QRadioButton("固定宽度", contentArea)
        radio3.toggled.connect(lambda: self.fixedWH("width"))
        radio3.setChecked(True)
        radio4 = QRadioButton("固定高度", contentArea)
        radio4.toggled.connect(lambda: self.fixedWH("height"))

        self.radioGroup2 = QButtonGroup(contentArea)
        self.radioGroup2.addButton(radio3)
        self.radioGroup2.addButton(radio4)

        label1 = QLabel("1.是否维持原有宽高比例：")
        label1.setFont(fontText)
        radio1 = QRadioButton("自定义宽高", contentArea)
        radio1.toggled.connect(lambda: self.scaleRadio(False))
        radio1.setChecked(True)
        radio2 = QRadioButton("保持", contentArea)
        radio2.toggled.connect(lambda: self.scaleRadio(True))

        radioGroup1 = QButtonGroup(contentArea)
        radioGroup1.addButton(radio1)
        radioGroup1.addButton(radio2)

        tips1 = QLabel(
            "常见照片比例：\n一寸：    2.5：3.5\n小二寸：  3.3：4.8\n二寸：    3.5：5.3\n五寸：    3.5：5.0\n六寸：    4.0：6.0")

        btn1 = QPushButton("开始调整")
        btn1.setFont(fontText)
        btn1.setFixedSize(112, 32)
        btn1.clicked.connect(self.startChange)

        contentLayout = QGridLayout()
        contentLayout.setSpacing(8)
        contentLayout.addWidget(title, 0, 0, 1, 4)
        contentLayout.addWidget(btn1, 0, 7, 1, 4)
        contentLayout.addWidget(label1, 3, 0, 1, 9)
        contentLayout.addWidget(radio1, 4, 0, 1, 4)
        contentLayout.addWidget(radio2, 4, 4, 1, 4)
        contentLayout.addWidget(radio3, 5, 0, 1, 4)
        contentLayout.addWidget(radio4, 5, 4, 1, 4)
        contentLayout.addWidget(label2, 6, 0, 1, 9)
        contentLayout.addWidget(label3, 7, 0, 1, 3)
        contentLayout.addWidget(self.input1, 7, 3, 1, 8)
        contentLayout.addWidget(label4, 8, 0, 1, 3)
        contentLayout.addWidget(self.input2, 8, 3, 1, 8)
        contentLayout.addWidget(tips1, 9, 0, 3, 12)
        # contentLayout.setAlignment(Qt.AlignTop)

        contentArea.setLayout(contentLayout)
        layout = QHBoxLayout()
        layout.addWidget(contentArea)

        self.setLayout(layout)
