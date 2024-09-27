from PyQt5.QtWidgets import qApp, QWidget, QMainWindow, QStyle, QLabel, QVBoxLayout, QHBoxLayout, QSystemTrayIcon, QAction, QMenu, QPushButton, QComboBox, QLineEdit
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon
from KeepAlive.core import KeepAliveThread, GetPublicIpThread
from KeepAlive.style.palette import palette
from KeepAlive.core.calendar import  get_month_list, get_runtime_seconds
from KeepAlive.widgets.SwitchWidget import SwitchWidget
from KeepAlive.widgets.MonthSelect import MonthSelect
from KeepAlive.widgets.YearSelect import YearSelect
from KeepAlive.widgets.TimeSheetTable import TimeSheetTable
import pandas as pd
from KeepAlive.core.db import TimeSheetDb
from KeepAlive.windows.NewProjectWindow import NewProjectWindow
from datetime import datetime

class MainWindow(QMainWindow):
    createNewProject = pyqtSignal(str)
    closeNewProjectWindow = pyqtSignal()
    month_list = get_month_list()
    def __init__(self):
        QMainWindow.__init__(self)
        self.createNewProject.connect(self.on_create_project)
        self.closeNewProjectWindow.connect(self.close_new_project_window)
        self.db = TimeSheetDb()
        self.start_text = 'Start'
        self.runtime = '00:00:00'
        self.icon = self.style().standardIcon(QStyle.SP_ComputerIcon)
        self.timeSheet = self.db.getTimeSheet()
        self.keepAliveProcess = None
        self.time = 0
        self.projectList = self.db.getProjects()
        self.newProjectWindow = None
        self.setWindowIcon(self.icon)
        self.init_systemTray()
        self.initUI()
        self.ipThread = GetPublicIpThread()
        self.ipThread.finished.connect(self.showIp)
        self.ipThread.run()
    
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

        keep_alive_label = QLabel()
        keep_alive_label.setText("Keep windows active")
        keep_alive_label.setMinimumSize(200, 20)
        keep_alive_label.setMaximumSize(200, 20)
        keep_alive_label.setAlignment(Qt.AlignLeft)
        keep_alive_label.setContentsMargins(0, 0, 0, 0)

        self.keep_alive_button = SwitchWidget()
        self.keep_alive_button.click.connect(self.on_should_keep_alive_change)
        
        self.time_label = QLabel()
        self.time_label.setText(self.runtime)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setMinimumSize(60, 20)
        self.time_label.setMaximumSize(60, 20)
        self.time_label.setWordWrap(True)
        self.time_label.setContentsMargins(5, 5, 5, 5)

        self.projectSelect = QComboBox() 
        for project in self.projectList:
            self.projectSelect.addItem(project[1])
        self.projectSelect.currentTextChanged.connect(self.set_current_project)

        self.yearSelect = YearSelect() 
        
        self.monthSelect = MonthSelect(self.month_list)      

        self.yearSelect.yearChange.connect(self.set_timeSheet_year)
        self.monthSelect.monthChange.connect(self.set_timeSheet_month)

        self.time_table = TimeSheetTable()
        self.time_table.onUpdateCell.connect(self.on_table_cell_change)
        self.time_table.onRuntimeChange.connect(self.on_runtime_change)
        if not len(self.projectList):
            self.time_table.hide()
        
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
        ka_controls_layout = QHBoxLayout()
        ka_controls_layout.addWidget(keep_alive_label)
        ka_controls_layout.addWidget(self.keep_alive_button)
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignLeft)
        table_controls_layout = QHBoxLayout()
        table_controls_layout.addWidget(self.projectSelect)
        table_controls_layout.addWidget(self.yearSelect)
        table_controls_layout.addWidget(self.monthSelect)
        layout.addLayout(top_layout)
        layout.addLayout(controls_layout)
        layout.addLayout(ka_controls_layout)
        layout.addLayout(bottom_layout)
        layout.addLayout(table_controls_layout)
        layout.addWidget(self.time_table)
        self.central_widget.setLayout(layout)
        self._createActions()
        self._createMenuBar()
        self.show()

    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a title
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.exitAction)
        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addAction(self.aboutAction)

    def _createActions(self):
        self.newAction = QAction("&New Project", self)
        self.newAction.triggered.connect(self.open_new_project_window)
        self.exitAction = QAction("&Exit", self)
        self.exitAction.triggered.connect(self.quitEvent)
        self.aboutAction = QAction("&About", self)

    def open_new_project_window(self):
        self.newProjectWindow = NewProjectWindow(self)
        self.newProjectWindow.show()

    def close_new_project_window(self):
        self.newProjectWindow.close()
        self.newProjectWindow = None

    def set_current_project(self, project):
        self.db.setProjectIdByName(project)
        self.time = 0
        self.time_label.setText('00:00:00')
        self.render_table()

    def set_timeSheet_year(self, newYear):
        monthNumber = self.month_list.index(self.monthSelect.currentText()) + 1
        if monthNumber > 12:
            monthNumber = 1
        if newYear:
            self.render_table(pd.to_datetime(f"{newYear}/{monthNumber}/1"))

    def set_timeSheet_month(self, monthNumber):
        self.render_table(pd.to_datetime(f"{self.yearSelect.currentText()}/{monthNumber}/1"))
    
    def on_should_keep_alive_change(self):
        if self.keepAliveProcess != None and self.keepAliveProcess.is_alive():
            self.keepAliveProcess.stop()
            self.statusBar().showMessage('')
        else:
            self.keepAliveProcess = KeepAliveThread()
            self.keepAliveProcess.run()
            self.statusBar().showMessage('Keep-Alive is now running.')

    def on_table_cell_change(self, date, startTime, endTime, duration):
        self.db.updateTimestamp(date, startTime, endTime, duration)
        self.render_table()

    def on_runtime_change(self, runtime):
        self.runtime =runtime
        self.time_label.setText(runtime)
        self.time = get_runtime_seconds(runtime)

    def render_table(self, date = datetime.now()):
        if not self.db.isConnectionOpen():
            return
        self.timeSheet = self.db.getTimeSheet(date)
        self.yearSelect.load_data(self.timeSheet, date)
        self.monthSelect.load_data(date)
        self.time_table.load_data(self.timeSheet, date)

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
        if self.start_button.text() == 'Stop':
            self.time_label.setText(self.runtime)
            self.start_button.setText('Start')
            self.start_action.setText('Start')
            self.createTimestamp(True)
            self.timer.stop()
        else:
            self.start_button.setText('Stop')
            self.start_action.setText('Stop')
            self.createTimestamp()
            self.timer.start(1000)

    @pyqtSlot(str)
    def showIp(self, ip):
        self.public_ip_label.setText(ip)

    @pyqtSlot(str)
    def on_create_project(self, projectName):
        self.db.createProject(projectName)
        self.projectSelect.addItem(projectName)
        if not len(self.projectList):
            self.db.setProjectIdByName(projectName)
            self.render_table()
            self.time_table.show()
        self.close_new_project_window()

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
            self.toggleKeepAliveProcess()
            self.keepAliveProcess.stop()
        if self.ipThread != None and self.ipThread.is_alive():
            self.ipThread.stop()
        qApp.quit()
        self.db.closeConnection()  

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)