from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import  QColor
from KeepAlive.widgets.TableWidget import TableWidget
from KeepAlive.core.calendar import is_weekday, get_current_days,get_runtime_seconds, get_runtime_text
from datetime import datetime

class TimeSheetTable(TableWidget):
    onRuntimeChange = pyqtSignal(str)
    onUpdateCell = pyqtSignal(str,str,str,str)
    headers = ['Date', 'Start', 'End', 'Duration', '']
    disabled_columns = [0, 3, 4]
    def __init__(self):
        super().__init__(self.headers)
        header = self.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
    
    def load_data(self, timeSheet, date = datetime.now()):
        calendarData = get_current_days(date)
        (yearNumber, monthNumber, monthName, numOfDays, day) = calendarData
        receiversCount = self.receivers(self.itemChanged) 
        if receiversCount > 0:     
            self.itemChanged.disconnect(self.on_table_cell_change)
        self._clear()
        self.setRowCount(numOfDays) 
        for i in range(len(self.headers)):
            self.setHorizontalHeaderItem(i, QTableWidgetItem(self.headers[i])) 
        for row in range(numOfDays):
            (dayName, is_week_day, data) = is_weekday(f"{row+1}/{monthNumber}/{yearNumber}", timeSheet)
            for column in range(len(self.headers)):
                item = QTableWidgetItem('')
                if column == 0: 
                    item = QTableWidgetItem(f"{row + 1}/{monthNumber}/{yearNumber} {dayName}")
                if data != None:
                    if row + 1 == day:
                        if data[3] != '':
                            self.onRuntimeChange.emit(data[3])
                    if column == 1 or column == 2 or column == 3:
                        item =  QTableWidgetItem(f"{data[column]}")
                if(not is_week_day):
                    item.setBackground(QColor('#707070'))
                if column in self.disabled_columns:
                    item.setFlags(Qt.ItemIsEnabled)
                if column == 4 and data != None and data[1] != '' and data[2] != '':
                    btn = QPushButton()
                    btn.setText('Calculate')
                    btn.clicked.connect(self.on_calculate_duration)
                    self.setCellWidget(row, column, btn)
                else:
                    self.setItem(row, column, item) 
        self.itemChanged.connect(self.on_table_cell_change)

    def on_table_cell_change(self, item):
        itemText = item.text()
        time = itemText.split(':')
        if len(time) == 3:
            itemRow = item.row()
            itemColumn = item.column()
            date = self.item(itemRow, 0).text()
            startTime = self.item(itemRow, 1).text()
            endTime = self.item(itemRow, 2).text()
            duration = self.item(itemRow, 3).text()
            if itemColumn == 1:
                startTime = itemText
            elif itemColumn == 2:
                endTime = itemText
            self.onUpdateCell.emit(date, startTime, endTime, duration)
    
    def on_calculate_duration(self):
        items = self.selectedItems()
        if(len(items) == 2):
            startTime = items[0].text()
            endTime = items[1].text()
            duration = get_runtime_seconds(endTime) - get_runtime_seconds(startTime)
            duration_text = get_runtime_text(duration)
            date = self.item(items[0].row(), 0).text()
            self.onUpdateCell.emit(date, startTime, endTime, duration_text)

