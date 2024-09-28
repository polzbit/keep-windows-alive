from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal
from KeepAlive.core.calendar import  get_current_days
import pandas as pd
from datetime import datetime

class MonthSelect(QComboBox):
    monthChange = pyqtSignal(int)
    def __init__(self, month_list):
        super().__init__()
        self.month_list = month_list
        self.load_data()
    
    def load_data(self, date = datetime.now()):
        currentDate = pd.to_datetime(date)
        monthName = currentDate.month_name()
        receiversCount = self.receivers(self.currentTextChanged) 
        if receiversCount > 0:     
            self.currentTextChanged.disconnect(self.on_change)
        self.clear()
        for month in self.month_list:
            self.addItem(month)
        self.setCurrentText(monthName)
        self.currentTextChanged.connect(self.on_change)
    
    def on_change(self, newMonth):
        monthNumber = self.month_list.index(newMonth) + 1
        self.monthChange.emit(monthNumber)
