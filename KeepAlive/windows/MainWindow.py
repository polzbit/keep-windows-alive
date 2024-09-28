from PyQt5.QtWidgets import qApp, QWidget, QTabWidget, QMainWindow, QStyle, QLabel, QVBoxLayout, QHBoxLayout, QSystemTrayIcon, QAction, QMenu, QPushButton, QComboBox, QLineEdit
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon
from KeepAlive.core import KeepAliveThread, GetPublicIpThread
from KeepAlive.style.palette import palette
from KeepAlive.core.calendar import  get_month_list, get_runtime_seconds
from KeepAlive.widgets.SwitchWidget import SwitchWidget
from KeepAlive.widgets.MonthSelect import MonthSelect
from KeepAlive.widgets.YearSelect import YearSelect
from KeepAlive.widgets.TasksTab import TasksTab
from KeepAlive.widgets.TimeSheetTab import TimeSheetTab
import pandas as pd
from KeepAlive.core.db.time_sheet_model import TimeSheet
from KeepAlive.core.db.tasks_model import Tasks
from KeepAlive.core.db.projects_model import Projects
from KeepAlive.windows.NewProjectWindow import NewProjectWindow
from datetime import datetime
from PyQt5.QtSql import QSqlDatabase
from sys import exit as sysExit

class MainWindow(QMainWindow):
    createNewProject = pyqtSignal(str)
    closeNewProjectWindow = pyqtSignal()
    month_list = get_month_list()
    def __init__(self, con: QSqlDatabase):
        QMainWindow.__init__(self)
        self.createNewProject.connect(self.on_create_project)
        self.closeNewProjectWindow.connect(self.close_new_project_window)
        self.con = con
        self.time_sheet_model = TimeSheet()
        self.projects_model = Projects()
        self.tasks_model = Tasks()
        self.icon = self.style().standardIcon(QStyle.SP_ComputerIcon)
        self.keepAliveProcess = None
        self.tabIndex = 0
        self.projectList = self.projects_model.getProjects()
        self.projectId = self.projectList[0][0]
        self.timeSheet = self.time_sheet_model.getTimeSheet(self.projectId)
        self.tasks = self.tasks_model.getTasks(self.projectId)
        self.newProjectWindow = None
        self.setWindowIcon(self.icon)
        self.init_systemTray()
        self.initUI()
        self.ipThread = GetPublicIpThread()
        self.ipThread.finished.connect(self.showIp)
        self.ipThread.run()
    
    def createTimestamp(self, end = False):
        self.time_sheet_model.createTimestamp(self.projectId, self.time_sheet_tab.runtime, end)
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
        self.public_ip_label.setReadOnly(True)

        refresh_button = QPushButton()
        refresh_button.setMinimumSize(30, 30)
        refresh_button.setMaximumSize(30, 30)
        refresh_button.setContentsMargins(0, 0, 0, 0)
        refresh_button.clicked.connect(self.refreshPublicIp)
        refresh_button.setIcon(QIcon('.\\KeepAlive\\style\\icons\\refresh.png'))

        keep_alive_label = QLabel()
        keep_alive_label.setText("Keep windows active")
        keep_alive_label.setMinimumSize(200, 20)
        keep_alive_label.setMaximumSize(200, 20)
        keep_alive_label.setAlignment(Qt.AlignLeft)
        keep_alive_label.setContentsMargins(0, 0, 0, 0)

        self.keep_alive_button = SwitchWidget()
        self.keep_alive_button.click.connect(self.on_should_keep_alive_change)

        self.projectSelect = QComboBox() 
        for project in self.projectList:
            self.projectSelect.addItem(project[1])
        self.projectSelect.currentTextChanged.connect(self.set_current_project)

        self.yearSelect = YearSelect() 
        
        self.monthSelect = MonthSelect(self.month_list)      

        self.yearSelect.yearChange.connect(self.set_timeSheet_year)
        self.monthSelect.monthChange.connect(self.set_timeSheet_month)

        self.statusBar().showMessage('')
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.time_sheet_tab = TimeSheetTab()
        self.tasks_tab = TasksTab() 

        self.time_sheet_tab.onUpdateCell.connect(self.on_table_cell_change)
        self.time_sheet_tab.onStartChange.connect(self.on_start_change)

        self.tasks_tab.onUpdateCell.connect(self.on_task_cell_change)
        self.tasks_tab.onDelete.connect(self.on_task_delete)

        self.tabs.addTab(self.time_sheet_tab, "Time Sheet")
        self.tabs.addTab(self.tasks_tab, "Tasks")
        self.tabs.currentChanged.connect(self.on_tab_change)

        if not len(self.projectList):
            self.time_sheet_tab.time_table.hide()

        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        top_layout.addWidget(ip_text_label)
        top_layout.addWidget(self.public_ip_label)
        top_layout.addWidget(refresh_button)
        ka_controls_layout = QHBoxLayout()
        ka_controls_layout.addWidget(keep_alive_label)
        ka_controls_layout.addWidget(self.keep_alive_button)
        table_controls_layout = QHBoxLayout()
        table_controls_layout.addWidget(self.projectSelect)
        table_controls_layout.addWidget(self.yearSelect)
        table_controls_layout.addWidget(self.monthSelect)
        layout.addLayout(top_layout)
        layout.addLayout(ka_controls_layout)
        layout.addLayout(table_controls_layout)
        layout.addWidget(self.tabs)
        self.central_widget.setLayout(layout)
        self._createActions()
        self._createMenuBar()
        self.render_table()
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
        self.projectId = self.projects_model.getProjectIdByName(project)
        if not self.tabIndex:
            self.time_sheet_tab.time = 0
            self.time_sheet_tab.time_label.setText('00:00:00')
            self.render_table()
        else:
            self.render_tasks_table()

    def set_timeSheet_year(self, newYear):
        monthNumber = self.month_list.index(self.monthSelect.currentText()) + 1
        if monthNumber > 12:
            monthNumber = 1
        if newYear:
            date = pd.to_datetime(f"{newYear}/{monthNumber}/1")
            if not self.tabIndex:
                self.render_table(date)
            else:
                self.render_tasks_table(date)

    def on_task_delete(self, index):
        taskId =  None
        for i in range(len(self.tasks)):
            if i == index:
                taskId = self.tasks[index][0]
                break
        if taskId:
            self.tasks_model.delete([('id', taskId)])
            self.render_tasks_table()

    def on_tab_change(self, index):
        monthNumber = self.month_list.index(self.monthSelect.currentText()) + 1
        if monthNumber > 12:
            monthNumber = 1
        currentDate = pd.to_datetime(f"{self.yearSelect.currentText()}/{monthNumber}/1")
        self.tabIndex = index
        if not index:
            self.render_table(currentDate)
        else:
            self.render_tasks_table(currentDate)

    def set_timeSheet_month(self, monthNumber):
        date = pd.to_datetime(f"{self.yearSelect.currentText()}/{monthNumber}/1")
        if not self.tabIndex:
            self.render_table(date)
        else:
            self.render_tasks_table(date)
    
    def on_should_keep_alive_change(self):
        if self.keepAliveProcess != None and self.keepAliveProcess.is_alive():
            self.keepAliveProcess.stop()
            self.statusBar().showMessage('')
        else:
            self.keepAliveProcess = KeepAliveThread()
            self.keepAliveProcess.run()
            self.statusBar().showMessage('Keep-Alive is now running.')

    def on_table_cell_change(self, date, startTime, endTime, duration):
        self.time_sheet_model.updateTimestamp(date, self.projectId, startTime, endTime, duration)
        self.render_table()
    
    def on_task_cell_change(self, taskIndex:int, date:str, title:str, duration:str):
        taskId =  None
        for i in range(len(self.tasks)):
            if i == taskIndex:
                taskId = self.tasks[taskIndex][0]
                break
        
        if not duration and not duration.isnumeric():
            duration = ''
        start =  pd.to_datetime(datetime.now())
        if not date:
            try:
                currentDate = pd.to_datetime(date, dayfirst=True)
                start = pd.to_datetime(f"{currentDate.year}/{currentDate.month}/{currentDate.day}")
            except ValueError:
                pass
        self.tasks_model.updateTask(self.projectId, taskId, start, title, duration)
        self.render_tasks_table()
    
    def on_start_change(self, isStarting):
        if isStarting:
            self.createTimestamp(True)
        else:
            self.createTimestamp()

    def render_tasks_table(self, date = pd.to_datetime(datetime.now())):
        if not self.con.open():
            return
        self.tasks = self.tasks_model.getTasks(self.projectId, date)
        self.yearSelect.load_data(self.tasks, date)
        self.monthSelect.load_data(date)
        self.tasks_tab.tasks_table.load_data(self.tasks)

    def render_table(self, date = pd.to_datetime(datetime.now())):
        if not self.con.open():
            return
        self.timeSheet = self.time_sheet_model.getTimeSheet(self.projectId, date)
        self.yearSelect.load_data(self.timeSheet, date)
        self.monthSelect.load_data(date)
        self.time_sheet_tab.time_table.load_data(self.timeSheet, date)

    def init_systemTray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.icon)

        show_action = QAction("Open...", self)
        quit_action = QAction("Exit", self)
        show_action.triggered.connect(self.show) 
        quit_action.triggered.connect(self.quitEvent)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
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

    @pyqtSlot(str)
    def showIp(self, ip):
        self.public_ip_label.setText(ip)

    @pyqtSlot(str)
    def on_create_project(self, projectName):
        self.projects_model.createProject(projectName)
        self.projectSelect.addItem(projectName)
        if not len(self.projectList):
            self.projectId = self.projects_model.getProjectIdByName(projectName)
            self.render_table()
            self.time_sheet_tab.time_table.show()
        self.close_new_project_window()

    def refreshPublicIp(self):
        self.public_ip_label.setText('loading...')
        if(not self.ipThread.is_alive()):
            self.ipThread = GetPublicIpThread()
            self.ipThread.finished.connect(self.showIp)
            self.ipThread.run()

    def quitEvent(self):
        if self.keepAliveProcess != None and self.keepAliveProcess.is_alive():
            self.keepAliveProcess.stop()
        if self.ipThread != None and self.ipThread.is_alive():
            self.ipThread.stop()
        qApp.quit()
        self.con.close()
        del self.con
        self.con = None
        QSqlDatabase.removeDatabase("QSQLITE")
        sysExit(0)

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)