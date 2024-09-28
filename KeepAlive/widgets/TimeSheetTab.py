from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import  QColor
from KeepAlive.core.calendar import get_runtime_seconds
import pandas as pd
from datetime import datetime
from KeepAlive.widgets.TimeSheetTable import TimeSheetTable

class TimeSheetTab(QWidget):
    onStartChange = pyqtSignal(bool)
    onUpdateCell = pyqtSignal(int, str, str, str)
    def __init__(self):
        super().__init__()
        self.runtime = '00:00:00'
        self.time = 0
        self.initUI()

    def initUI(self):
        self.start_button = QPushButton()
        self.start_button.setMinimumSize(60, 40)
        self.start_button.setMaximumSize(60, 40)
        self.start_button.setContentsMargins(0, 0, 0, 0)
        self.start_button.clicked.connect(self.toggleKeepAliveProcess)
        self.start_button.setText('Start')

        self.time_label = QLabel()
        self.time_label.setText(self.runtime)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setMinimumSize(60, 20)
        self.time_label.setMaximumSize(60, 20)
        self.time_label.setWordWrap(True)
        self.time_label.setContentsMargins(5, 5, 5, 5)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)

        self.time_table = TimeSheetTable()
        self.time_table.onRuntimeChange.connect(self.on_runtime_change)
        self.onUpdateCell = self.time_table.onUpdateCell

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.time_label)
        layout = QVBoxLayout()
        layout.addLayout(controls_layout)
        layout.addWidget(self.time_table)
        self.setLayout(layout)

    def toggleKeepAliveProcess(self):
        if self.start_button.text() == 'Stop':
            self.time_label.setText(self.runtime)
            self.start_button.setText('Start')
            self.onStartChange.emit(True)
            self.timer.stop()
        else:
            self.start_button.setText('Stop')
            self.onStartChange.emit(False)
            self.timer.start(1000)

    def showTime(self):
        self.time += 1
        sec = self.time
        hour = sec // 3600
        sec %= 3600
        min = sec // 60
        sec %= 60
        self.runtime = "%02d:%02d:%02d" % (hour, min, sec)
        self.time_label.setText(self.runtime)

    def on_runtime_change(self, runtime):
        self.runtime = runtime
        self.time_label.setText(runtime)
        self.time = get_runtime_seconds(runtime)
