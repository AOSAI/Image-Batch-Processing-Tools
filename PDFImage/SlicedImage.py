from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer, QSize
from PyQt5.QtGui import QIcon, QFont, QIntValidator
from PyQt5.QtWidgets import (QFileDialog, QLabel, QLineEdit, QPushButton,
                             QFormLayout, QWidget, QHBoxLayout, QVBoxLayout,
                             QFileDialog, QButtonGroup, QMessageBox,
                             QVBoxLayout, QRadioButton, QApplication, QListWidgetItem)
import os
from PIL import Image
from commonComponent.ProgressDialog import ProgressDialog

class ImageProcessorThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, inputList, outputDir, param, mode, position=1):
        super().__init__()
        self.inputList = inputList
        self.outputDir = outputDir
        self.param = param  # num_flag for 'num', pixelList for 'pixel'
        self.mode = mode  # 'num' or 'pixel'
        self.position = position  # 控制图像翻转

    def SlicedImagesbyNum(self):
        os.makedirs(self.outputDir, exist_ok=True)
        step = 0
        num_flag = self.param

        for img_path in self.inputList:
            step += 1
            self.progress_signal.emit(int((step / len(self.inputList)) * 100))

            # 计算每个块的宽度和高度
            img = Image.open(img_path)
            width, height = img.size
            sub_width = width // (num_flag[1] + 1)
            sub_height = height // (num_flag[0] + 1)

            base_name = os.path.basename(img_path)
            file_name, ext = os.path.splitext(base_name)

            # 循环切割并保存子图像
            for row in range(num_flag[0] + 1):
                for col in range(num_flag[1] + 1):
                    # 计算每个子图像的左上角和右下角坐标，切割图像
                    left = col * sub_width
                    upper = row * sub_height
                    right = left + sub_width
                    lower = upper + sub_height
                    sub_image = img.crop((left, upper, right, lower))

                    # 生成子图像的文件名，并保存子图像
                    output_name = f"{file_name}_row{row+1}_col{col+1}.{ext}"
                    output_path = os.path.join(self.outputDir, output_name)
                    sub_image.save(output_path)

    def imageTranspose(self, img, flag):
        if flag == 2:  # 垂直翻转（沿左右对称轴），右上角开始
            return img.transpose(Image.FLIP_LEFT_RIGHT)
        elif flag == 3:  # 水平翻转（沿上下对称轴），左下角开始
            return img.transpose(Image.FLIP_TOP_BOTTOM)
        elif flag == 4:  # 水平垂直翻转（沿左右和上下对称轴），右下角开始
            return img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
        return img
    
    def SlicedImagesbyPixel(self):
        os.makedirs(self.outputDir, exist_ok=True)
        step = 0
        pixelList = self.param

        for img_path in self.inputList:
            step += 1
            self.progress_signal.emit(int((step / len(self.inputList)) * 100))
            
            img = Image.open(img_path)
            img = self.imageTranspose(img, self.position)
            width, height = img.size
            
            base_name = os.path.basename(img_path)
            file_name, ext = os.path.splitext(base_name)
            
            for y in range(0, height, pixelList[1]):
                for x in range(0, width, pixelList[0]):
                    # 处理边界问题
                    right = min(x + pixelList[0], width)
                    lower = min(y + pixelList[1], height)
                    
                    # 切块并翻转
                    sub_image = img.crop((x, y, right, lower))
                    sub_image = self.imageTranspose(sub_image, self.position)
                    
                    # 设定图像名称，并保存
                    output_name = f"{file_name}_x{x}_y{y}.{ext}"
                    sub_image.save(os.path.join(self.outputDir, output_name))

    def run(self):
        if self.mode == 'num':
            self.SlicedImagesbyNum()
            self.progress_signal.emit(100)
        elif self.mode == 'pixel':
            self.SlicedImagesbyPixel()
            self.progress_signal.emit(100)

