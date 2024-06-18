from PyQt5.QtWidgets import qApp, QWidget, QMainWindow, QStyle, QLabel, QCheckBox, QVBoxLayout, QHBoxLayout, QSystemTrayIcon, QAction, QMenu, QPushButton, QComboBox, QLineEdit, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QIcon, QColor
from KeepAlive.core import KeepAliveThread, GetPublicIpThread
from KeepAlive.style.palette import palette
from KeepAlive.core.calendar import get_current_days, is_weekday, get_month_list
from KeepAlive.widgets.TableWidget import TableWidget
import pandas as pd

class MainWindow(QMainWindow):
    table_headers = ['Date', 'Start', 'End', 'Duration']
    month_list = get_month_list()
    def __init__(self, db):
        QMainWindow.__init__(self)
        self.start_text = 'Start'
        self.runtime = '00:00:00'
        self.icon = self.style().standardIcon(QStyle.SP_ComputerIcon)
        self.timeSheet = db.getTimeSheet()
        self.db = db
        self.keepAliveProcess = None
        self.shouldUpdate = True
        self.time = 0
        self.calendarData = (0, 0, '', 0)
        self.setWindowIcon(self.icon)
        self.init_systemTray()
        self.initUI()
        self.ipThread = GetPublicIpThread()
        self.ipThread.finished.connect(self.showIp)
        self.ipThread.run()
        # self.db.createTable()
        # self.db.clearTimeSheetTable()
    
    def createTimestamp(self, end = False):
        self.db.createTimestamp(self.runtime, end)
        self.render_table()

    def initUI(self):
        self.setPalette(palette)
        self.setMinimumWidth(500)       
        self.setMaximumWidth(500)       
        self.setWindowTitle("Keep Windows Alive") 
        self.central_widget = QWidget(self)           
        self.setCentralWidget(self.central_widget) 

        ip_text_label = QLabel()
        ip_text_label.setText("IP: ")
        ip_text_label.setMinimumSize(60, 20)
        ip_text_label.setMaximumSize(60, 20)
        ip_text_label.setAlignment(Qt.AlignCenter)
        ip_text_label.setContentsMargins(0, 0, 0, 0)

        self.public_ip_label = QLineEdit()
        self.public_ip_label.setText("Loading...")
        self.public_ip_label.setAlignment(Qt.AlignCenter)
        self.public_ip_label.setMinimumSize(150, 30)
        self.public_ip_label.setMaximumSize(150, 30)
        self.public_ip_label.setContentsMargins(0, 0, 0, 0)

        refresh_button = QPushButton()
        refresh_button.setMinimumSize(30, 30)
        refresh_button.setMaximumSize(30, 30)
        refresh_button.setContentsMargins(0, 0, 0, 0)
        refresh_button.clicked.connect(self.refreshPublicIp)
        refresh_button.setIcon(QIcon('.\\KeepAlive\\style\\icons\\refresh.png'))

        self.start_button = QPushButton()
        self.start_button.setMinimumSize(60, 40)
        self.start_button.setMaximumSize(60, 40)
        self.start_button.setContentsMargins(0, 0, 0, 0)
        self.start_button.clicked.connect(self.toggleKeepAliveProcess)
        self.start_button.setText('Start')

        quit_button = QPushButton()
        quit_button.setMinimumSize(60, 40)
        quit_button.setMaximumSize(60, 40)
        quit_button.setContentsMargins(0, 0, 0, 0)
        quit_button.clicked.connect(self.quitEvent)
        quit_button.setText('Exit')
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        
        self.time_label = QLabel()
        self.time_label.setText(self.runtime)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setMinimumSize(60, 20)
        self.time_label.setMaximumSize(60, 20)
        self.time_label.setWordWrap(True)
        self.time_label.setContentsMargins(5, 5, 5, 5)

        self.shouldUpdateCheckbox = QCheckBox()
        self.shouldUpdateCheckbox.stateChanged.connect(self.on_should_update_change)
        self.shouldUpdateCheckbox.setChecked(True)

        shouldUpdateLabel = QLabel()
        shouldUpdateLabel.setText("Should update")
        shouldUpdateLabel.setMinimumSize(100, 20)
        shouldUpdateLabel.setMaximumSize(100, 20)
        shouldUpdateLabel.setAlignment(Qt.AlignLeft)
        shouldUpdateLabel.setContentsMargins(0, 0, 0, 0)

        self.yearSelect = QComboBox() 
        
        self.monthSelect = QComboBox()      

        self.time_table = TableWidget(self.table_headers)
        header = self.time_table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.render_table() 

        self.statusBar().showMessage('')

        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        top_layout.addWidget(ip_text_label)
        top_layout.addWidget(self.public_ip_label)
        top_layout.addWidget(refresh_button)
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.time_label)
        controls_layout.addWidget(quit_button)
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignLeft)
        bottom_layout.addWidget(self.shouldUpdateCheckbox)
        bottom_layout.addWidget(shouldUpdateLabel)
        table_controls_layout = QHBoxLayout()
        table_controls_layout.addWidget(self.yearSelect)
        table_controls_layout.addWidget(self.monthSelect)
        layout.addLayout(top_layout)
        layout.addLayout(controls_layout)
        layout.addLayout(bottom_layout)
        layout.addLayout(table_controls_layout)
        layout.addWidget(self.time_table)
        self.central_widget.setLayout(layout)
        self.show()

    def set_timeSheet_year(self, newYear):
        monthNumber = self.month_list.index(self.monthSelect.currentText()) + 1
        self.render_table(pd.to_datetime(f"{newYear}/{monthNumber}/1"))

    def set_timeSheet_month(self, newMonth):
        monthNumber = self.month_list.index(newMonth) + 1
        self.render_table(pd.to_datetime(f"{self.yearSelect.currentText()}/{monthNumber}/1"))

    def on_should_update_change(self, checked):
        self.shouldUpdate = checked
    
    def render_table(self, date = None):
        if date != None:
            self.timeSheet = self.db.getTimeSheet(date)
            self.calendarData = get_current_days(date)
            (yearNumber, monthNumber, monthName, numOfDays) = self.calendarData
        else:
            self.timeSheet = self.db.getTimeSheet()
            self.calendarData = get_current_days()
            (yearNumber, monthNumber, monthName, numOfDays) = self.calendarData
            def mapYears(variable):
                date = pd.to_datetime(variable[1])
                return date.year
            yearList = []
            def filterYears(variable):
                date = pd.to_datetime(variable)
                if date.year not in yearList:
                    yearList.append(date.year)
                    return True
                return False

            filteredYearList = list(filter(filterYears, list(map(mapYears ,self.timeSheet))))
            if(not len(filteredYearList)):
                filteredYearList = [yearNumber]
            self.yearSelect.clear()
            self.yearSelect.addItem(str(filteredYearList[0] - 1))
            for year in filteredYearList:
                self.yearSelect.addItem(str(year))
            self.yearSelect.addItem(str(filteredYearList[-1] + 1))
            
            self.yearSelect.setCurrentText(str(yearNumber)) 
            for month in self.month_list:
                self.monthSelect.addItem(month)
            self.monthSelect.setCurrentText(monthName) 

            self.yearSelect.currentTextChanged.connect(self.set_timeSheet_year)
            self.monthSelect.currentTextChanged.connect(self.set_timeSheet_month)

        self.time_table._clear()
        self.time_table.setRowCount(numOfDays)  
        for i in range(len(self.table_headers)):
            self.time_table.setHorizontalHeaderItem(i, QTableWidgetItem(self.table_headers[i]))

        for row in range(numOfDays):
            (dayName, is_week_day, data) = is_weekday(f"{row+1}/{monthNumber}/{yearNumber}", self.timeSheet)
            for column in range(len(self.table_headers)):
                item =  QTableWidgetItem(f"")
                if column == 0: 
                    item = QTableWidgetItem(f"{row + 1}/{monthNumber}/{yearNumber} {dayName}")
                if data != None:
                    if  column == 1:
                        item =  QTableWidgetItem(f"{data[1]}")
                    if data[2] != '' and column == 2:
                        item =  QTableWidgetItem(f"{data[2]}")
                    if data[3] != '' and column == 3:
                        item =  QTableWidgetItem(f"{data[3]}")
                if(not is_week_day):
                    item.setBackground(QColor('#c0c0c0'))
                item.setFlags(Qt.ItemIsEnabled)
                self.time_table.setItem(row, column, item) 

    def init_systemTray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.icon)

        show_action = QAction("Open...", self)
        self.start_action = QAction("Start", self)
        quit_action = QAction("Exit", self)
        show_action.triggered.connect(self.show) 
        self.start_action.triggered.connect(self.toggleKeepAliveProcess) 
        quit_action.triggered.connect(self.quitEvent)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(self.start_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)

        # on tray event call systemIcon()
        self.tray_icon.activated.connect(self.tryIconClick)
        self.tray_icon.show()

    def tryIconClick(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def toggleKeepAliveProcess(self):
        if self.keepAliveProcess != None and self.keepAliveProcess.is_alive():
            self.time_label.setText(self.runtime)
            self.start_button.setText('Start')
            self.start_action.setText('Start')
            self.statusBar().showMessage('')
            if self.shouldUpdate:
                self.createTimestamp(True)
            self.timer.stop()
            self.keepAliveProcess.stop()
        else:
            self.time = 0
            self.start_button.setText('Stop')
            self.start_action.setText('Stop')
            if self.shouldUpdate:
                self.createTimestamp()
            self.statusBar().showMessage('Keep-Alive is now running.')
            self.keepAliveProcess = KeepAliveThread()
            self.timer.start(1000)
            self.keepAliveProcess.run()

    @pyqtSlot(str)
    def showIp(self, ip):
        self.public_ip_label.setText(ip)

    def refreshPublicIp(self):
        self.public_ip_label.setText('loading...')
        if(not self.ipThread.is_alive()):
            self.ipThread = GetPublicIpThread()
            self.ipThread.finished.connect(self.showIp)
            self.ipThread.run()


    def showTime(self):
        self.time += 1
        sec = self.time
        hour = sec // 3600
        sec %= 3600
        min = sec // 60
        sec %= 60
        self.runtime = "%02d:%02d:%02d" % (hour, min, sec)
        self.time_label.setText(self.runtime)

    def quitEvent(self):
        if self.keepAliveProcess != None and self.keepAliveProcess.is_alive():
            self.keepAliveProcess.stop()
        qApp.quit()

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)