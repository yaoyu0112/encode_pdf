import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QFileDialog, QLineEdit,
    QMessageBox, QProgressBar
)

from PyQt6.QtCore import Qt, QPropertyAnimation
from pypdf import PdfReader, PdfWriter


class DropLabel(QLabel):

    def __init__(self):
        super().__init__("拖拉 PDF 到這裡\n或點擊選擇檔案")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #999;
                padding: 30px;
                font-size: 16px;
            }
        """)
        self.setAcceptDrops(True)
        self.file_path = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        url = event.mimeData().urls()[0]
        path = url.toLocalFile()

        if path.lower().endswith(".pdf"):
            self.file_path = path
            self.setText(path)
        else:
            QMessageBox.warning(self, "錯誤", "請拖入 PDF 檔案")


class PdfUnlocker(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF 密碼移除工具")
        self.resize(500, 350)

        # 拖拉區
        self.drop_label = DropLabel()

        # 密碼輸入
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("輸入 PDF 密碼")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # 按鈕
        self.select_btn = QPushButton("選擇 PDF")
        self.select_btn.clicked.connect(self.select_pdf)

        self.unlock_btn = QPushButton("開始解鎖")
        self.unlock_btn.clicked.connect(self.unlock_pdf)

        # 進度條
        self.progress = QProgressBar()
        self.progress.setValue(0)

        # 成功動畫文字
        self.success_label = QLabel("✔ 解鎖完成")
        self.success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.success_label.setStyleSheet("font-size:18px;color:green;")
        self.success_label.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.drop_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.select_btn)
        layout.addWidget(self.unlock_btn)
        layout.addWidget(self.progress)
        layout.addWidget(self.success_label)

        self.setLayout(layout)

    def select_pdf(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "選擇 PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if file:
            self.drop_label.file_path = file
            self.drop_label.setText(file)

    def unlock_pdf(self):

        pdf_path = self.drop_label.file_path
        password = self.password_input.text()

        if not pdf_path:
            QMessageBox.warning(self, "錯誤", "請選擇 PDF")
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "儲存解鎖後 PDF",
            "unlocked.pdf",
            "PDF Files (*.pdf)"
        )

        if not save_path:
            return

        try:
            reader = PdfReader(pdf_path)

            # === 密碼錯誤可重試 ===
            if reader.is_encrypted:
                result = reader.decrypt(password)

                if result == 0:
                    QMessageBox.critical(self, "失敗", "密碼錯誤，請重新輸入")
                    self.password_input.clear()
                    return

            writer = PdfWriter()
            total_pages = len(reader.pages)

            # 初始化進度條
            self.progress.setMaximum(total_pages)
            self.progress.setValue(0)

            # === 進度條處理 ===
            for index, page in enumerate(reader.pages):
                writer.add_page(page)
                self.progress.setValue(index + 1)
                QApplication.processEvents()

            with open(save_path, "wb") as f:
                writer.write(f)

            # === 成功動畫 ===
            self.play_success_animation()

        except Exception as e:
            QMessageBox.critical(self, "錯誤", str(e))

    def play_success_animation(self):

        self.success_label.setVisible(True)

        animation = QPropertyAnimation(self.success_label, b"windowOpacity")
        animation.setDuration(800)
        animation.setStartValue(0)
        animation.setEndValue(1)

        animation.start()
        self.anim = animation   # 防止被 GC


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PdfUnlocker()
    win.show()
    sys.exit(app.exec())
