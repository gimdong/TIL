import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QFileDialog, QGraphicsScene, QGraphicsView, QGraphicsTextItem,
    QTableWidget, QTableWidgetItem, QInputDialog, QLabel
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


class SignalEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Signal Editor")
        self.resize(600, 400)

        self.table = QTableWidget(0, 1)
        self.table.setHorizontalHeaderLabels(["Signal Name"])
        self.table.verticalHeader().setVisible(True)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.add_row_button = QPushButton("Add Signal")
        self.add_col_button = QPushButton("Add Time")
        self.export_button = QPushButton("Export JSON")

        self.add_row_button.clicked.connect(self.add_signal)
        self.add_col_button.clicked.connect(self.add_time)
        self.export_button.clicked.connect(self.export_json)

        self.table.cellClicked.connect(self.toggle_cell)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_row_button)
        btn_layout.addWidget(self.add_col_button)
        btn_layout.addWidget(self.export_button)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.time_unit = 10  # ns

    def add_signal(self):
        signal_name, ok = QInputDialog.getText(self, "Signal Name", "Enter signal name:")
        if ok and signal_name:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(signal_name))
            for col in range(1, self.table.columnCount()):
                self.table.setItem(row, col, QTableWidgetItem("0"))

    def add_time(self):
        col = self.table.columnCount()
        self.table.insertColumn(col)
        self.table.setHorizontalHeaderItem(col, QTableWidgetItem(f"T{col-1}"))
        for row in range(self.table.rowCount()):
            self.table.setItem(row, col, QTableWidgetItem("0"))

    def toggle_cell(self, row, col):
        if col == 0:
            return  # ignore signal name column
        item = self.table.item(row, col)
        if not item:
            item = QTableWidgetItem("0")
            self.table.setItem(row, col, item)
        current = item.text()
        item.setText("1" if current == "0" else "0")

    def export_json(self):
        signal_data = {}
        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 0)
            if not name_item:
                continue
            name = name_item.text()
            signal_data[name] = []
            for col in range(1, self.table.columnCount()):
                cell = self.table.item(row, col)
                signal_data[name].append(int(cell.text()) if cell else 0)

        result = {
            "time_unit": self.time_unit,
            "signals": signal_data
        }

        path, _ = QFileDialog.getSaveFileName(self, "Save JSON", "", "JSON Files (*.json)")
        if path:
            with open(path, "w") as f:
                json.dump(result, f, indent=4)
            print(f"Exported to {path}")


class WaveToolGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WaveTool")
        self.setGeometry(100, 100, 800, 600)

        self.scene = QGraphicsScene()
        self.view = ZoomableGraphicsView(self.scene)  # 변경: ZoomableGraphicsView 사용

        self.load_button = QPushButton("Load JSON")
        self.draw_button = QPushButton("Draw Waveform")
        self.editor_button = QPushButton("Open Signal Editor")

        self.load_button.clicked.connect(self.load_json)
        self.draw_button.clicked.connect(self.plot_waveform)
        self.editor_button.clicked.connect(self.open_editor)

        layout = QVBoxLayout()
        layout.addWidget(self.view)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.load_button)
        btn_layout.addWidget(self.draw_button)
        btn_layout.addWidget(self.editor_button)

        layout.addLayout(btn_layout)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.signals_dict = {}
        self.time_unit = 10  # ns

    def load_json(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open JSON", "", "JSON Files (*.json)")
        if path:
            with open(path, "r") as f:
                data = json.load(f)
            self.time_unit = data.get("time_unit", 10)
            self.signals_dict = data["signals"]
            print(f"Loaded from {path}")

    def open_editor(self):
        self.editor = SignalEditor()
        self.editor.show()

    def plot_waveform(self):
        self.scene.clear()
        self.scene.setBackgroundBrush(Qt.white)
        if not self.signals_dict:
            return

        signal_names = list(self.signals_dict.keys())
        num_timesteps = max(len(v) for v in self.signals_dict.values())

        x_scale = 30  # 시간축 간격
        y_spacing = 40  # 신호 간 간격
        high = 0       # high 위치 (위쪽)
        low = 20       # low 위치 (아래쪽)
        label_offset = 60  # 신호 이름 왼쪽 여백

        for i, name in enumerate(signal_names):
            values = self.signals_dict[name]
            y_base = i * y_spacing + 20  # 위쪽 여백
            # 신호 이름
            label = QGraphicsTextItem(name)
            label.setFont(QFont("Arial", 12))
            label.setDefaultTextColor(QColor(0, 102, 204))  # 파란색 계열
            label.setPos(0, y_base + (low + high) // 2 - 10)
            self.scene.addItem(label)

            # 파형 그리기
            prev_val = values[0]
            prev_x = label_offset
            prev_y = y_base + (high if prev_val else low)
            for t in range(len(values)):
                x = label_offset + t * x_scale
                y = y_base + (high if values[t] else low)
                # 값이 바뀌면 수직선
                if t > 0 and values[t] != prev_val:
                    self.scene.addLine(prev_x, prev_y, prev_x, y, )
                # 수평선
                if t > 0:
                    self.scene.addLine(prev_x, y, x, y)
                prev_x = x
                prev_y = y
                prev_val = values[t]
            # 마지막 수평선
            self.scene.addLine(prev_x, prev_y, label_offset + len(values) * x_scale, prev_y)
# QGraphicsView를 상속받아 확대/축소 기능 추가
class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._zoom = 0

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        self.scale(factor, factor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WaveToolGUI()
    window.show()
    sys.exit(app.exec_())
