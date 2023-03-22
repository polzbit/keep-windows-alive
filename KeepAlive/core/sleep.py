from PyQt5.QtCore import QEventLoop, QTimer

def sleep(seconds):
    loop = QEventLoop()
    QTimer.singleShot(seconds * 1000, loop.quit)
    loop.exec_()