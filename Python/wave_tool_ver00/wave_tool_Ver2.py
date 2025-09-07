import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsTextItem,
    QGraphicsRectItem, QInputDialog, QTextEdit, QMainWindow, QAction, QFileDialog, QToolBar, QLabel
)
from PyQt5.QtGui import QPen, QColor, QBrush, QPainter, QIcon
from PyQt5.QtCore import Qt, QRectF


class WaveformView(QGraphicsView):
    def __init__(self, scene, parent):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(self.ScrollHandDrag)
        self.parent = parent

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = self.mapToScene(event.pos())
            self.parent.process_click(pos)
        super().mousePressEvent(event)


class NandFlashAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NAND Flash Timing Analyzer v4.3")

        # 메인 위젯 생성
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)

        # 툴바 생성
        self.create_toolbar()
        self.create_menubar()

        # 그래픽 뷰어 영역
        self.scene = QGraphicsScene()
        self.view = WaveformView(self.scene, self)
        main_layout.addWidget(self.view)

        # Summary Text 추가
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        main_layout.addWidget(QLabel("Waveform Summary"))
        main_layout.addWidget(self.summary_text)

        self.x_spacing = 60
        self.y_spacing = 50
        self.current_data = {}

        self.SIGNAL_COLORS = {
            "CLE": QColor(0, 128, 255),
            "ALE": QColor(255, 128, 0),
            "WE#": QColor(255, 0, 0),
            "RE#": QColor(0, 200, 0),
            "CE#": QColor(128, 0, 255),
            "IO": QColor(255, 0, 255),
            "R/B#": QColor(128, 128, 0)
        }

    def create_menubar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("파일")

        open_action = QAction("열기", self)
        open_action.triggered.connect(self.load_file)
        file_menu.addAction(open_action)

        save_action = QAction("저장", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        export_action = QAction("VCD 내보내기", self)
        export_action.triggered.connect(self.export_vcd)
        file_menu.addAction(export_action)

        exit_action = QAction("종료", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        open_btn = QAction(QIcon.fromTheme("document-open"), "열기", self)
        open_btn.triggered.connect(self.load_file)
        toolbar.addAction(open_btn)

        save_btn = QAction(QIcon.fromTheme("document-save"), "저장", self)
        save_btn.triggered.connect(self.save_file)
        toolbar.addAction(save_btn)

        export_btn = QAction(QIcon.fromTheme("document-export"), "VCD Export", self)
        export_btn.triggered.connect(self.export_vcd)
        toolbar.addAction(export_btn)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "NAND Flash JSON 열기", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'r') as f:
                data = json.load(f)
                self.current_data = data
                self.draw_waveform(data)

    def save_file(self):
        if not self.current_data:
            return
        file_name, _ = QFileDialog.getSaveFileName(self, "NAND Flash JSON 저장", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'w') as f:
                json.dump(self.current_data, f, indent=4)

    def draw_waveform(self, data):
        self.scene.clear()

        level_cycles = max(len(s["levels"]) for s in data["signals"] if s["type"] == "level")
        data_cycles = max(len(s["values"]) for s in data["signals"] if s["type"] == "data")
        num_cycles = max(level_cycles, data_cycles)

        self.draw_time_scale(num_cycles)

        for idx, signal in enumerate(data["signals"]):
            name = signal["name"]
            if name == "clk":  # clk 제거
                continue
            y = idx * self.y_spacing
            name_item = QGraphicsTextItem(name)
            name_item.setPos(10, y)
            self.scene.addItem(name_item)

            x_start = 100
            color = self.SIGNAL_COLORS.get(name, Qt.black)

            if signal["type"] == "data":
                self.draw_data(x_start, y, signal["values"], color)
            elif signal["type"] == "level":
                self.draw_level(x_start, y, signal["levels"], color)

        self.update_summary()

    def draw_time_scale(self, num_cycles):
        x_start = 100
        for i in range(num_cycles):
            x0 = x_start + i * self.x_spacing
            ns_time = (i + 1) * 10
            text = QGraphicsTextItem(f"{ns_time}ns")
            text.setPos(x0 + 5, -30)
            self.scene.addItem(text)
            self.scene.addLine(x0, -10, x0, len(self.current_data["signals"]) * self.y_spacing, QPen(Qt.gray, 0.5, Qt.DashLine))

    def draw_data(self, x_start, y, data_list, color=None):
        for i, data in enumerate(data_list):
            rect = QGraphicsRectItem(QRectF(x_start + i*self.x_spacing, y+10, self.x_spacing, 20))
            rect.setBrush(QBrush(color or QColor(255, 0, 255)))
            rect.setPen(QPen(Qt.black, 1))
            self.scene.addItem(rect)
            text = QGraphicsTextItem(data)
            text.setPos(x_start + i*self.x_spacing + 10, y+10)
            self.scene.addItem(text)

    def draw_level(self, x_start, y, levels, color=None):
        pen = QPen(color or Qt.black, 2)
        for i, level in enumerate(levels):
            y_pos = y + 10 if level else y + 30
            self.scene.addLine(x_start + i*self.x_spacing, y_pos, x_start + (i+1)*self.x_spacing, y_pos, pen)
            if i > 0 and levels[i-1] != level:
                self.scene.addLine(x_start + i*self.x_spacing, y+10, x_start + i*self.x_spacing, y+30, pen)

    def process_click(self, pos):
        x, y = pos.x(), pos.y()
        if x < 100 or y < 0:
            return

        time_idx = int((x - 100) / self.x_spacing)
        signal_idx = int(y / self.y_spacing)
        signals = [s for s in self.current_data["signals"] if s["name"] != "clk"]
        if signal_idx >= len(signals):
            return

        signal = signals[signal_idx]
        if signal["type"] == "level":
            levels = signal["levels"]
            if 0 <= time_idx < len(levels):
                levels[time_idx] = 1 - levels[time_idx]
                self.draw_waveform(self.current_data)

        elif signal["type"] == "data":
            values = signal["values"]
            if 0 <= time_idx < len(values):
                text, ok = QInputDialog.getText(self, "Edit IO Value", "Enter new value:", text=values[time_idx])
                if ok:
                    values[time_idx] = text
                    self.draw_waveform(self.current_data)

    def update_summary(self):
        if not self.current_data:
            self.summary_text.clear()
            return

        signals_dict = {s['name']: s for s in self.current_data["signals"]}
        level_signals = ['CLE', 'ALE', 'WE#', 'RE#', 'CE#', 'R/B#']
        data_signal = signals_dict.get("IO", {}).get("values", [])
        cycles = max(len(signals_dict.get(name, {}).get("levels", [])) for name in level_signals)
        cycles = max(cycles, len(data_signal))

        summary_lines = []
        for t in range(cycles):
            time_ns = (t + 1) * 10
            line = f"{time_ns}ns: "
            for name in level_signals:
                levels = signals_dict.get(name, {}).get("levels", [])
                val = levels[t] if t < len(levels) else "-"
                line += f"{name}_{'H' if val==1 else 'L' if val==0 else '-'} "
            io_val = data_signal[t] if t < len(data_signal) else "--"
            line += f"IO<0x{io_val}>" if io_val != "--" else "IO<-->"
            summary_lines.append(line)

        self.summary_text.setText("\n".join(summary_lines))

    def export_vcd(self):
        if not self.current_data:
            return

        signals = {s['name']: s for s in self.current_data['signals']}
        signal_order = ['CE#', 'CLE', 'ALE', 'WE#', 'RE#', 'R/B#']

        vcd_lines = [
            "$date today $end",
            "$version NAND Analyzer $end",
            "$timescale 1ns $end"
        ]

        id_table = {name: chr(33+i) for i, name in enumerate(signal_order)}
        for name in signal_order:
            vcd_lines.append(f"$var wire 1 {id_table[name]} {name} $end")

        vcd_lines.append("$enddefinitions $end")
        vcd_lines.append("$dumpvars")

        cycles = len(signals['CE#']['levels'])
        last_vals = {}

        for t in range(cycles):
            vcd_lines.append(f"#{t}")
            for name in signal_order:
                sig = signals[name]
                val = sig['levels'][t]
                if last_vals.get(name) != val:
                    vcd_lines.append(f"{val}{id_table[name]}")
                    last_vals[name] = val

        file_name, _ = QFileDialog.getSaveFileName(self, "VCD 내보내기", "", "VCD Files (*.vcd)")
        if file_name:
            with open(file_name, 'w') as f:
                for line in vcd_lines:
                    f.write(line + '\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NandFlashAnalyzer()
    window.resize(1600, 900)
    window.show()
    sys.exit(app.exec_())
