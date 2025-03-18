from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer, QSize
from PyQt5.QtGui import QIcon, QFont, QIntValidator
from PyQt5.QtWidgets import (QSizePolicy, QLabel, QLineEdit, QPushButton,
                             QFormLayout, QWidget, QHBoxLayout, QVBoxLayout,
                             QFileDialog, QButtonGroup, QMessageBox,
                             QVBoxLayout, QRadioButton, QListWidget, QListWidgetItem)
import os
import fitz
import imageProcessing.BatchProcessing as batch

class PDFDragDropWidget(QWidget):
    """自定义 PDF 拖拽区域"""
    def __init__(self, on_files_dropped):
        super().__init__()
        self.on_files_dropped = on_files_dropped
        self.setAcceptDrops(True)
        self.setFixedSize(460, 300)
        self.setStyleSheet("background:#f5f6fa; border: 2px dashed #aaa; padding: 20px;")

        self.label = QLabel("拖拽 PDF 文件到这里", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; color: #555;")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    # 处理拖拽进入事件
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    # 处理文件释放事件
    def dropEvent(self, event):
        pdf_files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(".pdf"):
                pdf_files.append(file_path)

        if pdf_files:
            self.on_files_dropped(pdf_files)
        else:
            QMessageBox.warning(self, "提示", "未检测到 PDF 文件，请重新拖拽！")

class ToImages(QWidget):
    def __init__(self):
        super().__init__()
        self.pdf_list = []
        self.pdf_dir = ""
        self.fontText = QFont()
        self.fontText.setPixelSize(16)
        self.contentLayout()
        self.signal = batch.signalandslot()

    def leftLayout(self):
        leftArea = QWidget()
        leftArea.setFixedSize(480, 600)

        self.dragDropWidget = PDFDragDropWidget(self.process_pdfs)

        leftTitle = QLabel("# 请选择您需要提取图像的PDF文件:")
        leftTitle.setFont(self.fontText)
        leftTitle.setFixedSize(460, 30)

        chooseBtn1 = QPushButton("选择多个PDF文件")
        chooseBtn1.setFont(self.fontText)
        chooseBtn1.setFixedHeight(40)
        chooseBtn1.clicked.connect(self.selectFiles)

        chooseBtn2 = QPushButton("选择一个文件夹")
        chooseBtn2.setFont(self.fontText)
        chooseBtn2.setFixedHeight(40)
        chooseBtn2.clicked.connect(self.selectDirs)

        self.outputPath = QLineEdit()
        self.outputPath.setFixedHeight(36)
        self.outputPath.setPlaceholderText("请选择拆分图像的保存目录")
        chooseBtn3 = QPushButton("选择输出位置")
        chooseBtn3.setFont(self.fontText)
        chooseBtn3.setFixedHeight(36)
        chooseBtn3.clicked.connect(self.getOutputPath)

        layout1 = QHBoxLayout()
        layout1.addWidget(self.outputPath)
        layout1.addWidget(chooseBtn3)

        radio3 = QRadioButton("按文件名创建子文件夹")
        radio3.setFont(self.fontText)
        radio3.toggled.connect(lambda: self.radioChecked1(1))
        radio3.setChecked(True)
        radio4 = QRadioButton("全部在输出目录输出")
        radio4.setFont(self.fontText)
        radio4.toggled.connect(lambda: self.radioChecked1(2))

        radioGroup1 = QButtonGroup(leftArea)
        radioGroup1.addButton(radio3)
        radioGroup1.addButton(radio4)
        layout2 = QHBoxLayout()
        layout2.addWidget(radio3)
        layout2.addWidget(radio4)

        layout = QVBoxLayout()
        layout.addWidget(leftTitle)
        layout.addWidget(self.dragDropWidget)
        layout.addWidget(chooseBtn1)
        layout.addWidget(chooseBtn2)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        leftArea.setLayout(layout)
        return leftArea

    def rightLayout(self):
        rightArea = QWidget()
        rightArea.setFixedSize(480, 600)

        startBtn = QPushButton("开始拆分")
        startBtn.setFont(self.fontText)
        startBtn.setFixedHeight(40)
        startBtn.clicked.connect(self.startSplit)

        resetBtn = QPushButton("清空重置")
        resetBtn.setFont(self.fontText)
        resetBtn.setFixedHeight(40)
        resetBtn.clicked.connect(self.reset)

        self.label1 = QLabel(f"# 已选择：{len(self.pdf_list)} 个PDF文件")
        self.label1.setFont(self.fontText)

        self.fileListWidget = QListWidget()
        self.fileListWidget.setFixedSize(460, 400)
        self.fileListWidget.setStyleSheet("border: 1px solid #aaa; font-size: 14px; padding: 5px;")

        layout = QVBoxLayout()
        layout.addWidget(startBtn)
        layout.addWidget(resetBtn)
        layout.addWidget(self.label1)
        layout.addWidget(self.fileListWidget)
        rightArea.setLayout(layout)
        return rightArea

    def contentLayout(self):
        contentLayout = QHBoxLayout()
        contentLayout.addWidget(self.leftLayout(), Qt.AlignCenter)
        contentLayout.addWidget(self.rightLayout(), Qt.AlignCenter)
        self.setLayout(contentLayout)

    def startSplit(self):
        if len(self.pdf_list) == 0 or self.outputPath.text() == "":
            QMessageBox.warning(self, "警告", "您还未选择需要压缩的文件或未指定输出目录")

        self.signal.new_progress.emit(0, len(self.pdf_list))
        step = 0
        if self.radioValue1 == 1:
            # 为每个 PDF 创建单独的子文件夹
            for pdf_path in self.pdf_list:
                file_name = os.path.basename(pdf_path)                    
                pdf_output_dir = os.path.join(self.outputPath.text(), os.path.splitext(file_name)[0])
                self.extract_images_from_pdf(pdf_path, pdf_output_dir, 1, 0)
                step += 1
                self.signal.new_progress.emit(1, step)
            
            QMessageBox.information(self, "提示", "提取图像任务已完成！")
            os.startfile(self.outputPath.text())
            self.reset()
        else:
            count = 1
            for pdf_path in self.pdf_list:
                self.extract_images_from_pdf(pdf_path, self.outputPath.text(), 2, count)
                count += 1
                step += 1
                self.signal.new_progress.emit(1, step)
            
            QMessageBox.information(self, "提示", "提取图像任务已完成！")
            os.startfile(self.outputPath.text())
            self.reset()
    
    def reset(self):
        self.pdf_dir = ""
        self.pdf_list = []
        self.fileListWidget.clear()
        self.label1.setText(f"# 已选择：{len(self.pdf_list)} 个PDF文件")
        self.outputPath.setText("")

    def shorten_filename(self, filename, max_length=24):
        name, ext = os.path.splitext(filename)
        if len(name) > max_length:
            name = name[:max_length] + "..."
        return name + ext

    def showList(self):
        self.fileListWidget.clear()
        for pdf_path in self.pdf_list:
            # 只显示文件名
            file_name = self.shorten_filename(os.path.basename(pdf_path))
            self.fileListWidget.addItem(QListWidgetItem(file_name))

    def radioChecked1(self, e):
        self.radioValue1 = e

    def getOutputPath(self):
        path = QFileDialog.getExistingDirectory(self, "选择文件夹", "C:\\")
        self.outputPath.setText(path)

    def process_pdfs(self, pdf_list):
        for pdf in pdf_list:
            if pdf not in self.pdf_list:
                self.pdf_list.append(pdf)
        self.showList()
        self.label1.setText(f"# 已选择：{len(self.pdf_list)} 个PDF文件")

    def selectFiles(self):
        self.pdf_list.clear()
        filePath, fileType = QFileDialog.getOpenFileNames(self, "选择文件", "C:\\", "PDF Files (*.pdf)")
        self.pdf_list = filePath
        self.showList()
        self.label1.setText(f"# 已选择：{len(self.pdf_list)} 个PDF文件")
    
    def selectDirs(self):
        self.pdf_list.clear()
        self.pdf_dir = QFileDialog.getExistingDirectory(self, "选择文件夹", "C:\\")

        for filename in os.listdir(self.pdf_dir):
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(self.pdf_dir, filename)
                self.pdf_list.append(pdf_path)
        
        self.showList()
        self.label1.setText(f"# 文件夹中包含：{len(self.pdf_list)} 个PDF文件")

    def extract_images_from_pdf(self, pdf_path, output_folder, flag, count):
        pdf_document = fitz.open(pdf_path)
        os.makedirs(output_folder, exist_ok=True)

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]  # 获取 PDF 当前的对象
            images = page.get_images(full=True)  # 获取当前页所有图片的元数据

            for img_index, img in enumerate(images):
                xref = img[0]  # 图片的交叉引用 ID，是 PDF 内部用来标识图片的
                base_image = pdf_document.extract_image(xref)  # 提取出真实的图片数据
                image_bytes = base_image["image"]  # 获取图片的二进制数据
                image_ext = base_image["ext"]  # 获取图片的扩展名（如 png, jpeg）
                
                # 保存图片
                if flag == 1:
                    image_path = f"page{page_number+1}_img{img_index+1}.{image_ext}"
                else:
                    image_path = f"pdf{count}_page{page_number+1}_img{img_index+1}.{image_ext}"

                with open(os.path.join(output_folder, image_path), "wb") as image_file:
                    image_file.write(image_bytes)
