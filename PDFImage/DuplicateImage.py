from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer, QSize
from PyQt5.QtGui import QIcon, QFont, QIntValidator
from PyQt5.QtWidgets import (QFileDialog, QLabel, QLineEdit, QPushButton,
                             QTextBrowser, QWidget, QHBoxLayout, QVBoxLayout,
                             QFileDialog, QButtonGroup, QMessageBox,
                             QVBoxLayout, QRadioButton, QApplication, QListWidgetItem)
import imagehash, hashlib, os
from commonComponent.ProgressDialog import ProgressDialog

class ImageProcessThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, inputList, outputDir, algorithm, method):
        super().__init__()
        self.inputList = inputList
        self.outputDir = outputDir

    def calculate_md5(self, image_path):
        """ 计算文件的 MD5 哈希值 """
        with open(image_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def find_duplicate_images_md5(self, folder_path):
        md5_dict = {}
        duplicates = []
        step = 0
        
        for file in self.inputList:
            step += 1
            self.progress_signal.emit(int((step / len(self.inputList)) * 100))
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_md5 = self.calculate_md5(file)

                if file_md5 in md5_dict:
                    duplicates.append((md5_dict[file_md5], file))
                else:
                    md5_dict[file_md5] = file

        self.progress_signal.emit(100)
        return duplicates

    def function_pHash(self):
        return 0

    def run(self):
        return 0
            


class RemoveDuplicateImages(QWidget):
    def __init__(self):
        super().__init__()
        self.imageList = []
        self.dirList = ""
        self.fontText = QFont()
        self.fontText.setPixelSize(16)
        self.chooseFileLayout()
        self.radioGroupLayout()
        self.bottomLayout()
        self.leftLayout()
        self.contentLayout()

    def chooseFileLayout(self):
        title1 = QLabel("# 请将需要去重的图像集放入同一个文件夹中:")
        title1.setFont(self.fontText)
        title1.setFixedSize(460, 30)

        chooseBtn1 = QPushButton("选择一个文件夹")
        chooseBtn1.setFont(self.fontText)
        chooseBtn1.setFixedHeight(36)
        chooseBtn1.clicked.connect(self.selectDirs)

        self.label1 = QLabel("# 提示：尚未选择文件夹")
        self.label1.setFont(self.fontText)

        self.outputPath = QLineEdit()
        self.outputPath.setFixedHeight(36)
        self.outputPath.setPlaceholderText("仅在选择备份原始图像数据时可用")
        self.outputPath.setEnabled(False)
        self.outputBtn = QPushButton("选择输出位置")
        self.outputBtn.setFont(self.fontText)
        self.outputBtn.setFixedHeight(36)
        self.outputBtn.clicked.connect(self.getOutputPath)
        self.outputBtn.setEnabled(False)

        layout1 = QHBoxLayout()
        layout1.addWidget(self.outputPath)
        layout1.addWidget(self.outputBtn)

        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(title1)
        self.layout1.addWidget(chooseBtn1)
        self.layout1.addWidget(self.label1)
        self.layout1.addLayout(layout1)

    def radioGroupLayout(self):
        title2 = QLabel("# 请选择辨别图像的方式:")
        title2.setFont(self.fontText)
        title2.setFixedSize(460, 30)

        radio1 = QRadioButton("MD5-哈希值")
        radio1.setFont(self.fontText)
        radio1.toggled.connect(lambda: self.radioChecked1(1))
        radio1.setChecked(True)
        radio2 = QRadioButton("感知哈希(pHash)")
        radio2.setFont(self.fontText)
        radio2.toggled.connect(lambda: self.radioChecked1(2))
        self.radioGroup1 = QButtonGroup(self)
        self.radioGroup1.addButton(radio1)
        self.radioGroup1.addButton(radio2)

        title3 = QLabel("# 请选择相同/相似图像的处理办法:")
        title3.setFont(self.fontText)
        title3.setFixedSize(460, 30)

        radio3 = QRadioButton("直接删除")
        radio3.setFont(self.fontText)
        radio3.toggled.connect(lambda: self.radioChecked2(1))
        radio3.setChecked(True)
        radio4 = QRadioButton("交互式处理，由人判断")
        radio4.setFont(self.fontText)
        radio4.toggled.connect(lambda: self.radioChecked2(2))
        self.radioGroup2 = QButtonGroup(self)
        self.radioGroup2.addButton(radio3)
        self.radioGroup2.addButton(radio4)

        title4 = QLabel("# 请选择是否备份原始图像数据:")
        title4.setFont(self.fontText)
        title4.setFixedSize(460, 30)

        radio5 = QRadioButton("否，不需要数据备份")
        radio5.setFont(self.fontText)
        radio5.toggled.connect(lambda: self.radioChecked3(1))
        radio5.setChecked(True)
        radio6 = QRadioButton("是，在新目录中保存")
        radio6.setFont(self.fontText)
        radio6.toggled.connect(lambda: self.radioChecked3(2))
        self.radioGroup3 = QButtonGroup(self)
        self.radioGroup3.addButton(radio5)
        self.radioGroup3.addButton(radio6)
        
        layout2 = QHBoxLayout()
        layout2.addWidget(radio1)
        layout2.addWidget(radio2)
        layout3 = QHBoxLayout()
        layout3.addWidget(radio3)
        layout3.addWidget(radio4)
        layout4 = QHBoxLayout()
        layout4.addWidget(radio5)
        layout4.addWidget(radio6)

        self.layout2 = QVBoxLayout()
        self.layout2.addWidget(title2)
        self.layout2.addLayout(layout2)
        self.layout2.addWidget(title3)
        self.layout2.addLayout(layout3)
        self.layout2.addWidget(title4)
        self.layout2.addLayout(layout4)

    def bottomLayout(self):
        startBtn = QPushButton("开始去重")
        startBtn.setFont(self.fontText)
        startBtn.setFixedHeight(36)
        startBtn.clicked.connect(self.startSliced)

        resetBtn = QPushButton("清空重置")
        resetBtn.setFont(self.fontText)
        resetBtn.setFixedHeight(36)
        resetBtn.clicked.connect(self.reset)

        self.layout3 = QVBoxLayout()
        self.layout3.addWidget(startBtn)
        self.layout3.addWidget(resetBtn)

    def leftLayout(self):
        leftWidget = QTextBrowser()
        leftWidget.setFixedSize(480, 600)
        leftWidget.setStyleSheet("background: transparent; border: none;"
                                 "font-size: 16px; margin-top: 3px;"
                                )
        leftWidget.setHtml("""
            <p># 小葵花妈妈课堂开课啦！</p>
            <p>普通的哈希值算法（MD5，SHA-1等）主要用于检测图像的二进制数据是否完全一致。这种判别的条件十分苛刻，稍有不同就会判断为不同。比如：</p>
            <li>1. 分辨率不同（如 1024×1024 vs 1023×1023）</li>
            <li>2. 格式转换（如 PNG 转 JPG）</li>
            <li>3. 颜色稍有变化（如亮度调整、滤镜）</li>
            <li>4. 轻微裁剪、旋转</li>
            <li>5. 压缩算法不同（如不同质量的 JPEG）</li>
            <p>感知哈希（Perceptual Hashing）是像素级相似检测方法的一种，其思想为：将图像转换为 低分辨率灰度图，然后计算其哈希值，即使有小的视觉变化（如缩放、轻微编辑、格式转换），哈希值仍然相近。</p>
            <p>像素级相似检测，还有 ORB/SIFT特征匹配、深度学习等算法。前者通过提取图像的关键特征点来比较相似性，不适用于大量具有相似背景或主体的判别；后者有点大炮打蚊子，大材小用了。</p>
            <p># 使用小Tips：</p> 
            <p>可以先用MD5先筛选一遍，直接删除即可，因为必然是相同的图像；然后再用感知哈希，选择交互式处理，筛选完了由自己来判断是否删除。这样的组合比较合理。</p>               
        """)
        self.layout4 = QVBoxLayout()
        self.layout4.addWidget(leftWidget)

    def contentLayout(self):
        layout = QVBoxLayout()
        layout.addLayout(self.layout1)
        layout.addStretch(1)
        layout.addLayout(self.layout2)
        layout.addStretch(1)
        layout.addLayout(self.layout3)
        layout.setContentsMargins(0, 0, 0, 20)  # 设置外边距
        layout.setSpacing(15)  # # 设置所有子控件之间的间距
        
        rightWidget = QWidget()
        rightWidget.setFixedSize(480, 600)
        rightWidget.setLayout(layout)

        layout1 = QHBoxLayout()
        layout1.addLayout(self.layout4)
        layout1.addWidget(rightWidget)
        self.setLayout(layout1)

    def startSliced(self):
        if len(self.imageList) == 0:
            QMessageBox.warning(self, "警告", "您还未选择需要去重的图像集")
            return 0
        
        outputPath = ""
        if self.radioValue3 == 2:
            if self.outputPath.text() == "":
                QMessageBox.warning(self, "警告", "您还未设置新的输出目录")
                return 0
            else:
                outputPath = os.path.join(self.outputPath.text(), os.path.basename(self.dirList))
        else:
            outputPath = self.dirList

        # 开启进度条显示，并强制刷新
        self.progress_dialog = ProgressDialog(self)
        self.progress_dialog.show()
        QApplication.processEvents()
        self.worker_thread = ImageProcessThread(self.imageList, outputPath, self.value1, "num")
        self.worker_thread.progress_signal.connect(self.progress_dialog.update_progress)
        self.worker_thread.start()
        self.worker_thread.finished.connect(lambda: self.on_thread_finished(outputPath))
        
    def on_thread_finished(self, outputPath):
        os.startfile(outputPath)
        self.reset()

    def reset(self):
        self.imageList.clear()
        self.dirList = ""
        self.label1.setText("# 已选择：0 个文件夹、0 张图像")
        self.outputPath.setText("")

    def getOutputPath(self):
        path = QFileDialog.getExistingDirectory(self, "选择文件夹", "C:\\")
        self.outputPath.setText(path)

    def radioChecked3(self, e):
        if e == 2:
            self.outputPath.setEnabled(True)
            self.outputBtn.setEnabled(True)
        else:
            self.outputPath.setEnabled(False)
            self.outputBtn.setEnabled(False)
        self.radioValue3 = e

    def radioChecked2(self, e):
        self.radioValue2 = e

    def radioChecked1(self, e):
        self.radioValue1 = e
    
    def selectDirs(self):
        self.imageList.clear()
        self.dirList = QFileDialog.getExistingDirectory(self, "选择文件夹", "C:\\")

        for filename in os.listdir(self.dirList):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                pdf_path = os.path.join(self.dirList, filename)
                self.imageList.append(pdf_path)

        self.label1.setText(f"# 已选择：1 个文件夹、{len(self.imageList)} 张图像")