from PyQt5.QtWidgets import (QSizePolicy, QLabel, QLineEdit, QPushButton,
                             QFormLayout, QMainWindow, QHBoxLayout, QFileDialog,
                             QGridLayout, QMessageBox, QVBoxLayout,
                             QApplication, QAction, QWidget, QFrame)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import os
from PDFImage import PDFToImages, ImagesToPDF
from PDFImage import SlicedImage, SplicingImages, DuplicateImage

class PDFImageMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.toolsBar()
        self.PDFToImages = PDFToImages.ToImages()
        # self.ImagesToPDF = ImagesToPDF()
        self.contentLayout()

    def splitPage(self):
        self.setPage = PDFToImages.ToImages()
        self.setCentralWidget(self.setPage)

    def mergePage(self):
        self.setPage = ImagesToPDF.PDFDragDropWidget()
        self.setCentralWidget(self.setPage)

    def slicedPage(self):
        self.setPage = SlicedImage.ToSlicedImages()
        self.setCentralWidget(self.setPage)

    def splicingPage(self):
        self.setPage = SplicingImages.ToSplicingImages()
        self.setCentralWidget(self.setPage)

    def duplicatePage(self):
        self.setPage = DuplicateImage.RemoveDuplicateImages()
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
        
        transToImages = QAction(QIcon(root_path + "/PDF_output.png"), "提取", self)
        transToImages.setToolTip("将PDF中的图像无损提取出来")
        transToImages.triggered.connect(self.splitPage)
        pdfImageTools.addAction(transToImages)

        slicedImage = QAction(QIcon(root_path + "/sliced_image.png"), "切分", self)
        slicedImage.setToolTip("将图像按照规则分块切分")
        slicedImage.triggered.connect(self.slicedPage)
        pdfImageTools.addAction(slicedImage)

        splicingImages = QAction(QIcon(root_path + "/splicing_images.png"), "拼接", self)
        splicingImages.setToolTip("将图像按照规则拼接在一起")
        splicingImages.triggered.connect(self.splicingPage)
        pdfImageTools.addAction(splicingImages)

        duplicateImages = QAction(QIcon(root_path + "/remove_duplicate.png"), "去重", self)
        duplicateImages.setToolTip("去除文件夹中重复的图像")
        duplicateImages.triggered.connect(self.duplicatePage)
        pdfImageTools.addAction(duplicateImages)

    def contentLayout(self):
        self.setCentralWidget(self.PDFToImages)