from PyQt5.QtWidgets import  QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from KeepAlive.style.palette import palette

class NewProjectWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        self.setPalette(palette)
        self.setMinimumWidth(300)       
        self.setMaximumWidth(300)       
        self.setWindowTitle("Create new project") 

        label = QLabel("Project name:")
        label.setMinimumSize(80, 20)
        label.setMaximumSize(80, 20)
        label.setAlignment(Qt.AlignCenter)
        label.setContentsMargins(0, 0, 0, 0)

        self.name_label = QLineEdit()
        self.name_label.setAlignment(Qt.AlignLeft)
        self.name_label.setMinimumSize(150, 30)
        self.name_label.setMaximumSize(150, 30)
        self.name_label.setContentsMargins(0, 0, 0, 0)

        start_button = QPushButton()
        start_button.setMinimumSize(60, 40)
        start_button.setMaximumSize(60, 40)
        start_button.setContentsMargins(0, 0, 0, 0)
        start_button.clicked.connect(self.handleCreate)
        start_button.setText('Create')

        cancel_button = QPushButton()
        cancel_button.setMinimumSize(60, 40)
        cancel_button.setMaximumSize(60, 40)
        cancel_button.setContentsMargins(0, 0, 0, 0)
        cancel_button.clicked.connect(self.handleCancel)
        cancel_button.setText('Cancel')

        row_layout = QHBoxLayout()
        row_layout.addWidget(label)
        row_layout.addWidget(self.name_label)
        control_layout = QHBoxLayout()
        control_layout.addWidget(start_button)
        control_layout.addWidget(cancel_button)

        layout = QVBoxLayout(self)
        layout.addLayout(row_layout)
        layout.addLayout(control_layout)

    def handleCreate(self):
        txt = self.name_label.text()
        if txt:
            self.parent.createNewProject.emit(self.name_label.text())

    def handleCancel(self):
        self.parent.closeNewProjectWindow.emit()