class ToSlicedImages(QWidget):
    def __init__(self):
        super().__init__()
        self.imageList = []
        self.dirList = ""
        self.fontText = QFont()
        self.fontText.setPixelSize(16)
        self.chooseFileLayout()
        self.radioGroup1Layout()
        self.radioGroup2Layout()
        self.bottomLayout()
        self.contentLayout()

    def chooseFileLayout(self):
        leftTitle1 = QLabel("# 请选择需要切块的图像:")
        leftTitle1.setFont(self.fontText)
        leftTitle1.setFixedSize(460, 30)

        chooseBtn1 = QPushButton("选择多张图像")
        chooseBtn1.setFont(self.fontText)
        chooseBtn1.setFixedHeight(36)
        chooseBtn1.clicked.connect(self.selectFiles)

        chooseBtn2 = QPushButton("选择一个文件夹")
        chooseBtn2.setFont(self.fontText)
        chooseBtn2.setFixedHeight(36)
        chooseBtn2.clicked.connect(self.selectDirs)

        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(leftTitle1)
        self.layout1.addWidget(chooseBtn1)
        self.layout1.addWidget(chooseBtn2)

    def radioGroup1Layout(self):
        leftTitle2 = QLabel("# 按照比例数量切分:")
        leftTitle2.setFont(self.fontText)
        leftTitle2.setFixedSize(460, 30)

        self.widthNum = QLineEdit()
        self.widthNum.setFixedHeight(36)
        self.widthNum.setPlaceholderText("几行(三行水平切两刀)")
        self.widthNum.setEnabled(False)
        sign_x = QLabel("x")
        sign_x.setFont(self.fontText)       
        self.heightNum = QLineEdit()
        self.heightNum.setFixedHeight(36)
        self.heightNum.setPlaceholderText("几列(四列垂直切三刀)")
        self.heightNum.setEnabled(False)

        layout4 = QHBoxLayout()
        layout4.addWidget(self.widthNum)
        layout4.addWidget(sign_x)
        layout4.addWidget(self.heightNum)

        radio1 = QRadioButton("垂直中线切一刀")
        radio1.setFont(self.fontText)
        radio1.toggled.connect(lambda: self.radioChecked1(1))
        radio1.setChecked(True)
        radio2 = QRadioButton("水平中线切一刀")
        radio2.setFont(self.fontText)
        radio2.toggled.connect(lambda: self.radioChecked1(2))
        radio3 = QRadioButton("两刀切四块")
        radio3.setFont(self.fontText)
        radio3.toggled.connect(lambda: self.radioChecked1(3))
        radio4 = QRadioButton("自定义刀法")
        radio4.setFont(self.fontText)
        radio4.toggled.connect(lambda: self.radioChecked1(4))

        self.radioGroup1 = QButtonGroup(self)
        self.radioGroup1.addButton(radio1)
        self.radioGroup1.addButton(radio2)
        self.radioGroup1.addButton(radio3)
        self.radioGroup1.addButton(radio4)

        layout2 = QHBoxLayout()
        layout2.addWidget(radio1)
        layout2.addWidget(radio2)
        layout3 = QHBoxLayout()
        layout3.addWidget(radio3)
        layout3.addWidget(radio4)

        self.layout5 = QVBoxLayout()
        self.layout5.addWidget(leftTitle2)
        self.layout5.addLayout(layout2)
        self.layout5.addLayout(layout3)
        self.layout5.addLayout(layout4)

    def radioGroup2Layout(self):
        leftTitle3 = QLabel("# 按照宽高像素切分(写入像素值会忽略比例切分选项):")
        leftTitle3.setFont(self.fontText)
        leftTitle3.setFixedSize(460, 30)

        self.widthPixel = QLineEdit()
        self.widthPixel.setFixedHeight(36)
        self.widthPixel.setPlaceholderText("宽度(px)")
        sign_x = QLabel("x")
        sign_x.setFont(self.fontText)
        self.heightPixel = QLineEdit()
        self.heightPixel.setFixedHeight(36)
        self.heightPixel.setPlaceholderText("高度(px)")

        layout6 = QHBoxLayout()
        layout6.addWidget(self.widthPixel)
        layout6.addWidget(sign_x)
        layout6.addWidget(self.heightPixel)

        radio5 = QRadioButton("从左上角开始")
        radio5.setFont(self.fontText)
        radio5.toggled.connect(lambda: self.radioChecked2(1))
        radio5.setChecked(True)
        radio6 = QRadioButton("从右上角开始")
        radio6.setFont(self.fontText)
        radio6.toggled.connect(lambda: self.radioChecked2(2))
        radio7 = QRadioButton("从左下角开始")
        radio7.setFont(self.fontText)
        radio7.toggled.connect(lambda: self.radioChecked2(3))
        radio8 = QRadioButton("从右下角开始")
        radio8.setFont(self.fontText)
        radio8.toggled.connect(lambda: self.radioChecked2(4))

        self.radioGroup2 = QButtonGroup(self)
        self.radioGroup2.addButton(radio5)
        self.radioGroup2.addButton(radio6)
        self.radioGroup2.addButton(radio7)
        self.radioGroup2.addButton(radio8)

        layout7 = QHBoxLayout()
        layout7.addWidget(radio5)
        layout7.addWidget(radio6)
        layout8 = QHBoxLayout()
        layout8.addWidget(radio7)
        layout8.addWidget(radio8)

        self.layout9 = QVBoxLayout()
        self.layout9.addWidget(leftTitle3)
        self.layout9.addLayout(layout6)
        self.layout9.addLayout(layout7)
        self.layout9.addLayout(layout8)

    def bottomLayout(self):
        self.label1 = QLabel("# 已选择：0 个文件夹、0 张图像")
        self.label1.setFont(self.fontText)

        self.outputPath = QLineEdit()
        self.outputPath.setFixedHeight(36)
        self.outputPath.setPlaceholderText("仅图像会直接输出，有文件夹会生成子目录")
        outputBtn = QPushButton("选择输出位置")
        outputBtn.setFont(self.fontText)
        outputBtn.setFixedHeight(36)
        outputBtn.clicked.connect(self.getOutputPath)

        layout1 = QHBoxLayout()
        layout1.addWidget(self.outputPath)
        layout1.addWidget(outputBtn)

        startBtn = QPushButton("开始切块")
        startBtn.setFont(self.fontText)
        startBtn.setFixedHeight(36)
        startBtn.clicked.connect(self.startSliced)

        resetBtn = QPushButton("清空重置")
        resetBtn.setFont(self.fontText)
        resetBtn.setFixedHeight(36)
        resetBtn.clicked.connect(self.reset)

        self.layout10 = QVBoxLayout()
        self.layout10.addWidget(self.label1)
        self.layout10.addLayout(layout1)
        self.layout10.addWidget(startBtn)
        self.layout10.addWidget(resetBtn)

    def contentLayout(self):
        layout = QVBoxLayout()
        layout.addLayout(self.layout1)
        layout.addStretch(2)
        layout.addLayout(self.layout5)
        layout.addStretch(2)
        layout.addLayout(self.layout9)
        layout.addStretch(3)
        layout.addLayout(self.layout10)
        layout.setContentsMargins(0, 0, 0, 20)  # 设置外边距
        
        contentWidget = QWidget()
        contentWidget.setFixedSize(480, 600)
        contentWidget.setLayout(layout)

        layout1 = QHBoxLayout()
        layout1.addWidget(contentWidget)
        self.setLayout(layout1)

    def startSliced(self):
        if len(self.imageList) == 0 or self.outputPath.text() == "":
            QMessageBox.warning(self, "警告", "您还未选择需要分块的图像或未指定输出目录")
            return 0
        outputPath = os.path.join(self.outputPath.text(), os.path.basename(self.dirList))

        if self.radioValue1 == 4:
            if self.widthNum.text() == "" or self.heightNum.text() == "":
                QMessageBox.warning(self, "警告", "自定义分块的行列数未输入完全")
                return 0
            else:
                self.value1 = [int(self.widthNum.text()), int(self.heightNum.text())]

        if bool(self.widthPixel.text()) ^ bool(self.heightPixel.text()):
            QMessageBox.warning(self, "警告", "宽高像素值未输入完全")
            return 0
        else:
            # 开启进度条显示，并强制刷新
            self.progress_dialog = ProgressDialog(self)
            self.progress_dialog.show()
            QApplication.processEvents()

            if self.widthPixel.text() == "" and self.heightPixel.text() == "":
                self.worker_thread = ImageProcessorThread(self.imageList, outputPath, self.value1, "num")
                self.worker_thread.progress_signal.connect(self.progress_dialog.update_progress)
                self.worker_thread.start()
                # 异步操作，连接 finished 信号；如果使用 wait() 会阻塞主线程，导致进度条不更新
                self.worker_thread.finished.connect(lambda: self.on_thread_finished(outputPath))
            else:
                pixelList = [int(self.widthPixel.text()), int(self.heightPixel.text())]
                self.worker_thread = ImageProcessorThread(self.imageList, outputPath, pixelList, "pixel", self.radioValue2)
                self.worker_thread.progress_signal.connect(self.progress_dialog.update_progress)
                self.worker_thread.start()
                self.worker_thread.finished.connect(lambda: self.on_thread_finished(outputPath))

    def on_thread_finished(self, outputPath):
        # 线程完成后执行的操作
        os.startfile(outputPath)
        self.reset()

    def reset(self):
        self.imageList.clear()
        self.dirList = ""
        self.label1.setText("# 已选择：0 个文件夹、0 张图像")
        self.widthNum.setText("")
        self.heightNum.setText("")
        self.widthPixel.setText("")
        self.heightPixel.setText("")
        self.outputPath.setText("")

    def getOutputPath(self):
        path = QFileDialog.getExistingDirectory(self, "选择文件夹", "C:\\")
        self.outputPath.setText(path)

    def radioChecked2(self, e):
        self.radioValue2 = e

    def radioChecked1(self, e):
        if e == 1:
            self.value1 = [0, 1]
        if e == 2:
            self.value1 = [1, 0]
        if e == 3:
            self.value1 = [1, 1]

        if e == 4:
            self.widthNum.setEnabled(True)
            self.heightNum.setEnabled(True)
        else:
            self.widthNum.setEnabled(False)
            self.heightNum.setEnabled(False)
        self.radioValue1 = e
    
    def selectFiles(self):
        self.imageList.clear()
        filePath, fileType = QFileDialog.getOpenFileNames(self, "选择文件", "C:\\", "All Files (*);;Images (*.jpg *.jpeg *.png)")
        self.imageList = filePath
        self.label1.setText(f"# 已选择：0 个文件夹、{len(self.imageList)} 张图像")
    
    def selectDirs(self):
        self.imageList.clear()
        self.dirList = QFileDialog.getExistingDirectory(self, "选择文件夹", "C:\\")

        for filename in os.listdir(self.dirList):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                pdf_path = os.path.join(self.dirList, filename)
                self.imageList.append(pdf_path)

        self.label1.setText(f"# 已选择：1 个文件夹、{len(self.imageList)} 张图像")
