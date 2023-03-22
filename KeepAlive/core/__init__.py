from PyQt5.QtCore import QThread
from KeepAlive.core.volume import increase_volume, decrease_volume
from KeepAlive.core.sleep import sleep

class KeepAliveThread(QThread):
    def __init__(self,parent=None):
        super(KeepAliveThread, self).__init__(parent)
        self.threadActive = True

    def run(self):
        while(self.threadActive):
            increase_volume()
            sleep(1)
            decrease_volume()
            sleep(300)

    def stop(self):
        self.threadActive = False
        self.wait()

    def is_alive(self):
        return self.threadActive