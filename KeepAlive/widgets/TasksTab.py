from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import  QColor, QIcon
from KeepAlive.core.calendar import get_runtime_seconds
import pandas as pd
from datetime import datetime
from KeepAlive.widgets.TasksTable import TasksTable

class TasksTab(QWidget):
    onUpdateCell = pyqtSignal(int, str, str, str)
    onDelete = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.show_controls = True
        self.initUI()
    
    def initUI(self):
        self.price_text_label = QLabel()
        self.price_text_label.setText("Factor")
        self.price_text_label.setMinimumSize(100, 20)
        self.price_text_label.setMaximumSize(100, 20)
        self.price_text_label.setAlignment(Qt.AlignLeft)
        self.price_text_label.setContentsMargins(0, 0, 0, 0)

        self.price_label = QLineEdit()
        self.price_label.setText("200")
        self.price_label.setAlignment(Qt.AlignCenter)
        self.price_label.setMinimumSize(50, 30)
        self.price_label.setMaximumSize(50, 30)
        self.price_label.setContentsMargins(0, 0, 0, 0)
        self.price_label.textChanged.connect(self.on_factor_change)

        self.hours_label = QLabel()
        self.hours_label.setText("Total hours")
        self.hours_label.setMinimumSize(95, 20)
        self.hours_label.setMaximumSize(95, 20)
        self.hours_label.setAlignment(Qt.AlignLeft)
        self.hours_label.setContentsMargins(0, 0, 0, 0)

        self.total_hours_label = QLineEdit()
        self.total_hours_label.setText("0")
        self.total_hours_label.setAlignment(Qt.AlignCenter)
        self.total_hours_label.setMinimumSize(50, 30)
        self.total_hours_label.setMaximumSize(50, 30)
        self.total_hours_label.setContentsMargins(0, 0, 0, 0)
        self.total_hours_label.setReadOnly(True)

        self.monthly_label = QLabel()
        self.monthly_label.setText("Monthly total")
        self.monthly_label.setMinimumSize(95, 20)
        self.monthly_label.setMaximumSize(95, 20)
        self.monthly_label.setAlignment(Qt.AlignLeft)
        self.monthly_label.setContentsMargins(0, 0, 0, 0)

        self.total_monthly = QLineEdit()
        self.total_monthly.setText("0")
        self.total_monthly.setAlignment(Qt.AlignCenter)
        self.total_monthly.setMinimumSize(50, 30)
        self.total_monthly.setMaximumSize(50, 30)
        self.total_monthly.setContentsMargins(0, 0, 0, 0)
        self.total_monthly.setReadOnly(True)

        self.paid_text_label = QLabel()
        self.paid_text_label.setText("Paid")
        self.paid_text_label.setMinimumSize(200, 20)
        self.paid_text_label.setMaximumSize(200, 20)
        self.paid_text_label.setAlignment(Qt.AlignLeft)
        self.paid_text_label.setContentsMargins(0, 0, 0, 0)

        self.paid_label = QLineEdit()
        self.paid_label.setText("0")
        self.paid_label.setAlignment(Qt.AlignCenter)
        self.paid_label.setMinimumSize(50, 30)
        self.paid_label.setMaximumSize(50, 30)
        self.paid_label.setContentsMargins(0, 0, 0, 0)
        self.paid_label.setReadOnly(True)

        self.sum_text_label = QLabel()
        self.sum_text_label.setText("Remaining")
        self.sum_text_label.setMinimumSize(200, 20)
        self.sum_text_label.setMaximumSize(200, 20)
        self.sum_text_label.setAlignment(Qt.AlignLeft)
        self.sum_text_label.setContentsMargins(0, 0, 0, 0)

        self.sum_label = QLineEdit()
        self.sum_label.setText("0")
        self.sum_label.setAlignment(Qt.AlignCenter)
        self.sum_label.setMinimumSize(50, 30)
        self.sum_label.setMaximumSize(50, 30)
        self.sum_label.setContentsMargins(0, 0, 0, 0)
        self.sum_label.setReadOnly(True)

        self.show_button = QPushButton()
        self.show_button.setText('Show')
        self.show_button.setMinimumSize(50, 30)
        self.show_button.setMaximumSize(50, 30)
        self.show_button.setContentsMargins(0, 0, 0, 0)
        self.show_button.clicked.connect(self.toggleControls)
        
        self.tasks_table = TasksTable()
        self.onDelete = self.tasks_table.onDelete
        self.onUpdateCell = self.tasks_table.onUpdateCell
        self.tasks_table.onTotalHoursChange.connect(self.on_total_hours_change)

        layout_top = QHBoxLayout()
        layout_top.addWidget(self.show_button)

        controls_layout_top = QHBoxLayout()
        controls_layout_top.addWidget(self.price_text_label)
        controls_layout_top.addWidget(self.price_label)
        controls_layout_top.addWidget(self.paid_text_label)
        controls_layout_top.addWidget(self.paid_label)
        controls_layout_top.addWidget(self.sum_text_label)
        controls_layout_top.addWidget(self.sum_label)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.hours_label)
        controls_layout.addWidget(self.total_hours_label)
        controls_layout.addWidget(self.monthly_label)
        controls_layout.addWidget(self.total_monthly)
        controls_layout.addSpacing(600)

        layout = QVBoxLayout()
        layout.addLayout(layout_top)
        layout.addLayout(controls_layout_top)
        layout.addLayout(controls_layout)
        layout.addWidget(self.tasks_table)
        self.setLayout(layout)
        self.toggleControls()

    def toggleControls(self):
        self.show_controls = not self.show_controls
        if self.show_controls:
            self.show_button.setText('Hide')
            self.price_text_label.show()
            self.price_label.show()
            self.paid_text_label.show()
            self.paid_label.show()
            self.sum_text_label.show()
            self.sum_label.show()
            self.hours_label.show()
            self.total_hours_label.show()
            self.monthly_label.show()
            self.total_monthly.show()
        else:
            self.show_button.setText('Show')
            self.price_text_label.hide()
            self.price_label.hide()
            self.paid_text_label.hide()
            self.paid_label.hide()
            self.sum_text_label.hide()
            self.sum_label.hide()
            self.hours_label.hide()
            self.total_hours_label.hide()
            self.monthly_label.hide()
            self.total_monthly.hide()

    def on_factor_change(self, text: str):
        if text.isnumeric():
            total = int(self.total_hours_label.text()) * int(text)
            self.total_monthly.setText(f'{total}')

    def on_total_hours_change(self, totalHours):
        total = totalHours * int(self.price_label.text())
        self.total_hours_label.setText(f'{totalHours}')
        self.total_monthly.setText(f'{total}')