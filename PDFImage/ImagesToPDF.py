from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QUrl

class PDFDragDropWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 批量拖拽处理")
        self.setGeometry(100, 100, 400, 200)
        self.setAcceptDrops(True)  # 启用拖拽
        
        self.label = QLabel("拖拽 PDF 文件到这里", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border: 2px dashed #aaa; padding: 20px; font-size: 16px;")
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    # 处理拖拽进入事件
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()  # 接受拖拽
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
            self.process_pdfs(pdf_files)
        else:
            QMessageBox.warning(self, "提示", "未检测到 PDF 文件，请重新拖拽！")
    
    # 处理拖拽进来的 PDF 文件
    def process_pdfs(self, file_list):
        QMessageBox.information(self, "文件接收", f"共接收到 {len(file_list)} 个 PDF 文件。")
        # 在这里调用你已有的批量提取函数
        for pdf in file_list:
            print(f"处理文件: {pdf}")
            # extract_images_from_pdf(pdf, output_dir)  # 调用你已有的函数

if __name__ == "__main__":
    app = QApplication([])
    window = PDFDragDropWidget()
    window.show()
    app.exec_()
