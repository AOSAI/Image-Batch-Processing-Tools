from PyQt5.QtWidgets import (QSizePolicy, QLabel, QLineEdit, QPushButton,
                             QFormLayout, QMainWindow, QHBoxLayout, QFileDialog,
                             QGridLayout, QMessageBox, QVBoxLayout,
                             QApplication, QAction, QWidget, QFrame)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import os
from PDFImage import PDFToImages
from PDFImage import ImagesToPDF

class PDFImageMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.toolsBar()
        self.PDFToImages = PDFToImages.ToImages()
        # self.ImagesToPDF = ImagesToPDF()
        self.contentLayout()

    def splitPage(self):
        self.setPage = self.PDFToImages
        self.setCentralWidget(self.setPage)

    def mergePage(self):
        self.setPage = ImagesToPDF.PDFDragDropWidget()
        self.setCentralWidget(self.setPage)

    def toolsBar(self):
        root_path = "\\".join(os.path.abspath(__file__).split("\\")[0:-2]) + "/public"

        pdfImageTools = self.addToolBar("pdfImageTools")
        pdfImageTools.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        pdfImageTools.setIconSize(QSize(36, 36))

        transToPDFs = QAction(QIcon(root_path + "/PDF_input.png"), "合并", self)
        transToPDFs.setToolTip("将图像合并成PDF文件")
        transToPDFs.triggered.connect(self.mergePage)
        pdfImageTools.addAction(transToPDFs)
        
        transToImages = QAction(QIcon(root_path + "/PDF_output.png"), "拆分", self)
        transToImages.setToolTip("将PDF中的图像无损提取出来")
        transToImages.triggered.connect(self.splitPage)
        pdfImageTools.addAction(transToImages)

    def contentLayout(self):
        self.setCentralWidget(self.PDFToImages)