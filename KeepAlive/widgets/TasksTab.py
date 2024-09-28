from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import  QColor
from KeepAlive.core.calendar import get_runtime_seconds
import pandas as pd
from datetime import datetime
from KeepAlive.widgets.TasksTable import TasksTable

class TasksTab(QWidget):
    onUpdateCell = pyqtSignal(int, str, str, str)
    onDelete = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        price_text_label = QLabel()
        price_text_label.setText("Factor")
        price_text_label.setMinimumSize(100, 20)
        price_text_label.setMaximumSize(100, 20)
        price_text_label.setAlignment(Qt.AlignLeft)
        price_text_label.setContentsMargins(0, 0, 0, 0)

        self.price_label = QLineEdit()
        self.price_label.setText("200")
        self.price_label.setAlignment(Qt.AlignCenter)
        self.price_label.setMinimumSize(50, 30)
        self.price_label.setMaximumSize(50, 30)
        self.price_label.setContentsMargins(0, 0, 0, 0)
        self.price_label.textChanged.connect(self.on_factor_change)

        hours_label = QLabel()
        hours_label.setText("Total hours")
        hours_label.setMinimumSize(95, 20)
        hours_label.setMaximumSize(95, 20)
        hours_label.setAlignment(Qt.AlignLeft)
        hours_label.setContentsMargins(0, 0, 0, 0)

        self.total_hours_label = QLineEdit()
        self.total_hours_label.setText("0")
        self.total_hours_label.setAlignment(Qt.AlignCenter)
        self.total_hours_label.setMinimumSize(50, 30)
        self.total_hours_label.setMaximumSize(50, 30)
        self.total_hours_label.setContentsMargins(0, 0, 0, 0)
        self.total_hours_label.setReadOnly(True)

        monthly_label = QLabel()
        monthly_label.setText("Monthly total")
        monthly_label.setMinimumSize(95, 20)
        monthly_label.setMaximumSize(95, 20)
        monthly_label.setAlignment(Qt.AlignLeft)
        monthly_label.setContentsMargins(0, 0, 0, 0)

        self.total_monthly = QLineEdit()
        self.total_monthly.setText("0")
        self.total_monthly.setAlignment(Qt.AlignCenter)
        self.total_monthly.setMinimumSize(50, 30)
        self.total_monthly.setMaximumSize(50, 30)
        self.total_monthly.setContentsMargins(0, 0, 0, 0)
        self.total_monthly.setReadOnly(True)

        paid_text_label = QLabel()
        paid_text_label.setText("Paid")
        paid_text_label.setMinimumSize(200, 20)
        paid_text_label.setMaximumSize(200, 20)
        paid_text_label.setAlignment(Qt.AlignLeft)
        paid_text_label.setContentsMargins(0, 0, 0, 0)

        self.paid_label = QLineEdit()
        self.paid_label.setText("0")
        self.paid_label.setAlignment(Qt.AlignCenter)
        self.paid_label.setMinimumSize(50, 30)
        self.paid_label.setMaximumSize(50, 30)
        self.paid_label.setContentsMargins(0, 0, 0, 0)
        self.paid_label.setReadOnly(True)

        sum_text_label = QLabel()
        sum_text_label.setText("Remaining")
        sum_text_label.setMinimumSize(200, 20)
        sum_text_label.setMaximumSize(200, 20)
        sum_text_label.setAlignment(Qt.AlignLeft)
        sum_text_label.setContentsMargins(0, 0, 0, 0)

        self.sum_label = QLineEdit()
        self.sum_label.setText("0")
        self.sum_label.setAlignment(Qt.AlignCenter)
        self.sum_label.setMinimumSize(50, 30)
        self.sum_label.setMaximumSize(50, 30)
        self.sum_label.setContentsMargins(0, 0, 0, 0)
        self.sum_label.setReadOnly(True)

        self.tasks_table = TasksTable()
        self.onDelete = self.tasks_table.onDelete
        self.onUpdateCell = self.tasks_table.onUpdateCell
        self.tasks_table.onTotalHoursChange.connect(self.on_total_hours_change)

        controls_layout_top = QHBoxLayout()
        controls_layout_top.addWidget(price_text_label)
        controls_layout_top.addWidget(self.price_label)
        controls_layout_top.addWidget(paid_text_label)
        controls_layout_top.addWidget(self.paid_label)
        controls_layout_top.addWidget(sum_text_label)
        controls_layout_top.addWidget(self.sum_label)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(hours_label)
        controls_layout.addWidget(self.total_hours_label)
        controls_layout.addWidget(monthly_label)
        controls_layout.addWidget(self.total_monthly)
        controls_layout.addSpacing(600)

        layout = QVBoxLayout()
        layout.addLayout(controls_layout_top)
        layout.addLayout(controls_layout)
        layout.addWidget(self.tasks_table)
        self.setLayout(layout)

    def on_factor_change(self, text: str):
        if text.isnumeric():
            total = int(self.total_hours_label.text()) * int(text)
            self.total_monthly.setText(f'{total}')

    def on_total_hours_change(self, totalHours):
        total = totalHours * int(self.price_label.text())
        self.total_hours_label.setText(f'{totalHours}')
        self.total_monthly.setText(f'{total}')