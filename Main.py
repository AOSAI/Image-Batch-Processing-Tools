from PyQt5.QtWidgets import (QMainWindow, QApplication, QDesktopWidget,
                             QAction, QWidget, QVBoxLayout, QProgressBar,
                             QLabel)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QFileInfo, Qt
import sys
import imageProcessing.BatchProcessing as ImgTools
import fileProcessing.fileMain as fileTools
from PDFImage import PDFImage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainUI()
        self.mainMenu()
        self.mainStatus()
        self.menuClicked(None)

    # def closeEvent(self, event):
    #     self.fileTools.decompression.cleanup_temp_dir()
    #     # 调用父类的 closeEvent 来执行默认的关闭操作
    #     super().closeEvent(event)

    def progressChange(self, type, value):
        if type == 0:
            self.progressBar.setMaximum(value)
        if type == 1:
            self.progressBar.setValue(value)

    def mainStatus(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.progressBar.setFixedWidth(200)
        label = QLabel("状态栏")
        self.statusBar().addPermanentWidget(label, Qt.AlignLeft)
        self.statusBar().addPermanentWidget(self.progressBar, Qt.AlignRight)

    def mainMenu(self):
        menuBar = self.menuBar()
        font = QFont()
        # font.setFamily("华文行楷")
        font.setPixelSize(16)
        menuBar.setFont(font)

        fileMenu = QAction("压缩解压", self)
        fileMenu.triggered.connect(lambda: self.menuClicked("fileProcessing"))
        menuBar.addAction(fileMenu)

        imgMenu = menuBar.addMenu('图像处理')
        imgProcess = QAction("批量处理", self)
        imgProcess.triggered.connect(lambda: self.menuClicked("imageProcessing"))
        imgMenu.addAction(imgProcess)

        PDFImgMenu = menuBar.addMenu("PDF图像")
        PDFImgMenu.aboutToShow.connect(lambda: self.menuClicked("PDFImage"))

        imgCrawlerMenu = menuBar.addMenu("网络爬虫")

    def menuClicked(self, target):
        if target == None:
            self.fileTools = fileTools.fileMain()
            self.setCentralWidget(self.fileTools)
        if target == "imageProcessing":
            self.imgTools = ImgTools.BatchProcessing()
            self.imgTools.compress.signal.new_progress.connect(self.progressChange)
            self.imgTools.shape.signal.new_progress.connect(self.progressChange)
            self.imgTools.resolution.signal.new_progress.connect(self.progressChange)
            self.setCentralWidget(self.imgTools)
        if target == "fileProcessing":
            self.fileTools = fileTools.fileMain()
            self.setCentralWidget(self.fileTools)
        if target == "PDFImage":
            self.pdfImgTools = PDFImage.PDFImageMain()
            self.pdfImgTools.PDFToImages.signal.new_progress.connect(self.progressChange)
            self.setCentralWidget(self.pdfImgTools)

    def mainUI(self):
        self.resize(1000, 720)
        self.setWindowTitle("哆啦A梦的百宝箱")
        root_path = QFileInfo(__file__).absolutePath()
        self.setWindowIcon(QIcon(root_path + '/public/mainlogo.png'))
        # 让程序运行时窗口居中打开
        frame = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(cp)
        self.move(frame.topLeft())
        self.setFixedSize(self.width(), self.height())
        # self.setCentralWidget(imgTools.ImageCompress())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
