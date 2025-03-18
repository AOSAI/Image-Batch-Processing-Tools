from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer, QSize
from PyQt5.QtGui import QIcon, QFont, QIntValidator
from PyQt5.QtWidgets import (QSizePolicy, QLabel, QLineEdit, QPushButton,
                             QFormLayout, QWidget, QHBoxLayout, QVBoxLayout,
                             QFileDialog, QGridLayout, QMessageBox,
                             QVBoxLayout, QApplication, QMainWindow, QAction)
import os
import zipfile


class fileCompression(QWidget):
    def __init__(self):
        super().__init__()
        self.file_list = []
        self.folder = ""
        self.setFixedWidth(340)
        self.contentLayout()

    def doCompression(self):
        if self.file_list == [] and self.folder == "":
            QMessageBox.warning(self, "警告", "您还未选择需要压缩的文件或文件夹")
            return 0

        if self.folder == "":
            output1 = "\\".join(
                self.file_list[0].split("/")[0:-1]) if self.outputPath.text(
                ) == "" else self.outputPath.text()
            output2 = output1 + "/compressedFile.zip"

            zip = zipfile.ZipFile(output2, "w", zipfile.ZIP_DEFLATED)
            for file in self.file_list:
                zip.write(file)
            zip.close()
            os.startfile(output1)
        if self.file_list == []:
            output1 = self.folder + '.zip'  # 压缩文件的名字
            output2 = "\\".join(self.folder.split("/")[:-1])
            zip = zipfile.ZipFile(output1, 'w', zipfile.ZIP_DEFLATED)
            for root, dirs, files in os.walk(self.folder):
                relative_root = '' if root == self.folder else root.replace(
                    self.folder, '') + os.sep  # 计算文件相对路径
                for filename in files:
                    zip.write(os.path.join(root, filename),
                              relative_root + filename)  # 文件路径 压缩文件路径（相对路径）
            zip.close()
            os.startfile(output2)

    def selectFiles(self):
        filePath, fileType = QFileDialog.getOpenFileNames(
            self, "选择文件", "C:\\", "All Files (*);")
        self.folder = ""
        self.file_list = filePath
        self.label1.setText(f"已选择：{len(self.file_list)}个文件")

    def selectFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, "选择文件夹", "C:\\")
        self.file_list = []
        self.folder = folderPath
        self.label1.setText(f"已选择1个文件夹：{self.folder}")

    def compressedPath(self):
        path = QFileDialog.getExistingDirectory(self, "选择文件夹", "C:\\")
        # path = path + "/compressedFile.zip"
        self.outputPath.setText(path)

    def contentLayout(self):
        fontText1 = QFont()
        fontText1.setPixelSize(14)

        chooseBtn1 = QPushButton("选择文件")
        chooseBtn1.setFont(fontText1)
        chooseBtn1.setFixedHeight(30)
        chooseBtn1.clicked.connect(self.selectFiles)

        chooseBtn2 = QPushButton("选择文件夹")
        chooseBtn2.setFont(fontText1)
        chooseBtn2.setFixedHeight(30)
        chooseBtn2.clicked.connect(self.selectFolder)

        self.label1 = QLabel("已选择：0个文件 / 0个文件夹")
        self.label1.setFont(fontText1)

        self.outputPath = QLineEdit()
        self.outputPath.setFixedHeight(30)
        self.outputPath.setPlaceholderText("默认为第一个已选文件的路径下")
        chooseBtn3 = QPushButton("选择输出位置")
        chooseBtn3.setFont(fontText1)
        chooseBtn3.setFixedHeight(30)
        chooseBtn3.clicked.connect(self.compressedPath)

        layout1 = QHBoxLayout()
        layout1.addWidget(chooseBtn1)
        layout1.addWidget(chooseBtn2)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.outputPath)
        layout2.addWidget(chooseBtn3)

        contentLayout = QVBoxLayout()
        contentLayout.addLayout(layout1)
        contentLayout.addWidget(self.label1)
        contentLayout.addLayout(layout2)
        contentLayout.setAlignment(Qt.AlignTop)
        contentLayout.setSpacing(30)

        self.setLayout(contentLayout)
