import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NAND Timing Viewer (PyQt5)")
        self.resize(1280, 800)
        widget = QWidget()
        layout = QVBoxLayout()
        self.webview = QWebEngineView()
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test.html"))
        self.webview.load(QUrl.fromLocalFile(html_path))
        layout.addWidget(self.webview)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

if __name__ == "__main__":
    from PyQt5.QtCore import QUrl
    app = QApplication(sys.argv)
    window = MainWindow()                                                                                                                                  
    window.show()
    sys.exit(app.exec_())
