from KeepAlive.core.volume import increase_volume, decrease_volume
from PyQt5.QtCore import QThread, QEventLoop, QTimer

class KeepAliveThread(QThread):
    def __init__(self,parent=None):
        super(KeepAliveThread, self).__init__(parent)
        self.threadActive = True

    def run(self):
        while(self.threadActive):
            increase_volume()
            loop = QEventLoop()
            QTimer.singleShot(1000, loop.quit)
            loop.exec_()
            decrease_volume()
            loop = QEventLoop()
            QTimer.singleShot(300000, loop.quit)
            loop.exec_()

    def stop(self):
        self.threadActive = False
        self.wait()

    def is_alive(self):
        return self.threadActive