from PyQt5.QtCore import QThread, pyqtSignal
from KeepAlive.core.volume import increase_volume, decrease_volume
from KeepAlive.core.sleep import sleep
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PyQt5.QtCore import QUrl, QEventLoop
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
    
class GetPublicIpThread(QThread):
    finished = pyqtSignal(str)
    def __init__(self,parent=None):
        super(GetPublicIpThread, self).__init__(parent)
        self.threadActive = True
        self.networkManager = QNetworkAccessManager()
        self.networkManager.finished.connect(self.handleResponse)
        

    def run(self):
        reply = self.networkManager.get(QNetworkRequest(QUrl("https://api.ipify.org"))) 
        loop = QEventLoop() 
        reply.finished.connect(loop.quit)
        loop.exec_()
    
    def handleResponse(self, reply):
        er = reply.error() 
        if er == QNetworkReply.NoError:
            bytes_string = reply.readAll()
            self.finished.emit(str(bytes_string, 'utf-8'))
        else:
            self.finished.emit(reply.errorString())
        self.threadActive = False

    def stop(self):
        self.threadActive = False
        self.wait()

    def is_alive(self):
        return self.threadActive