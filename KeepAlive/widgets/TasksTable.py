from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import  QColor
from KeepAlive.widgets.TableWidget import TableWidget
from datetime import datetime
import pandas as pd

class TasksTable(TableWidget):
    onUpdateCell = pyqtSignal(int, str, str, str)
    onDelete = pyqtSignal(int)
    onTotalHoursChange = pyqtSignal(int)
    headers = ['Date', 'Title', 'Duration', '']
    disabled_columns = [0]
    def __init__(self):
        super().__init__(self.headers)
        header = self.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
    
    def load_data(self, tasks):
        receiversCount = self.receivers(self.itemChanged) 
        if receiversCount > 0:     
            self.itemChanged.disconnect(self.on_table_cell_change)
        self._clear()
        tasksLength = len(tasks)
        self.setRowCount(tasksLength + 1) 
        for i in range(len(self.headers)):
            self.setHorizontalHeaderItem(i, QTableWidgetItem(self.headers[i])) 
        total_hours = 0
        for row in range(tasksLength):
            task = tasks[row]
            for column in range(len(self.headers)):
                item =  QTableWidgetItem(f"")
                if column == 0: 
                    date = pd.to_datetime(task[column + 1], dayfirst=False)
                    item = QTableWidgetItem(f"{date.day}/{date.month}/{date.year} {date.day_name()}")
                if column == 1 or column == 2:
                    item =  QTableWidgetItem(f"{task[column + 1]}")
                if column == 2 and f'{task[column + 1]}'.isnumeric():
                    total_hours += int(task[column + 1])
                if column == 3:
                    btn = QPushButton()
                    btn.setText('Delete')
                    btn.clicked.connect(self.on_delete)
                    self.setCellWidget(row, column, btn) 
                if column in self.disabled_columns:
                    item.setFlags(Qt.ItemIsEnabled)
                self.setItem(row, column, item) 
        self.onTotalHoursChange.emit(total_hours)
        item = QTableWidgetItem('')
        item.setBackground(QColor('#707070'))
        self.setItem(tasksLength , 0, item)
        item = QTableWidgetItem('')
        item.setBackground(QColor('#707070'))
        self.setItem(tasksLength , 1, item)
        item = QTableWidgetItem('')
        item.setBackground(QColor('#707070'))
        self.setItem(tasksLength , 2, item)
        item = QTableWidgetItem('')
        item.setBackground(QColor('#707070'))
        self.setItem(tasksLength , 3, item)
        self.itemChanged.connect(self.on_table_cell_change)

    def on_table_cell_change(self, item):
        itemText = item.text()
        itemRow = item.row()
        itemColumn = item.column()
        date = self.item(itemRow, 0).text()
        title = self.item(itemRow, 1).text()
        duration = self.item(itemRow, 2).text()
        if itemColumn == 0:
            date = itemText
        if itemColumn == 1:
            title = itemText
        elif itemColumn == 2:
            duration = itemText
        self.onUpdateCell.emit(itemRow, date, title, duration)

    def on_delete(self):
        items = self.selectedItems()
        self.onDelete.emit(items[0].row())    

