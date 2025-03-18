from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer, QSize, QDir, QModelIndex
from PyQt5.QtGui import QIcon, QFont, QStandardItemModel
from PyQt5.QtWidgets import (QSizePolicy, QLabel, QLineEdit, QPushButton,
                             QFormLayout, QWidget, QHBoxLayout, QFileDialog,
                             QGridLayout, QMessageBox, QVBoxLayout,
                             QApplication, QMainWindow, QAction,
                             QFileSystemModel, QTreeView, QFrame)
import os
import zipfile
import shutil
import atexit
import tempfile
import subprocess
import platform


class fileDecompression(QWidget):
    def __init__(self):
        super().__init__()
        self.zip_file = ""
        self.selected_row = ""
        self.temp_dir = ""
        self.setFixedWidth(620)
        self.contentLayout()

    def open_file(self, file_path):
        try:
            if platform.system() == 'Windows':
                subprocess.run(['start', '', file_path],
                               check=True,
                               shell=True)
            elif platform.system() == 'Darwin':
                subprocess.run(['open', file_path], check=True)
            elif platform.system() == 'Linux':
                subprocess.run(['xdg-open', file_path], check=True)
            else:
                QMessageBox.critical(self, "错误", "不支持该操作系统")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "错误", f"无法打开文件 {file_path}")

    def doDecompression(self):
        if self.zip_file == "":
            QMessageBox.warning(self, "警告", "您还未选择需要解压的ZIP文件")
            return 0

        zip = zipfile.ZipFile(self.zip_file)
        output = self.outputPath.text(
        ) if self.outputPath.text() != "" else os.path.dirname(self.zip_file)
        zip.extractall(output)  # 会被解压到输入的路径中
        zip.close()
        os.startfile(output)

    def removeFilefromZip(self):
        if self.zip_file == "":
            QMessageBox.warning(self, "警告", "您还未选择压缩文件")
            return 0
        if self.selected_row == "":
            QMessageBox.warning(self, "警告", "您还未选择想要删除的文件")
            return 0

        del_path = self.temp_dir + self.selected_row
        try:
            if os.path.isfile(del_path):
                os.remove(del_path)
            else:
                shutil.rmtree(del_path)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"删除失败：{e}")

        with zipfile.ZipFile(self.zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.temp_dir)
                    zipf.write(file_path, arcname=relative_path)

    def treeDoubleClicked(self, index: QModelIndex):
        if isinstance(index, QModelIndex):
            full_path = self.model.filePath(index)
            if os.path.isfile(full_path):
                self.open_file(full_path)

    def treeFirstClicked(self, index: QModelIndex):
        if isinstance(index, QModelIndex):
            full_path = self.model.filePath(index)
            if self.temp_dir != "":
                self.selected_row = full_path[len(self.temp_dir):]

    def selectFiles(self):
        filePath, fileType = QFileDialog.getOpenFileName(
            self, "选择文件", "C:\\", "*.zip;")
        self.zip_file = filePath
        self.zipTreeView(self.zip_file)

    def compressedPath(self):
        path = QFileDialog.getExistingDirectory(self, "选择文件夹", "C:\\")
        self.outputPath.setText(path)

    def cleanup_temp_dir(self):
        abstract_model = self.model.pyqtConfigure()
        file_system_watcher = abstract_model.fileSystemWatcher()
        file_system_watcher.removePath(self.temp_dir)
        shutil.rmtree(self.temp_dir)

    def zipTreeView(self, zip_data):
        self.temp_dir = tempfile.mkdtemp()  # 创建临时文件夹
        atexit.register(self.cleanup_temp_dir)  # 注册退出时执行的函数

        with zipfile.ZipFile(zip_data, 'r') as zip_ref:
            all_entries = zip_ref.namelist()

            def writeFile():
                with zip_ref.open(subname) as file_data:
                    with open(file_path, 'wb') as output_file:
                        shutil.copyfileobj(file_data, output_file)

            # 解压缩 zip 文件到临时文件夹
            for subname in all_entries:
                try:
                    file_name = subname.encode('cp437').decode(
                        'gbk', 'replace')
                except Exception as e:
                    file_name = subname.encode('utf-8').decode(
                        'gbk', 'replace')

                file_path = os.path.join(self.temp_dir, file_name)

                if '/' or '\\' in file_name:
                    if file_name[-1] == '/' or file_name[-1] == '\\':
                        os.makedirs(file_path, exist_ok=True)
                    else:
                        folder_path = os.path.dirname(file_path)
                        os.makedirs(folder_path, exist_ok=True)
                        writeFile()
                else:
                    writeFile()

            self.model.setRootPath(self.temp_dir)

        # 设置 QTreeView 展示文件系统
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.temp_dir))

    def contentLayout(self):
        fontText1 = QFont()
        fontText1.setPixelSize(14)

        chooseBtn1 = QPushButton("选择文件")
        chooseBtn1.setFont(fontText1)
        chooseBtn1.setFixedHeight(30)
        chooseBtn1.clicked.connect(self.selectFiles)

        self.outputPath = QLineEdit()
        self.outputPath.setFixedHeight(30)
        self.outputPath.setPlaceholderText("默认为当前文件路径下解压")
        chooseBtn2 = QPushButton("选择输出位置")
        chooseBtn2.setFont(fontText1)
        chooseBtn2.setFixedHeight(30)
        chooseBtn2.clicked.connect(self.compressedPath)

        layout1 = QHBoxLayout()
        layout1.addWidget(self.outputPath)
        layout1.addWidget(chooseBtn2)

        v_line = QFrame()
        v_line.setFrameShape(QFrame.HLine)
        v_line.setFrameShadow(QFrame.Plain)
        v_line.setLineWidth(1)

        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.doubleClicked.connect(self.treeDoubleClicked)
        self.tree.clicked.connect(self.treeFirstClicked)
        self.tree.setFixedHeight(350)
        self.tree.header().setDefaultSectionSize(100)
        self.tree.header().resizeSection(0, 200)

        self.tree_header_model = QStandardItemModel()
        self.tree_header_model.setColumnCount(4)
        self.tree_header_model.setHeaderData(0, Qt.Horizontal, "文件名称", 0)
        self.tree_header_model.setHeaderData(1, Qt.Horizontal, "文件大小", 0)
        # tree_header_model.setHeaderData(2, Qt.Horizontal, "压缩后大小", 0)
        self.tree_header_model.setHeaderData(2, Qt.Horizontal, "文件类型", 0)
        self.tree_header_model.setHeaderData(3, Qt.Horizontal, "最后修改日期", 0)
        # tree_header_model.setHeaderData(5, Qt.Horizontal, "CRC32", 0)

        self.tree.header().setModel(self.tree_header_model)
        self.tree.setRootIndex(self.model.index(""))

        contentLayout = QVBoxLayout()
        contentLayout.addWidget(chooseBtn1)
        contentLayout.addLayout(layout1)
        contentLayout.addWidget(v_line)
        contentLayout.addWidget(self.tree)
        contentLayout.setAlignment(Qt.AlignTop)
        contentLayout.setSpacing(30)

        self.setLayout(contentLayout)
