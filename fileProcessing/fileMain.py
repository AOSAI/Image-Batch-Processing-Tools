from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer, QSize
from PyQt5.QtGui import QIcon, QFont, QIntValidator
from PyQt5.QtWidgets import (QSizePolicy, QLabel, QLineEdit, QPushButton,
                             QFormLayout, QWidget, QHBoxLayout, QFileDialog,
                             QGridLayout, QMessageBox, QVBoxLayout,
                             QApplication, QMainWindow, QAction, QFrame)
import os
import zipfile
import fileProcessing.compression as compression
import fileProcessing.decompression as decompression


class fileMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.compression = compression.fileCompression()
        self.decompression = decompression.fileDecompression()
        self.toolsBar()
        self.contentLayout()

    def setMouseMenuMethod(self):
        QMessageBox.warning(self, "说明", "该功能暂未实现")

    def deleteFilesMethod(self):
        self.decompression.removeFilefromZip()

    def decompressionMethod(self):
        self.decompression.doDecompression()

    def addFilesMethod(self):
        self.compression.doCompression()

    def toolsBar(self):
        compress_tools = self.addToolBar("compress_tools")
        compress_tools.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        compress_tools.setIconSize(QSize(36, 36))
        root_path = "\\".join(
            os.path.abspath(__file__).split("\\")[0:-2]) + "/public"

        addFiles = QAction(QIcon(root_path + "/logo_add.png"), "压缩至", self)
        addFiles.setToolTip("压缩文件")
        addFiles.triggered.connect(self.addFilesMethod)
        compress_tools.addAction(addFiles)

        deCompress_tools = self.addToolBar("deCompress_tools")
        deCompress_tools.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        deCompress_tools.setIconSize(QSize(36, 36))

        decompression = QAction(QIcon(root_path + "/logo_freeze.png"), "解压到", self)
        decompression.setToolTip("解压文件")
        decompression.triggered.connect(self.decompressionMethod)
        deCompress_tools.addAction(decompression)

        deleteFiles = QAction(QIcon(root_path + "/logo_delete.png"), "删除", self)
        deleteFiles.setToolTip("删除文件")
        deleteFiles.triggered.connect(self.deleteFilesMethod)
        deCompress_tools.addAction(deleteFiles)

        other_tools = self.addToolBar("other_tools")
        other_tools.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        other_tools.setIconSize(QSize(36, 36))

        setMouseMenu = QAction(QIcon(root_path + "/logo_mouseMenu.png"), "菜单栏", self)
        setMouseMenu.setToolTip("将压缩·解压添加到鼠标右键菜单栏")
        setMouseMenu.triggered.connect(self.setMouseMenuMethod)
        other_tools.addAction(setMouseMenu)

    def contentLayout(self):
        contentArea = QWidget()
        contentArea.setFixedSize(1000, 600)

        v_line = QFrame()
        v_line.setFrameShape(QFrame.VLine)
        v_line.setFrameShadow(QFrame.Plain)
        v_line.setLineWidth(1)

        layout = QHBoxLayout()
        layout.addWidget(self.compression)
        layout.addWidget(v_line)
        layout.addWidget(self.decompression)
        contentArea.setLayout(layout)

        self.setCentralWidget(contentArea)
