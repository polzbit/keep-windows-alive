from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import  QColor
from KeepAlive.core.calendar import mapYears, get_current_days
import pandas as pd
from datetime import datetime

class YearSelect(QComboBox):
    yearChange = pyqtSignal(str)
    def __init__(self):
        super().__init__()
    
    def load_data(self, data, date = datetime.now()):
        (yearNumber, monthNumber, monthName, numOfDays, day) = get_current_days(date)
        yearList = []
        def filterYears(variable):
            date = pd.to_datetime(variable)
            if date.year not in yearList:
                yearList.append(date.year)
                return True
            return False
        
        filteredYearList = list(filter(filterYears, list(map(mapYears, data))))
        if(not len(filteredYearList)):
            filteredYearList = [yearNumber]
        receiversCount = self.receivers(self.currentTextChanged) 
        if receiversCount > 0:     
            self.currentTextChanged.disconnect(self.on_change)
        self.clear()
        self.addItem(str(filteredYearList[0] - 1))
        for year in filteredYearList:
            self.addItem(str(year))
        self.addItem(str(filteredYearList[-1] + 1))
        self.setCurrentText(str(yearNumber)) 
        self.currentTextChanged.connect(self.on_change)
    
    def on_change(self, newYear):
        self.yearChange.emit(newYear)
