from PyQt5.QtWidgets import qApp, QWidget, QMainWindow, QStyle, QLabel, QVBoxLayout, QHBoxLayout, QSystemTrayIcon, QAction, QMenu, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from KeepAlive.core import KeepAliveThread
from KeepAlive.style.palette import palette

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.start_text = 'Start'
        self.icon = self.style().standardIcon(QStyle.SP_ComputerIcon)
        self.setWindowIcon(self.icon)
        self.init_systemTray()
        self.initUI()
        self.keepAliveProcess = None
        self.time = 0

    def initUI(self):
        self.setPalette(palette)
        self.setMinimumSize(300, 100)       
        self.setMaximumSize(300, 100)       
        self.setWindowTitle("Keep Windows Alive") 
        self.central_widget = QWidget(self)           
        self.setCentralWidget(self.central_widget) 

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
        self.time_label.setText("00:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setMinimumSize(60, 20)
        self.time_label.setMaximumSize(60, 20)
        self.time_label.setWordWrap(True)
        self.time_label.setContentsMargins(5, 5, 5, 5)

        self.statusBar().showMessage('')

        layout = QVBoxLayout()
        top_controls_layout = QHBoxLayout()
        top_controls_layout.addWidget(self.start_button)
        top_controls_layout.addWidget(self.time_label)
        top_controls_layout.addWidget(quit_button)
        layout.addLayout(top_controls_layout)
        self.central_widget.setLayout(layout)
        self.show()

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
            self.time_label.setText("00:00")
            self.start_button.setText('Start')
            self.start_action.setText('Start')
            self.statusBar().showMessage('')
            self.timer.stop()
            self.keepAliveProcess.stop()
        else:
            self.time = 0
            self.start_button.setText('Stop')
            self.start_action.setText('Stop')
            self.statusBar().showMessage('Keep-Alive is now running.')
            self.keepAliveProcess = KeepAliveThread()
            self.timer.start(1000)
            self.keepAliveProcess.run()

    def showTime(self):
        self.time += 1
        self.runtime = "%02d:%02d" % (self.time / 60, self.time % 60)
        self.time_label.setText(self.runtime)

    def quitEvent(self):
        if self.keepAliveProcess != None and self.keepAliveProcess.is_alive():
            self.keepAliveProcess.stop()
        qApp.quit()

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)