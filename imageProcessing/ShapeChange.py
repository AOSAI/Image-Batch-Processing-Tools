from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QRadioButton,
                             QPushButton, QGridLayout, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.Qt import QButtonGroup
from PIL import Image, ImageDraw
import os
import imageProcessing.BatchProcessing as batch


class shapeChange(QWidget):
    def __init__(self):
        super().__init__()
        self.contentLayout()
        self.positionValue = 2
        self.shapeValue = 1
        self.compressValue = False
        self.imageList = []
        self.signal = batch.signalandslot()

    def getImagesSignal(self, imgs):
        self.imageList = imgs

    def startChange(self):
        if self.imageList == []:
            QMessageBox.warning(self, "警告", "您还未选择的图片，无法执行操作")
            return 0

        base_path = os.path.dirname(self.imageList[0])
        expect_folder = base_path + "/ShapeCrop"
        if not os.path.exists(expect_folder):
            os.mkdir(expect_folder)

        self.signal.new_progress.emit(0, len(self.imageList))
        step = 0
        for index, item in enumerate(self.imageList):
            new_photo = expect_folder + "/" + item.split("/")[-1]
            self.changeByPillow(item, new_photo, self.positionValue,
                                self.shapeValue, self.compressValue)
            step += 1
            self.signal.new_progress.emit(1, step)
            # time.sleep(0.05)
        os.startfile(expect_folder)

    def changeByPillow(self, originImg, newImg, position, shape, compress):
        img = Image.open(originImg)
        width, height = img.size
        shortLen = width if height > width else height

        if shape == 1 and width == height:
            img.save(newImg, quality=100)

        if compress == True:
            new_img = img.resize((shortLen, shortLen))
            if shape == 1:
                new_img.save(newImg, quality=100)
            else:
                newImg = "".join(newImg.split(".")[0:-1]) + ".PNG"
                new_img.save(newImg)
                new_img = self.makeCircle(newImg)
        else:
            if position == 1:
                box = (0, 0, width,
                       width) if width < height else (0, 0, height, height)
            elif position == 3:
                box = (0, height - width, width,
                       height) if width < height else (width - height, 0,
                                                       width, height)
            else:
                box = ((0, height / 2 - width / 2, width,
                        height / 2 + width / 2) if width < height else
                       (width / 2 - height / 2, 0, width / 2 + height / 2,
                        height))
            new_img = img.crop(box)
            if shape == 1:
                new_img.save(newImg, quality=100)
            else:
                newImg = "".join(newImg.split(".")[0:-1]) + ".PNG"
                new_img.save(newImg)
                new_img = self.makeCircle(newImg)

    def makeCircle(self, path):
        img = Image.open(path)
        w, h = img.size
        bg = Image.new("RGBA", (w, h), color=(0, 0, 0, 0))
        mask = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, w, h), fill=(0, 0, 0, 255))
        bg.paste(img, (0, 0, w, h), mask)
        bg.save(path)

    # def makeCircle(self, path):
    #     img = Image.open(path)
    #     w, h = img.size
    #     r = w/2
    #     img1 = Image.new("RGBA", (1080, 1080), (0, 0, 0, 0))
    #     pima = img.load()  # 像素的访问对象
    #     pimb = img1.load()
    #     for i in range(w):
    #         for j in range(w):
    #             lx = abs(i-r)  # 到圆心距离的横坐标
    #             ly = abs(j-r)  # 到圆心距离的纵坐标
    #             l  = (pow(lx,2) + pow(ly,2))** 0.5  # 三角函数 半径
    #             if l < r:
    #                 pimb[i,j] = pima[i,j]
    #     img1.save(path)

    def positionRadio(self, num):
        self.positionValue = num

    def shapeRadio(self, num):
        self.shapeValue = num

    def compressRadio(self, status):
        if status == True:
            for item in self.radioGroup1.buttons():
                item.setEnabled(False)
        else:
            for item in self.radioGroup1.buttons():
                item.setEnabled(True)
        self.compressValue = status

    def contentLayout(self):
        contentArea = QWidget()
        contentArea.setFixedSize(640, 240)
        contentArea.setStyleSheet("background:#F0F0F0;")

        fontTitle = QFont()
        fontTitle.setPixelSize(22)
        fontTitle.setBold(700)

        title = QLabel("形状裁剪")
        title.setFont(fontTitle)
        # title.setAlignment(Qt.AlignCenter)

        fontText = QFont()
        fontText.setPixelSize(16)

        label1 = QLabel("1.裁剪起始位置：")
        label1.setFont(fontText)
        radio1 = QRadioButton("左边/上边", contentArea)
        radio1.toggled.connect(lambda: self.positionRadio(1))
        radio2 = QRadioButton("中间", contentArea)
        radio2.toggled.connect(lambda: self.positionRadio(2))
        radio2.setChecked(True)
        radio3 = QRadioButton("右边/下边", contentArea)
        radio3.toggled.connect(lambda: self.positionRadio(3))

        self.radioGroup1 = QButtonGroup(contentArea)
        self.radioGroup1.addButton(radio1, 1)
        self.radioGroup1.addButton(radio2, 2)
        self.radioGroup1.addButton(radio3, 3)

        label2 = QLabel("2.保留形状类型：")
        label2.setFont(fontText)
        radio4 = QRadioButton("正方形", contentArea)
        radio4.toggled.connect(lambda: self.shapeRadio(1))
        radio4.setChecked(True)
        radio5 = QRadioButton("圆形", contentArea)
        radio5.toggled.connect(lambda: self.shapeRadio(2))
        # radio5.setEnabled(False)

        radioGroup2 = QButtonGroup(contentArea)
        radioGroup2.addButton(radio4)
        radioGroup2.addButton(radio5)

        label3 = QLabel("3.是否缩放宽高：")
        label3.setFont(fontText)
        radio6 = QRadioButton("不缩放", contentArea)
        radio6.toggled.connect(lambda: self.compressRadio(False))
        radio6.setChecked(True)
        radio7 = QRadioButton("缩放", contentArea)
        radio7.toggled.connect(lambda: self.compressRadio(True))

        radioGroup3 = QButtonGroup(contentArea)
        radioGroup3.addButton(radio6)
        radioGroup3.addButton(radio7)

        btn1 = QPushButton("开始裁剪")
        btn1.setFont(fontText)
        btn1.setFixedSize(112, 32)
        btn1.clicked.connect(self.startChange)

        contentLayout = QGridLayout()
        contentLayout.addWidget(title, 0, 0, 1, 2)
        contentLayout.addWidget(btn1, 0, 4, 1, 2)
        contentLayout.addWidget(label1, 3, 0, 1, 1)
        contentLayout.addWidget(radio1, 3, 1, 1, 1)
        contentLayout.addWidget(radio2, 3, 2, 1, 1)
        contentLayout.addWidget(radio3, 3, 3, 1, 1)
        contentLayout.addWidget(label2, 5, 0, 1, 1)
        contentLayout.addWidget(radio4, 5, 1, 1, 1)
        contentLayout.addWidget(radio5, 5, 2, 1, 1)
        contentLayout.addWidget(label3, 7, 0, 1, 1)
        contentLayout.addWidget(radio6, 7, 1, 1, 1)
        contentLayout.addWidget(radio7, 7, 2, 1, 1)
        contentLayout.setAlignment(Qt.AlignTop)
        contentLayout.setSpacing(30)

        contentArea.setLayout(contentLayout)
        layout = QHBoxLayout()
        layout.addWidget(contentArea)

        self.setLayout(layout)
